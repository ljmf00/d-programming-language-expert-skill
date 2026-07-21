# D Programming Language Expert

An agent skill providing comprehensive, verified guidance on the
[D programming language](https://dlang.org): syntax and semantics, the Phobos
standard library, the runtime (druntime), templates and metaprogramming, ranges
and algorithms, concurrency, tooling, and language evolution.

The skill activates when you work with `.d`/`.di` files, `dub.sdl`/`dub.json`,
Phobos (`std.*`) or druntime (`core.*`) imports, or ask about DMD/LDC, DIPs, and
D-specific idioms.

## Installation

Install it into Claude Code as a plugin, straight from this repository:

```
/plugin marketplace add ljmf00/d-programming-language-expert-skill
/plugin install dlang-skills@d-programming-language-experts
```

The first command registers this repo as a marketplace; the second installs the
`dlang-skills` plugin from it. Claude then activates each skill automatically on
D-related work (see below). Run `/plugin marketplace update d-programming-language-experts`
to pull later changes.

For code intelligence on D sources (go-to-definition, references, hover), also
install the `d-lsp` plugin, which wires [serve-d](https://github.com/Pure-D/serve-d)
into Claude Code's LSP tool (`serve-d` must be on your `PATH`):

```
/plugin install d-lsp@d-programming-language-experts
```

The server logs to `serve-d.log` in the plugin's data directory (managed by
Claude Code under `~/.claude`, persists across plugin updates).

## Layout

- `skills/d-programming-language-expert/` -- the skill itself:
  - [SKILL.md](./skills/d-programming-language-expert/SKILL.md) -- entry point and table of subskills.
  - `00-d-language-index.md` -- high-level overview; start here.
  - `01-` to `14-*.md` -- self-contained knowledge modules, one per topic.
  - [verify.py](./skills/d-programming-language-expert/verify.py) -- checks the code snippets across the subskills compile.
- `plugins/d-lsp/` -- the `d-lsp` plugin: [.lsp.json](./plugins/d-lsp/.lsp.json)
  configures serve-d as the language server for `.d`/`.di` files.

Each module was authored from authoritative sources (the D language spec, the
LDC compiler, and the Phobos source) and its snippets verified against LDC.

## License

This skill is licensed under the MIT license.

Note that quoted D source code and documentation (from the language spec, the
LDC compiler, and the Phobos standard library) remain under their original
[Boost Software License 1.0](https://www.boost.org/LICENSE_1_0.txt).
