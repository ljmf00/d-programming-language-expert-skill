---
name: d-lang-documentation
description: >-
  D documentation with DDoc: comment syntax, Params/Returns/Throws
  sections, formatting and reference macros ($(D ...), $(REF ...),
  $(LINK2 ...)), section organization, embedded and extractable code
  examples, generating HTML docs. Use when writing or reviewing D
  documentation comments.
license: MIT
metadata:
  topics: ddoc documentation comments macros doctest
  order: 15
---

# D Documentation (DDoc)

Guide to D's built-in documentation system: DDoc comment syntax, standard sections, macros, and embedded code examples. Testing and contracts live in [12-testing.md](12-testing.md).

## Table of Contents

- [DDoc Documentation Basics](#ddoc-documentation-basics)
- [DDoc Params/Returns/Throws](#ddoc-paramsreturnsthrows)
- [DDoc Macros: D, I, B](#ddoc-macros-d-i-b)
- [DDoc Macros: REF and LINK2](#ddoc-macros-ref-and-link2)
- [DDoc Sections and Subrefs](#ddoc-sections-and-subrefs)
- [DDoc DDOC\_ Macros](#ddoc-ddoc_-macros)
- [Embedded Code Examples](#embedded-code-examples)
- [Doctest Extraction](#doctest-extraction)

---

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

## Quick Reference

### DDoc Generation

```bash
# Generate HTML documentation
ldc2 -d -o- mymodule.d > mymodule.html

# Generate with custom output
dmd -D -Df=output.html mymodule.d
```

## References

- [DDoc Documentation](https://dlang.org/spec/ddoc.html)
- [D Style Guide](https://dlang.org/dstyle.html)
