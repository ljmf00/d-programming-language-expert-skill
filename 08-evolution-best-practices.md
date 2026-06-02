---
name: d-lang-best-practices
description: >-
  D evolution and best practices: accepted DIPs with -preview= status,
  advanced idioms (opApply, alias this, scope guards), anti-patterns,
  and error handling strategies. Use when following D conventions or
  understanding which language features are default vs preview.
license: MIT
metadata:
  topics: dips best-practices idioms anti-patterns error-handling
  order: 08
---

# D Programming Language - Evolution & Best Practices

## Table of Contents
- [Accepted DIPs Reference](#accepted-dips-reference)
- [DIP 1013: Deprecation Process](#dip-1013-deprecation-process)
- [DIP 1029: throw as Function Attribute](#dip-1029-throw-as-function-attribute)
- [DIP 1034: noreturn Bottom Type](#dip-1034-noreturn-bottom-type)
- [DIP 1038: @mustuse](#dip-1038-mustuse)
- [DIP 1043: Shortened Method Syntax](#dip-1043-shortened-method-syntax)
- [DIP 1048: Language Bitfields](#dip-1048-language-bitfields)
- [DIP 1030: Named Arguments](#dip-1030-named-arguments)
- [Advanced Patterns](#advanced-patterns)
- [Common Idioms](#common-idioms)
- [Anti-Patterns](#anti-patterns-to-avoid)
- [Error Handling Strategies](#error-handling-strategies)
- [Quick Reference](#quick-reference)

## Accepted DIPs Reference

Key DIPs and their current default/preview status. "Default" means enabled in
current stable DMD and LDC. "Preview" requires an explicit flag.

| DIP | Title | Status | Compiler Flag |
|-----|-------|--------|---------------|
| [1000](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1000.md) | Scoped Pointers | Preview | `-preview=dip1000` |
| [1014](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1014.md) | Move Semantics | Default | — |
| [1018](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1018.md) | Copy Constructor | Default | — |
| [1029](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1029.md) | throw as Function Attribute | Default | — |
| [1030](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1030.md) | Named Arguments | Default | — |
| [1034](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1034.md) | noreturn Bottom Type | Default | — |
| [1035](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1035.md) | @system Variables | Preview | `-preview=systemVariables` |
| [1038](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1038.md) | @mustuse | Default | — |
| [1043](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1043.md) | Shortened Method Syntax | Default | — |
| [1048](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1048.md) | Language Bitfields | Default (DMD 2.108+/LDC 1.36+) | — |
| [1052](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1052.md) | Editions | In progress | — |
| [1053](https://github.com/dlang/DIPs/blob/master/DIPs/accepted/DIP1053.md) | Tuple Unpacking | In progress | — |

## DIP 1013: Deprecation Process

```d
// Mark a symbol as deprecated
deprecated("Use newFunc instead")
void oldFunc() { }

// Compile with deprecation warnings treated as errors
// dmd -de main.d
// dmd -dw main.d  (warnings only)
```

## DIP 1029: throw as Function Attribute

DIP 1029 made `throw` an explicit function attribute (symmetric with `nothrow`).
In practice: annotate functions that do not throw with `nothrow`; leave others
unannotated. Exception specifications are not enforced at call sites.

```d
void canThrow() { throw new Exception("oops"); }
void cannotThrow() nothrow { }

alias SafeCallback = void function() nothrow;
```

## DIP 1034: noreturn Bottom Type

```d
import std.stdio : stderr;

noreturn fatalError(string msg) {
    stderr.writeln("FATAL: ", msg);
    assert(0);
}

int safeDivide(int a, int b) {
    if (b == 0)
        fatalError("Division by zero");  // noreturn — compiler knows this exits
    return a / b;
}
```

## DIP 1038: @mustuse

`@mustuse` applies to struct/union types (not to functions). Any discarded
return value of that type is a compile error.

```d
import core.attribute : mustuse;

@mustuse struct ImportantResult {
    int value;
}

ImportantResult compute() {
    return ImportantResult(42);
}

void main() {
    auto val = compute();  // OK: result is used
    // compute();          // Error: @mustuse return value discarded
}
```

## DIP 1043: Shortened Method Syntax

```d
// Single-expression functions and methods using =>
int add(int a, int b) pure nothrow @safe @nogc => a + b;
int getVal() const @safe => 42;

// Works with templates
T maxOf(T)(T a, T b) => a > b ? a : b;
```

## DIP 1048: Language Bitfields

Language-level bitfields (DMD 2.108+). Distinct from `std.bitmanip.bitfields`
which is a library mixin predating this DIP.

```d
struct PacketHeader {
    uint ver:4;    // 4-bit field
    uint type:2;   // 2-bit field
    uint rsvd:2;   // 2-bit padding
}

void main() {
    import std.stdio : writeln;
    PacketHeader h;
    h.ver = 3;
    writeln(h.ver);  // 3
}
```

## DIP 1030: Named Arguments

```d
void configure(int port, string host, bool ssl) { }

// Named arguments — can reorder, skip optional args
configure(host: "localhost", port: 8080, ssl: false);

// Also works with struct literals
struct Config { int port = 8080; string host = "localhost"; bool ssl; }
void setup(Config cfg) { }
setup(Config(host: "example.com", ssl: true));
```

## Advanced Patterns

### opApply: Custom foreach Iteration

```d
import std.stdio : writeln;

struct MyRange {
    int[] data;

    int opApply(scope int delegate(ref int) dg) {
        foreach (ref e; data) {
            if (auto r = dg(e)) return r;
        }
        return 0;
    }

    int opApply(scope int delegate(size_t, ref int) dg) {
        foreach (i, ref e; data) {
            if (auto r = dg(i, e)) return r;
        }
        return 0;
    }
}

void main() {
    auto mr = MyRange([1, 2, 3]);
    foreach (ref e; mr) e *= 2;
    foreach (i, e; mr) writeln(i, ": ", e);
}
```

### Alias This for Subtype Emulation

```d
struct Inches {
    double value;
    alias value this;  // implicitly converts to double
}

struct Meters {
    double value;
    alias value this;
}

void main() {
    Inches a = Inches(12.0);
    double d = a;  // implicit conversion via alias this
}
```

### Compile-Time State Machine with final switch

```d
import std.algorithm : map;
import std.array : array;

enum State { idle, running, paused, stopped }

string dispatch(State s) {
    final switch (s) {  // compiler error if a case is missing
        case State.idle:    return "Start";
        case State.running: return "Pause";
        case State.paused:  return "Resume";
        case State.stopped: return "Reset";
    }
}

void main() {
    import std.stdio : writeln;
    auto commands = [State.idle, State.running, State.paused, State.stopped]
        .map!(s => dispatch(s)).array;
    writeln(commands);
}
```

### ref return scope (DIP 1000)

Returns a reference into a slice without escaping. Requires `-preview=dip1000`
for full enforcement; compiles without the flag but escape checking is advisory.

```d
ref int findMax(return scope int[] arr) {
    size_t idx = 0;
    foreach (i, e; arr)
        if (e > arr[idx]) idx = i;
    return arr[idx];
}
```

## Common Idioms

### Template Constraints

```d
import std.traits : isNumeric;
import std.range : isRandomAccessRange;

// Prefer constraints over static assert — gives better error messages
auto doubled(T)(T value) if (isNumeric!T) {
    return value * 2;
}
```

### Error Handling with enforce

```d
import std.exception : enforce;

void process(string data) {
    enforce(data.length > 0, "Data must not be empty");
    enforce(data.length < 1024, "Data too large");
}
```

### Unit Tests as Living Documentation

```d
/// Adds two integers.
int add(int a, int b) => a + b;

unittest {
    assert(add(2, 3) == 5);
    assert(add(0, 0) == 0);
    assert(add(-1, 1) == 0);
}
```

### Contracts

```d
struct BankAccount {
    double balance;

    void deposit(double amount)
    in  { assert(amount > 0, "Amount must be positive"); }
    out { assert(balance >= 0, "Balance cannot be negative"); }
    do  { balance += amount; }
}
```

### Lazy Parameters

```d
import std.stdio : writeln;
import std.conv : to;

// msg is only evaluated if the condition is true — cheap to pass a lambda
void debugLog(lazy string msg) {
    debug writeln(msg);
}

void main() {
    int x = 42;
    debugLog("x is " ~ x.to!string);  // expression not evaluated in release
}
```

### @property for Getters/Setters

```d
class Temperature {
private:
    double _celsius;

public:
    @property double celsius() const { return _celsius; }
    @property void celsius(double v) { _celsius = v; }

    @property double fahrenheit() const { return _celsius * 9.0 / 5.0 + 32.0; }
}
```

## Anti-Patterns to Avoid

### Wildcard Imports in Library Code

```d
// Bad: pollutes namespace, hides dependencies
import std;

// Good: explicit, greppable
import std.stdio : writeln, writefln;
import std.algorithm : filter, map;
```

### Unnecessary Casts

```d
// Bad: truncates silently
auto x = cast(int)3.14;

// Good: explicit conversion with overflow checking
import std.conv : to;
auto y = to!int(3.14);
```

### Global Mutable State

```d
// Bad: shared mutable without synchronization
__gshared int g_counter = 0;

// Better: thread-local (default) or properly synchronized shared
int t_counter = 0;         // thread-local
shared int s_counter = 0;  // requires atomic ops to access safely
```

### Memory Leaks with Manual Allocation

```d
import core.stdc.stdlib : malloc, free;

// Bad: missing free
void bad() {
    auto buf = malloc(1024);
    // ... no free
}

// Good: scope guard guarantees cleanup
void good() {
    auto buf = malloc(1024);
    scope(exit) free(buf);
    // ... use buf
}
```

### Raw Pointer Dereference in @safe Code

```d
// Bad: dangling pointer, undefined behavior
// int* ptr;
// *ptr = 42;  // crashes or corrupts memory

// Good: use slices, refs, or Nullable — stay in @safe
int x = 42;
int* ptr = &x;  // valid pointer to a live variable
*ptr = 99;
```

### Avoid Deeply Chained Transformations Without Naming Steps

```d
import std.algorithm : filter, map;
import std.range : iota;

// Hard to debug: one long chain with no intermediate names
auto bad = iota(0, 10).map!(a => a + 1).filter!(a => a > 3).map!(a => a * 2);

// Better: name intermediate ranges — zero runtime cost, much easier to inspect
auto shifted  = iota(0, 10).map!(a => a + 1);
auto filtered = shifted.filter!(a => a > 3);
auto result   = filtered.map!(a => a * 2);
```

## Error Handling Strategies

### Nullable for Optional Results

```d
import std.typecons : Nullable;
import std.stdio : writeln;

Nullable!int findUser(string name) {
    if (name == "admin") return Nullable!int(1);
    return Nullable!int.init;  // empty
}

void main() {
    auto uid = findUser("admin");
    if (!uid.isNull)
        writeln("Found user: ", uid.get);
}
```

### Scope Guards for Transaction Safety

```d
import std.stdio : writeln;

struct Account {
    double balance;
    void withdraw(double amount) { balance -= amount; }
    void deposit(double amount)  { balance += amount; }
}

void transfer(ref Account from, ref Account to, double amount)
in  { assert(amount > 0 && from.balance >= amount); }
out { assert(from.balance >= 0); }
do  {
    from.withdraw(amount);
    scope(failure) from.deposit(amount);  // rollback on exception
    to.deposit(amount);
    scope(success) writeln("Transfer complete");
}
```

## Quick Reference

### Best Practices Checklist

```d
import std.stdio : writeln;  // ✓ selective import

int add(int a, int b) pure nothrow @safe @nogc => a + b;  // ✓ attributes + =>

void main() {
    auto result = add(3, 4);
    scope(exit) writeln("Done: ", result);  // ✓ scope guard
}
```

### Key DIPs Summary

```
DIP 1000: scope pointers          → -preview=dip1000 (not default)
DIP 1009: expression contracts    → in (a > 0) out (r; r >= 0) do { ... }
DIP 1010: static foreach          → static foreach (i; 0 .. 5) { }
DIP 1013: deprecation process     → deprecated("use newFunc instead")
DIP 1014: move semantics          → move constructor: this(T t) if (...)
DIP 1018: copy constructor        → this(ref return scope const T rhs)
DIP 1029: throw attribute         → nothrow / throw (explicit)
DIP 1030: named arguments         → configure(port: 8080, host: "x")
DIP 1034: noreturn type           → noreturn neverReturns()
DIP 1035: @system variables       → -preview=systemVariables (not default)
DIP 1038: @mustuse                → @mustuse struct Result { ... }
DIP 1043: shortened methods       → int add(int a, int b) => a + b
DIP 1046: ref local variables     → ref int r = someVar; (not yet default)
DIP 1048: language bitfields      → uint x:4; (DMD 2.108+, LDC 1.36+)
DIP 1052: editions                → in progress, not yet usable
DIP 1053: tuple unpacking         → auto (a, b) = tup; (in progress)
```
