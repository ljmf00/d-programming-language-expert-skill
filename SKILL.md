---
name: d-programming-language-expert
description: >-
  D programming language expert. Covers syntax, semantics, standard library
  (Phobos), compiler runtime (druntime), memory model, templates and
  metaprogramming, ranges and algorithms, concurrency and parallelism,
  tooling ecosystem, and language evolution.
  TRIGGER when: editing .d or .di files; working with dub.sdl or dub.json;
  code imports Phobos (std.*) or druntime (core.*) modules; questions about
  DMD/LDC compiler flags, DIPs, or D-specific idioms (ranges, UFCS, mixins,
  @safe/@nogc, scope guards).
  SKIP: non-D files that happen to use a .d extension (e.g. Makefile .d
  dependency files); other-language template engines; generic programming
  discussions not tied to actual D source.
license: MIT
compatibility: opencode claude
metadata:
  languages: d
  file-types: .d .di
  topics: language-core std-library runtime tooling best-practices
---

# D Language Expert — Table of Skills

When you encounter D source files (`.d`, `.di`), load the relevant
subskill below to get comprehensive, accurate guidance on the topic.
Each subskill file is a self-contained knowledge module with verified
code snippets—read the one that matches what you're working on.

## How to use this skill

1. Identify which aspect of D the task involves (syntax, library, runtime, etc.)
2. Read the corresponding subskill file listed below
3. Cross-reference with other subskills when the task spans multiple areas
4. Follow the patterns and conventions documented in each subskill

Each subskill file was authored from authoritative sources: the D language
specification (`dmd/spec/`), the LDC compiler implementation (`ldc/`), and
the Phobos standard library source (`phobos/std/`). All code snippets have
been verified to compile with LDC.

## Subskills

### Index & Quick Reference

| File | Module | When to load |
|------|--------|-------------|
| [00-d-language-index.md](00-d-language-index.md) | **Index** | Start here for a high-level overview of the entire D language. Covers language origin, philosophy, module structure, and guides you to the right subskill. |
| [07-tooling-ecosystem.md](07-tooling-ecosystem.md) | **Tooling** | DMD/LDC compilers, dub package manager, DDoc documentation generation, libdparse, DustMite test-case reducer, IDEs, debugging with GDB/LLDB, profiling. |

### Core Language (spec)

| File | Module | When to load |
|------|--------|-------------|
| [01-core-language.md](01-core-language.md) | **Core Language** | Syntax, types, functions, control flow, classes, structs, operator overloading, templates, attributes (`@safe`, `@nogc`, `pure`, `nothrow` etc.), error handling (exceptions, `nothrow`, scope guards), conditional compilation (`version`/`debug`/`static if`), `__traits`, Better C, interfacing C/C++/Objective-C. |
| [04-templates-metaprogramming.md](04-templates-metaprogramming.md) | **Templates & Metaprogramming** | Template parameters (type/value/alias/seq), constraints, IFTI, variadic templates, eponymous templates, alias sequences, `static foreach` (DIP 1010), CTFE, mixins (template and string), `std.meta` (`AliasSeq`, `staticMap`, `Filter`, `Erase`, `allSatisfy`), `std.traits` (`isNumeric`, `isCallable`, `ReturnType`, `Parameters`, `Fields`, `BaseClassesTuple`). |
| [02-memory-management.md](02-memory-management.md) | **Memory Management & Safety** | GC (`GC.enable`/`disable`, `addRoot`/`removeRoot`), `@safe`/`@trusted`/`@system` memory safety, `const`/`immutable`/`shared` qualifiers, `scope` (DIP 1000), value vs reference semantics, copy constructors (DIP 1018), move semantics (DIP 1014), `@live` ownership/borrowing system, RAII and destructors. |

### Standard Library (Phobos)

| File | Module | When to load |
|------|--------|-------------|
| [03-ranges-algorithms.md](03-ranges-algorithms.md) | **Ranges & Algorithms** | Range primitives (`empty`/`front`/`popFront`), range traits (`isInputRange`, `isForwardRange`, `isBidirectionalRange`, `isRandomAccessRange`), algorithms (`map`, `filter`, `reduce`, `sort`, `find`, `canFind`), range combinators (`chain`, `zip`, `lockstep`, `iota`, `repeat`, `cycle`, `generate`, `tee`, `chunks`, `slide`, `stride`, `cache`). |
| [05-phobos-modules.md](05-phobos-modules.md) | **Phobos Standard Library Modules** | Input/output (`std.stdio`), JSON (`std.json`), UUIDs (`std.uuid`), hashing (`std.digest`), containers (`std.container`), sum types (`std.sumtype`), checked integers (`std.checkedint`), big integers (`std.bigint`), sockets (`std.socket`), CSV parsing (`std.csv`), URIs (`std.uri`), HTTP (`std.net.curl`), memory-mapped files (`std.mmfile`), argument parsing (`std.getopt`), type utilities (`std.typecons`), conversion (`std.conv`). |
| [06-concurrency-parallelism.md](06-concurrency-parallelism.md) | **Concurrency & Parallelism** | `std.concurrency` (`spawn`, `receive`, `send`, `receiveOnly`, `Generator`), `std.parallelism` (`parallel` foreach, `taskPool`, `task`, `amap`, `areduce`), threads (`core.thread.Thread`), fibers (`core.thread.Fiber`), synchronization (`Mutex`, `Condition`, `Semaphore`, `ReadWriteMutex`, `Barrier`), atomic operations (`core.atomic`: `atomicOp`, `atomicLoad`, `atomicStore`, `cas`), data sharing patterns, thread-local storage |

### Evolution & Best Practices

| File | Module | When to load |
|------|--------|-------------|
| [08-evolution-best-practices.md](08-evolution-best-practices.md) | **Evolution & Best Practices** | DIPs (scope, move semantics, copy ctor, noreturn, `@mustuse`, `=>` methods, bitfields, editions), code organization patterns, error handling strategies, testing (`std.experimental.testing`, unit-threaded), logging, deprecation management, idiom guides. |

### Runtime & FFI

| File | Module | When to load |
|------|--------|-------------|
| [09-runtime-internals.md](09-runtime-internals.md) | **Runtime Internals** | GC (`core.memory`), TypeInfo/`typeid`, `Object`/`Throwable` hierarchy, array/string internals, `core.lifetime` (emplace, move, forward), `core.exception`, ModuleInfo, TLS/`__gshared`, `core.thread` basics. Use when debugging runtime behavior or working with low-level D runtime APIs. |
| [10-ffi-interop.md](10-ffi-interop.md) | **FFI & Interop** | `extern(C)`, `extern(C++)`, `extern(C++, class)` C++ interop, `extern(Objective-C)`, COM, `pragma` (lib, mangle, inline, msg), C header import via `core.stdc.*`, `core.sys.posix.*`, Better C mode, calling conventions. Use when calling C/C++/ObjC libraries from D or exposing D. |

### Performance & Optimization

| File | Module | When to load |
|------|--------|-------------|
| [11-performance-optimization.md](11-performance-optimization.md) | **Performance Optimization** | `core.simd` types (float4, int4), LDC `@inline`/`@noinline`, cache-friendly SoA vs AoS layout, memory alignment, loop optimization patterns, const/immutable for alias analysis, LDC `-O` flags, PGO workflow, LTO. Use when optimizing D code for speed. |

### Testing, Documentation & Async

| File | Module | When to load |
|------|--------|-------------|
| [12-testing-documentation.md](12-testing-documentation.md) | **Testing & Documentation** | `unittest` blocks (advanced patterns), pre/post-condition `in`/`out` contracts, contract inheritance, DDoc documentation generation, DDoc macros (`$(D ...)`, `$(REF ...)`, etc.), embedded code examples. Use when writing tests or docs. |
| [13-async-event-driven.md](13-async-event-driven.md) | **Async & Event-Driven** | Fiber schedulers, `std.concurrency.Generator!T` coroutines, POSIX epoll/kqueue/select, non-blocking I/O, event loop patterns, cooperative multitasking. Use when writing async D code without external frameworks. |

## Verification

All code snippets in these subskill files pass compilation with LDC.
Run the verifier at any time:

```
python3 verify.py [--verbose] [--fail-fast]
```
