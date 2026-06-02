---
name: d-lang-gotchas
description: >-
  D language gotchas and AI-relevant pitfalls: array slice reference semantics,
  string immutability, foreach ref aliasing, struct vs class value/reference,
  shared threading model, DIP 1000 scope status, GC closure pressure, and
  default initialization rules. Load this to avoid the subtle mistakes that
  most often appear in AI-generated D code.
license: MIT
metadata:
  topics: gotchas pitfalls memory safety concurrency idioms
  order: 14
---

# D Language — Gotchas & AI-Relevant Pitfalls

Subtle behaviors that most often produce wrong or non-idiomatic AI-generated D code. Read this alongside the task-specific subskill.

## Table of Contents
- [Array Slices Have Reference Semantics](#array-slices-have-reference-semantics)
- [`string` Is Immutable](#string-is-immutable)
- [`foreach` Copies; `foreach ref` Aliases](#foreach-copies-foreach-ref-aliases)
- [Struct vs Class: Value vs Reference](#struct-vs-class-value-vs-reference)
- [`shared` Does Not Mean Thread-Safe Access](#shared-does-not-mean-thread-safe-access)
- [DIP 1000 `scope` Is Still Behind a Preview Flag](#dip-1000-scope-is-still-behind-a-preview-flag)
- [GC Pressure from Closures](#gc-pressure-from-closures)
- [Default Initialization Rules](#default-initialization-rules)
- [Array Append May Reallocate](#array-append-may-reallocate)
- [UFCS Lookup Is Module-Scoped](#ufcs-lookup-is-module-scoped)

---

## Array Slices Have Reference Semantics

A D slice does not own its memory — it is a `(ptr, length)` view into an existing array. Mutating through a slice mutates the source.

```d
import std.stdio : writeln;

void main() {
    int[] source = [1, 2, 3, 4, 5];
    int[] view = source[1 .. 4];  // view shares source's memory

    view[0] = 99;
    writeln(source);  // [1, 99, 3, 4, 5] — source is mutated!
}
```

To get an independent copy, use `.dup`:

```d
import std.stdio : writeln;

void main() {
    int[] source = [1, 2, 3, 4, 5];
    int[] copy = source[1 .. 4].dup;  // independent allocation

    copy[0] = 99;
    writeln(source);  // [1, 2, 3, 4, 5] — source unchanged
}
```

---

## `string` Is Immutable

`string` is an alias for `immutable(char)[]`. You cannot mutate characters through a `string` reference. This catches many C-background developers.

```d
void main() {
    string s = "hello";
    // s[0] = 'H';  // Error: cannot modify immutable expression

    // Correct: build a mutable copy first
    char[] buf = s.dup;
    buf[0] = 'H';
    s = buf.idup;  // convert back to immutable string
}
```

`~=` appending works on `string` but creates a new allocation:

```d
import std.stdio : writeln;

void main() {
    string s = "foo";
    s ~= "bar";   // s now points to a new allocation; original "foo" unchanged
    writeln(s);   // "foobar"
}
```

Use `char[]` (mutable) for builder patterns; convert to `string` with `.idup` at the boundary.

---

## `foreach` Copies; `foreach ref` Aliases

By default `foreach` over an array copies each element. Modifying the loop variable does not affect the array.

```d
import std.stdio : writeln;

void main() {
    int[] arr = [1, 2, 3];

    foreach (x; arr)
        x *= 2;           // modifies local copy only

    writeln(arr);         // [1, 2, 3] — unchanged
}
```

Use `ref` to alias the element in-place:

```d
import std.stdio : writeln;

void main() {
    int[] arr = [1, 2, 3];

    foreach (ref x; arr)
        x *= 2;           // modifies arr element directly

    writeln(arr);         // [2, 4, 6]
}
```

The same applies to `foreach` over structs — always decide whether copy or alias is intended.

---

## Struct vs Class: Value vs Reference

Structs are value types; classes are reference types. This affects assignment, function passing, and GC pressure.

```d
struct Point { int x, y; }

class Node {
    int val;
    this(int v) { val = v; }
}

void main() {
    // Struct: copy on assignment
    Point a = Point(1, 2);
    Point b = a;
    b.x = 99;
    assert(a.x == 1);  // a is unaffected

    // Class: reference copy on assignment
    auto n1 = new Node(1);
    auto n2 = n1;       // n2 is an alias, not a copy
    n2.val = 99;
    assert(n1.val == 99);  // n1 is also 99
}
```

`new ClassName()` always allocates on the GC heap. For stack allocation of class instances use `scope` (with `-preview=dip1000`) or `core.lifetime.emplace` into a manually allocated buffer.

---

## `shared` Does Not Mean Thread-Safe Access

`shared` marks data as being shared across threads, which prevents the compiler from making thread-local assumptions. It does **not** add automatic locking or atomics. Accessing `shared` data without synchronization is still a data race.

```d
import core.atomic : atomicLoad, atomicStore;

shared int counter = 0;

void increment() {
    // Wrong: not atomic, data race on counter
    // counter++;

    // Correct: use atomic operations
    atomicStore(counter, atomicLoad(counter) + 1);
}
```

For compound operations, use `core.sync.mutex.Mutex` or `synchronized` blocks. For simple counters prefer `core.atomic.atomicFetchAdd`.

---

## DIP 1000 `scope` Is Still Behind a Preview Flag

DIP 1000 (scope variables, preventing pointer escape) is not enabled by default in current DMD or LDC. Code that relies on DIP 1000 for memory safety must be compiled with `-preview=dip1000`.

```d
// This function signature intends DIP 1000 borrow semantics
@safe int* getPtr(scope int* p) {
    return p;  // DIP 1000 rejects this; without the flag it may compile
}
```

Check the compiler version and flags before relying on `scope` for safety guarantees. Without `-preview=dip1000`, `scope` on parameters is advisory only.

---

## GC Pressure from Closures

A closure that captures a local variable forces the captured variable onto the GC heap. In tight loops or `@nogc` contexts this is a problem.

```d
import std.algorithm : map;
import std.array : array;
import std.range : iota;

void main() {
    int factor = 3;

    // This closure captures `factor` — GC allocation for the delegate context
    auto result = iota(5).map!(x => x * factor).array;
}
```

For `@nogc` code, avoid closures over locals or use function pointers with explicit context passed as a parameter. `std.functional.partial` and `std.functional.curry` can help but also involve allocations.

---

## Default Initialization Rules

D zero-initializes all variables by default unless `= void` is used. This includes:

- Integer types → `0`
- Floating-point types → `float.nan` / `double.nan` (not `0.0`)
- Pointers → `null`
- Bools → `false`
- Structs → each field recursively zero-initialized
- Slice → `null` (length 0, null pointer)

```d
import std.stdio : writeln;
import std.math : isNaN;

void main() {
    double x;
    assert(isNaN(x));  // float/double default is NaN, not 0.0!

    int* p;
    assert(p is null);

    int[] arr;
    assert(arr.length == 0 && arr.ptr is null);
}
```

Use `= void` to skip initialization for a performance-sensitive hot path, but only when the code immediately writes before reading:

```d
void fillBuffer(ubyte[] dst) {
    ubyte[4096] buf = void;  // uninitialized — must write before read
    // ... fill buf, then copy to dst
}
```

---

## Array Append May Reallocate

Appending with `~=` may or may not reallocate. D arrays track capacity but the GC decides when to reallocate. After reallocation, existing slices into the old buffer become stale.

```d
import std.stdio : writeln;

void main() {
    int[] arr = [1, 2, 3];
    int[] view = arr;       // view aliases arr

    arr ~= 4;               // may reallocate arr

    // view may now point to stale memory — don't write through view after ~= on arr
    writeln(arr);           // [1, 2, 3, 4]
    writeln(view);          // [1, 2, 3] — but ptr may differ from arr.ptr
}
```

Use `arr.reserve(n)` before batch appends to reduce reallocations. Use `assumeSafeAppend` only when you are certain no other slice shares the backing store.

---

## UFCS Lookup Is Module-Scoped

Uniform Function Call Syntax (`value.func()` = `func(value)`) only finds functions visible in the current scope. A function in another module must be imported even if the type is from that module.

```d
import std.range : iota;
// import std.array;  // needed for .array

void main() {
    // auto arr = iota(5).array;  // Error: array not in scope
    // Must import std.array for .array to resolve via UFCS
}
```

This is a frequent source of "no property array for type…" errors. Always import the module that owns the function, not just the module that owns the type.
