---
name: d-lang-templates
description: >-
  D templates and metaprogramming: template parameters, constraints, IFTI,
  variadic templates, eponymous templates, alias sequences, static foreach,
  CTFE, mixins, std.meta (staticMap, Filter, AliasSeq), std.traits
  (ReturnType, Parameters, isNumeric, isCallable).
  Use when writing generic code or compile-time logic.
license: MIT
metadata:
  topics: templates metaprogramming ctfe mixins traits compile-time
  order: 04
---

# D Programming Language - Templates & Metaprogramming

Comprehensive guide to D's template system, compile-time features, and metaprogramming capabilities.

## Table of Contents
- [Template Basics](#template-basics)
- [Template Parameters](#template-parameters)
- [Template Constraints](#template-constraints)
- [Variadic Templates](#variadic-templates)
- [Eponymous Templates](#eponymous-templates)
- [Template Parameter Deduction](#template-parameter-deduction)
- [Alias Sequences](#alias-sequences)
- [`static foreach` (DIP 1010)](#static-foreach-dip-1010)
- [Compile-Time Function Execution](#compile-time-function-execution)
- [Mixins](#mixins)
- [std.meta](#stdmeta)
- [std.traits](#stdtraits)
- [Quick Reference](#quick-reference)

## Template Basics

### Function Templates
```d
// Basic template function
auto max(T)(T a, T b) {
    return (a > b) ? a : b;
}

// Usage
auto result = max(3, 5);      // int
auto result2 = max(3.14, 2.71); // double
```

### Class Templates
```d
class Stack(T) {
    private T[] data;
    
    void push(T value) {
        data ~= value;
    }
    
    T pop() {
        auto v = data[$ - 1];
        data = data[0 .. $ - 1];
        return v;
    }
    
    @property bool empty() const {
        return data.length == 0;
    }
}

// Usage
auto intStack = new Stack!int;
intStack.push(42);
```

### Struct Templates
```d
struct Pair(T, U) {
    T first;
    U second;
    
    this(T first, U second) {
        this.first = first;
        this.second = second;
    }
}

// Usage
auto pair = Pair!(int, string)(42, "hello");
```

### Template Specialization
```d
// Primary template with specialization via static if
auto isEven(T)(T value) {
    static if (is(T == int)) {
        // Optimized for int
        return (value & 1) == 0;
    } else {
        return value % 2 == 0;
    }
}
```

## Template Parameters

### Type Parameters
```d
// Single type parameter
auto identity(T)(T value) {
    return value;
}

// Multiple type parameters
auto tuple(T, U)(T first, U second) {
    return [first, second];
}
```

### Non-Type Parameters
```d
// Integer constant parameter
struct Array(T, size_t N) {
    T[N] data;
}

// Usage
Array!(int, 10) arr;  // int[10]
```

### Template Parameters (alias)
```d
// Alias parameter (for functions, types, templates)
bool greater(int a, int b) { return a > b; }

auto sorted(alias Pred, T)(T[] arr) {
    return arr.sort!Pred;
}

// Usage
auto result = sorted!greater([3, 1, 2]);
```

### Template Template Parameters
```d
// Template taking a template as parameter via alias
struct MyVec(T) { T[] data; }

template Wrap(alias Template, T) {
    alias type = Template!T;
}

// Usage
alias MyVecOfInt = Wrap!(MyVec, int);
```

### Default Template Parameters
```d
// Default type parameter
class Container(T = int) {
    T[] data;
}

// Usage
auto c1 = new Container!();      // Container!(int)
auto c2 = new Container!(double); // Container!(double)
```

## Template Constraints

### if Constraints
```d
// Constraint on template parameter
auto doubleValue(T)(T value) if (isNumeric!T) {
    return value * 2;
}

// Multiple constraints
auto process(T)(T value) if (isIntegral!T && T.sizeof <= 4) {
    // Process 32-bit or smaller integers
}
```

### is Expressions
```d
import std.traits : isCallable;
import std.range : isInputRange;

void example(T)() {
    // Check if type is integral
    static if (is(T : int)) { }

    // Check if type has member
    static if (is(typeof(T.member))) { }

    // Check if type is callable
    static if (isCallable!T) { }

    // Check if type is a range
    static if (isInputRange!T) { }
}
```

### Template Predicates
```d
import std.traits : isIntegral, isFloatingPoint, isNumeric,
                    isPointer, isArray;

void example(T)() {
    static if (isIntegral!T) {
        // T is an integral type
    }

    static if (isFloatingPoint!T) {
        // T is a floating point type
    }
}
```

### Constraint Examples
```d
// Only for types with opCmp
auto sort(T)(T[] arr) if (is(typeof(T.init.opCmp(T.init)))) {
    // Sort using opCmp
}

// Only for numeric types
auto add(T)(T a, T b) if (isNumeric!T) {
    return a + b;
}

// Only for ranges
auto processRange(R)(R range) if (isInputRange!R) {
    foreach (elem; range) {
        // Process element
    }
}
```

## Variadic Templates

### Variadic Function Templates
```d
// Variadic template function
auto sum(T...)(T args) {
    static if (T.length == 0) {
        return 0;
    } else {
        return args[0] + sum!(T[1 .. $])(args[1 .. $]);
    }
}

// Usage
auto result = sum(1, 2, 3, 4, 5);  // 15
```

### Variadic Class Templates
```d
// Variadic template struct
struct Tuple(T...) {
    T data;
}

// Usage
auto t = Tuple!(int, string, double)(42, "hello", 3.14);
```

### Template Tuples
```d
// Template tuple parameter
auto process(T...)(T args) {
    static foreach (i; 0 .. T.length) {
        // Process each argument
    }
}
```

## Eponymous Templates

An eponymous template has the same name as a member within it, allowing direct use:

```d
// Eponymous template alias
template GreatestCommonDivisor(T) {
    static if (is(T == int)) {
        alias GCD = int;
    } else {
        alias GCD = T;
    }
}

// Usage: GCD!int directly resolves to the inner alias
alias gcdType = GreatestCommonDivisor!int;

// Eponymous template with variable
template Factorial(int n) {
    static if (n <= 0)
        enum factorial = 1;
    else
        enum factorial = n * Factorial!(n-1).factorial;
}

// Usage
enum f5 = Factorial!5.factorial;  // 120

// Eponymous template using enum (more concise)
template Square(int n) {
    enum Square = n * n;
}

// Usage
enum s = Square!5;  // 25
```

## Template Parameter Deduction

```d
// D can deduce template parameters from function arguments

// Explicit: specify T in call
auto result = max!(int)(5, 10);

// Implicit: T is deduced from arguments
auto result2 = max(5, 10);  // T = int
auto result3 = max(5.0, 10.0);  // T = double

// Deduction with multiple parameters
void pair(T, U)(T first, U second) { }

pair(1, "hello");  // T = int, U = string
pair!(int, string)(1, "hello");  // Explicit

// Deduction with alias parameters
void call(alias func, T)(T arg) {
    func(arg);
}

call!writeln("hello");  // alias = writeln, T = string
```

### AliasSeq
```d
import std.meta : AliasSeq;

// Create alias sequence
alias Types = AliasSeq!(int, double, string);

// Access elements
static assert(is(Types[0] == int));
static assert(is(Types[1] == double));

// Slice alias sequence
alias IntAndDouble = Types[0 .. 2];
```

### aliasSeqOf
```d
import std.meta : AliasSeq, aliasSeqOf;

// Create alias sequence using AliasSeq
alias Seq = AliasSeq!(1, 2, 3);

// Create alias sequence from types
alias TypeSeq = AliasSeq!(int, double, string);
```

### Iterating Alias Sequences
```d
import std.meta : AliasSeq;

alias Types = AliasSeq!(int, double, string);

static foreach (i; 0 .. Types.length) {
    // Process each type
    static if (is(Types[i] == int)) {
        // Handle int
    }
}
```

## `static foreach` (DIP 1010)

### Basic static foreach
```d
// Iterate at compile-time without run-time overhead
static foreach (i; 0 .. 5) {
    mixin("int value" ~ i.to!string ~ " = " ~ i.to!string ~ ";");
}
// Generates:
// int value0 = 0;
// int value1 = 1;
// int value2 = 2;
// int value3 = 3;
// int value4 = 4;
```

### static foreach over types
```d
import std.meta : AliasSeq;

alias Types = AliasSeq!(int, double, string);

static foreach (i, T; Types) {
    mixin(T.stringof ~ "[] arr" ~ i.stringof ~ " = new " ~ T.stringof ~ "[10];");
}
// Generates:
// int[] arr0 = new int[10];
// double[] arr1 = new double[10];
// string[] arr2 = new string[10];
```

### static foreach with compile-time state
```d
import std.meta : AliasSeq;

alias Types = AliasSeq!(int, double, string);

// Zero-based dispatch
static foreach (i, T; Types) {
    static assert(i < Types.length);
}
```

## Compile-Time Function Execution

### CTFE Basics
```d
// Function that can run at compile-time
pure int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Run at compile-time
enum FACT_5 = factorial(5);  // 120

// Use in template
enum SIZE = factorial(10);
int[SIZE] arr;  // int[3628800]
```

### CTFE Requirements
```d
// Must be pure and @safe (usually)
pure int compute(int x) {
    return x * 2;
}

// Can be called at compile-time
enum result = compute(21);
```

### CTFE with Arrays
```d
// Build array at compile-time
int[] buildArray(int size) {
    int[] arr = new int[size];
    for (int i = 0; i < size; i++) {
        arr[i] = i * 2;
    }
    return arr;
}

enum arr = buildArray(10);  // [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### CTFE with Strings
```d
// String manipulation at compile-time
string reverseString(string s) {
    char[] result = new char[s.length];
    for (int i = 0; i < s.length; i++) {
        result[i] = s[s.length - 1 - i];
    }
    return result.idup;
}

enum reversed = reverseString("hello");  // "olleh"
```

### CTFE with Classes
```d
class Config {
    string name;
    int value;
    
    this(string name, int value) {
        this.name = name;
        this.value = value;
    }
}

// Usage
auto config = new Config("test", 42);
config.value = 42;
```

## Mixins

### String Mixins
```d
// Generate code at compile-time
string generateCode(string name) {
    return `void ` ~ name ~ `() {
        writeln("Generated function: ` ~ name ~ `");
    }`;
}

mixin(generateCode("myFunction"));
myFunction();
```

### Template Mixins
```d
// Reusable template mixin
template Equality() {
    bool opEquals(ref const typeof(this) other) const {
        // Generate equality comparison
        return true;
    }
    
    int opCmp(ref const typeof(this) other) const {
        // Generate comparison
        return 0;
    }
}

struct MyStruct {
    int x;
    int y;
    
    mixin Equality;
}
```

### Mixin with Variables
```d
void example() {
    enum code = "int x = 42;";
    mixin(code);
    writeln(x);  // 42
}
```

### Mixin with Templates
```d
template GenerateMethods(string name) {
    mixin(`void ` ~ name ~ `() {
        writeln("Generated method: ", ` ~ name ~ `);
    }`);
}

class MyClass {
    mixin GenerateMethods!("method1");
    mixin GenerateMethods!("method2");
}
```

### q{} String Literal
```d
// q{} allows embedding code without escaping
string code = q{
    void function() {
        int x = 10;
        if (x > 5) {
            writeln("x is greater than 5");
        }
    }
};
```

### Mixin for Code Generation
```d
template GenerateProperties(names...) {
    static foreach (name; names) {
        mixin(`private int _` ~ name ~ `;`);
        mixin(`@property int ` ~ name ~ `() const { return _` ~ name ~ `; }`);
        mixin(`@property void ` ~ name ~ `(int value) { _` ~ name ~ ` = value; }`);
    }
}

class MyClass {
    mixin GenerateProperties!("x", "y", "z");
}
```

## Tuple Unpacking

```d
import std.typecons : tuple;

// Access tuple elements by index
auto t = tuple(42, "hello", 3.14);
auto x = t[0];  // 42
auto y = t[1];  // "hello"
auto z = t[2];  // 3.14

// Use .expand to pass elements to a function
auto sum = (t[0] + 0);  // use elements individually

// In template context
template Unpack(T...) {
    void apply(T args) {
        // Destructure args at compile-time
        static foreach (i; 0 .. T.length) {
            pragma(msg, T[i].stringof, ": ", args[i]);
        }
    }
}
```

## std.meta

### staticMap
```d
import std.meta : staticMap;

// Apply template to each type in sequence
template MakePtr(T) {
    alias type = T*;
}

alias PtrTypes = staticMap!(MakePtr, int, double, string);
```

### Filter
```d
import std.meta : Filter;

// Filter types by predicate
alias Integers = Filter!(isIntegral, int, double, string, long);
// Integers == AliasSeq!(int, long)
```

### Erase
```d
import std.meta : Erase;

// Remove type from sequence
alias WithoutInt = Erase!(int, int, double, string);
// WithoutInt == AliasSeq!(double, string)
```

### allSatisfy / anySatisfy
```d
import std.meta : allSatisfy, anySatisfy;

static if (allSatisfy!(isIntegral, int, long, byte)) {
    // All types are integral
}

static if (anySatisfy!(isFloatingPoint, int, double, string)) {
    // At least one type is floating point
}
```

### Alias
```d
import std.meta : Alias;

// Create alias
alias MyInt = Alias!(int);
```

## std.traits

### Type Categories
```d
import std.traits : isIntegral, isFloatingPoint, isNumeric,
                    isPointer, isArray, isAssociativeArray,
                    isStaticArray, isDynamicArray;

void example(T)() {
    static if (isIntegral!T) { }
    static if (isFloatingPoint!T) { }
    static if (isNumeric!T) { }
    static if (isPointer!T) { }
    static if (isArray!T) { }
    static if (is(T : string)) { }
}
```

### Function Traits
```d
import std.traits : isFunction, isCallable, isDelegate,
                    ReturnType, Parameters;

void example(T)() {
    // Check if type is a function
    static if (isFunction!T) { }
}

// Get return type
alias Func = int function(int, int);
alias Ret = ReturnType!Func;  // int

// Get parameters
alias Params = Parameters!Func;  // AliasSeq!(int, int)
```

### Aggregate Traits
```d
import std.traits : hasMember, hasStaticMember, isNested,
                    BaseClassesTuple, InterfacesTuple;

class MyClass {
    int member;
}

// Check for member
static if (hasMember!(MyClass, "member")) { }

// Get base classes (Object by default)
alias Bases = BaseClassesTuple!(MyClass);

// Get interfaces
alias Intfs = InterfacesTuple!(MyClass);
```

### Type Conversion
```d
import std.traits : isImplicitlyConvertible, isAssignable,
                    CommonType, CopyConstness;

// Check conversion
static if (isImplicitlyConvertible!(int, long)) { }

// Check assignment
static if (isAssignable!(int, int)) { }

// Common type
alias CT = CommonType!(int, double);  // double

// Copy constness
alias CC = CopyConstness!(int, const int);  // const int
```

### Qualifier Operations
```d
import std.traits : Unqual, Unconst, Unshared;

// Remove all qualifiers
alias UQ = Unqual!(const int);  // int

// Remove const
alias UC = Unconst!(const int);  // int

// Remove shared
alias US = Unshared!(shared int);  // int
```

## Macros & Code Generation

D's compile-time introspection (`__traits`), string mixins, UDAs, and template-based expansion provide a powerful macro system for generating code at compile time without external preprocessors.

### String Mixins for Code Generation
```d
import std.stdio;

// Build code at compile time and mix it in
enum code = q{ writeln("Generated!"); };
void genMixinStr() { mixin(code); }
```

### Using __traits for Introspection
```d
import std.stdio;
struct S { int x, y; }
void genTraitsIntro() {
    foreach (idx, member; __traits(allMembers, S)) {
        writeln(member);
    }
}
```

### User-Defined Attributes (UDAs) for Code Gen
```d
import std.stdio;
struct Serializable { string name; }

@Serializable("person")
struct Person {
    int id;
    string name;
}

void genUDAIntro() {
    foreach (attr; __traits(getAttributes, Person)) {
        writeln(attr);
    }
}
```

### static foreach Code Expansion
```d
import std.stdio;
void genStaticForeachExpand() {
    static foreach (i; 0 .. 3) {
        pragma(msg, "Expanded iteration ", i);
    }
    writeln("static foreach compiled");
}
```

### Template Code Generation with staticMap
```d
import std.meta : staticMap;
import std.stdio;

template GenGetter(string name) {
    string GenGetter() { return "auto " ~ name ~ "() { return _" ~ name ~ "; }"; }
}

void genStaticMapDemo() {
    // staticMap generates code per element
    writeln("Code generation with templates");
}
```

### Compile-Time Format Strings
```d
import std.format : format;
import std.stdio;
enum greeting = format!"Hello, %s!"("World");
void genFmtString() { writeln(greeting); }
```

### Mixin Templates (parameterized code blocks)
```d
import std.stdio;

// Parameterized mixin: injects field-aware code
mixin template FieldLabel(T, string fname) {
    string label() { return fname; }
}

struct Point {
    int x, y;
    mixin FieldLabel!(int, "x") xLabel;
}

void genMixinTempl() {
    Point p = Point(1, 2);
    writeln(p.xLabel.label());  // Prints: x
}
```

## Quick Reference

### Template Basics
```d
// Function template
auto func(T)(T param) { }

// Class template
class Class(T) { }

// Struct template
struct Struct(T) { }

// Template with constraint
auto func(T)(T param) if (is(T == int)) { }
```

### Template Parameters
```d
// Type parameter
auto func(T)(T param) { }

// Non-type parameter
auto func(T, size_t N)(T[N] arr) { }

// Alias parameter
auto func(alias pred)(T) { }

// Template template parameter
template TemplateTemplate(Template, T) { }
```

### Template Constraints
```d
// if constraint
auto func(T)(T param) if (isNumeric!T) { }

void example(T)() {
    // is expression
    static if (is(T : int)) { }

    // Template predicates
    static if (isIntegral!T) { }
}
```

### Variadic Templates
```d
// Variadic function
auto func(T...)(T args) { }

// Variadic class
class Class(T...) { }

// Template tuple
auto func(T...)(T args) { }

// Eponymous template
template Square(int n) { enum Square = n * n; }
enum s = Square!5;  // 25
```

### static foreach
```d
import std.meta : AliasSeq;

alias Types = AliasSeq!(int, double, string);

static foreach (i; 0 .. 5) { }          // Iterate integers
static foreach (T; Types) { }            // Iterate types
static foreach (i, T; Types) { }         // With index
static foreach_reverse (i; 0 .. 10) { }  // Reverse
```

### CTFE
```d
// Compile-time function
pure int func(int x) { return x * 2; }

// Call at compile-time
enum result = func(21);

// Build array at compile-time
int[] buildArray(int size) {
    auto result = new int[](size);
    foreach (i; 0 .. size) result[i] = i * i;
    return result;
}
enum arr = buildArray(10);
```

### Tuple Unpacking
```d
import std.typecons : tuple;

// Access tuple elements by index
auto t = tuple(1, "hello", 3.14);
auto a = t[0];  // 1
auto b = t[1];  // "hello"
auto c = t[2];  // 3.14
```

### Mixins
```d
// String mixin (with a compile-time string)
mixin("int x = 42;");

// Template mixin
template Simple() { int y; }
mixin Simple!();
```

### std.meta
```d
import std.meta : AliasSeq, staticMap, Filter, Erase,
                  allSatisfy, anySatisfy, Reverse;

template MakePtr(T) { alias type = T*; }

alias Seq = AliasSeq!(int, double);
alias Mapped = staticMap!(MakePtr, Seq);
alias Filtered = Filter!(isIntegral, Seq);
alias Reversed = Reverse!(Seq);
```

### std.traits
```d
import std.traits : isIntegral, isFloatingPoint, isNumeric,
                    isPointer, isArray, isCallable,
                    isDelegate, isFunction;
import std.traits : ReturnType, Parameters,
                    Unqual, Unconst, Unshared,
                    CommonType;
import std.traits : BaseClassesTuple, InterfacesTuple,
                    Fields, FieldNameTuple, EnumMembers;
import std.traits : hasMember;

void example(T, alias func)() {
    static if (isIntegral!T) { }
    alias Ret = ReturnType!func;
    alias Params = Parameters!func;
}
```

## Common Idioms

### Type-Safe Factory
```d
auto create(T)(T value) {
    static if (isNumeric!T) {
        return new NumericWrapper!(T)(value);
    } else {
        return new GenericWrapper!(T)(value);
    }
}
```

### Generic Swap
```d
void swap(T)(ref T a, ref T b) {
    T temp = a;
    a = b;
    b = temp;
}
```

### Compile-Time Array Generation
```d
int[] generateArray(int size) {
    int[] arr = new int[size];
    for (int i = 0; i < size; i++) {
        arr[i] = i * i;
    }
    return arr;
}

enum squares = generateArray(10);  // [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### Mixin for Operator Overloading
```d
struct Point {
    int x, y;
    mixin OpOverload!();
}

template OpOverload() {
    auto opBinary(string op)(Point other) const if (op == "+" || op == "-") {
        static if (op == "+") {
            return Point(x + other.x, y + other.y);
        } else {
            return Point(x - other.x, y - other.y);
        }
    }
}
```

## References
- [D Language Specification: Templates](https://dlang.org/spec/template.html)
- [D Language Specification: CTFE](https://dlang.org/spec/compile-time.html)
- [Phobos std.meta](https://dlang.org/phobos/std_meta.html)
- [Phobos std.traits](https://dlang.org/phobos/std_traits.html)
- [D Templates Tutorial](https://github.com/PhilippeSigaud/D-templates-tutorial)
