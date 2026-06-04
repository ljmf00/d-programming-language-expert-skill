---
name: d-lang-memory
description: >-
  D memory management and safety: GC, RAII, scope, @safe/@trusted/@system,
  const/immutable/shared, copy constructors (DIP 1018), move semantics
  (DIP 1040 move constructors, DIP 1014 opPostMove), @live ownership system,
  destructors.
  Use when optimizing memory or ensuring memory safety.
license: MIT
metadata:
  topics: gc memory-safety const immutable shared live scope raii
  order: 02
---

# D Programming Language - Memory Management

Comprehensive guide to D's memory management: garbage collection, RAII, memory safety attributes, and the const/immutable system.

## Table of Contents

- [Garbage Collection](#garbage-collection)
- [RAII and Scope Statements](#raii-and-scope-statements)
- [Memory Safety Model](#memory-safety-model)
- [const and immutable](#const-and-immutable)
- [shared Keyword](#shared-keyword)
- [Copy Constructor (DIP 1018)](#copy-constructor-dip-1018)
- [Postblit vs Copy Constructor](#postblit-vs-copy-constructor)
- [Move Semantics (DIP 1040)](#move-semantics-dip-1040)
- [core.memory (GC API) Detailed](#corememory-gc-api-detailed)
- [Reference Counting](#reference-counting)
- [`@system` Variables (DIP 1035)](#@system-variables-dip-1035)
- [`@live` Function Attribute](#@live-function-attribute)
- [Allocator Framework (std.experimental.allocator)](#allocator-framework-stdexperimentalallocator)
- [Manual Memory Management](#manual-memory-management)
- [Custom Allocators](#custom-allocators)
- [Quick Reference](#quick-reference)

## Garbage Collection

### Automatic Memory Management

```d
// Objects on the garbage-collected heap
class MyClass {
    int data;
}

void main() {
    auto obj = new MyClass();  // Allocated on GC heap
    obj.data = 42;
    // No need to delete - GC handles it
}
```

### GC Control

```d
import core.memory : GC;

// Force garbage collection
GC.collect();
```

### GC-Free Code

```d
// @nogc functions cannot allocate on GC heap
void noGCFunction() @nogc {
    // Cannot use:
    // - new (for classes)
    // - dynamic arrays (unless reusing existing capacity)
    // - string concatenation
    // - most Phobos functions

    // Can use:
    // - stack allocation
    // - static arrays
    // - pointers
    int x = 42;
}
```

### When GC Runs

- When heap is full
- Explicitly via `GC.collect()`
- At program exit
- Periodically in background thread (if enabled)

## RAII and Scope Statements

### RAII (Resource Acquisition Is Initialization)

```d
import std.stdio : File;

void processFile() {
    auto file = File("data.txt", "r");  // Acquire resource
    foreach (line; file.byLine()) {
        // Process line
    }
}  // File automatically closed here (destructor)
```

### scope Statement

```d
// scope(exit): execute on scope exit
void example() {
    scope(exit) writeln("Exiting example");

    // ... code ...

    return;  // "Exiting example" printed
}

// scope(failure): execute only on exception
void riskyOperation() {
    scope(failure) writeln("Rolling back");

    // ... potentially throwing code ...
}

// scope(success): execute only on successful exit
void transaction() {
    scope(success) writeln("Committed");
    scope(failure) writeln("Rolling back");

    // ... code ...
}
```

### scope (Lifetime Annotation)

```d
// scope: prevents pointer values from escaping this scope
struct Handle {
    int* ptr;
    ~this() { /* cleanup */ }
}

void func() {
    scope Handle h;  // Destructor called at scope exit, ptr cannot escape
}
```

### RAII Patterns

```d
import std.stdio;

// File handling
void readFile(string path) {
    auto file = File(path, "r");
    foreach (line; file.byLineCopy()) {
        // Process line
    }
}  // Automatically closed

// Mutex locking
import core.sync.mutex : Mutex;

void criticalSection(Mutex mutex) {
    mutex.lock();
    // ... critical section ...
    mutex.unlock();
}  // Manual release

// Custom RAII wrapper
struct TempFile {
    string path;

    this(string content) {
        import std.file : write;
        path = "tempfile.txt";
        write(path, content);
    }

    ~this() {
        import std.file : remove;
        try { remove(path); } catch (Exception) { }
    }
}
```

## Memory Safety Model

### @safe: Memory-Safe Code

```d
// @safe: no pointer arithmetic, no casts, no unsafe operations
int safeFunction() @safe {
    int x = 42;
    int* p = &x;
    // *p = 10;  // Error: dereferencing pointer in @safe
    return x;
}
```

### @system: Unsafe Code

```d
// @system: allows all operations
int systemFunction() @system {
    int x = 42;
    int* p = &x;
    *p = 10;  // OK in @system
    return x;
}
```

### @trusted: Manually Verified Safe

```d
// @trusted: compiler trusts this is safe
int trustedFunction() @trusted {
    // Manually verified to be safe
    int x = 42;
    int* p = &x;
    *p = 10;
    return x;
}
```

### Safety Hierarchy

```
@safe (most restrictive)
  -> calls
@trusted (manually verified)
  -> calls
@system (least restrictive)
```

### Safety Rules

```d
// @safe allows:
int safeCode() @safe {
    int x = 42;
    int y = x + 1;           // Arithmetic
    int[] arr = [1, 2, 3];   // Dynamic arrays
    int first = arr[0];       // Array indexing (bounds checked)
    return arr[0];
}

// @safe disallows:
// int unsafeCode() @safe {
//     int x = 42;
//     int* p = &x;           // Error: pointer to local
//     // *p = 10;            // Error: pointer dereference
//     // cast(int)p;         // Error: cast
//     // asm { ... }         // Error: inline asm
// }
```

### Building Safe Code

```d
// Start with @safe
int safeFunc() @safe {
    return 42;
}

// If you need unsafe operations, use @trusted wrapper
int unsafeOperation() @system {
    return 42;
}

int trustedWrapper() @trusted {
    return unsafeOperation();  // Call @system code
}

// Mark caller as @system if it calls @trusted
int caller() @system {
    return trustedWrapper();
}
```

## const and immutable

### const: Read-Only View

```d
// const: read-only, but underlying data may be mutable
const int x = 42;
// x = 10;  // Error: cannot modify const

const(int)* p;     // Pointer to const int
// int* const p;   // Const pointer to int (not valid D syntax, use ref)

// Transitive const
const int[][] arr;  // 2D array where all elements are const
// arr[0][0] = 10;  // Error
```

### immutable: Truly Read-Only

```d
// immutable: truly read-only, thread-safe, shareable
immutable int x = 42;
// x = 10;  // Error

immutable string s = "Hello";  // Immutable string (default for string literals)

// Immutable data can be shared across threads
immutable int[] sharedData = [1, 2, 3];
```

### const vs immutable

```d
// const: mutable underlying data, read-only view
void processConst(const(int[]) arr) {
    // Cannot modify arr through this parameter
    // But underlying data may be modified by other references
}

// immutable: truly read-only, safe to share
void processImmutable(immutable(int[]) arr) {
    // Cannot modify arr
    // Underlying data is guaranteed not to change
    // Safe to share with other threads
}
```

### const in Functions

```d
// const parameter: function promises not to modify
void process(const int[] arr) {
    // arr is read-only through this parameter
}

// immutable parameter: data is truly constant
void process(immutable int[] arr) {
    // arr is truly constant
}

// Return const
const(int)[] getConstSlice(const(int[]) arr) {
    return arr[0 .. 2];
}
```

### const and Classes

```d
class MyClass {
    int value;

    this(int v) {
        value = v;
    }

    void modify() {
        value = 42;
    }

    void show() const {
        // Cannot call non-const methods
        // show();  // Error
        // value = 42;  // Error
    }
}

void main() {
    auto obj = new MyClass(10);
    const objConst = obj;  // const reference
    // objConst.modify();  // Error: cannot call non-const method
    objConst.show();       // OK
}
```

### immutable for Concurrency

```d
// Immutable data is thread-safe by definition
immutable int[] data = [1, 2, 3, 4, 5];

// Can be shared across threads without synchronization
void threadFunction(immutable int[] data) {
    // Safe to read without locks
    foreach (elem; data) {
        // Process elem
    }
}
```

## shared Keyword

### shared Data

```d
// shared: data shared between threads
shared int counter = 0;

// Access requires synchronization
import core.sync.mutex : Mutex;

void increment(shared int* counter, Mutex mutex) {
    mutex.lock();
    // Cast away shared for synchronized access
    auto local = cast(int*)counter;
    (*local)++;
    mutex.unlock();
}
```

### shared Classes

```d
shared class SharedData {
    int value;

    this(int v) {
        value = v;
    }
}

void main() {
    shared SharedData data = new shared SharedData(42);
}
```

### shared and const/immutable

```d
// shared const: shared, read-only
shared const int x = 42;

// shared immutable: shared, truly constant
shared immutable int y = 42;

// immutable is implicitly shared
immutable int z = 42;  // Also shared
```

## Manual Memory Management

### malloc/free

```d
import core.stdc.stdlib : malloc, free;

void manualAllocation() {
    enum size = 1024;
    auto ptr = malloc(size);
    scope(exit) free(ptr);

    // Use ptr...
}
```

### Custom Allocation with std.experimental.allocator

Class-level `new`/`delete` overloads (`opNew`/`opDelete`) and the `delete`
keyword were **removed** from the language. To allocate outside the GC, use
`std.experimental.allocator` (or `core.stdc.stdlib` directly):

```d
import std.experimental.allocator : make, dispose;
import std.experimental.allocator.mallocator : Mallocator;

class MyClass {
    int data;

    this(int d) {
        data = d;
    }
}

void customAllocation() {
    // make!T constructs on the chosen allocator; dispose runs the destructor
    // and frees the memory.
    auto obj = Mallocator.instance.make!MyClass(42);
    scope(exit) Mallocator.instance.dispose(obj);
}
```

### Stack Allocation

```d
// Stack allocation for structs
struct Point {
    double x, y;
}

void stackAllocation() {
    Point p;  // Allocated on stack
    p.x = 1.0;
    p.y = 2.0;
}  // Automatically freed at scope exit
```

## Copy Constructor (DIP 1018)

```d
struct Data {
    int[] buffer;

    // Copy constructor (DIP 1018): parameter is taken by `ref`.
    this(ref return scope const typeof(this) other) {
        this.buffer = new int[other.buffer.length];
        this.buffer[] = other.buffer[];
    }
}
```

> A `this(ref S)` constructor is a **copy** constructor, not a move constructor.
> A move constructor takes its parameter **by value** (`this(S)`) — see
> [Move Semantics](#move-semantics-dip-1040) below.

## Postblit vs Copy Constructor

```d
// Postblit (old-style, predates DIP 1018)
struct OldStyle {
    int[] data;
    this(this) {  // Postblit: called after bitwise copy
        data = data.dup;  // Deep copy
    }
}

// Copy constructor (modern, DIP 1018)
struct NewStyle {
    int[] data;
    this(ref return scope const typeof(this) other) {
        this.data = other.data.dup;
    }
}
```

## Move Semantics (DIP 1040)

A **move constructor** takes its own type **by value** — `this(S)` — so it binds
to rvalues and ends the source's lifetime (DIP 1040, DMD 2.111+/LDC 1.41+). This
is distinct from the by-`ref` copy constructor and from the legacy DIP 1014
`opPostMove` blit-fixup hook. Application code normally uses
[`core.lifetime.move`](https://dlang.org/phobos/core_lifetime.html#.move) rather
than the `__rvalue(...)` primitive directly.

```d
import core.lifetime : move;

// Move-only type: copying disabled, transfer via a by-value move constructor.
struct Buffer {
    int[] data;

    this(int[] d) {
        data = d;
    }

    // Move constructor (by value) — NOT `this(ref Buffer)`, which is a copy ctor.
    this(Buffer rhs) {
        data = rhs.data;
        rhs.data = null;  // leave the source benign for its own destructor
    }

    @disable this(ref Buffer);  // no copying
}

void main() {
    auto src = Buffer([1, 2, 3]);
    auto dst = move(src);  // destructive move: src.data is now null
    // auto copy = dst;    // error: copy construction is @disabled
}
```

> `__rvalue(x)` forces an lvalue to be treated as an rvalue (D's `std::move`
> analogue) and is `@system`; prefer `core.lifetime.move`, which infers safety.

## core.memory (GC API) Detailed

### GC Control Functions

```d
import core.memory : GC;

void gcExample() {
    // Explicitly add/remove roots
    auto ptr = GC.malloc(100);
    GC.addRoot(cast(void*)ptr);       // Prevent collection
    GC.removeRoot(cast(void*)ptr);    // Allow collection
}
```

### Allocation Attributes

```d
import core.memory : GC;

// BlkAttr flags:
GC.BlkAttr.NONE               // Finalize on collect
GC.BlkAttr.FINALIZE            // Run finalizer on collect
GC.BlkAttr.NO_SCAN             // Don't scan for pointers
GC.BlkAttr.NO_MOVE             // Don't move during compaction
GC.BlkAttr.APPENDABLE          // Allows appending
```

## Reference Counting

### Manual Reference Counting

Reference counting needs value semantics, so it is a **struct** (a class is a GC
reference and cannot have a postblit or copy constructor). Use a copy constructor
to bump the count and the destructor to drop it — there is no `delete` keyword:

```d
struct RefCounted(T) {
    private T* ptr;
    private int* refCount;

    this(T value) {
        ptr = new T(value);
        refCount = new int(1);
    }

    // Copy constructor (DIP 1018): increment on copy.
    this(ref return scope const RefCounted other) {
        ptr = cast(T*) other.ptr;
        refCount = cast(int*) other.refCount;
        if (refCount) (*refCount)++;
    }

    ~this() {  // Decrement on destroy
        if (refCount && --(*refCount) == 0) {
            // Drop our references; the GC reclaims the blocks (or call
            // destroy()/the allocator's dispose for non-GC storage).
            ptr = null;
            refCount = null;
        }
    }

    ref T get() {
        return *ptr;
    }
}
```

### Using std.typecons.RefCounted

```d
import std.typecons : RefCounted;

struct ExpensiveResource {
    int[1000] data;
}

auto resource = RefCounted!(ExpensiveResource)(ExpensiveResource());
// Automatically reference-counted
```

## `@system` Variables (DIP 1035)

```d
// @system variables: opt out of safe by default
@system int* ptr;  // This variable is @system, not @safe

// Usage in @safe code
@safe void safeFunc() {
    // Can access @system variables but with restrictions
}
```

## `@live` Function Attribute

The `@live` attribute enables ownership/borrowing checking similar to Rust:

```d
// The @live attribute enables ownership/borrowing checking on functions
// @live is supported by both DMD and LDC (experimental in both).
```

## Allocator Framework (std.experimental.allocator)

```d
import std.experimental.allocator : make, dispose;
import std.experimental.allocator.mallocator : Mallocator;

// Simple malloc allocator
void example() {
    auto alloc = Mallocator.instance;

    // Allocate and construct
    auto obj = alloc.make!int(42);
    scope(exit) alloc.dispose(obj);
}
```

### Allocator Building Blocks

```d
// Allocator building blocks are available in std.experimental.allocator
// APIs may vary between D compiler versions.
// See: https://dlang.org/phobos/std_experimental_allocator.html
```

## Custom Allocators

### Custom Allocator Class

```d
class PoolAllocator {
    private byte[1024 * 1024] pool;  // 1 MB pool
    private size_t offset = 0;

    void* allocate(size_t size) {
        if (offset + size > pool.length) {
            throw new Exception("Pool exhausted");
        }
        void* ptr = pool[offset .. $].ptr;
        offset += size;
        return ptr;
    }

    void deallocate(void* ptr) {
        // Pool allocator doesn't deallocate individually
    }

    void reset() {
        offset = 0;
    }
}
```

### Using Custom Allocator

```d
// Custom allocator APIs are available in std.experimental.allocator.
// The API surface is version-dependent; see Phobos documentation.
```

## Quick Reference

### GC Control

```d
import core.memory : GC;

void gcExample() {
    GC.collect();          // Force collection
    GC.disable();          // Disable GC
    GC.enable();           // Enable GC
}
```

### scope Statements

```d
import std.stdio;

void example() {
    scope(exit) writeln("cleanup");      // Always execute
    scope(failure) writeln("rollback");  // On exception
    scope(success) writeln("commit");    // On success
}
```

### Memory Safety

```d
// @safe      Memory-safe code
// @system    Unsafe code allowed
// @trusted   Manually verified safe
// @live      Ownership/borrowing opt-in (experimental)
```

### const/immutable

```d
// const int x;        Read-only view (requires initialization)
// immutable int y;     Truly read-only (thread-safe)
// shared int z;        Shared between threads
// inout int w;         Qualifier carried through (inside template functions only)
```

### RAII Patterns

```d
import std.stdio;

void main() {
    // File handling
    auto file = File("output.txt", "w");
    file.writeln("Hello");

    // Mutex locking
    import core.sync.mutex : Mutex;
    auto mutex = new Mutex();
    mutex.lock();
    // ... critical section ...
    mutex.unlock();
}
```

### GC API Functions

```d
import core.memory : GC;

void gcApiExample() {
    GC.collect();              // Force collection
    GC.disable();              // Disable GC
    GC.enable();               // Enable GC
    auto p = GC.malloc(100);   // Allocate GC memory
    auto q = GC.calloc(100);   // Allocate zeroed GC memory
}
```

### Lifecycle Functions

```d
// this(T args)                  Constructor
// this(this)                    Postblit (legacy copy hook)
// this(ref return scope const S) Copy constructor (DIP 1018)
// this(S)                        Move constructor (DIP 1040, by value)
// ~this()                        Destructor
// destroy(obj)                   Explicit finalization (object.destroy)
```

## Common Idioms

### Safe Resource Management

```d
import std.stdio;

auto acquireResource() { return File("output.txt", "w"); }
void releaseResource(File f) { f.close(); }

void processResource() {
    auto resource = acquireResource();
    scope(exit) releaseResource(resource);

    resource.writeln("Hello");
}
```

### Immutable Data Sharing

```d
// Create immutable data
immutable int[] data = [1, 2, 3, 4, 5];

// Share across threads
void threadFunc(immutable int[] data) {
    // Safe to read without locks
}
```

### GC-Free Code

```d
void noGCFunction() @nogc {
    // Use stack allocation
    int[100] buffer;

    // Use pointers
    int* ptr = &buffer[0];

    // Avoid:
    // - new
    // - dynamic arrays
    // - string concatenation
}
```

### Copy vs Move

```d
import std.algorithm.mutation : move;

void main() {
    auto source = [1, 2, 3];
    auto copy = source;          // Copy
    auto dest = move(source);    // Move (source is emptied)
}
```

## References

- [SafeD Article](https://dlang.org/articles/safed.html)
- [const FAQ](https://dlang.org/articles/const-faq.html)
- [Memory Safety Specification](https://dlang.org/spec/memory-safe-d.html)
- [DIP 1014 - Hooking D's struct move semantics (`opPostMove`)](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1014.md)
- [DIP 1018 - Copy Constructor](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1018.md)
- [DIP 1040 - Copying, Moving, and Forwarding (move constructors)](https://github.com/dlang/DIPs/blob/master/DIPs/other/DIP1040.md)
- [core.lifetime.move](https://dlang.org/phobos/core_lifetime.html#.move)
- [DIP 1035 - @system Variables](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1035.md)
- [D Language Specification](https://dlang.org/spec/)
