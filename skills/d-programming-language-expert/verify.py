#!/usr/bin/env python3
"""
D Snippet Verifier for D Language Skills Corpus.

Compiles all ```d code blocks with ldc2 using smart wrapping.
Auto-detects declarations vs statements and wraps appropriately.
Runs in parallel.

Usage:
    python3 verify_snippets.py [--ldc PATH] [--verbose] [--jobs N] [--fail-fast]
"""

import re, subprocess, tempfile, os, json, argparse, sys, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Optional, Tuple

SKILLS_DIR = Path(__file__).parent
print_lock = threading.Lock()

DEFAULT_IMPORTS = """import std.stdio;
import std.algorithm;
import std.range;
import std.array;
import std.conv;
import std.typecons;
import std.exception;
import std.format;
import std.math;
import std.string;
import std.traits;
import std.meta;"""

# Markers that identify a block as non-compilable pseudocode/prose rather than D.
# NOTE: do NOT add bare "DIP NNNN" here — it matches ordinary code comments like
# `// Expression-based contracts (DIP 1009)` and would silently exclude real,
# possibly-broken snippets from compilation. DIP-prose tables live in markdown
# (not ```d fences), and comment-only blocks are already caught by is_quick_ref.
NON_D_PATTERNS = ['→', '$(D', '$(I', '$(B', '$(LINK2', '$(REF', '$(SECTION',
                  '$(SUBREF', '$(DDOC_', 'import libdparse']


# Per-snippet version gate, e.g. `//@requires dmd>=2.111` as the block's first
# line. The frontend version is parsed from the compiler banner; a too-old
# compiler skips the block (rather than failing), while a new-enough one compiles
# it normally — so version-gated snippets get really verified once the toolchain
# catches up.
REQUIRES_RE = re.compile(r'^\s*//@requires\s+dmd\s*>=\s*([\d.]+)',
                         re.MULTILINE | re.IGNORECASE)


def parse_requires(code: str) -> Optional[Tuple[int, ...]]:
    m = REQUIRES_RE.search(code)
    return tuple(int(x) for x in m.group(1).split(".")) if m else None


def parse_frontend_version(banner: str) -> Optional[Tuple[int, ...]]:
    """Extract the DMD frontend version from a compiler --version banner.

    Works for LDC ('based on DMD v2.108.1') and ldmd2 ('... v2.108.1')."""
    m = re.search(r'v(\d+)\.(\d+)(?:\.(\d+))?', banner)
    if not m:
        return None
    return tuple(int(g) for g in m.groups() if g is not None)


def version_ge(have: Tuple[int, ...], want: Tuple[int, ...]) -> bool:
    pad = lambda t: t + (0,) * (3 - len(t))
    return pad(have) >= pad(want)


def detect_ldc() -> str:
    for c in ["ldc2", "ldmd2"]:
        try:
            r = subprocess.run(["which", c], capture_output=True, text=True)
            if r.returncode == 0: return r.stdout.strip()
        except FileNotFoundError:
            continue
    for loc in ["/usr/bin/ldc2", "/usr/local/bin/ldc2",
                "/etc/profiles/per-user/luis/bin/ldc2"]:
        if os.path.exists(loc): return loc
    raise FileNotFoundError("ldc2 not found")


def extract_d_blocks(md_file: Path) -> List[Dict]:
    content = md_file.read_text(encoding="utf-8")
    blocks = []
    for m in re.finditer(r'```d\s*\n(.*?)```', content, re.DOTALL):
        code = m.group(1).strip()
        line_num = content[:m.start()].count("\n") + 1
        blocks.append({"code": code, "line": line_num,
                       "file": str(md_file), "name": f"{md_file.name}:{line_num}"})
    return blocks


def has_main(code: str) -> bool:
    return bool(re.search(r'\bvoid\s+main\s*\(', code))


def is_pseudo(code: str) -> bool:
    return any(pat in line for line in code.split("\n") for pat in NON_D_PATTERNS if line.strip())


def is_quick_ref(code: str) -> bool:
    lines = [l.strip() for l in code.split("\n") if l.strip() and not l.strip().startswith("//")]
    if len(lines) == 0:
        return False
    if all(l.startswith("//") for l in code.split("\n") if l.strip()):
        return True
    sig = sum(1 for l in lines if re.match(
        r'^[\w(!.$]+\s*\([^)]*\)\s*(//.*)?$', l) or re.match(r'^[\w.]+\s*//', l))
    if len(lines) <= 3:
        return sig >= len(lines) * 0.8
    return sig >= len(lines) * 0.6


def needs_default_imports(code: str) -> bool:
    return "import " not in code


def split_code(code: str) -> Tuple[List[str], List[str]]:
    """Split code into module-level declarations and function-level statements."""
    decls = []
    stmts = []
    in_unittest = False
    unittest_block = []

    for line in code.split("\n"):
        s = line.strip()
        # Track unittest blocks (they go at module level)
        if s == "unittest" or s.startswith("unittest {"):
            in_unittest = True
            unittest_block.append(line)
            continue

        if in_unittest:
            unittest_block.append(line)
            if s == "}":
                # End of unittest - flush to decls
                decls.extend(unittest_block)
                unittest_block = []
                in_unittest = False
            continue

        if not s or s.startswith("//") or s.startswith("/*"):
            decls.append(line)
            continue

        # Classify line
        if (re.match(r'^(import|module|enum|struct|class|interface|union|template|mixin\s+'
                     r'template|alias|version|debug|static assert|static if|static foreach|'
                     r'unittest|mixin\()', s) or
            re.match(r'^@(safe|system|trusted|nogc|live|property|disable|mustuse)', s) or
            re.match(r'^(public|private|protected|package|export)\s', s) or
            re.match(r'^(pure|nothrow|const|immutable|shared|__gshared)\s', s) or
            re.match(r'^(extern|deprecated|final|abstract|override|synchronized)\b', s) or
            re.match(r'^(ref|out|inout|scope)\s', s) or
            s.startswith("}") or  # closing brace (end of struct/class/enum)
            re.match(r'^[a-zA-Z_]\w*\s+\w+\s*=\s*', s) or  # decl: type name = value
            re.match(r'^auto\s+\w+\s*=\s*', s) or  # auto variable
            re.match(r'^\w[\w.]*\s+\w+(\s*\(|\s*\{|\s*;|\s*=\s)', s) or  # type varname( or type varname; or type varname =
            re.match(r'^this\(', s) or  # constructor
            re.match(r'^~this\(', s) or  # destructor
            re.match(r'^nothrow\s', s) or re.match(r'^pure\s', s) or
            re.match(r'^@\w+', s)):  # UML attributes
            decls.append(line)
        else:
            stmts.append(line)

    if unittest_block:  # Unterminated unittest block
        decls.extend(unittest_block)

    return decls, stmts


def smart_wrap(code: str) -> List[Tuple[str, str]]:
    """Generate candidate wrapped versions. Returns list of (label, code)."""
    candidates = []

    # If has module declaration, keep it at top
    has_module = re.search(r'^module\s+', code, re.MULTILINE)

    # If already has main, just return as-is (with imports if needed)
    if has_main(code):
        candidates.append(("as-is", code))
        if needs_default_imports(code) and not has_module:
            candidates.append(("+def", DEFAULT_IMPORTS + "\n\n" + code))
        elif has_module:
            candidates.append(("+def", re.sub(r'^(module\s+[^;]+;)', r'\1\n\n' + DEFAULT_IMPORTS, code, count=1, flags=re.MULTILINE)))
        return candidates

    # Split into declarations and statements
    decls, stmts = split_code(code)
    decl_text = "\n".join(decls)
    stmt_text = "\n".join(stmts)

    # Build candidates
    def add_candidate(label, code_text):
        candidates.append((label, code_text))
        # Always add default imports variant, deduplication is harmless
        if has_module:
            fixed = re.sub(r'^(module\s+[^;]+;)', r'\1\n\n' + DEFAULT_IMPORTS, code_text, count=1, flags=re.MULTILINE)
            candidates.append(("+def+" + label, fixed))
        else:
            candidates.append(("+def+" + label, DEFAULT_IMPORTS + "\n\n" + code_text))

    # Strategy 1: decls at module level, stmts in void main()
    if stmt_text.strip():
        if decl_text.strip():
            wrapped = decl_text + "\n\nvoid main() {\n" + stmt_text + "\n}"
        else:
            wrapped = "void main() {\n" + stmt_text + "\n}"
        add_candidate("smart", wrapped)
    else:
        add_candidate("decls", decl_text + "\n\nvoid main() {}")

    # Strategy 2: everything in void main()
    add_candidate("main{code}", f"void main() {{\n{code}\n}}")

    # Strategy 3: declarations + empty main
    add_candidate("decls+main{}", code + "\n\nvoid main() {}")

    # Strategy 4: everything in a unittest block
    if has_module:
        m = re.search(r'^(module\s+[^;]+;)\s*\n?', code, re.MULTILINE)
        if m:
            mod_line = m.group(1)
            rest = code[m.end():].strip()
            add_candidate("unittest", f"{mod_line}\n\nunittest {{\n{rest}\n}}")
    else:
        add_candidate("unittest", f"unittest {{\n{code}\n}}")

    return candidates


def try_compile(code: str, ldc_path: str, extra_args: Optional[List[str]] = None
                ) -> Tuple[bool, str]:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".d", delete=False) as f:
        f.write(code); f.flush(); p = f.name
    try:
        cmd = [ldc_path, "-o-", "-c", "-d", "-unittest"]
        if extra_args: cmd.extend(extra_args)
        cmd.append(p)
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode == 0, r.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    finally:
        os.unlink(p)


def verify_snippet(snippet: Dict, ldc_path: str,
                    frontend_ver: Optional[Tuple[int, ...]] = None,
                    stop_event: threading.Event = threading.Event()
                    ) -> Dict:
    code = snippet["code"]
    name = snippet["name"]
    if not code.strip():
        return {"name": name, "success": True, "strategy": "empty"}
    req = parse_requires(code)
    if req and not (frontend_ver and version_ge(frontend_ver, req)):
        want = ".".join(map(str, req))
        return {"name": name, "success": True, "skipped": True,
                "strategy": f"needs dmd>={want}"}
    if is_pseudo(code):
        return {"name": name, "success": True, "strategy": "pseudo"}
    if is_quick_ref(code):
        return {"name": name, "success": True, "strategy": "quick-ref"}

    candidates = smart_wrap(code)
    for label, c in candidates:
        if stop_event.is_set():
            return {"name": name, "success": True, "strategy": "cancelled"}
        ok, _ = try_compile(c, ldc_path)
        if ok:
            return {"name": name, "success": True, "strategy": label}
        # Try with -preview=all
        ok2, _ = try_compile(c, ldc_path, ["-preview=all"])
        if ok2:
            return {"name": name, "success": True, "strategy": label + " -preview"}

    _, err = try_compile(candidates[-1][1], ldc_path)
    return {"name": name, "success": False,
            "strategy": candidates[-1][0], "error": err[:400]}


def print_result(result: Dict, verbose: bool):
    with print_lock:
        if result.get("skipped"):
            print(f"  SKIP  {result['name']:50s} [{result['strategy']}]")
        elif result["success"]:
            if verbose:
                print(f"  PASS  {result['name']:50s} [{result['strategy']}]")
        else:
            print(f"  FAIL  {result['name']:50s} [{result['strategy']}]")
            for l in result.get("error", "").split("\n")[:3]:
                print(f"        {l[:120]}")


def main():
    p = argparse.ArgumentParser(description="Verify D snippets compile with ldc2.")
    p.add_argument("--ldc", default="", help="Path to ldc2")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--skip", default="", help="Comma-separated file patterns")
    p.add_argument("--fail-fast", "-x", action="store_true",
                   help="Stop on first failure")
    p.add_argument("--jobs", "-j", type=int, default=0,
                   help="Parallel jobs (default: CPU count, max 8)")
    args = p.parse_args()

    try:
        ldc_path = args.ldc or detect_ldc()
    except FileNotFoundError:
        print("ERROR: ldc2 not found. Use --ldc PATH.")
        sys.exit(1)

    ver = subprocess.run([ldc_path, "--version"], capture_output=True, text=True, timeout=5)
    frontend_ver = parse_frontend_version(ver.stdout)
    print(f"Compiler: {ldc_path}")
    print(f"Version:  {ver.stdout.split(chr(10))[0]}")
    if frontend_ver:
        print(f"Frontend: DMD v{'.'.join(map(str, frontend_ver))}")
    print()

    md_files = sorted(SKILLS_DIR.glob("*.md"))
    skip_pats = [s.strip() for s in args.skip.split(",") if s.strip()]

    all_blocks = []
    for f in md_files:
        if any(sp in f.name for sp in skip_pats):
            print(f"  Skipping {f.name}")
            continue
        all_blocks.extend(extract_d_blocks(f))

    total = len(all_blocks)
    workers = args.jobs or min(os.cpu_count() or 4, 8)
    print(f"{len(md_files)} files, {total} D blocks, {workers} workers\n")

    results = []
    stop_event = threading.Event()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(verify_snippet, b, ldc_path, frontend_ver, stop_event): b
                   for b in all_blocks}
        for i, fut in enumerate(as_completed(futures), 1):
            r = fut.result()
            results.append(r)
            print_result(r, args.verbose)
            if args.fail_fast and not r["success"]:
                stop_event.set()
                for f in futures:
                    f.cancel()
                break
            if not args.verbose and i % 50 == 0:
                with print_lock:
                    print(f"  ... {i}/{total}", file=sys.stderr)

    skipped = sum(1 for r in results if r.get("skipped"))
    passed = sum(1 for r in results if r["success"] and not r.get("skipped")
                 and r["strategy"] != "cancelled")
    cancelled = sum(1 for r in results if r["strategy"] == "cancelled")
    failed = sum(1 for r in results if not r["success"])
    tested = passed + failed

    print(f"\n{'='*60}")
    print(f"  PASSED: {passed}/{tested}")
    print(f"  FAILED: {failed}/{tested}")
    if skipped:
        print(f"  SKIPPED: {skipped}/{total} (version-gated)")
    if cancelled:
        print(f"  CANCELLED: {cancelled}/{total}")
    print(f"{'='*60}")

    if failed:
        print("\nFailed snippets:")
        for r in results:
            if not r["success"]:
                print(f"  {r['name']:50s} [{r['strategy']}]")
                for l in r.get("error", "").split("\n")[:2]:
                    print(f"    {l[:120]}")

    if args.json:
        print(json.dumps(results, indent=2))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
