# D Programming Language Expert

An agent skill providing comprehensive, verified guidance on the
[D programming language](https://dlang.org): syntax and semantics, the Phobos
standard library, the runtime (druntime), templates and metaprogramming, ranges
and algorithms, concurrency, tooling, and language evolution.

The skill activates when you work with `.d`/`.di` files, `dub.sdl`/`dub.json`,
Phobos (`std.*`) or druntime (`core.*`) imports, or ask about DMD/LDC, DIPs, and
D-specific idioms.

## Layout

- [SKILL.md](./SKILL.md) -- entry point and table of subskills.
- `00-d-language-index.md` -- high-level overview; start here.
- `01-` to `14-*.md` -- self-contained knowledge modules, one per topic.
- [verify.py](./verify.py) -- checks the code snippets across the subskills compile.

Each module was authored from authoritative sources (the D language spec, the
LDC compiler, and the Phobos source) and its snippets verified against LDC.

## License

This skill is licensed under the MIT license.

Note that quoted D source code and documentation (from the language spec, the
LDC compiler, and the Phobos standard library) remain under their original
[Boost Software License 1.0](https://www.boost.org/LICENSE_1_0.txt).
