---
name: d-lang-runtime-internals
description: >-
  D runtime internals: GC, TypeInfo, Object/Throwable hierarchy, array/string
  internals, core.lifetime (emplace, move, forward), ModuleInfo, thread-local
  storage, core.thread. Use when debugging runtime behavior, understanding
  memory layout, or working with low-level D runtime APIs.
license: MIT
metadata:
  topics: runtime gc typeinfo object array core.lifetime core.thread tls
  order: 09
---

# D Programming Language - Runtime Internals

Comprehensive guide to D's druntime internals: garbage collection, type information system, Object/Throwable hierarchy, array and string internals, lifetime management, module lifecycle, and threading primitives.

## Table of Contents
- [Garbage Collection (core.memory)](#garbage-collection-corememory)
- [TypeInfo and typeid](#typeinfo-and-typeid)
- [Object Base Class](#object-base-class)
- [Throwable Hierarchy](#throwable-hierarchy)
- [Array and String Internal Layout](#array-and-string-internal-layout)
- [core.lifetime (emplace, move, forward)](#corelifetime-emplace-move-forward)
- [core.exception Handlers](#coreexception-handlers)
- [ModuleInfo and Module Lifecycle](#moduleinfo-and-module-lifecycle)
- [Thread-Local Storage](#thread-local-storage)
- [core.thread Basics](#corethread-basics)
- [Quick Reference](#quick-reference)

## Garbage Collection (core.memory)

### GC Enable/Disable
```d
import core.memory : GC;

void toggleGC() {
    GC.disable();  // Pause GC (useful for real-time sections)
    // ... critical section ...
    GC.enable();   // Resume GC
}
```

### Force Collection
```d
import core.memory : GC;

void forceCollect() {
    GC.collect();  // Force a full collection cycle
}
```

### GC Statistics
```d
import core.memory : GC;
import std.stdio;

void printGCStats() {
    auto stats = GC.stats();
    writeln("Used size: ", stats.usedSize);
    writeln("Free size: ", stats.freeSize);
}
```

### GC Roots
```d
import core.memory : GC;

void manageRoots() {
    int value = 42;
    void* root = &value;
    
    GC.addRoot(root);      // Prevent root from being collected
    GC.removeRoot(root);   // Allow root to be collected
}
```

### GC Allocation
```d
import core.memory : GC;

void gcAllocate() {
    // Allocate raw memory from GC
    void* ptr = GC.malloc(100);
    // Memory is tracked by GC, no need to free
}
```

### GC Allocation with Attributes
```d
import core.memory : GC;

void gcAllocateAttr() {
    // Allocate with NO_SCAN: GC won't scan for pointers in this block
    void* ptr = GC.malloc(100, GC.BlkAttr.NO_SCAN);
    // Useful for binary data without pointer references
}
```

### GC-Free Code with @nogc
```d
void noGCFunc() @nogc {
    // No GC allocations allowed
    int x = 42;
    int[10] arr;  // Stack allocation is fine
    // new int()  // Error: GC allocation in @nogc
}
```

### GC Disable Pattern for Real-Time
```d
import core.memory : GC;

void realTimeSection() {
    GC.disable();
    scope(exit) GC.enable();  // Always re-enable on exit
    
    // Deterministic execution here
    // No GC pauses possible
}
```

## TypeInfo and typeid

### Basic typeid Usage
```d
import std.stdio;

void checkTypes() {
    int x = 42;
    auto ti = typeid(x);  // Get TypeInfo for runtime type
    writeln(ti.toString());     // Runtime type name
}
```

### typeid with Classes
```d
import std.stdio;

class Animal { }
class Dog : Animal { }

void checkClassTypes() {
    auto ti = typeid(Dog);
    writeln(ti.toString()); // Full type name
    
    Animal a = new Dog();
    writeln(typeid(a));     // Runtime type
}
```

### Runtime Type Comparison
```d
import std.stdio;

void compareTypes() {
    int x = 42;
    bool isInt = typeid(int) == typeid(typeof(x));
    writeln(isInt);  // true
    
    bool isNotString = typeid(int) != typeid(string);
    writeln(isNotString);  // true
}
```

### TypeInfo for Value Types
```d
import std.stdio;

struct Point {
    int x;
    int y;
}

void structTypeInfo() {
    auto ti = typeid(Point);
    writeln(ti.toString());  // Full type name
}
```

### TypeInfo Hierarchy Navigation
```d
import std.stdio;

class Base { }
class Derived : Base { }

void typeHierarchy() {
    auto derivedTi = typeid(Derived);
    writeln(derivedTi.toString());  // "class Derived"
    
    auto baseTi = typeid(Base);
    writeln(baseTi.toString());  // "class Base"
}
```

### typeid with Templates
```d
import std.stdio;

void templateTypes() {
    auto ti1 = typeid(int[]);
    writeln(ti1.toString());  // "int[]"
    
    auto ti2 = typeid(int[string]);
    writeln(ti2.toString());  // "int[string]"
}
```

### typeid Returns TypeInfo
```d
import std.stdio;

void typeInfoReturn() {
    TypeInfo ti = typeid(double);
    writeln(ti.toString());  // "double"
    
    TypeInfo ti2 = typeid(bool);
    writeln(ti2.toString());  // "bool"
}
```

## Object Base Class

### Object is Root of All Classes
```d
class MyClass {
    int value;
}

void checkObjectBase() {
    // All classes inherit from Object implicitly
    MyClass obj = new MyClass();
    Object base = obj;  // Implicit upcast to Object
    assert(base !is null);
}
```

### Object.toString
```d
import std.stdio;

class Person {
    string name;
    
    this(string n) {
        name = n;
    }
    
    override string toString() {
        return "Person(" ~ name ~ ")";
    }
}

void testToString() {
    auto p = new Person("Alice");
    writeln(p.toString());  // "Person(Alice)"
}
```

### Object.opEquals
```d
import std.stdio;

class Box {
    int value;
    
    this(int v) {
        value = v;
    }
    
    override bool opEquals(Object other) {
        auto b = cast(Box) other;
        return b !is null && value == b.value;
    }
}

void testOpEquals() {
    auto a = new Box(42);
    auto b = new Box(42);
    writeln(a == b);  // true (uses opEquals)
}
```

### Object.toHash
```d
import std.stdio;

class Key {
    int id;
    
    this(int i) {
        id = i;
    }
    
    override size_t toHash() const {
        return id;
    }
    
    override bool opEquals(Object other) const {
        auto k = cast(Key) other;
        return k !is null && id == k.id;
    }
}

void testToHash() {
    auto k = new Key(123);
    writeln(k.toHash());  // 123
}
```

### Object.opCmp
```d
import std.stdio;

class Item {
    int priority;
    
    this(int p) {
        priority = p;
    }
    
    override int opCmp(Object other) {
        auto i = cast(Item) other;
        if (i is null) return 1;
        return priority - i.priority;
    }
}

void testOpCmp() {
    auto a = new Item(1);
    auto b = new Item(2);
    writeln(a < b);  // true (uses opCmp)
}
```

## Throwable Hierarchy

### Exception Base Class
```d
import std.stdio;

void throwException() {
    try {
        throw new Exception("Something went wrong");
    }
    catch (Exception e) {
        writeln("Caught: ", e.msg);
    }
}
```

### AssertError
```d
import std.stdio;
import core.exception : AssertError;

void testAssertError() {
    try {
        assert(false, "This always fails");
    }
    catch (AssertError e) {
        writeln("Assert failed: ", e.msg);
    }
}
```

### RangeError
```d
import std.stdio;
import core.exception : RangeError;

void testRangeError() {
    try {
        int[] arr = [1, 2, 3];
        int x = arr[10];  // Out of bounds
    }
    catch (RangeError e) {
        writeln("Range error: ", e.msg);
    }
}
```

### OutOfMemoryError
```d
import std.stdio;
import core.exception : OutOfMemoryError;

void testOOM() {
    try {
        // OutOfMemoryError is thrown by GC when allocation fails
        // Normally only happens under extreme memory pressure
        throw new OutOfMemoryError("Manual OOM test");
    }
    catch (OutOfMemoryError e) {
        writeln("OOM: ", e.msg);
    }
}
```

### Throwable Properties
```d
import std.stdio;

void checkThrowableProps() {
    try {
        throw new Exception("Test message");
    }
    catch (Exception e) {
        writeln(e.msg);           // "Test message"
        writeln(e.toString());    // Full exception info
    }
}
```

### std.exception.enforce
```d
import std.stdio;
import std.exception : enforce;

void testEnforce() {
    try {
        enforce(false, "Condition not met");
    }
    catch (Exception e) {
        writeln("Enforced: ", e.msg);
    }
}
```

### Custom Exception
```d
import std.stdio;

class MyError : Exception {
    int errorCode;
    
    this(string msg, int code) {
        super(msg);
        errorCode = code;
    }
}

void throwCustom() {
    try {
        throw new MyError("Custom error", 404);
    }
    catch (MyError e) {
        writeln("Code: ", e.errorCode);
        writeln("Msg: ", e.msg);
    }
}
```

### Catch Order Matters
```d
import std.stdio;

void catchOrder() {
    try {
        throw new Exception("base");
    }
    catch (Exception e) {  // Catches Exception and all subclasses
        writeln("Caught: ", e.msg);
    }
}
```

## Array and String Internal Layout

### Dynamic Array Structure
```d
import std.stdio;

void arrayLayout() {
    int[] arr = [1, 2, 3, 4, 5];
    writeln("length: ", arr.length);   // size_t: 5
    writeln("ptr: ", arr.ptr);         // int*: pointer to data
    writeln("first: ", *arr.ptr);      // 1
}
```

### String is Immutable Char Array
```d
import std.stdio;

void stringLayout() {
    string s = "Hello";
    // string == immutable(char)[]
    writeln(s.length);     // 5
    writeln(s[0]);         // 'H'
    writeln(s.ptr);        // pointer to string data
}
```

### Array Slice Operations
```d
import std.stdio;

void arraySlices() {
    int[10] data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    int[] slice = data[2 .. 8];  // [2, 3, 4, 5, 6, 7]
    writeln(slice.length);  // 6
    writeln(slice.ptr);     // Points to data[2]
}
```

### Array Concatenation
```d
import std.stdio;

void arrayConcat() {
    int[] a = [1, 2, 3];
    int[] b = [4, 5, 6];
    int[] c = a ~ b;  // [1, 2, 3, 4, 5, 6]
    writeln(c.length);  // 6
}
```

### Array Duplication
```d
import std.stdio;

void arrayDup() {
    int[] original = [1, 2, 3];
    int[] copy = original.dup;  // Deep copy
    
    copy[0] = 99;
    writeln(original[0]);  // 1 (unchanged)
    writeln(copy[0]);      // 99
}
```

### Empty Array vs Null
```d
import std.stdio;

void emptyVsNull() {
    int[] empty = [];
    int[] nul = null;
    
    writeln(empty.length);  // 0
    writeln(nul.length);    // 0 (null array has length 0)
    
    writeln(empty == nul);  // true (both are "empty")
}
```

### Associative Array Internals
```d
import std.stdio;

void aaInternals() {
    int[string] map;
    map["one"] = 1;
    map["two"] = 2;
    
    writeln(map.length);  // 2
    writeln(map.keys);    // Range of keys
}
```

### Multi-Dimensional Array Layout
```d
import std.stdio;

void multiDimArray() {
    // Jagged array: array of arrays
    int[][] matrix = [[1, 2], [3, 4, 5]];
    writeln(matrix.length);      // 2
    writeln(matrix[0].length);   // 2
    writeln(matrix[1].length);   // 3
}
```

## core.lifetime (emplace, move, forward)

### emplace: Construct in Place
```d
import core.lifetime : emplace;
import core.memory : GC;
import std.stdio;

struct Point {
    int x;
    int y;
    this(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

void testEmplacePoint() {
    auto buf = cast(Point*)GC.malloc(Point.sizeof);
    auto p = emplace!Point(buf, 10, 20);
    writeln(p.x);  // 10
    writeln(p.y);  // 20
}

// Note: emplace takes T* not void*; cast the buffer
```

### emplace Without Constructor Args
```d
import core.lifetime : emplace;
import core.memory : GC;

struct Simple {
    int value;
}

void testEmplaceSimple() {
    auto buf = cast(Simple*)GC.malloc(Simple.sizeof);
    auto s = emplace!Simple(buf);
    s.value = 99;
    writeln(s.value);  // 99
}
```

### forward: Preserve Value Category
```d
import core.lifetime : forward;
import std.stdio;

void sink(int x) {
    writeln("rvalue: ", x);
}

void sink(ref int x) {
    writeln("lvalue: ", x);
}

void testForward(T)(T arg) {
    sink(forward!arg);  // Preserves lvalue/rvalue category
}

void callForward() {
    int y = 5;
    testForward(y);     // "lvalue: 5"
    testForward(42);    // "rvalue: 42"
}
```

### move: Transfer Ownership
```d
import core.lifetime : move;
import std.stdio;

void testMove() {
    int[] src = [1, 2, 3];
    int[] dst = move(src);
    
    writeln(dst.length);  // 3
    writeln(src.length);  // 0 (src is emptied)
}
```

### move with Structs
```d
import core.lifetime : move;
import std.stdio;

struct Resource {
    int[] data;
    
    // Move constructor
    this(ref Resource other) {
        this.data = other.data;
        other.data = null;
    }
    
    // Disable copy
    @disable this(this);
}

void testMoveStruct() {
    auto src = Resource([1, 2, 3]);
    auto dst = move(src);
    writeln(dst.data.length);  // 3
}
```

### moveEmplace: Move-Construct in Place
```d
import core.lifetime : moveEmplace;
import core.memory : GC;

struct Movable {
    int value;
    
    this(ref Movable other) {
        value = other.value;
        other.value = 0;
    }
    
    @disable this(this);
}

void testMoveEmplace() {
    auto src = Movable(42);
    auto buf = cast(Movable*)GC.malloc(Movable.sizeof);
    moveEmplace!Movable(src, *buf);
    writeln(buf.value);  // 42
}
```

### Emplace on Stack Buffer
```d
import core.lifetime : emplace;
import std.stdio;

struct Small {
    short a;
    short b;
    
    this(short a_, short b_) {
        a = a_;
        b = b_;
    }
}

void testStackEmplace() {
    align(4) ubyte[4] buf;  // 4-byte aligned buffer
    auto s = cast(Small*)&buf;
    emplace!Small(s, cast(short)1, cast(short)2);
    writeln(s.a);  // 1
    writeln(s.b);  // 2
}
```

## core.exception Functions

### onOutOfMemoryError
```d
import core.exception : onOutOfMemoryError, OutOfMemoryError;

// Call to throw OutOfMemoryError with file/line info
void handleOOM() {
    try {
        onOutOfMemoryError(null);
    }
    catch (OutOfMemoryError e) {
        // Handle out of memory
    }
}
```

### onRangeError
```d
import core.exception : onRangeError, RangeError;

// Call to throw RangeError with file/line info
void handleRange() {
    try {
        onRangeError();
    }
    catch (RangeError e) {
        // Handle range error
    }
}
```

## ModuleInfo and Module Lifecycle

### Module Constructor
```d
import std.stdio;

// Runs once at program startup (per-thread)
static this() {
    writeln("Module initializing");
}
```

### Module Destructor
```d
import std.stdio;

// Runs once at program exit (per-thread)
static ~this() {
    writeln("Module finalizing");
}
```

### Shared Module Constructor
```d
import std.stdio;

// Runs once globally (shared across all threads)
shared static this() {
    writeln("Shared module init");
}
```

### Shared Module Destructor
```d
import std.stdio;

// Runs once globally at exit
shared static ~this() {
    writeln("Shared module cleanup");
}
```

### Module Init Order
```d
// Module constructors run in dependency order:
// 1. Modules with no dependencies first
// 2. Then modules depending on them
// 3. Destructors run in reverse order

int dependency1 = initialize();

int initialize() {
    return 42;
}
```

### ModuleInfo Structure
```d
// ModuleInfo contains:
// - Module name
// - Pointer to static this() / ~this()
// - Pointer to shared static this() / ~this()
// - Linked list of all modules

// Accessible via runtime internals for debugging
```

## Thread-Local Storage

### Default: Thread-Local
```d
import std.stdio;

// Global variables are thread-local by default
int threadLocalVar = 0;

void checkTLS() {
    threadLocalVar = 42;
    writeln(threadLocalVar);  // Each thread sees its own copy
}
```

### __gshared: True Global
```d
import std.stdio;

// __gshared: single copy shared across all threads
__gshared int globalVar = 0;

void checkGShared() {
    globalVar = 42;
    writeln(globalVar);  // All threads see same value
}
```

### shared: Type-Safe Shared
```d
import std.stdio;

// shared: compiler-enforced thread safety
shared int syncVar = 0;

void checkShared() {
    // Access requires casting away shared
    // or using atomic operations
    writeln(cast(int)syncVar);
}
```

### __gshared vs shared vs TLS
```d
// Thread-local (default): each thread has own copy
int tlsVar = 0;

// __gshared: one copy, no compiler checks
__gshared int gsVar = 0;

// shared: one copy, compiler enforces sync
shared int shVar = 0;
```

### TLS with Structs
```d
import std.stdio;

struct ThreadData {
    int counter;
    string name;
}

// Each thread gets its own ThreadData instance
ThreadData threadData;

void useThreadData() {
    threadData.counter++;
    threadData.name = "worker";
    writeln(threadData.counter);
}
```

### __gshared Array
```d
import std.stdio;

// __gshared array: shared across threads
__gshared int[10] sharedBuffer;

void useSharedBuffer() {
    sharedBuffer[0] = 42;
    writeln(sharedBuffer[0]);  // All threads see 42
}
```

## core.thread Basics

### Create and Start Thread
```d
import core.thread : Thread;
import std.stdio;

void createThread() {
    auto t = new Thread({
        writeln("Thread running");
    });
    t.start();
    t.join();  // Wait for completion
}
```

### Thread with Named Function
```d
import core.thread : Thread;
import std.stdio;

void workerFunction() {
    writeln("Worker executing");
}

void createThreadWithFunc() {
    auto t = new Thread(&workerFunction);
    t.start();
    t.join();
}
```

### Thread with Arguments
```d
import core.thread : Thread;
import std.stdio;

void createThreadWithArgs() {
    string msg = "Count";
    int count = 5;
    auto t = new Thread(() {
        writeln(msg, ": ", count);
    });
    t.start();
    t.join();
}
```

### Thread Properties
```d
import core.thread : Thread;
import std.stdio;

void checkThreadProps() {
    auto t = new Thread({
        // work
    });
    
    writeln(t.id);      // Thread ID
    writeln(t.isRunning);  // false (not started yet)
    
    t.start();
    writeln(t.isRunning);  // true
    t.join();
}
```

### Multiple Threads
```d
import core.thread : Thread;
import std.stdio;

void createMultipleThreads() {
    Thread[3] threads;
    
    foreach (i; 0 .. 3) {
        int id = i;
        threads[i] = new Thread(() {
            writeln("Thread ", id, " running");
        });
        threads[i].start();
    }
    
    foreach (t; threads) {
        t.join();
    }
}
```

### Thread Priority
```d
import core.thread : Thread;
import std.stdio;

void setThreadPriority() {
    auto t = new Thread({
        writeln("High priority thread");
    });
    t.start();
    
    // Set thread priority (platform dependent)
    t.join();
}
```

### Thread Duration
```d
import core.thread : Thread;
import std.stdio;

void setThreadDuration() {
    auto t = new Thread({
        writeln("Joinable thread");
    });
    t.start();
    
    // Thread duration policy (platform dependent)
    t.join();
}
```

## Quick Reference

### GC API
```d
import core.memory : GC;
GC.enable();              // Resume GC
GC.disable();             // Pause GC
GC.collect();             // Force collection
auto p = GC.malloc(1024); // Allocate from GC
GC.addRoot(&p);           // Add GC root
GC.removeRoot(&p);        // Remove GC root
auto stats = GC.stats();  // Get statistics
```

### TypeInfo
```d
auto ti = typeid(int);        // TypeInfo for type
auto ti2 = typeid(42);        // Runtime type of value
ti.toString();                // Full type description
typeid(int) == typeid(int);   // Type comparison
```

### Object Methods
```d
obj.toString()        // String representation
obj.opEquals(other)   // Equality check
obj.toHash()          // Hash code
obj.opCmp(other)      // Comparison (-1, 0, +1)
```

### core.lifetime
```d
import core.lifetime;
emplace!T(ptr, args...)    // Construct T at ptr
move(src)                  // Transfer ownership
forward!arg                // Preserve value category
moveEmplace!T(ptr, src)    // Move-construct at ptr
```

### Module Lifecycle
```d
static this() { }          // Per-thread module constructor
static ~this() { }         // Per-thread module destructor
shared static this() { }   // Global module constructor
shared static ~this() { }  // Global module destructor
```

### Thread-Local Storage
```d
int tlsVar;                // Thread-local (default)
__gshared int gsVar;       // True global, no checks
shared int shVar;          // Shared, compiler-checked
immutable int immVar;      // Immutable, thread-safe
```

### core.thread
```d
import core.thread : Thread;
void worker() {}
auto t = new Thread(&worker);  // Create thread
auto s = new Thread({});       // Create with delegate
s.start();                     // Start execution
s.join();                      // Wait for completion
s.id;                          // Thread ID
s.isRunning;                   // Running status
```

## References
- [core.memory](https://dlang.org/phobos/core_memory.html)
- [core.lifetime](https://dlang.org/phobos/core_lifetime.html)
- [core.exception](https://dlang.org/phobos/core_exception.html)
- [core.thread](https://dlang.org/phobos/core_thread.html)
- [object.d](https://dlang.org/phobos/object.html)
- [D Runtime Internals](https://dlang.org/spec/module.html)
