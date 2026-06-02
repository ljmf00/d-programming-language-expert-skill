---
name: d-lang-expert-index
description: >-
  D language quick-reference cheatsheet: naming conventions, import style,
  common patterns, and a full navigation table mapping tasks to subskill files.
  Load this alongside a task-specific subskill for an instant orientation.
license: MIT
metadata:
  topics: index navigation reference cheatsheet
  order: 00
---

# D Programming Language — Quick Reference

## Subskill Navigation

| File | Module | When to load |
|------|--------|-------------|
| [01-core-language.md](01-core-language.md) | **Core Language** | Syntax, types, functions, OOP, attributes, error handling, conditional compilation |
| [02-memory-management.md](02-memory-management.md) | **Memory Management** | GC, RAII, `@safe`/`@trusted`/`@system`, `const`/`immutable`/`shared`, copy/move, `@live` |
| [03-ranges-algorithms.md](03-ranges-algorithms.md) | **Ranges & Algorithms** | Range primitives, `std.algorithm`, `std.range` combinators |
| [04-templates-metaprogramming.md](04-templates-metaprogramming.md) | **Templates & Metaprogramming** | Template parameters, IFTI, CTFE, mixins, `std.meta`, `std.traits` |
| [05-phobos-modules.md](05-phobos-modules.md) | **Phobos Standard Library** | `std.stdio`, `std.json`, `std.sumtype`, `std.typecons`, `std.conv`, sockets, datetime |
| [06-concurrency-parallelism.md](06-concurrency-parallelism.md) | **Concurrency & Parallelism** | `std.concurrency`, `std.parallelism`, fibers, atomics, mutexes |
| [07-tooling-ecosystem.md](07-tooling-ecosystem.md) | **Tooling & Ecosystem** | DMD/LDC compilers, DUB, DDoc, dfmt, DCD, debugging, profiling |
| [08-evolution-best-practices.md](08-evolution-best-practices.md) | **Evolution & Best Practices** | DIPs, style guide, idioms, anti-patterns, testing strategies |
| [09-runtime-internals.md](09-runtime-internals.md) | **Runtime Internals** | GC API, TypeInfo/`typeid`, `Object`/`Throwable`, array internals, `core.lifetime` |
| [10-ffi-interop.md](10-ffi-interop.md) | **FFI & Interop** | `extern(C)`, `extern(C++)`, `extern(Objective-C)`, Better C mode, calling conventions |
| [11-performance-optimization.md](11-performance-optimization.md) | **Performance Optimization** | `core.simd`, LDC inline/noinline, SoA vs AoS layout, PGO, LTO |
| [12-testing-documentation.md](12-testing-documentation.md) | **Testing & Documentation** | `unittest` patterns, contracts (`in`/`out`), DDoc generation |
| [13-async-event-driven.md](13-async-event-driven.md) | **Async & Event-Driven** | Fiber schedulers, `Generator!T`, POSIX epoll/kqueue, event loop patterns |
| [14-gotchas.md](14-gotchas.md) | **D Gotchas** | AI-relevant pitfalls: slice semantics, `string` immutability, `shared`, DIP 1000 |

## Task → Subskill

| Task | Subskill |
|------|----------|
| Write basic program | [Core Language](01-core-language.md) |
| Handle memory safely | [Memory Management](02-memory-management.md) |
| Process collections / data pipelines | [Ranges & Algorithms](03-ranges-algorithms.md) |
| Generic / compile-time code | [Templates & Metaprogramming](04-templates-metaprogramming.md) |
| Use std library (I/O, JSON, datetime…) | [Phobos Modules](05-phobos-modules.md) |
| Multi-threaded / parallel code | [Concurrency & Parallelism](06-concurrency-parallelism.md) |
| Build/package/format/lint | [Tooling & Ecosystem](07-tooling-ecosystem.md) |
| Idiomatic patterns, DIPs | [Evolution & Best Practices](08-evolution-best-practices.md) |
| Debug GC / runtime behavior | [Runtime Internals](09-runtime-internals.md) |
| Call C/C++/ObjC from D | [FFI & Interop](10-ffi-interop.md) |
| Optimize for speed / SIMD | [Performance Optimization](11-performance-optimization.md) |
| Write tests / DDoc | [Testing & Documentation](12-testing-documentation.md) |
| Async / event-driven I/O | [Async & Event-Driven](13-async-event-driven.md) |
| Avoid subtle D bugs | [D Gotchas](14-gotchas.md) |

## Naming Conventions

```d
// Modules: lowercase_with_underscores
module my_package.my_module;

// Types (structs, classes, enums, interfaces): PascalCase
struct MyStruct { }
class MyClass {
    private int _privateField;
}
enum MyEnum { none }

// Functions and variables: camelCase
void myFunction() { }
int myVariable = 0;

// Constants: UPPER_SNAKE_CASE
const int MAX_SIZE = 100;

// Enum members: camelCase
enum Color { red, green, blue }
```

## Import Style

```d
// Preferred: named selective imports
import std.algorithm : filter, map, sort;
import std.range : iota, take;

// Convenience wildcard — only in short scripts / REPL
import std;
```

## Function Style

```d
// Shortened method syntax (DIP 1043, supported in current LDC/DMD)
int add(int a, int b) pure nothrow @safe @nogc => a + b;

// Traditional style
int multiply(int a, int b) pure nothrow @safe @nogc {
    return a * b;
}
```

## Common Patterns

### Range Pipeline

```d
import std;

void main() {
    iota(1, 101)
        .filter!(a => a % 2 == 0)
        .map!(a => a * a)
        .each!writeln;
}
```

### RAII Resource Management

```d
import std.stdio : File;

void processFile(string path) {
    auto file = File(path, "r");
    foreach (line; file.byLine())
        processLine(line);
}  // file closed automatically at scope exit
```

### Immutable Data (Thread-Safe Sharing)

```d
import std.stdio : writeln;

void main() {
    immutable int[] data = [1, 2, 3, 4, 5];
    writeln(data);  // safe to share across threads
}
```

### Scope Guard

```d
void acquireResource() {
    acquire();
    scope(exit)    release();       // always runs
    scope(failure) rollback();      // runs on exception
    scope(success) commit();        // runs on normal exit
    doWork();
}
```
