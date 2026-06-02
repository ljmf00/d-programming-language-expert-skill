---
name: d-lang-best-practices
description: >-
  D evolution and best practices: DIPs (scope, noreturn, @mustuse, => methods,
  bitfields, editions), code organization patterns, error handling strategies,
  testing frameworks, logging, deprecation management, idiom and style guides.
  Use when following D conventions or understanding language evolution.
license: MIT
metadata:
  topics: dips best-practices idioms testing style-guide
  order: 08
---

# D Programming Language - Evolution & Best Practices

Comprehensive guide to D's evolution (DIPs - D Improvement Proposals), idiomatic patterns, style guide, and community best practices.

## Table of Contents
- [DIP Process Overview](#dip-process-overview)
- [Key Accepted DIPs](#key-accepted-dips)
- [DIP 1013: Deprecation Process](#dip-1013-deprecation-process)
- [DIP 1029: throw as Function Attribute](#dip-1029-throw-as-function-attribute)
- [DIP 1034: noreturn Bottom Type](#dip-1034-noreturn-bottom-type)
- [DIP 1038: @mustuse](#dip-1038-mustuse)
- [DIP 1043: Shortened Method Syntax](#dip-1043-shortened-method-syntax)
- [DIP 1051: Bitfields](#dip-1051-bitfields)
- [DIP 1052: Editions](#dip-1052-editions)
- [DIPs in Review](#dips-in-review)
- [DStyle: Idiomatic D](#dstyle-idiomatic-d)
- [Common Idioms](#common-idioms)
- [Advanced Patterns](#advanced-patterns)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Testing Strategies](#testing-strategies)
- [Error Handling Strategies](#error-handling-strategies)
- [Learning Pathways](#learning-pathways)
- [Migration Guide](#migration-guide)
- [Community Resources](#community-resources)
- [Quick Reference](#quick-reference)

## DIP Process Overview

### What is a DIP?
A DIP (D Improvement Proposal) is a design document that proposes new features or changes to the D programming language. The DIP process ensures that significant changes to the language are properly reviewed and documented.

### DIP Lifecycle
1. **Draft** - Initial proposal
2. **Review** - Community and committee review
3. **Accepted/Rejected** - Decision by the language maintainers
4. **Implemented** - Code changes in DMD/LDC
5. **Stabilized** - Feature is enabled by default

### DIP Categories
```d
// DIP types
enum DipType {
    LanguageChange,      // Core language features
    LibraryChange,       // Phobos/standard library
    ProcessChange,       // DIP process improvements
    SpecificationChange  // Specification updates
}
```

## DIP 1013: Deprecation Process

Established the formal process for deprecating features in D:

```d
// Mark a symbol as deprecated
deprecated("Use newFunc instead")
void oldFunc() { }

// Compile with deprecation warnings
// dmd -de main.d
// dmd -dw main.d  (warnings as errors for deprecated)
```

## DIP 1029: throw as Function Attribute

```d
// Use nothrow attribute for functions that don't throw
void canThrow() { }

// Function type with nothrow
alias SafeFunc = void function() nothrow;
```

## DIP 1034: noreturn Bottom Type

```d
// noreturn: a function that never returns
noreturn fatalError(string msg) {
    stderr.writeln("FATAL: ", msg);
    assert(0);
}

// Compiler knows this function never returns
int safeDivide(int a, int b) {
    if (b == 0) {
        fatalError("Division by zero");  // noreturn
    }
    return a / b;  // No need for return after noreturn call
}
```

## DIP 1038: @mustuse

```d
import core.attribute : mustuse;

// @mustuse applies to struct/union return types (not to functions)
@mustuse struct ImportantResult {
    int value;
}

ImportantResult compute() {
    return ImportantResult(42);
}

void main() {
    auto val = compute();  // OK: used
    // compute();  // Error: return value of type @mustuse is discarded
}
```

## DIP 1043: Shortened Method Syntax

```d
// Already covered in Core Language skill
// Key pattern: use for simple getters, single expressions
int add(int a, int b) pure => a + b;
int getVal() const @safe => 42;
T max(T)(T a, T b) => a > b ? a : b;
```

## DIP 1051: Bitfields

```d
import std.bitmanip;

// Bitfield generation
struct PacketFlags {
    mixin(bitfields!(
        uint, "ver",    4,     // 4 bits
        uint, "type",   2,     // 2 bits
        uint, "rsvd",   2,     // 2 bits
    ));
    
    // Generates: ver, type, rsvd properties
    // with proper bit-level get/set
}

void main() {
    import std.stdio;
    auto flags = PacketFlags();
    flags.ver = 2;
    writeln(flags.ver);  // 2
}
```

## DIP 1052: Editions

```d
// Editions allow language evolution with backward compatibility
version (D_Std_D2019) {
    // Use newer language features
}

// Set edition in dub.json
/*
{
    "editions": ["2024"]
}
*/
```

## DIPs in Review

| DIP | Title | Status | Description |
|-----|-------|--------|-------------|
| [1000](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1000.md) | Scoped Pointers | Accepted | `scope` annotations for pointers |
| [1018](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1018.md) | Enum Types as Manifest Constants | Accepted | Strongly typed enums |
| [1030](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1030.md) | Named Arguments | Accepted | Named function arguments |
| [1035](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1035.md) | Hash Code | Accepted | `hashOf` for types |
| [1043](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1043.md) | Shortened Method Syntax | Accepted | `=>` syntax for functions |
| [1048](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1048.md) | Bitfields | Accepted | Bitfield support in language |
| [1052](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1052.md) | Editions | Accepted | Language versioning |
| [1053](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1053.md) | Variadic Arguments Improvements | Accepted | Better variadic support |

## Key Accepted DIPs

### DIP 1030: Named Arguments
```d
// Struct for named arguments
void configure(int port, string host, bool ssl) { }
configure(8080, "localhost", true);  // Must match order

// Using a struct for named-like arguments
struct Config {
    int port = 8080;
    string host = "localhost";
    bool ssl = false;
}
void configure(Config cfg) { }
configure(Config(host: "localhost", port: 8080, ssl: true));
```

### DIP 1043: Shortened Method Syntax
```d
// Traditional function definition
int add(int a, int b) {
    return a + b;
}

// Shortened method syntax (DIP 1043)
int add2(int a, int b) pure => a + b;

// Works with all attributes
int doubleVal(int x) pure nothrow @safe @nogc => x * 2;

// Works with templates
T max(T)(T a, T b) => a > b ? a : b;
```

### DIP 1018: Enum Types as Manifest Constants
```d
// Traditional enum (weakly typed)
enum Color { RED, GREEN, BLUE }

// Strongly typed enum using struct
struct Status {
    private int value;
    enum : int { OK = 0, ERROR = 1, PENDING = 2 }
}
```

### DIP 1052: Editions
```d
// Current edition version
version(D_Std_D2019) {
    // Use 2019 edition features
}
```

### DIP 1053: Variadic Arguments Improvements
```d
// Before
void process(T...)(T args) {
    static foreach (i; 0 .. T.length) {
        // Process each argument
    }
}

// After (improved variadic)
void process(T...)(T args) {
    foreach (i; 0 .. args.length) {
        // Improved reflection
    }
}
```

## Advanced Patterns

### opApply: Custom Foreach Iteration
```d
struct MyRange {
    int[] data;
    
    int opApply(scope int delegate(ref int element) dg) {
        int result;
        foreach (ref elem; data) {
            result = dg(elem);
            if (result) break;
        }
        return result;
    }
    
    int opApply(scope int delegate(size_t i, ref int element) dg) {
        int result;
        foreach (i, ref elem; data) {
            result = dg(i, elem);
            if (result) break;
        }
        return result;
    }
}

void main() {
    auto mr = MyRange([1, 2, 3, 4, 5]);
    foreach (ref e; mr) { e *= 2; }
    foreach (i, e; mr) { writeln(i, ": ", e); }
}
```

### ref return scope (DIP 1000)
```d
int* findMax(scope int[] arr) return scope {
    size_t maxIdx = 0;
    foreach (i, e; arr) {
        if (e > arr[maxIdx]) maxIdx = i;
    }
    return &arr[maxIdx];
}
```

### Alias This for Subtype Emulation
```d
struct Inches {
    private double _value;
    alias _value this;
}

struct Meters {
    private double _value;
    alias _value this;
}
```

### Compile-Time State Machine
```d
enum State { Idle, Running, Paused, Stopped }
string dispatch(State s) {
    final switch (s) {
        case State.Idle: return "Start";
        case State.Running: return "Pause";
        case State.Paused: return "Resume";
        case State.Stopped: return "Reset";
    }
}
enum commands = [State.Idle, State.Running, State.Paused, State.Stopped]
    .map!(s => dispatch(s)).array;
```

## Testing Strategies

### Built-in Unit Tests
```d
import std.algorithm : map;
import std.range : iota;

int squareSum(int n) {
    return iota(1, n + 1)
        .map!(a => a * a)
        .reduce!((a, b) => a + b);
}

unittest {
    assert(squareSum(3) == 14);
    assert(squareSum(0) == 0);
    assert(squareSum(1) == 1);
}
```

### Integration with unit-threaded
```d
// Unit tests use assert for verification
int square(int n) { return n * n; }
version (unittest) {
    assert(square(3) == 9);
}
```

## Error Handling Strategies

### Return vs Exception
```d
import std.typecons : Nullable;

auto result = to!int("42");
writeln(result);

Nullable!int findUser(string name) {
    return Nullable!int(42);
}
```

### Scope Guards for Transaction Safety
```d
import std.stdio;

struct Account {
    double balance;
    void withdraw(double amount) { balance -= amount; }
    void deposit(double amount) { balance += amount; }
}

void transfer(Account from, Account to, double amount)
in { assert(amount > 0); assert(from.balance >= amount); }
out { assert(from.balance >= 0); }
do {
    from.withdraw(amount);
    scope(failure) from.deposit(amount);
    to.deposit(amount);
    scope(success) writeln("Transfer complete");
}
```

## Learning Pathways

### Beginner Path
1. D Tour (https://tour.dlang.org) - Interactive introduction
2. Programming in D (https://ddili.org/ders/d.en/) - Free comprehensive book
3. Core Language skill - Fundamentals

### Intermediate Path
1. Phobos Modules skill - Standard library mastery
2. Ranges & Algorithms skill - Data processing
3. DUB skill - Project management
4. Experiment: Build a CLI tool, parse files, process data

### Advanced Path
1. Templates & Metaprogramming skill - Generic code
2. Concurrency skill - Multi-threaded applications
3. DIPs skill - Language evolution
4. Memory Management skill - Safe and efficient memory use
5. Experiment: Write a library, web server, or game

## DIPs in Review

### Current Proposals
The following DIPs are in review or discussion:

| DIP | Title | Description |
|-----|-------|-------------|
| [1049](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1049.md) | Iterator Support | Range-compatible iterators |
| [1054](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1054.md) | Scope Improvements | Enhanced scope guarantees |

### Recent Discussions
Key topics in the community:
- Better error messages for templates
- Improved type deduction
- Enhanced metaprogramming capabilities
- Improved garbage collection performance
- Better C++ interop

## DStyle: Idiomatic D

### Naming Conventions

**Modules:**
```d
// Package: lowercase with underscores
package my_package.sub_module

// Module file name matches module name
// my_package/sub_module.d
module my_package.sub_module;
```

**Types (PascalCase):**
```d
class MyClass { }
struct MyStruct { }
enum Color { RED, GREEN, BLUE }
interface Drawable { }
alias MyAlias = int;
```

**Functions (camelCase):**
```d
void processData() { }
int getValue() { return 42; }
void setValue(int v) { }
```

**Variables (camelCase):**
```d
int myVariable = 0;
string userName = "";
auto config = 42;
```

**Constants and Enums (UPPER_SNAKE_CASE):**
```d
enum Constants {
    MAX_USERS = 100,
    MIN_VALUE = 0
}

const int TIMEOUT_SECONDS = 30;
```

### Private Members
```d
class MyClass {
private:
    int _privateField;  // Leading underscore for private
    void _privateMethod() { }
}
```

### Formatting

**Braces:**
```d
// Allman style (preferred)
void myFunc() {
    // code
}

// K&R style (acceptable with consistency)
void myFunc2() {
    // code
}
```

**Indentation:**
```d
// 4 spaces per indentation level
void example() {
    int x = 42;
    if (x > 0) {
        writeln("Positive");
    }
}
```

### Comments
```d
// Line comment (preferred for simple explanations)

/* Block comment (for documentation or longer explanations) */

/// Documentation comment (for DDoc)
/** DDoc documentation comment */
```

### Import Style
```d
// Preferred: specific imports
import std.algorithm : filter, map, reduce;
import std.range : iota, take;

// For module-level imports, use qualified names
import std.stdio : writeln, writefln;

// Avoid wildcard imports
import std;  // Only in small scripts or REPL
```

## Common Idioms

### Function Chaining with UFCS
```d
// Use UFCS (Uniform Function Call Syntax) for method chaining
import std.algorithm : filter, map, reduce;
import std.range : iota;

auto result = iota(1, 101)
    .filter!(a => a % 2 == 0)
    .map!(a => a * a)
    .reduce!((a, b) => a + b);
```

### RAII Resource Management
```d
import std.stdio;

// Always use RAII for resource management
void processFile() {
    auto file = File("test.txt", "r");  // Automatically closed
    foreach (line; file.byLine()) {
        writeln(line);
    }
}

// Use scope for cleanup
void allocateResource() {
    auto resource = 42;
    scope(exit) writeln("Cleanup: ", resource);
    writeln("Using resource: ", resource);
}
```

### Immutable Data Sharing
```d
// Prefer immutable for thread-safe data
immutable int[] data = [1, 2, 3, 4, 5];

// Use const for parameters that shouldn't modify
void process(const int[] data) {
    // Cannot modify data
}
```

### Template Constraints
```d
// Prefer template constraints over compile-time errors
auto process(T)(T value) if (isNumeric!T) {
    return value * 2;
}

// Use static interfaces for generic code
auto sort(T)(T[] arr) if (isRandomAccessRange!T) {
    // Sort implementation
}
```

### Error Handling with enforce
```d
import std.exception : enforce;

void process(string data) {
    enforce(data.length > 0, "Data must not be empty");
    // Process data
}
```

### Unit Testing
```d
// Unit tests should accompany all functions
/// Adds two numbers
int add(int a, int b) => a + b;

unittest {
    assert(add(2, 3) == 5);
    assert(add(0, 0) == 0);
    assert(add(-1, 1) == 0);
}
```

### Contract Programming
```d
struct BankAccount {
    double balance;
}

void depositMoney(BankAccount account) {
    account.balance += 100.0;
}
```

### Lazy Evaluation
```d
// Use lazy for expensive computations that may not be needed
void logMessage(lazy string msg) {
    debug {
        writeln(msg);  // Only evaluated if needed
    }
}
```

### Property Functions
```d
// Use @property for getters/setters
class MyClass {
private:
    int _value;

    @property int value() const { return _value; }
    @property void value(int v) { _value = v; }
}
```

## Anti-Patterns to Avoid

### Avoid Wildcard Imports in Production
```d
// Bad
import std;

// Good
import std.stdio : writeln, writefln;
```

### Avoid Raw Pointer Manipulation in @safe Code
```d
// Bad
int* ptr;
*ptr = 42;

// Good
int x = 42;
ref int rx = x;
```

### Avoid Unnecessary Casts
```d
// Bad
auto x = cast(int)3.14;

// Good
import std.conv : to;
auto y = to!int(3.14);
```

### Avoid Global Mutable State
```d
// Bad
__gshared int g_counter = 0;

// Good
shared int s_counter = 0;
// Or use thread-local
int t_counter = 0;
```

### Avoid Memory Leaks with GC
```d
import core.stdc.stdlib;

// Bad (in @system code)
auto leakBuf = malloc(1024);
// Missing: free(leakBuf)

// Good
auto safeBuf = malloc(1024);
scope(exit) free(safeBuf);
```

### Avoid Deeply Nested Templates
```d
import std.algorithm;
import std.range;

auto data = iota(0, 10);

// Bad: deeply chained calls
auto chained = data
    .map!(a => a + 1)
    .filter!(a => a > 3)
    .map!(a => a * 2);

// Good: break into steps
auto step1 = data.map!(a => a + 1);
auto step2 = step1.filter!(a => a > 3);
auto finalResult = step2.map!(a => a * 2);
```

## Migration Guide

### From C to D
```c
// C code
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(3, 4);
    printf("%d\n", result);
    return 0;
}
```

```d
// Equivalent D code
int add(int a, int b) {
    return a + b;
}

void main() {
    auto result = add(3, 4);
    import std.stdio : writeln;
    writeln(result);
}
```

### From C++ to D
```cpp
// C++ code
class Animal {
private:
    std::string name;
    int age;

public:
    Animal(const std::string& name, int age)
        : name(name), age(age) {}

    virtual void speak() const {
        std::cout << name << " says nothing." << std::endl;
    }

    virtual ~Animal() = default;
};
```

```d
// Equivalent D code
class Animal {
    string name;
    int age;

    this(string name, int age) {
        this.name = name;
        this.age = age;
    }

    void speak() const {
        import std.stdio : writeln;
        writeln(name, " says nothing.");
    }
}
```

### From Java to D
```java
// Java code
public interface Drawable {
    void draw();
    double area();
}

public class Circle implements Drawable {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public void draw() {
        System.out.println("Drawing circle");
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}
```

```d
// Equivalent D code
interface Drawable {
    void draw();
    double area() const;
}

class Circle : Drawable {
    double radius;

    this(double radius) {
        this.radius = radius;
    }

    void draw() {
        import std.stdio : writeln;
        writeln("Drawing circle");
    }

    double area() const {
        import std.math : PI;
        return PI * radius * radius;
    }
}
```

### Common Migration Patterns

**Arrays:**
```d
// C-style: int* arr; size_t len;
// D-style:
int[] arr = [1, 2, 3, 4, 5];
auto len = arr.length;  // 5
auto first = arr[0];      // 1 (bounds checked)
```

**Strings:**
```d
// C-style: char* str;
// D-style:
string s = "Hello";
auto len = s.length;  // 5
auto first = s[0];      // 'H' (UTF-8)
```

**Memory Management:**
```d
import std.typecons : scoped;

// C-style: malloc/free
// D-style:
class MyClass { }
auto obj = new MyClass();  // GC managed
// Or with scoped:
auto scopedObj = scoped!MyClass();  // Stack allocated
```

## Community Resources

### Official Resources
- **Website**: https://dlang.org
- **Documentation**: https://dlang.org/phobos/
- **Specification**: https://dlang.org/spec/spec.html
- **Forum**: https://forum.dlang.org
- **Blog**: https://dlang.org/blog
- **Wiki**: https://wiki.dlang.org
- **GitHub**: https://github.com/dlang

### Community Resources
- **D Language Foundation**: https://dlang.org/foundation/
- **DUB Package Registry**: https://code.dlang.org
- **D Tour (Interactive)**: https://tour.dlang.org
- **DConf**: https://dconf.org

### Learning Resources
- **Programming in D** (Ali Çehreli): https://ddili.org/ders/d.en/
- **D Idioms**: https://p0nce.github.io/d-idioms/
- **Pragmatic D Tutorial**: https://qznc.github.io/d-tut/
- **D Templates Tutorial**: https://github.com/PhilippeSigaud/D-templates-tutorial

### News and Updates
- **D Blog**: https://dlang.org/blog
- **D Language News**: https://forum.dlang.org/group/digitalmars.D.announce
- **Reddit r/d_language**: https://reddit.com/r/d_language
- **Twitter @D_Programming**: https://twitter.com/D_Programming

### Package Ecosystem
- **Web Frameworks**: vibe.d, diamond, hunt-framework
- **Data Formats**: json, yaml, xml, msgpack
- **Database**: mysql-libd, poa, ddb
- **Network**: vibe-core, async, eventcore
- **Multimedia**: SDL2, SFML, OpenGL
- **Testing**: unit-threaded, dunit
- **Serialization**: dtl, serde-d
- **Logging**: hunt-log, dlog, logrotate

## Quick Reference

### Best Practices Checklist
```d
// ✅ Do:
import std.stdio : writeln;

// ✅ Do:
int add(int a, int b) pure nothrow @safe => a + b;

// ✅ Do:
void main() {
    auto result = add(3, 4);
    scope(exit) writeln("Done");
}

// ❌ Don't:
import std.stdio;

// ❌ Don't:
int add2(int a, int b) { return a + b; }  // No attributes
```

### Key DIPs Summary
```d
DIP 1000: Scoped Pointers       // scope return ref
DIP 1009: Expression Contracts  // in (a > 0) out (result => ...)
DIP 1010: Static foreach        // static foreach (i; 0 .. 5) { }
DIP 1013: Deprecation Process   // deprecated("use new", "2.100")
DIP 1014: Move Semantics        // Move constructor
DIP 1018: Copy Constructor      // this(ref return scope const ...)
DIP 1024: Shared Atomics        // atomicOp!"+="(sharedVar, 1)
DIP 1029: throw Attribute       // throw as function attribute
DIP 1030: Named Arguments       // configure(port: 8080)
DIP 1034: noreturn Type         // noreturn neverReturns()
DIP 1035: @system Variables     // @system int* ptr;
DIP 1038: @mustuse              // @mustuse struct Result { int value; }
DIP 1043: Shortened Methods     // int add(int a, int b) => a + b
DIP 1046: ref for Variables     // ref int r = someLvalue;
DIP 1051: Bitfields             // mixin(bitfields!(...))
DIP 1052: Editions              // Language versioning: (edition >= 2024)
DIP 1053: Tuple Unpacking       // auto (a, b, c) = tuple;
```

### Migration Equivalents
```d
// C to D
malloc/free  →  GC or scoped
printf       →  writeln
int* arr     →  int[] arr
char*        →  string
```

```d
// C++ to D
std::vector  →  int[]
std::string  →  string
std::map     →  int[string]
virtual      →  override (default)
```

```d
// Java to D
new Object()  →  new Object()
System.out    →  stdout
try/finally   →  scope(exit)
void foo()    →  void foo() const
```

### Idiomatic D Patterns
```d
import std.algorithm;
import std.range;

// Range pipeline
auto data = iota(1, 10);
auto result = data.filter!(a => a % 2 == 0).map!(a => a * a);

// Immutable sharing
immutable sharedData = [1, 2, 3, 4, 5];

// Template constraint
auto process(T)(T value) if (isNumeric!T) { return value * 2; }

// Compile-time computation
enum factorial10 = 3628800;
```

## References
- [DIP Repository](https://github.com/dlang/DIPs)
- [Accepted DIPs](https://github.com/dlang/DIPs/tree/master/DIPs/accepted)
- [DIP Process](https://github.com/dlang/DIPs/blob/master/docs/process-authoring.md)
- [DStyle Guide](https://dlang.org/dstyle.html)
- [D Blog: The GC Series](https://dlang.org/blog/the-gc-series)
- [D Community Hub](https://dlang.org/blog)
- [DConf Presentations](https://dconf.org)
- [Programming in D (Book)](https://ddili.org/ders/d.en/)
- [D Idioms](https://p0nce.github.io/d-idioms/)
