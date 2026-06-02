---
name: d-lang-expert-index
description: >-
  D language skill index - entry point and navigation for the entire D
  skill corpus. Lists all subskills with descriptions and cross-references
  to help agents find the right knowledge module quickly.
license: MIT
metadata:
  topics: index navigation reference
  order: 00
---

# D Programming Language - Complete Skill Index

This is a comprehensive collection of skills for the D programming language, designed to help AI assistants and developers write idiomatic, efficient D code.

## Quick Navigation

| Skill | Description | Best For |
|-------|-------------|----------|
| [Core Language](01-core-language.md) | Syntax, types, control flow, functions, OOP | Writing basic D programs |
| [Memory Management](02-memory-management.md) | GC, RAII, safety attributes, const/immutable | Safe, efficient memory handling |
| [Ranges & Algorithms](03-ranges-algorithms.md) | Range programming, std.algorithm, std.range | Data processing pipelines |
| [Templates & Metaprogramming](04-templates-metaprogramming.md) | Templates, mixins, CTFE, compile-time | Generic programming, code generation |
| [Phobos Modules](05-phobos-modules.md) | Standard library modules reference | Using Phobos effectively |
| [Concurrency & Parallelism](06-concurrency-parallelism.md) | Threads, message passing, parallelism | Multi-threaded applications |
| [Tooling & Ecosystem](07-tooling-ecosystem.md) | DMD, LDC, DUB, documentation | Building and managing projects |
| [Evolution & Best Practices](08-evolution-best-practices.md) | DIPs, idioms, patterns, style guide | Writing idiomatic D code |

## Getting Started

### For Beginners
1. Start with [Core Language](01-core-language.md) to understand syntax and types
2. Learn [Memory Management](02-memory-management.md) for safe coding practices
3. Explore [Phobos Modules](05-phobos-modules.md) for standard library usage

### For Intermediate Developers
1. Master [Ranges & Algorithms](03-ranges-algorithms.md) for data processing
2. Learn [Templates & Metaprogramming](04-templates-metaprogramming.md) for generic code
3. Study [Concurrency & Parallelism](06-concurrency-parallelism.md) for multi-threading

### For Advanced Users
1. Explore [Tooling & Ecosystem](07-tooling-ecosystem.md) for project management
2. Follow [Evolution & Best Practices](08-evolution-best-practices.md) for idiomatic patterns

## Key D Concepts

### Language Philosophy
- **Write Fast, Read Fast, Run Fast** - D combines productivity with performance
- **Multi-paradigm** - Supports imperative, OOP, functional, and generic programming
- **Memory Safe** - @safe subset eliminates entire classes of bugs
- **Zero-cost Abstractions** - High-level features compile to efficient code

### Core Features
- **Static typing** with type inference (`auto`)
- **Garbage collection** with manual memory management options
- **RAII** (Resource Acquisition Is Initialization)
- **Contracts** (preconditions, postconditions, invariants)
- **Unit testing** built into the language
- **Compile-time function execution** (CTFE)
- **Template metaprogramming** with partial specialization
- **Ranges** for generic sequence processing
- **First-class functions** with closures and delegates
- **Immutable data** for thread safety

### Standard Library (Phobos)
- **std.algorithm** - Generic algorithms (filter, map, reduce, sort)
- **std.range** - Range primitives and composition
- **std.array** - Array manipulation
- **std.string** - String operations
- **std.conv** - Type conversion
- **std.format** - Formatting (printf-style)
- **std.datetime** - Date and time handling
- **std.numeric** - Numeric algorithms
- **std.random** - Random number generation
- **std.parallelism** - Parallel execution
- **std.concurrency** - Message passing

### Tooling
- **DMD** - Reference compiler (pure D implementation)
- **LDC** - LLVM-based compiler (better optimization)
- **DUB** - Package manager and build system
- **DDoc** - Documentation generator
- **dfmt** - Code formatter
- **DCD** - Code completion

## Code Style Reference

### Naming Conventions
```d
// Modules: lowercase with underscores
module my_package.my_module;

// Types (structs, classes, enums): PascalCase
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

### Import Style
```d
// Preferred: specific imports
import std.algorithm : filter, map, reduce;
import std.range : iota, take;

// Avoid: wildcard imports (except for std)
import std;  // Only in small scripts or REPL
```

### Function Style
```d
// Preferred: shortened method syntax (DIP 1043)
int add(int a, int b) pure nothrow @safe @nogc => a + b;

// Traditional style (still valid)
int multiply(int a, int b) pure nothrow @safe @nogc {
    return a * b;
}
```

## Common Patterns

### Range Pipeline
```d
import std;

void main() {
    iota(1, 101)          // 1 to 100
        .filter!(a => a % 2 == 0)  // even numbers
        .map!(a => a * a)          // square them
        .array                    // materialize for sort
        .sort                     // sort (already sorted, but demonstrates chaining)
        .each!writeln;            // print each
}
```

### RAII Resource Management
```d
import std.stdio : File;

void processFile() {
    auto file = File("data.txt", "r");  // Automatically closed at scope exit
    foreach (line; file.byLine()) {
        // Process line
    }
}  // file is automatically closed here
```

### Immutable Data Sharing
```d
import std.stdio : writeln;

void main() {
    immutable data = [1, 2, 3, 4, 5];  // Thread-safe, shareable
    writeln(data);
}
```

## Resources

- **Official Website**: https://dlang.org
- **Language Specification**: https://dlang.org/spec/spec.html
- **Phobos Documentation**: https://dlang.org/phobos/
- **DUB Packages**: https://code.dlang.org
- **D Forum**: https://forum.dlang.org
- **D Wiki**: https://wiki.dlang.org
- **DIPs**: https://github.com/dlang/DIPs
- **D Tour (Interactive)**: https://tour.dlang.org

## When to Use Which Skill

| Task | Use This Skill |
|------|---------------|
| Write a simple program | [Core Language](01-core-language.md) |
| Handle files/network | [Phobos Modules](05-phobos-modules.md) |
| Process collections | [Ranges & Algorithms](03-ranges-algorithms.md) |
| Create generic code | [Templates & Metaprogramming](04-templates-metaprogramming.md) |
| Ensure memory safety | [Memory Management](02-memory-management.md) |
| Multi-threaded code | [Concurrency & Parallelism](06-concurrency-parallelism.md) |
| Set up a project | [Tooling & Ecosystem](07-tooling-ecosystem.md) |
| Write idiomatic D | [Evolution & Best Practices](08-evolution-best-practices.md) |
