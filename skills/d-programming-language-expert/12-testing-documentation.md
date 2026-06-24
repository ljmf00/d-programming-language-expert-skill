---
name: d-lang-testing-docs
description: >-
  D testing and documentation: unittest blocks, pre/post-condition
  contracts, DDoc documentation generation, DDoc macros and sections,
  embedded code examples, contract inheritance. Use when writing
  tests, documentation, or verifying D code correctness.
license: MIT
metadata:
  topics: testing unittest contracts ddoc documentation doctest
  order: 12
---

# D Testing & Documentation

Comprehensive guide to D's testing infrastructure, contract programming, DDoc documentation system, and embedded code examples.

## Table of Contents

- [Unittest Blocks](#unittest-blocks)
- [Unittest with Setup/Teardown](#unittest-with-setup-teardown)
- [Unittest with Imports](#unittest-with-imports)
- [Unittest with scope(exit)](#unittest-with-scopeexit)
- [Conditional Unittests](#conditional-unittests)
- [Pre/Post-Condition Contracts](#prepost-condition-contracts)
- [Contracts on Struct Methods](#contracts-on-struct-methods)
- [Contracts with Return Value Capture](#contracts-with-return-value-capture)
- [Contract Inheritance](#contract-inheritance)
- [Class Invariants](#class-invariants)
- [Debug-Only Contracts](#debug-only-contracts)
- [assert with Messages](#assert-with-messages)
- [std.experimental.testing](#stdexperimentaltesting)
- [DDoc Documentation Basics](#ddoc-documentation-basics)
- [DDoc Params/Returns/Throws](#ddoc-paramsreturnsthrows)
- [DDoc Macros: D, I, B](#ddoc-macros-d-i-b)
- [DDoc Macros: REF and LINK2](#ddoc-macros-ref-and-link2)
- [DDoc Sections and Subrefs](#ddoc-sections-and-subrefs)
- [DDoc DDOC\_ Macros](#ddoc-ddoc_-macros)
- [Embedded Code Examples](#embedded-code-examples)
- [Doctest Extraction](#doctest-extraction)
- [Testing Best Practices](#testing-best-practices)

---

## Unittest Blocks

### Basic Unittest

```d
// Basic unittest block at module level
unittest {
    assert(1 + 1 == 2);
}
```

### Multiple Assertions

```d
// Multiple assertions in a single unittest block
unittest {
    assert(2 + 3 == 5);
    assert(10 - 3 == 7);
    assert(4 * 5 == 20);
}
```

### Unittest with Message

```d
// Unittest with descriptive assertion messages
unittest {
    int result = 6;
    assert(result == 6, "Expected result to be 6");
    assert(result > 0, "Result must be positive");
}
```

## Unittest with Setup/Teardown

### Setup with Local Variables

```d
// Setup and test with local variables
unittest {
    import std.stdio;
    int x = 42;
    assert(x == 42);
    x = 0;
}
```

### Unittest with scope(exit) Cleanup

```d
// Use scope(exit) for guaranteed cleanup in unittests
unittest {
    import std.stdio;
    int value = 100;
    scope(exit) writeln("cleanup done");
    assert(value == 100);
}
```

### Unittest with scope(failure)

```d
// Use scope(failure) for cleanup only on test failure
unittest {
    import std.stdio;
    int value = 100;
    scope(failure) writeln("test failed");
    assert(value == 100);
}
```

## Unittest with Imports

### Unittest with Module-Level Import

```d
import std.array;

// Import at module level, used in unittest
unittest {
    auto arr = [1, 2, 3];
    assert(arr.length == 3);
}
```

### Unittest with Local Import

```d
// Import inside unittest block (scoped to test only)
unittest {
    import std.conv : to;
    int x = to!int("42");
    assert(x == 42);
}
```

## Conditional Unittests

### OS-Specific Unittest

```d
// Run unittest only on Linux
version (Linux) {
    unittest {
        assert(42 == 42);
    }
}
```

### Debug-Only Code in Unittests

```d
// Debug-only code inside unittest blocks
unittest {
    int x = 10;
    debug {
        assert(x > 0);
    }
    assert(x == 10);
}
```

## Pre/Post-Condition Contracts

### Basic Pre-Condition (in)

```d
// Pre-condition: validates input before execution
int divide(int a, int b)
in (b != 0, "Cannot divide by zero")
{
    return a / b;
}
```

### Basic Post-Condition (out)

```d
// Post-condition: validates output after execution
int absolute(int value)
out (result; result >= 0)
{
    return value < 0 ? -value : value;
}
```

### Combined in/out Contracts

```d
// Both pre and post conditions
int factorial(int n)
in (n >= 0 && n <= 20, "n must be 0..20")
out (result; result > 0, "Factorial must be positive")
{
    int r = 1;
    foreach (i; 1 .. n + 1) r *= i;
    return r;
}
```

## Contracts on Struct Methods

### Struct Method with Contract

```d
// Contract on struct method
struct Buffer {
    int[] data;
    void append(int v)
    in (data.length < 100)
    out (; data[$ - 1] == v)
    {
        data ~= v;
    }
}
```

### Struct with Invariant

```d
// Struct invariant checked after every public method
struct Counter {
    int count;
    void increment() { count++; }
    invariant (count >= 0, "Count must be non-negative");
}
```

## Contracts with Return Value Capture

### Post-Condition with Result

```d
// Capture return value in post-condition
int clamp(int value, int min, int max)
in (min <= max, "min must not exceed max")
out (result; result >= min && result <= max, "Result must be in range")
{
    if (value < min) return min;
    if (value > max) return max;
    return value;
}
```

## Contract Inheritance

### Abstract Class with Contract

```d
// Abstract class defining contract interface
abstract class Shape {
    pure nothrow @safe double area() @property;
}
```

### Subclass Implementing Contract

```d
// Subclass implementing abstract method
import std.math : PI;

abstract class BaseShape {
    pure nothrow @safe double area() @property;
}

class Circle : BaseShape {
    double radius;
    this(double r) { radius = r; }
    override pure nothrow @safe double area() @property {
        return PI * radius * radius;
    }
}
```

## Class Invariants

### Class with Invariant

```d
// Class invariant checked after every public method call
class Account {
    double balance;
    this(double initial) { balance = initial; }
    void deposit(double amount) { balance += amount; }
    invariant (balance >= 0, "Balance cannot be negative");
}
```

## Debug-Only Contracts

### Debug Block for Extra Checks

```d
// Extra assertions only in debug builds
int process(int x) {
    assert(x >= 0);
    debug {
        assert(x < 1000000, "x suspiciously large");
    }
    return x * 2;
}
```

## assert with Messages

### Assert with Custom Message

```d
import std.conv : to;

// assert with string message for better error reporting
void validate(int value) {
    assert(value > 0, "Value must be positive, got: " ~ value.to!string);
}
```

### Assert with Ternary Expression

```d
// assert condition with descriptive failure check
bool isEven(int n) {
    bool result = n % 2 == 0;
    assert(result || n % 2 != 0, "Unexpected state");
    return result;
}
```

## std.experimental.testing

### Basic Assertion Framework

```d
// Note: std.experimental.testing availability varies by Phobos version
// Use standard assert() for portable testing
unittest {
    // Portable assertion (always available)
    assert(true, "This always passes");
    assert(1 == 1, "Equality check");
}
```

### Test Helper Functions

```d
// Custom test helpers for reusable assertions
import std.exception : enforce;

void assertEquals(int expected, int actual, string msg = "") {
    assert(expected == actual, msg);
}

unittest {
    assertEquals(5, 2 + 3, "Addition test");
}
```

## DDoc Documentation Basics

### Basic DDoc Comment

```d
/**
 * Calculates the sum of two integers.
 *
 * Params:
 *    a = First integer
 *    b = Second integer
 *
 * Returns:
 *    The sum of a and b
 */
int sum(int a, int b) {
    return a + b;
}
```

### DDoc with Example

```d
/**
 * Reverses a string.
 *
 * Params:
 *    s = Input string to reverse
 *
 * Returns:
 *    Reversed string
 *
 * Example:
 *    auto result = reverseStr("hello"); // "olleh"
 */
string reverseStr(string s) {
    char[] chars = s.dup;
    import std.algorithm : reverse;
    reverse(chars);
    return chars.idup;
}
```

## DDoc Params/Returns/Throws

### DDoc Throws Documentation

```d
/**
 * Divides two numbers.
 *
 * Params:
 *    numerator = The number to be divided
 *    denominator = The divisor
 *
 * Returns:
 *    The quotient
 *
 * Throws:
 *    Exception if denominator is zero
 */
double divideNumbers(double numerator, double denominator) {
    import std.exception : enforce;
    enforce(denominator != 0, "Division by zero");
    return numerator / denominator;
}
```

## DDoc Macros: D, I, B

### Inline Formatting Macros

```d
/**
 * $(B Bold text) for emphasis. $(I Italic text) for secondary emphasis.
 * $(D Code text) for inline code references.
 *
 * Example: Use $(D writeln) to print output.
 */
void printMessage(string msg) {
    import std.stdio;
    writeln(msg);
}
```

### Macro in Function Documentation

```d
/**
 * Checks if a number is $(B positive).
 *
 * $(D isPositive(5)) returns $(D true).
 * $(D isPositive(-1)) returns $(D false).
 *
 * $(I Note:) Zero is considered not positive.
 */
bool isPositive(int n) {
    return n > 0;
}
```

## DDoc Macros: REF and LINK2

### External Reference Macros

```d
/**
 * See $(REF std.stdio.writeln "writeln") for output functions.
 * Learn more at $(LINK2 "https://dlang.org/phobos/std_stdio.html" "std.stdio").
 */
void greet(string name) {
    import std.stdio;
    writeln("Hello, ", name);
}
```

## DDoc Sections and Subrefs

### DDoc Section Organization

```d
/**
 * $(SECTION Overview)
 * This module provides utility functions.
 *
 * $(SUBREF "utility" "Utility Functions")
 * Collection of helper functions.
 */
int utilityAdd(int a, int b) {
    return a + b;
}
```

## DDoc DDOC\_ Macros

### DDoc Conditional Macros

```d
/**
 * $(DDOC_VERSION "2.099") This feature requires D 2.099+.
 * $(DDOC_OS "Linux") Linux-specific functionality.
 */
int versionCheck() {
    return 1;
}
```

## Embedded Code Examples

### Code Example in DDoc

```d
/**
 * Demonstrates DDoc code embedding.
 *
 * $(CODE
 *    import std.stdio;
 *    void main() {
 *        writeln("Hello from DDoc!");
 *    }
 * )
 */
void showUsage() {
    import std.stdio;
    writeln("See documentation for usage");
}
```

### Inline Code with D Macro

```d
/**
 * Use $(D std.algorithm.sort) for sorting arrays.
 * Use $(D std.array.join) for concatenation.
 * See $(REF std.range "std.range") for range utilities.
 */
bool isSorted(int[] arr) {
    import std.algorithm : isSorted;
    return arr.isSorted();
}
```

## Doctest Extraction

### Doctest Pattern

```d
/**
 * Computes the maximum of two values.
 *
 * Example:
 *    auto m = maxVal(3, 7); // m is 7
 *    auto n = maxVal(-1, -5); // n is -1
 */
int maxVal(int a, int b) {
    return a > b ? a : b;
}
```

### Multiple Examples

```d
/**
 * Checks if a string is a palindrome.
 *
 * Examples:
 *    isPalindrome("racecar")  // true
 *    isPalindrome("hello")    // false
 *    isPalindrome("")         // true
 */
bool isPalindrome(string s) {
    import std.algorithm : equal;
    import std.range : retro;
    return s.equal(retro(s));
}
```

## Testing Best Practices

### Struct with Full Test Coverage

```d
// Well-tested struct with contracts and unittests
import std.stdio;

struct SafeArray {
    int[] data;

    void push(int value)
    in (data.length < 1000)
    out (; data[$ - 1] == value)
    {
        data ~= value;
    }

    int pop()
    in (data.length > 0, "Cannot pop from empty array")
    out (result; result >= 0)
    {
        auto val = data[$ - 1];
        data.length--;
        return val;
    }
}

unittest {
    SafeArray arr;
    arr.push(10);
    assert(arr.data.length == 1);
    assert(arr.pop() == 10);
    assert(arr.data.length == 0);
}
```

### Comprehensive Class Test

```d
// Class with invariant and unittest coverage
import std.exception : enforce;

class Stack {
    private int[] _items;

    void push(int item) {
        _items ~= item;
    }

    int pop() {
        enforce(_items.length > 0, "Stack is empty");
        auto val = _items[$ - 1];
        _items.length--;
        return val;
    }

    bool empty() const @property {
        return _items.length == 0;
    }

    invariant (_items.length >= 0);
}

unittest {
    auto stack = new Stack();
    assert(stack.empty);
    stack.push(42);
    assert(!stack.empty);
    assert(stack.pop() == 42);
    assert(stack.empty);
}
```

### Contract Testing Pattern

```d
// Testing contracts by triggering pre/post-conditions
import std.exception : assertThrown;
import core.exception : AssertError;

int safeDivide(int a, int b)
in (b != 0)
out (result; result * b == a || (a % b != 0 && result == a / b))
{
    return a / b;
}

void main() {
    assert(safeDivide(10, 2) == 5);
    assert(safeDivide(7, 2) == 3);
    assertThrown!AssertError(safeDivide(10, 0));
}
```

## Quick Reference

### Testing Commands

```bash
# Compile with unittests enabled
ldc2 -unittest -d mymodule.d

# Compile with contracts enabled
ldc2 -check -unittest -d mymodule.d

# Run generated binary
./mymodule
```

### DDoc Generation

```bash
# Generate HTML documentation
ldc2 -d -o- mymodule.d > mymodule.html

# Generate with custom output
dmd -D -Df=output.html mymodule.d
```

### Contract Summary

```d
// Contract syntax quick reference (expression-based, DIP 1009)
// Pre-condition (input validation)
//   in (condition, "optional message")
// Post-condition (output validation)
//   out (result; condition)   // result captures the return value
//   out (; condition)         // no result capture
// Body follows directly (no `do` needed with expression contracts)
//   { return value; }
// Class/struct invariant
//   invariant (condition);
```

> The block form (`in { assert(...); } do { ... }`) is still valid; prefer the
> expression form above when each contract is a single assertion.

## References

- [D Language Specification - Unit Tests](https://dlang.org/spec/module.html#unittests)
- [D Language Specification - Contracts](https://dlang.org/spec/function.html#contract-programming)
- [DDoc Documentation](https://dlang.org/spec/ddoc.html)
- [D Style Guide](https://dlang.org/dstyle.html)
- [Phobos std.exception](https://dlang.org/phobos/std_exception.html)
