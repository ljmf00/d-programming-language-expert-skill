---
name: d-lang-core
description: >-
  D core language knowledge base: types, variables, functions, control flow,
  classes, structs, operator overloading, templates, attributes, error
  handling, conditional compilation, __traits, Better C, FFI.
  Use when writing or reviewing core D syntax and semantics.
license: MIT
metadata:
  topics: syntax types functions oop templates attributes
  order: 01
---

# D Programming Language - Core Language

Comprehensive guide to D's core language features: syntax, types, control flow, functions, and object-oriented programming.

## Table of Contents

- [Basic Structure](#basic-structure)
- [Types and Variables](#types-and-variables)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Conditional Compilation](#conditional-compilation)
- [`__traits` - Compile-Time Reflection](#__traits---compile-time-reflection)
- [`is` Expression - Type Checking](#is-expression---type-checking)
- [`typeof` and `typeid`](#typeof-and-typeid)
- [`alias` and `with`](#alias-and-with)
- [Error Handling](#error-handling)
- [Properties](#properties)
- [Pragmas](#pragmas)
- [User-Defined Attributes (UDA)](#user-defined-attributes-uda)
- [`noreturn` - Bottom Type](#noreturn---bottom-type)
- [`final` and `override`](#final-and-override)
- [abstract Class](#abstract-class)
- [Better C Mode](#better-c-mode)
- [Inline Assembler](#inline-assembler)
- [SIMD Vector Extensions](#simd-vector-extensions)
- [Interfacing to C](#interfacing-to-c)
- [Interfacing to C++](#interfacing-to-c)
- [Interfacing to Objective-C](#interfacing-to-objective-c)
- [Lvalues vs Rvalues](#lvalues-vs-rvalues)
- [`__gshared` - Global Shared Data](#__gshared---global-shared-data)
- [`__parameters` - Function Parameter Info](#__parameters---function-parameter-info)
- [`__rvalue` Forced Rvalue](#__rvalue-forced-rvalue)
- [`import` Expressions](#import-expressions)
- [`mixin` Expressions](#mixin-expressions)
- [`assert` and Contract Expressions](#assert-and-contract-expressions)
- [Tuple Unpacking](#tuple-unpacking)
- [String Interpolation `i"`](#string-interpolation-i)
- [Bitfields](#bitfields)
- [`static` Constructors/Destructors](#static-constructorsdestructors)
- [Modules and Packages](#modules-and-packages)
- [Classes and Structs](#classes-and-structs)
- [Interfaces](#interfaces)
- [Enums and Unions](#enums-and-unions)
- [Delegates and Function Pointers](#delegates-and-function-pointers)
- [Operator Overloading](#operator-overloading)
- [Attributes](#attributes)
- [Quick Reference](#quick-reference)

## Basic Structure

### Hello World

```d
module myapp;  // Module name matches file name

import std.stdio;

void main() {
    writeln("Hello, World!");
}
```

### Module Structure

```d
module my_package.my_module;

// Imports
import std.stdio;

// Global variables
int globalVar = 0;

// Functions
void myFunction() {
    writeln("Inside myFunction");
}

// Unit tests (run at program startup)
unittest {
    myFunction();
}
```

## Types and Variables

### Primitive Types

```d
// Boolean
bool flag = true;

// Integers (fixed size, platform-independent)
byte b = -128;        // 8-bit signed
ubyte ub = 255;       // 8-bit unsigned
short sh = -32768;     // 16-bit signed
ushort us = 65535;    // 16-bit unsigned
int i = int.min;  // -2147483648, 32-bit signed
uint ui = 4294967295; // 32-bit unsigned
long l = long.min;  // -9223372036854775808, 64-bit signed
ulong ul = ulong.max; // 18446744073709551615, 64-bit unsigned

// Floating point
float f = 3.14f;      // 32-bit
double d = 3.14;      // 64-bit (default for float literals)
real r = 3.14L;       // 80-bit or 128-bit (platform dependent)

// Characters
char c = 'A';         // UTF-8 code unit (1 byte)
wchar wc = 'A';       // UTF-16 code unit (2 bytes)
dchar dc = 'A';       // UTF-32 code unit (4 bytes, any Unicode)

// Strings (immutable by default)
string s = "Hello";        // immutable(char)[]
wstring ws = "Hello";      // immutable(wchar)[]
dstring ds = "Hello";      // immutable(dchar)[]

// Special values
int* p = null;    // null pointer
```

### Type Modifiers

```d
// const: read-only view (mutable underlying data can be modified through other references)
const int x = 5;
const int* p;     // pointer to const int
// int* const p;  // const pointer to int (not valid D syntax, use ref)

// immutable: truly read-only, thread-safe, shareable across threads
immutable int y = 10;
immutable string s = "constant string";

// shared: data shared between threads (requires synchronization)
shared int z = 0;

// inout: qualifier carried through function calls
inout(int)[] slice(inout(int)[] arr) {
    return arr[0 .. 2];
}
```

### Variable Declarations

```d
import std.stdio;

void main() {
    // auto: type inference
    auto x = 42;           // int
    auto s = "hello";      // string (immutable(char)[])
    auto arr = [1, 2, 3];  // int[3] (static array)

    // ref local variables — DIP 1046; guarded because not yet default in all compilers
    int a = 10;
    static if (__traits(compiles, { int _x = 0; ref int _y = _x; })) {
        ref int b = a;     // b is an alias for a
        b = 20;            // a is now 20
        writeln(a);        // prints 20
    }

    // scope: class instance may be stack-allocated, destructor called at scope exit
    class Resource {}
    scope r = new Resource();
}
```

### Arrays

```d
// Static arrays (size known at compile time)
int[5] staticArr = [1, 2, 3, 4, 5];
char[3] name = ['H', 'e', 'l'];

// Dynamic arrays (size known at runtime)
int[] dynArr = new int[10];
dynArr = [1, 2, 3, 4, 5];

// Slices (views into arrays)
int[] slice = staticArr[1 .. 4];  // [2, 3, 4]

// Associative arrays (hash maps)
int[string] aa;
aa["one"] = 1;
aa["two"] = 2;

// Literal syntax
int[] arr = [1, 2, 3, 4, 5];
int[string] map = ["a": 1, "b": 2, "c": 3];
```

### Slices

```d
// Slice syntax: array[start .. end]
int[10] data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
int[] slice1 = data[0 .. 5];    // [0, 1, 2, 3, 4]
int[] slice2 = data[5 .. $];    // [5, 6, 7, 8, 9] ($ is last index + 1)
int[] slice3 = data[];          // copy of entire array
int[] slice4 = data[2 .. 8];    // [2, 3, 4, 5, 6, 7]

// Array operations
int[] a = [1, 2, 3];
int[] b = a ~ [4, 5];           // concatenation: [1, 2, 3, 4, 5]
a ~= 6;                          // append: [1, 2, 3, 6]
```

## Control Flow

### if/else

```d
import std.stdio;

void main() {
    int value = 42;

    if (value > 0) {
        writeln("positive");
    } else if (value < 0) {
        writeln("negative");
    } else {
        writeln("zero");
    }

    // Ternary operator
    string label = value > 0 ? "positive" : "non-positive";
    writeln(label);
}
```

### switch

```d
void main() {
    int value = 2;
    switch (value) {
        case 1:
            // falls through to case 2
        case 2:
            writeln("One or two");
            break;
        case 3:
        case 4:
            writeln("Three or four");
            break;
        default:
            writeln("Something else");
    }
}
```

### while

```d
void main() {
    int i = 0;
    while (i < 3) {
        writeln(i);
        i++;
    }

    do {
        writeln(i);
        i--;
    } while (i > 0);
}
```

### for

```d
import std.stdio;

void main() {
    // Traditional for
    for (int i = 0; i < 10; i++) {
        writeln(i);
    }

    // Range-based for
    foreach (i; 0 .. 10) {
        writeln(i);
    }

    // Foreach over array
    int[] arr = [1, 2, 3, 4, 5];
    foreach (elem; arr) {
        writeln(elem);
    }

    // Foreach with index
    foreach (i, elem; arr) {
        writeln(i, ": ", elem);
    }

    // Foreach reverse
    foreach_reverse (i; 0 .. 10) {
        writeln(i);
    }

    // Foreach over associative array
    int[string] aa = ["one": 1, "two": 2];
    foreach (key, value; aa) {
        writeln(key, " -> ", value);
    }

    // Foreach over class instances
    class Obj { void process() { } }
    Obj[] objects = [new Obj(), new Obj()];
    foreach (obj; objects) {
        obj.process();
    }
}
```

### foreach with ref

```d
void main() {
    int[] arr = [1, 2, 3];
    foreach (ref elem; arr) {
        elem *= 2;  // Modifies original array
    }
    // arr is now [2, 4, 6]
}
```

### break and continue

```d
import std.stdio;

void main() {
    // break and continue
    foreach (i; 0 .. 10) {
        if (i == 5) break;
        if (i % 2 == 0) continue;
        writeln(i);
    }

    // Labeled break
    outer:
    foreach (i; 0 .. 10) {
        foreach (j; 0 .. 10) {
            if (i + j > 10) break outer;
        }
    }
}
```

## Functions

### Basic Function

```d
// Basic function
int add(int a, int b) {
    return a + b;
}

// Shortened method syntax (DIP 1043)
int multiply(int a, int b) pure => a * b;

// Named arguments (DIP 1030)
void configure(string host, int port = 443, bool ssl = true) { }

void main() {
    configure(host: "localhost", port: 8080, ssl: true);  // Named, reorderable
    configure(host: "localhost");                          // Omitted params use defaults
}
```

### Function Attributes

```d
// pure: no side effects, same input always gives same output
int pureFunction(int x) pure {
    return x * 2;
}

// nothrow: never throws exceptions
int safeFunction(int x) nothrow {
    return x + 1;
}

// @safe: memory-safe, no pointer arithmetic, no casts
int safeCode(int x) @safe {
    return x;
}

// @nogc: no garbage collection allocations
int noGCFunction() @nogc {
    return 42;
}

// @disable: disable a function
@disable void deletedFunction();

// @live: opt-in ownership/borrowing system
@live void appendData(int[] data) {
    // ownership/borrowing enforced by compiler
}

// Combined attributes
int pureSafeNoGC() pure nothrow @safe @nogc {
    return 42;
}

// Auto-attribute inference: D deduces pure, nothrow, @safe, @nogc when possible
auto inferred(int x) {
    // Compiler infers pure, nothrow, @safe automatically
    return x * 2;
}
```

### auto ref: Forwarding References

```d
// auto ref: becomes ref if argument is an lvalue, value otherwise
auto ref autoRefFunc()(auto ref int x) {
    return x;
}

int a = 10;
auto d = autoRefFunc(a);   // d is ref int
auto c = autoRefFunc(42);  // c is int (rvalue)
```

### `inout` Function Parameters

```d
// inout: propagate qualifiers (const/immutable/mutable) through function
inout(int)[] slice(inout(int)[] arr, size_t start, size_t end) {
    return arr[start .. end];
}

void main() {
    int[] mutableArr = [1, 2, 3, 4, 5];
    const(int)[] constArr = [1, 2, 3, 4, 5];
    immutable(int)[] immArr = [1, 2, 3, 4, 5];

    auto s1 = slice(mutableArr, 1, 3);  // int[]
    auto s2 = slice(constArr, 1, 3);    // const(int)[]
    auto s3 = slice(immArr, 1, 3);      // immutable(int)[]
}
```

### Parameter Types

```d
// in: read-only input (copy for structs, reference for classes)
void processIn(in int x) {
    // x cannot be modified
}

// out: output parameter (initialized to 0/void, checked on exit)
void processOut(out int x) {
    // x is initialized to 0
    x = 42;
}  // x is checked here (contract)

// ref: reference to caller's variable
void processRef(ref int x) {
    x = 42;  // Modifies caller's variable
}

// lazy: argument not evaluated until used
void logMessage(lazy string msg) {
    debug writeln(msg);  // Only evaluated in debug builds
}

// Variadic functions
int sum(int[] values...) {
    int total;
    foreach (v; values) {
        total += v;
    }
    return total;
}
```

### Function Overloading

```d
void greet(string name) {
    writeln("Hello, ", name);
}

void greet(int id) {
    writeln("Hello, user #", id);
}

void greet(string first, string last) {
    writeln("Hello, ", first, " ", last);
}
```

### Overload Resolution

```d
// More specific overload is chosen
void process(int x) {
    writeln("int");
}

void process(long x) {
    writeln("long");
}

process(42);      // Calls process(int)
process(42L);     // Calls process(long)
```

### Closures and Delegates

```d
// Delegate: function with closure
int makeAdder(int n) {
    int delegate() adder = () {
        return n;  // Captures n from outer scope
    };
    return adder();
}

// Function literal
auto square = (int x) => x * x;
writeln(square(5));  // 25

// Delegate with state
int counter = 0;
auto increment = () {
    return ++counter;
};
```

### Nested Functions

```d
void outer() {
    int x = 10;

    void inner() {
        writeln(x);  // Can access outer's variables
    }

    inner();
}
```

## Modules and Packages

### Module Declaration

```d
// File: my_package/my_module.d
module my_package.my_module;

import std.stdio;

public void publicFunction() {
    writeln("Public");
}

void privateFunction() {
    writeln("Private");
}
```

### Import Styles

```d
// Specific imports (preferred)
import std.algorithm : filter, map, reduce;
import std.range : iota, take;

// Wildcard import (use sparingly)
import std.stdio;

// Import with alias
import my_alias = std.string;

// Private import (not re-exported)
private import std.string;
```

### Package Structure

```
my_package/
├── source/
│   ├── my_package/
│   │   ├── module1.d
│   │   ├── module2.d
│   │   └── subpackage/
│   │       ├── submodule.d
│   │       └── another.d
│   └── other_package/
│       └── other.d
└── dub.json
```

## Classes and Structs

### Struct (Value Type)

```d
struct Point {
    double x, y;

    // Constructor
    this(double x, double y) {
        this.x = x;
        this.y = y;
    }

    // Method
    double distance(Point other) const {
        import std.math : sqrt, pow;
        return sqrt(pow(x - other.x, 2) + pow(y - other.y, 2));
    }

    // Operator overloading
    Point opBinary(string op)(Point other) const if (op == "+") {
        return Point(x + other.x, y + other.y);
    }
}

void main() {
    Point p1 = Point(0, 0);
    Point p2 = Point(3, 4);
    auto dist = p1.distance(p2);  // 5.0
    auto p3 = p1 + p2;            // Uses opAdd
}
```

### Class (Reference Type)

```d
class Animal {
    string name;
    int age;

    this(string name, int age) {
        this.name = name;
        this.age = age;
    }

    string speak() {
        return "...";
    }

    ~this() {
        // Destructor (called by GC)
    }
}

class Dog : Animal {
    this(string name, int age) {
        super(name, age);
    }

    override string speak() {
        return "Woof!";
    }
}

void main() {
    auto dog = new Dog("Rex", 3);
    writeln(dog.speak());  // "Woof!"
}
```

### Class Features

```d
class MyClass {
    // Static members
    static int count = 0;
    static void staticMethod() {
        // Can only access static members
    }

    // Instance members
    int instanceVar;

    void instanceMethod() {
        // Can access both static and instance members
    }

    // Properties (getters/setters)
    private int _value;

    @property int value() const {
        return _value;
    }

    @property void value(int v) {
        _value = v;
    }
}
```

### Copy Constructor

```d
struct Copyable {
    int[] data;

    this(this) {
        // Postblit / copy constructor - called on copy
        data = data.dup;
    }
}
```

## Interfaces

### Basic Interface

```d
import std.stdio;

interface Drawable {
    void draw();
    double area() const;
}

interface Resizable {
    void resize(double factor);
}

class Circle : Drawable, Resizable {
    double radius;

    this(double radius) {
        this.radius = radius;
    }

    void draw() {
        writeln("Drawing circle with radius ", radius);
    }

    double area() const {
        import std.math : PI;
        return PI * radius * radius;
    }

    void resize(double factor) {
        radius *= factor;
    }
}
```

### Interface Implementation

```d
// Multiple interface inheritance
interface A {
    void methodA();
}

interface B : A {
    void methodB();
}

class C : B {
    void methodA() { /* ... */ }
    void methodB() { /* ... */ }
}
```

## Enums and Unions

### Enum

```d
// Basic enum
enum Color { RED, GREEN, BLUE }

// Enum with underlying type
enum Priority : int { LOW = 1, MEDIUM = 2, HIGH = 3 }

// Strongly typed enum (DIP 1018)
enum Status : int {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

// Using enums
void main() {
    Color c = Color.RED;
    switch (c) {
        case Color.RED:
            writeln("Red");
            break;
        case Color.GREEN:
            writeln("Green");
            break;
        default:
            writeln("Other");
            break;
    }
}
```

### Union

```d
union Data {
    int i;
    double d;
    char[8] bytes;
}

void main() {
    Data d;
    d.i = 42;
    // d.d and d.bytes are now undefined
}
```

## Delegates and Function Pointers

### Function Pointers

```d
import std.stdio;

int add(int a, int b) {
    return a + b;
}

void main() {
    // Function pointer type
    int function(int, int) funcPtr;
    funcPtr = &add;
    writeln(funcPtr(2, 3));  // 5
}
```

### Delegates (Closures)

```d
// Delegate type
int delegate(int) del;

// Create delegate with closure
int multiplier = 3;
del = (int x) {
    return x * multiplier;  // Captures multiplier
};
writeln(del(5));  // 15
```

## Operator Overloading

### Binary Operators

```d
struct Vector2 {
    double x, y;

    Vector2 opBinary(string op)(Vector2 other) if (op == "+") {
        return Vector2(x + other.x, y + other.y);
    }

    Vector2 opBinary(string op)(Vector2 other) if (op == "-") {
        return Vector2(x - other.x, y - other.y);
    }

    Vector2 opBinary(string op)(double scalar) if (op == "*") {
        return Vector2(x * scalar, y * scalar);
    }
}
```

### Comparison Operators

```d
struct Point {
    double x, y;

    int opCmp(ref const Point other) const {
        if (x != other.x) return (x < other.x) ? -1 : 1;
        if (y != other.y) return (y < other.y) ? -1 : 1;
        return 0;
    }
}
// Automatically provides <, <=, >, >=, ==, !=
```

### Indexing

```d
struct Container {
    int[10] data;

    ref int opIndex(size_t i) {
        return data[i];
    }

    int opIndex(size_t i) const {
        return data[i];
    }

    void opIndexAssign(int value, size_t i) {
        data[i] = value;
    }
}
```

## Conditional Compilation

### version Statement

```d
// Version identifiers:
// D version
version = MyFeature;  // Define a version identifier
version (Windows) { /* Windows-specific code */ }
version (linux) { /* Linux-specific code */ }
version (OSX) { /* macOS-specific code */ }
version (Posix) { /* POSIX systems */ }

// Compiler versions
version (DMD) { /* DMD compiler */ }
version (LDC) { /* LDC compiler */ }
version (GDC) { /* GDC compiler */ }

// CPU architecture
version (X86) { /* 32-bit x86 */ }
version (X86_64) { /* 64-bit x86 */ }
version (ARM) { /* ARM */ }
version (AArch64) { /* ARM 64-bit */ }

// Logic
version (A) {} else version (B) {} else {}
```

### debug Statement

```d
// Debug block: compiled only with -debug flag
debug {
    writeln("Debugging info");
}

// Named debug
debug (MyModule) {
    writeln("MyModule debug");
}

// Debug with -debug flag
/*
  dmd -debug main.d
*/
```

### static if

```d
// Compile-time conditional
static if (is(T == int)) {
    // Special case for int
} else static if (is(T == double)) {
    // Special case for double
} else {
    // General case
}

// static foreach (DIP 1010): iterate at compile-time
static foreach (i; 0 .. 5) {
    mixin("int x" ~ i.to!string ~ ";");  // Generates int x0; int x1; ... int x4;
}

alias Types = AliasSeq!(int, double, string);
static foreach (T; Types) {
    pragma(msg, T.stringof);  // Prints: int, double, string at compile-time
}
```

## `__traits` - Compile-Time Reflection

### Basic Usage

```d
static assert(__traits(isSame, int, int));             // true
static assert(__traits(compiles, 1 + 2));               // true
static assert(__traits(compiles, (string s) => s.length));  // true
```

### Commonly Used Traits

```d
import std.traits;

// Type inspection
static assert(__traits(hasMember, int, "max"));            // Does int have max?
static assert(__traits(compiles, 1 + 2));                   // Does the expression compile?
static assert(__traits(isSame, int, int));                  // Are int and int the same?
static assert(!__traits(isSame, int, long));                // Are int and long different?
```

### initSymbol Example

```d
// Bind a C symbol at compile-time
extern(C) __gshared int errno;
static int* errno_ptr = &errno;  // Captures at compile-time
```

## `is` Expression - Type Checking

### Forms of `is`

```d
alias T = int;

// Basic form
static if (is(int)) { }                  // Always true
static if (is(int[5])) { }               // true

// Type equality
static if (is(T == int)) { }             // T is exactly int

// Type category
static if (is(T == struct)) { }          // T is a struct
static if (is(T == class)) { }           // T is a class (false for int)

// Type qualifiers
static if (is(T == const)) { }           // T is const-qualified
static if (is(T == immutable)) { }       // T is immutable

// Type conversion
static if (is(T : int)) { }              // T implicitly converts to int
```

### Practical `is` Examples

```d
bool isPointer(T)() { return is(T == U*, U); }
bool isArray(T)() { return is(T == U[], U); }

// Check for specific members
static if (is(typeof(T.init.foo))) { }  // T has member foo
```

## `typeof` and `typeid`

### typeof

```d
// typeof: get the type of an expression
int x = 42;
typeof(x) y = 10;            // y is int
typeof(1 + 2.0) z;           // z is double

// typeof(function): get function type
typeof(&func) fptr;          // Function pointer

// typeof(return): in function bodies
int func() {
    typeof(return) result = 42;  // result is int
    return result;
}
```

### typeid

```d
import std.stdio;
import core.demangle;

class MyClass { }

void main() {
    Object obj = new MyClass();

    // typeid: get TypeInfo
    TypeInfo ti = typeid(int);
    writeln(ti.toString());              // Runtime type name (mangled)
    writeln(demangle(ti.toString()));    // Demangled name: "int"

    // Runtime type checking
    if (typeid(obj) == typeid(MyClass)) { }
}
```

## `alias` and `with`

### alias

```d
// Type alias
alias MyInt = int;
alias StringArray = string[];

// Alias template
alias AddFun(T) = T function(T, T);

// alias this: implicit conversion/subtyping (D's "inheritance for structs")
struct Point {
    private double[2] p;
    alias p this;           // Point behaves like a double[2]

    double dot(Point rhs) {
        return p[0] * rhs.p[0] + p[1] * rhs.p[1];
    }
}
```

### with

```d
import std.stdio;

struct S {
    int x;
    int y;
}

void main() {
    auto s = S(10, 20);

    with (s) {
        x += 1;  // Equivalent to s.x += 1
        y += 1;  // Equivalent to s.y += 1
    }

    // with for members lookup
    with (std.stdio) {
        writeln("Hello");  // No need to qualify
    }
}
```

## Error Handling

### try/catch/finally

```d
import std.stdio;

void main() {
    try {
        auto file = File("data.txt", "r");
        // Risky operation
    }
    catch (Exception e) {
        stderr.writeln("Error: ", e.msg);
    }
    finally {
        // Always executes, even if catch rethrows
        writeln("Cleanup code");
    }
}
```

### Throwable Hierarchy

```d
// Top hierarchy:
// Object
//   └── Throwable
//         ├── Exception (can be caught; safe)
//         └── Error (should not be caught; denotes unrecoverable)
//               └── AssertError

// Custom exception
class MyException : Exception {
    this(string msg, string file = __FILE__, size_t line = __LINE__) {
        super(msg, file, cast(int)line);
    }
}
```

### scope Guards

```d
import std.stdio;

void main() {
    auto file = File("test.txt", "w");
    scope(exit) file.close();           // Always on exit
    scope(failure) writeln("Failed!"); // Only on exception
    scope(success) writeln("Done!");   // Only on success
    file.writeln("Hello");
}
```

### enforce

```d
import std.exception : enforce;

void process(string data) {
    enforce(data.length > 0, "data cannot be empty");
    // Execution only continues if data is not empty
}
```

## Properties

### Built-in Type Properties

```d
// Every type has these properties
int initVal = int.init;      // Initial value: 0
string typeName = int.stringof;  // Type name: "int"
size_t typeSize = int.sizeof;    // Size in bytes: 4
size_t typeAlign = int.alignof;  // Alignment in bytes: 4
string mangled = int.mangleof;   // Mangled name: "i"

// Arrays
int[10] arr;
```

## Pragmas

### pragma(msg): Compile-Time Print

```d
pragma(msg, "Compiling module: ", __MODULE__);
pragma(msg, "Debug mode: ", "On");
// Messages are printed during compilation
```

### pragma(inline): Inline Control

```d
pragma(inline, true)   int func1() { return 1; }  // Force inline
pragma(inline, false)  int func2() { return 2; }  // Prevent inline
/* pragma(inline) */    int func3() { return 3; }  // Compiler decides (default)
```

### Other Pragmas

```d
pragma(lib, "somelib");      // Link with library
pragma(startaddress, main);   // Set entry point
pragma(mangle, "MyFunc");     // Override mangled name
```

## User-Defined Attributes (UDA)

### Defining and Using UDAs

```d
// UDA is just a type used as an attribute
struct Author {
    string name;
}
struct Version {
    int major, minor;
}

@Author("Alice")
@Version(1, 0)
class MyClass { }

// Access UDAs at compile-time
void main() {
    import std.traits : getUDAs;
    auto authors = getUDAs!(MyClass, Author);
    // authors == AliasSeq!(Author("Alice"))
}
```

## `noreturn` - Bottom Type (DIP 1034)

```d
// noreturn: function never returns
noreturn infiniteLoop() {
    while (true) { }
}

noreturn alwaysThrows() {
    throw new Exception("Always throws");
}

// Usage: helps compiler understand unreachable code
int example(bool condition) {
    if (condition) {
        return 0;
    } else {
        alwaysThrows();  // Compiler knows this never returns
    }
}
```

## `final` and `override`

```d
// final: prevent overriding
class Base {
    final void cannotOverride() { }
    void canOverride() { }
}

// override: mark overridden methods (ensures correctness)
class Derived : Base {
    override void canOverride() { }  // OK
    // override void cannotOverride() { }  // Error: final
}

// final class: prevents inheritance
final class SealedClass { }
```

## abstract Class

```d
abstract class Shape {
    abstract void draw();  // No implementation required
    double area() { return 0; }  // Can still have concrete methods
}

class Circle : Shape {
    override void draw() { }
    override double area() { return 3.14; }
}
```

## Better C Mode

Better C mode (`-betterC`) strips the D runtime libdruntime, enabling D as a C replacement for embedded/bare-metal systems.

```d
extern(C) void main() {
    import core.stdc.stdio : printf;
    printf("Hello from Better C\n");
}
```

### Limitations in Better C

```d
// Not available in -betterC:
// - Garbage collection
// - Exceptions (try/catch/throw)
// - TypeInfo and ClassInfo
// - Module constructors/destructors
// - Thread-local storage (__gshared required)
// - Synchronization
// - Static constructors
// - RTTI

// Available in -betterC:
// - All D language basics (structs, arrays, slices, functions)
// - Templates
// - CTFE
// - Mixins
// - core.stdc.* modules
// - C ABI interop
```

## Inline Assembler

### x86/x86_64 Inline Assembler

```d
version (D_InlineAsm_X86) {
    uint checkedMultiply(uint x, uint y) {
        uint result;
        asm {
            mov     EAX, x;
            mul     EAX, y;
            mov     result, EAX;
            jc      overflow;
        }
        return result;
    overflow:
        throw new Exception("overflow");
    }
}

// DMD asm syntax only; LDC uses GCC-style __asm__ instead
version(DigitalMars) {
    void increment(ref int val) {
        asm {
            mov EAX, val;
            add [EAX], 1;
        }
    }
}
```

### Inline Assembler Syntax

```d
/*
asm {
    instruction operands;
    ...
}

Operand syntax:
    Register: EAX, EBX, ECX, EDX, ESI, EDI, EBP, ESP
    Memory: [reg], [reg + offset], [reg + reg * scale]
    Immediate: constant integer
*/
```

## SIMD Vector Extensions

```d
// Using __vector for SIMD operations
void vectorExample() {
    int4 a = [1, 2, 3, 4];       // 4 ints in one vector
    int4 b = [5, 6, 7, 8];

    int4 c = a + b;               // Element-wise add
    int4 d = a * b;               // Element-wise multiply

    // Access elements
    int first = a[0];
    a[0] = 10;
}

// Using core.simd (if available)
import core.simd;
```

## Interfacing to C

### extern(C) Declarations

```d
// Call C functions directly
extern(C) {
    int printf(const char* format, ...);
    void* malloc(size_t size);
    void free(void* ptr);
}

void main() {
    printf("Hello %s\n".ptr, "World".ptr);
}
```

### C struct Compatibility

```d
extern(C) struct Point {
    int x;
    int y;
}

// Match C struct alignment (packed)
align(1) struct Packed {
    byte a;
    int b;
}
```

### Import C Headers (ImportC)

```d
// DMD can compile C source directly
// import "file.c"
/*
  dmd main.d file.c
*/

// ImportC: include C headers
// __import someheader.h;
```

## Interfacing to C++

### extern(C++) Declarations

```d
// Link with C++ code
extern(C++) {
    class MyCppClass {
        this();
        void method();
    }
}
```

### C++ Name Mangling

```d
// C++ function linkage (requires LDC with C++ interop support)
extern(C++) void cppFunc();
```

## Interfacing to Objective-C

```d
// Objective-C interop
/*
extern(Objective-C) interface NSObject {
    NSString* description();
}
*/
```

## Lvalues vs Rvalues

```d
void main() {
    int x = 10;            // x is an lvalue
    x = 20;                // OK: lvalue can be assigned to
    // 10 = 20;            // Error: 10 is an rvalue

    int* p = &x;           // OK: x is lvalue, can take address
    // int* p2 = &10;      // Error: 10 is rvalue, cannot take address

    int y;
    int* q = &(x = y);     // Assignment is lvalue in D
}
```

## `__gshared` - Global Shared Data

```d
// Default: global variables are thread-local (TLS)
int tlsCounter = 0;       // Each thread has its own copy

// __gshared: true global (shared across threads)
__gshared int globalCounter = 0;  // Single memory location

// Use __gshared when you need:
// - Static initialization in -betterC mode
// - C-compatible globals
// - Performance-critical shared data (with manual synchronization)
```

## Parameter Type Reflection

```d
import std.traits : ParameterTypeTuple;

void example(int a, double b) { }

alias Params = ParameterTypeTuple!example;  // (int, double)
```

## Forcing Rvalue Treatment

```d
void func(ref int x) { }
void func(int x) { }

void main() {
    int a = 10;
    func(a);            // Calls func(ref int)
    func(cast(int) a);  // Forces rvalue, calls func(int)
}
```

## `import` Expressions

```d
// import expression: compile-time import of file contents as string
// (requires -J flag to specify import path)
// enum config = import("config.txt");

// For demonstration, a string literal serves the same purpose
enum config = "file contents";
```

## `mixin` Expressions

```d
// Compile time string evaluation of D code
enum code = "int x = 42;";
mixin(code);  // Equivalent to: int x = 42;
writeln(x);   // 42

// Template mixin (reusable code) — used inside a struct
mixin template Equality() {
    bool opEquals(ref const typeof(this) other) const {
        return this.tupleof == other.tupleof;
    }
}

struct MyStruct {
    int a;
    double b;
    mixin Equality;  // Injects opEquals
}
```

## `assert` and Contract Expressions (DIP 1009)

```d
// Traditional assert
int x = 5;
assert(x > 0);
assert(x > 0, "x must be positive");

// Expression-based contracts (DIP 1009)
// The out result variable is introduced with `out (name; condition)` — note the
// semicolon. `out (name => condition)` is a syntax error.
int divide(int a, int b) in (b != 0) out (result; a % b != 0 || result * b == a) {
    return a / b;
}
```

## Tuple Usage

```d
import std.typecons : tuple;
import std.stdio;

// Create and access tuples
auto t = tuple(42, "hello", 3.14);
writeln(t[0]);  // 42
writeln(t[1]);  // "hello"

// Tuple in foreach using .expand
foreach (tup; [tuple("a", 1), tuple("b", 2)]) {
    writeln(tup[0], ": ", tup[1]);
}
```

## Formatted Output

```d
import std.stdio;

void main() {
    int x = 10;
    // Formatted output
    writefln("Value: %d", x);          // "Value: 10"
    writefln("Hex: %x", x);             // "Hex: a"
    writefln("Float: %.2f", 3.14);      // "Float: 3.14"
}
```

## Bitfields (DIP 1051)

```d
import std.stdio;
import std.bitmanip;

// Compile-time bitfield generation
struct Flags {
    mixin(bitfields!(
        uint, "readOnly", 1,      // 1 bit
        uint, "hidden", 1,        // 1 bit
        uint, "type", 2,          // 2 bits
        uint, "unused", 4,        // 4 bits
    ));
}

void main() {
    auto f = Flags();
    f.readOnly = 1;
    writeln(f.readOnly);  // 1
}
```

## `static` Constructors/Destructors

```d
// Module-level constructors (run at program start)
static this() {
    writeln("Module initializing");
}

// Module-level destructors (run at program end)
static ~this() {
    writeln("Module finalizing");
}

// Order depends on module dependencies
```

## Attributes

```d
// @safe: memory-safe code
int safeFunction() @safe {
    return 42;
}

// @system: unsafe code (requires explicit opt-in)
int systemFunction() @system {
    // Can do pointer arithmetic, casts, etc.
    return 42;
}

// @trusted: manually verified safe code
int trustedFunction() @trusted {
    // Compiler trusts this is safe
    return 42;
}
```

### Other Attributes

```d
// @property: marks getter/setter
struct Widget {
    private int _value;
    @property int value() const { return _value; }
    @property void value(int v) { _value = v; }
}

// @disable: disable a function or constructor
class MyClass {
    @disable this();  // Cannot default construct
    this(int x) { }   // Must provide x
}

// @nogc: no garbage collection
int noGCFunction() @nogc {
    return 42;
}

// pure: no side effects
int pureFunction(int x) pure {
    return x * 2;
}

// nothrow: never throws
int safeFunction() nothrow {
    return 42;
}
```

## Quick Reference

### Type Quick Reference

```d
// Integer types: byte, ubyte, short, ushort, int, uint, long, ulong
// Floating point: float, double, real
// Character types: char, wchar, dchar
// String types: string, wstring, dstring (immutable by default)
// Special: void, null
// Bottom type: noreturn
```

### Function Attribute Quick Reference

```d
// pure     - No side effects
// nothrow  - No exceptions
// @safe    - Memory safe
// @nogc    - No GC allocations
// @system  - Unsafe code allowed
// @trusted - Manually verified safe
// @property - Getter/setter
// @disable - Disabled
// @live    - Ownership/borrowing opt-in
```

### Control Flow Quick Reference

```d
void main() {
    int val;
    if (val > 0) { } else { }
    switch (val) { case 0: break; default: break; }
    while (val < 10) { val++; }
    do { val--; } while (val > 0);
    for (int i = 0; i < 10; i++) { }
    foreach (elem; [1, 2, 3]) { }
    foreach (i, elem; [1, 2, 3]) { }
    foreach_reverse (elem; [1, 2, 3]) { }
}
```

### Array Operations Quick Reference

```d
import std.stdio;

void main() {
    int[] arr = [1, 2, 3];
    size_t len = arr.length;  // Length
    auto concat = arr ~ [4, 5];  // Concatenation
    arr ~= 6;                // Append
    auto slice = arr[0 .. 2];  // Slice
    writeln(len, concat, slice);
}
```

### Special Types Quick Reference

```d
// void   - No type (function return)
// noreturn - Never returns (DIP 1034)
// null   - Null pointer/value
```

### Compile-Time Quick Reference

```d
// Static if, version, debug — all must be inside a function or at module scope
// Traits and is expressions need types/values to operate on

// Examples with concrete types:
static assert(__traits(compiles, 1 + 2));
static assert(__traits(isSame, int, int));
static assert(__traits(hasMember, int, "max"));

alias T = int;
static assert(is(T));
static assert(is(T == int));
```

## Common Idioms

### Empty Check

```d
void check(int[] arr) {
    if (arr.length == 0) { }  // Preferred
    if (arr.empty) { }        // Also valid (range style)
}
```

### Swap

```d
import std.algorithm.mutation : swap;

void main() {
    int a = 1, b = 2;
    swap(a, b);
}
```

### Range Iteration

```
foreach (i; 0 .. arr.length) { }           // Index
foreach (elem; arr) { }                     // Element
foreach (i, elem; arr) { }                  // Index + element
foreach (ref elem; arr) { }                 // Mutable element
```

### Function Chaining

```d
import std.algorithm : map, filter, reduce;
import std.range : iota;

auto result = iota(1, 101)
    .filter!(a => a % 2 == 0)
    .map!(a => a * a)
    .reduce!((a, b) => a + b);
```

## References

- [D Language Specification](https://dlang.org/spec/spec.html)
- [D Style Guide](https://dlang.org/dstyle.html)
- [D Tour](https://tour.dlang.org)
- [Phobos Documentation](https://dlang.org/phobos/)
