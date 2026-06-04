---
name: d-lang-ranges
description: >-
  D ranges and algorithms: range primitives (empty/front/popFront), range
  traits (isInputRange et al.), std.algorithm (map, filter, reduce, sort,
  find), range combinators (chain, zip, iota, cycle, chunks, slide).
  Use when processing collections or sequences of data.
license: MIT
metadata:
  topics: ranges algorithms iteration sorting searching
  order: 03
---

# D Programming Language - Ranges & Algorithms

Comprehensive guide to D's range-based programming model and the powerful std.algorithm library.

## Table of Contents

- [Range Basics](#range-basics)
- [Range Types](#range-types)
- [Range Primitives](#range-primitives)
- [Range Composition](#range-composition)
- [std.algorithm](#stdalgorithm)
- [Common Patterns](#common-patterns)
- [Performance Considerations](#performance-considerations)
- [Quick Reference](#quick-reference)

## Range Basics

### What is a Range?

A range is any type that provides a common interface to a sequence of values. Ranges generalize arrays, lists, and other sequential access patterns.

### Basic Input Range

```d
struct MyRange {
    int* ptr;
    size_t length;
    size_t index;

    @property bool empty() const {
        return index >= length;
    }

    @property ref int front() {
        return ptr[index];
    }

    void popFront() {
        index++;
    }
}
```

### Using Ranges

```d
import std.stdio;
import std.array;

void main() {
    int[] arr = [1, 2, 3, 4, 5];

    // Arrays are ranges
    while (!arr.empty) {
        writeln(arr.front);
        arr.popFront();
    }
}
```

### foreach and Ranges

```d
int[] arr = [1, 2, 3, 4, 5];

// foreach automatically uses range protocol
foreach (elem; arr) {
    writeln(elem);
}

// Equivalent to:
for (; !arr.empty; arr.popFront()) {
    writeln(arr.front);
}
```

## Range Types

### Range Hierarchy

```
Input Range
  ↓
Forward Range
  ↓
Bidirectional Range
  ↓
Random Access Range
  ↓
Slicing Range
```

### Input Range

```d
// Most basic range: front, popFront, empty
struct InputRange {
    int* ptr;
    size_t index;
    size_t length;

    @property bool empty() const { return index >= length; }
    @property ref int front() { return ptr[index]; }
    void popFront() { index++; }
}

// Can only be traversed once
```

### Forward Range

```d
// Input range + save()
struct ForwardRange {
    int* ptr;
    size_t index;
    size_t length;

    @property bool empty() const { return index >= length; }
    @property ref int front() { return ptr[index]; }
    void popFront() { index++; }

    typeof(this) save() {
        return this;  // Returns a copy
    }
}

// Can be saved and traversed multiple times
```

### Bidirectional Range

```d
// Forward range + back, popBack
struct BidirectionalRange {
    int[] data;
    size_t frontIndex;
    size_t backIndex;

    @property bool empty() const { return frontIndex >= backIndex; }
    @property ref int front() { return data[frontIndex]; }
    void popFront() { frontIndex++; }
    @property ref int back() { return data[backIndex - 1]; }
    void popBack() { backIndex--; }

    typeof(this) save() { return this; }
}
```

### Random Access Range

```d
// Bidirectional range + opIndex
struct RandomAccessRange {
    int[] data;

    @property bool empty() const { return data.length == 0; }
    @property ref int front() { return data[0]; }
    void popFront() { data = data[1 .. $]; }
    @property ref int back() { return data[$-1]; }
    void popBack() { data = data[0 .. $-1]; }
    @property size_t length() const { return data.length; }

    ref int opIndex(size_t i) { return data[i]; }
    void opIndexAssign(int v, size_t i) { data[i] = v; }

    typeof(this) save() { return this; }
}
```

### Range Traits

```d
import std.range.primitives : isInputRange, isForwardRange,
                              isBidirectionalRange, isRandomAccessRange,
                              isOutputRange, hasLength;

static assert(isInputRange!(int[]));
static assert(isForwardRange!(int[]));
static assert(isBidirectionalRange!(int[]));
static assert(isRandomAccessRange!(int[]));

// Combined trait checks
static assert(isInputRange!(int[]) && isForwardRange!(int[]) && hasLength!(int[]));
```

## Output Ranges

### Output Range Interface

```d
// An output range must support: put(range, value)
import std.range.primitives : put;

struct MyOutputRange {
    int[] store;

    void put(int value) {
        store ~= value;
    }
}

void main() {
    auto output = MyOutputRange();
    output.put(42);  // Single value
}
```

### Using Output Ranges

```d
import std.stdio;
import std.range;

// File as output range
auto file = File("output.txt", "w");
file.writeln("Hello, ", "World");  // File implements output range

// array as output range
import std.algorithm : map;
import std.array : array;
auto dest = [1, 2, 3, 4, 5].map!(a => a * 2).array;
```

## Range Interfaces (Runtime Polymorphism)

```d
import std.range;

// Arrays are input ranges
int[] someInputRange = [1, 2, 3];
while (!someInputRange.empty) {
    auto val = someInputRange.front;
    someInputRange.popFront;
}
```

## Range Primitives

### Essential Primitives

```d
import std.range.primitives;

// Check range properties
isInputRange!(Range)
isForwardRange!(Range)
isBidirectionalRange!(Range)
isRandomAccessRange!(Range)
hasLength!(Range)
hasSlicing!(Range)
hasAssignableElements!(Range)
hasMobileElements!(Range)
isOutputRange!(Range, ElementType)  // output range check

// Obtain element type
ElementType!R           // The element type of a range
ElementEncodingType!R   // The character encoding type
```

### Range Operations

```d
import std.range;

void main() {
    auto range = [1, 2, 3];

    // Save a range (forward range)
    auto saved = range.save();

    // Check if empty
    if (!range.empty) { }

    // Get front element
    auto front = range.front;
}
```

### Moving Elements

```d
import std.range.primitives : moveFront, moveBack, moveAt;

void main() {
    auto range = [1, 2, 3, 4, 5];

    // Move elements out (avoids copying)
    auto elem = moveFront(range);
    auto back = moveBack(range);
    auto at = moveAt(range, 3);
}
```

## Range Composition

```d
import std.range : chain;

int[] a = [1, 2, 3];
int[] b = [4, 5, 6];

auto combined = chain(a, b);  // [1, 2, 3, 4, 5, 6]
```

### zip: Pair Elements

```d
import std.range : zip;

int[] a = [1, 2, 3];
string[] b = ["a", "b", "c"];

foreach (x, y; zip(a, b)) {
    writeln(x, y);  // 1a, 2b, 3c
}
```

### enumerate: Index with Range

```d
import std.stdio;
import std.range : enumerate;

void main() {
    string[] arr = ["a", "b", "c"];

    foreach (i, elem; arr.enumerate) {
        writeln(i, ": ", elem);
    }
}
```

### take: Take First N Elements

```d
import std.range : take;

int[] arr = [1, 2, 3, 4, 5];

auto first3 = take(arr, 3);  // [1, 2, 3]
```

### drop: Skip First N Elements

```d
import std.range : drop;

int[] arr = [1, 2, 3, 4, 5];

auto rest = drop(arr, 2);  // [3, 4, 5]
```

### cycle: Repeat Infinitely

```d
import std.range : cycle;

int[] arr = [1, 2, 3];

auto cycled = cycle(arr);  // 1, 2, 3, 1, 2, 3, ...
```

### repeat: Repeat Element

```d
import std.range : repeat;

auto fiveOnes = repeat(1, 5);  // [1, 1, 1, 1, 1]
auto infiniteOnes = repeat(1);  // 1, 1, 1, ...
```

### iota: Number Sequence

```d
import std.range : iota;

iota(5);        // 0, 1, 2, 3, 4
iota(1, 6);     // 1, 2, 3, 4, 5
iota(0, 10, 2); // 0, 2, 4, 6, 8
```

### retro: Reverse Iteration

```d
import std.stdio;
import std.range : retro;

void main() {
    int[] arr = [1, 2, 3, 4, 5];

    foreach (elem; arr.retro) {
        writeln(elem);
    }
}
```

### stride: Skip Elements

```d
import std.range : stride;

int[] arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

foreach (elem; arr.stride(3)) {
    writeln(elem);  // 1, 4, 7, 10
}
```

### slide: Sliding Window

```d
import std.range : slide;

int[] arr = [1, 2, 3, 4, 5];

foreach (window; arr.slide(3)) {
    writeln(window);  // [1,2,3], [2,3,4], [3,4,5]
}
```

### chunks: Split into Chunks

```d
import std.range : chunks;

int[] arr = [1, 2, 3, 4, 5, 6, 7];

foreach (chunk; arr.chunks(3)) {
    writeln(chunk);  // [1,2,3], [4,5,6], [7]
}
```

## std.algorithm

### filter: Select Elements

```d
import std.algorithm : filter;

int[] arr = [1, 2, 3, 4, 5, 6];

auto evens = arr.filter!(a => a % 2 == 0);  // [2, 4, 6]
```

### map: Transform Elements

```d
import std.algorithm : map;

int[] arr = [1, 2, 3, 4, 5];

auto squared = arr.map!(a => a * a);  // [1, 4, 9, 16, 25]
```

### reduce: Accumulate Values

```d
import std.algorithm : reduce;

int[] arr = [1, 2, 3, 4, 5];

auto sum = arr.reduce!((a, b) => a + b);  // 15
auto product = arr.reduce!((a, b) => a * b);  // 120
```

### sort: Sort Range

```d
import std.algorithm : sort;

int[] arr = [5, 3, 1, 4, 2];
arr.sort();  // [1, 2, 3, 4, 5]

// Custom comparator
arr.sort!((a, b) => a > b);  // [5, 4, 3, 2, 1]
```

### find: Search for Element

```d
import std.algorithm : find;

int[] arr = [1, 2, 3, 4, 5];

auto result = arr.find(3);
if (!result.empty) {
    writeln("Found 3");
}
```

### canFind: Check Existence

```d
import std.algorithm : canFind;

int[] arr = [1, 2, 3, 4, 5];

if (arr.canFind(3)) {
    writeln("Contains 3");
}
```

### count: Count Elements

```d
import std.algorithm : count;

int[] arr = [1, 2, 3, 4, 5];

auto c = arr.count!(a => a > 2);  // 3
```

### each: Apply Function to Each

```d
import std.algorithm : each;

int[] arr = [1, 2, 3, 4, 5];

arr.each!writeln;  // Print each element
```

### reverse: Reverse in Place

```d
import std.algorithm : reverse;

int[] arr = [1, 2, 3, 4, 5];
arr.reverse();  // [5, 4, 3, 2, 1]
```

### uniq: Remove Consecutive Duplicates

```d
import std.algorithm : uniq;

int[] arr = [1, 1, 2, 2, 3, 3];
auto unique = arr.uniq;  // [1, 2, 3]
```

### group: Group Consecutive Elements

```d
import std.algorithm : group;

int[] arr = [1, 1, 2, 2, 3, 3];

foreach (count, value; arr.group) {
    writeln(value, ": ", count);
}
```

### chunkBy: Group by Property

```d
import std.algorithm : chunkBy;

int[] arr = [1, 2, 3, 4, 5, 6];

foreach (chunk; arr.chunkBy!((a, b) => (a % 2) == (b % 2))) {
    writeln(chunk);  // [1, 3, 5], [2, 4, 6]
}
```

### splitWhen: Split on Condition

```d
import std.stdio;
import std.algorithm : splitWhen;

int[] arr = [1, 2, 0, 3, 4, 0, 5];

foreach (chunk; arr.splitWhen!((a, b) => b == 0)) {
    writeln(chunk);
}
```

### joiner: Flatten Nested Ranges

```d
import std.algorithm : joiner;

int[][] arr = [[1, 2], [3, 4], [5, 6]];

auto flat = arr.joiner;  // [1, 2, 3, 4, 5, 6]
```

### substitute: Replace Elements

```d
import std.algorithm : substitute;

int[] arr = [1, 2, 3, 4, 5];

auto result = arr.substitute(3, 99);  // [1, 2, 99, 4, 5]
```

### tee: Side Effects in Pipeline (use each)

```d
import std.array;
import std.algorithm.iteration : each, map;

int[] arr = [1, 2, 3, 4, 5];

auto result = arr.map!(a => a * 2).array;
result.each!(a => writeln(a));
```

### Mutation Operations

```d
import std.stdio;
import std.algorithm.mutation;

void main() {
    // bringToFront: rotate elements
    int[] arr = [1, 2, 3, 4, 5];
    bringToFront(arr[0 .. 2], arr[2 .. $]);

    // move: efficient relocation
    int[] src = [1, 2, 3];
    int[] dst = [0, 0, 0];
    moveAll(src, dst);

    // fill: assign value to all elements
    fill(arr, 0);

    // swap: exchange values
    swap(arr[0], arr[4]);
    swapRanges(arr[0 .. 2], arr[3 .. 5]);

    writeln(arr);
}
```

### Sorting

```d
import std.algorithm.sorting;

// Partial sort
int[] arr = [5, 3, 1, 4, 2];
partialSort(arr, 3);     // First 3 elements sorted, rest unsorted

// Top-N selection
topN(arr, 3);            // arr[3] is the 3rd largest (quickselect)

// Merge sorted ranges
int[] a = [1, 3, 5];
int[] b = [2, 4, 6];
auto merged = merge(a, b);  // [1, 2, 3, 4, 5, 6]

// Permutations
int[] perm = [1, 2, 3];
nextPermutation(perm);       // [1, 3, 2]
nextPermutation(perm);       // [2, 1, 3]
bool hasNext = nextPermutation(perm);  // false when exhausted

// Multi-sort
struct Person { string name; int age; }
auto people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 30)];
auto sorted = multiSort!((a, b) => a.name < b.name,
                          (a, b) => a.age < b.age)(people);
```

### Set Operations

```d
import std.algorithm.setops;

int[] a = [1, 2, 3, 4, 5];
int[] b = [4, 5, 6, 7, 8];

auto diff = setDifference(a, b);         // [1, 2, 3]
auto inter = setIntersection(a, b);      // [4, 5]
auto sym = setSymmetricDifference(a, b);  // [1, 2, 3, 6, 7, 8]

// Cartesian product
auto product = cartesianProduct(a, b);  // [(1,4), (1,5), ...]
```

### Comparison

```d
import std.algorithm.comparison;

void main() {
    // Clamp values
    auto clamped = clamp(10, 0, 5);

    // Compare
    auto cmp = cmp([1, 2, 3], [1, 2, 4]);

    // Match
    auto m = mismatch([1, 2, 3], [1, 2, 4]);

    // Distance metrics
    auto lev = levenshteinDistance("kitten", "sitting");
}
```

### Additional std.range Adaptors

```d
import std.range : assumeSorted, generate, lockstep, only, recurrence,
                   takeNone, takeOne, takeExactly, transposed;

// assumeSorted: declare range as sorted (for performance)
int[] arr = [1, 2, 3, 4, 5];
auto sorted = assumeSorted(arr);

// only: create range from individual elements
auto single = only(42);          // Range of one element
auto multi = only(1, 2, 3, 4);   // Range of 4 elements

// recurrence: define a recurrence relation
auto fib = recurrence!("a[n-1] + a[n-2]")(1, 1);  // Fibonacci

// generate: call a function repeatedly
auto randoms = generate!(() => 42);

// lockstep: iterate multiple ranges in parallel (more flexible than zip)
auto r1 = [1, 2, 3];
auto r2 = [4, 5, 6];
auto r3 = [7, 8, 9];
foreach (a, b, c; lockstep(r1, r2, r3)) {
    // ...
}

// transposed: transpose a range of ranges
auto matrix = [[1, 2], [3, 4], [5, 6]];
auto trans = transposed(matrix);  // [[1, 3, 5], [2, 4, 6]]


// Use: takeNone, takeOne, takeExactly
auto none = takeNone(arr);        // Empty range
auto one = takeOne(arr);          // Range of first element only
auto exact = takeExactly(arr, 3); // Exactly 3 elements (no short-circuit)

// tee: copy range operations to another sink
auto logged = arr.tee!(x => writeln("Processing: ", x));
```

## Common Patterns

### Range Pipeline

```d
import std.algorithm : filter, map, reduce;
import std.algorithm.sorting : sort;
import std.array : array;
import std.range : iota;
import std.stdio : writeln;

void main() {
    auto result = iota(1, 101)
        .filter!(a => a % 2 == 0)
        .map!(a => a * a)
        .array
        .sort
        .reduce!((a, b) => a + b);

    writeln(result);
}
```

### Lazy Evaluation

```d
// Ranges are lazy - no computation until consumed
import std.algorithm : map, filter;
import std.range : iota;

auto range = iota(1, 1000000)
    .filter!(a => a % 2 == 0)
    .map!(a => a * a);

// Only first 5 elements are computed
import std.range : take;
foreach (elem; range.take(5)) {
    writeln(elem);
}
```

### Collecting Results

```d
import std.algorithm : map;
import std.array : array;

int[] arr = [1, 2, 3, 4, 5];

auto result = arr.map!(a => a * 2).array;  // [2, 4, 6, 8, 10]
```

### Converting to Array

```d
import std.range : iota;
import std.array : array;

auto arr = iota(1, 11).array;  // [1, 2, ..., 10]
```

### Chaining with save()

```d
import std.algorithm : map, filter;
import std.range : iota;

auto range = iota(1, 101);

// Save allows multiple traversals
auto even = range.save.filter!(a => a % 2 == 0);
auto odd = range.save.filter!(a => a % 2 != 0);
```

## Performance Considerations

### Lazy vs Eager

```d
auto range = [1, 2, 3, 4, 5];
auto pred = (int a) => a > 2;
auto transform = (int a) => a * 2;

// Lazy: computation happens when consumed
auto lazyRange = range.filter!pred.map!transform;

// Eager: computation happens immediately
auto eagerArray = range.filter!pred.map!transform.array;
```

### Avoiding Allocations

```d
auto arr = [3, 1, 4, 1, 5, 9, 2];
auto pred = (int a) => a > 2;
auto transform = (int a) => a * 2;
void process(int a) { writeln(a); }

// Prefer in-place operations
arr.sort();  // Sorts in place

// Avoid intermediate allocations
// Bad: creates multiple temporary arrays
auto result = arr.filter!pred.map!transform.array;

// Good: use each for side effects without allocation
arr.filter!pred.map!transform.each!process;
```

### Known Length

```d
// Ranges with known length are more efficient
auto range = [1, 2, 3];
auto len = range.length;  // Ranges with .length use O(1) ops
```

### Random Access Efficiency

```d
// Random access ranges support efficient indexing
import std.range : take;

auto range = [1, 2, 3, 4, 5];
auto first3 = range.take(3);  // Efficient on random-access ranges
```

## Quick Reference

### Range Primitives

```d
// @property bool empty() const
// @property ref T front()
// void popFront()
// @property ref T back()
// void popBack()
// @property size_t length() const
// ref T opIndex(size_t i)
// void opIndexAssign(T v, size_t i)
// typeof(this) save()
```

### Range Composition

```d
chain(r1, r2, ...)      // Concatenate
zip(r1, r2, ...)        // Pair elements
enumerate(range)         // Index with range
take(range, n)           // First n elements
drop(range, n)           // Skip first n
cycle(range)             // Repeat infinitely
repeat(value, n)         // Repeat element
iota(start, end, step)   // Number sequence
retro(range)             // Reverse iteration
stride(range, step)      // Skip elements
slide(range, window)     // Sliding window
chunks(range, size)      // Split into chunks
```

### std.algorithm (Quick Reference)

```d
filter!(pred)            // Select elements
map!(transform)          // Transform elements
reduce!(op)              // Accumulate values
sort()                   // Sort range
find(value)              // Search for element
canFind(value)           // Check existence
count!(pred)             // Count elements
each!(action)            // Apply function
reverse()                // Reverse in place
uniq()                   // Remove consecutive duplicates
group()                  // Group consecutive elements
chunkBy!(pred)           // Group by property
splitWhen!(pred)         // Split on condition
joiner()                 // Flatten nested ranges
substitute(old, new)     // Replace elements
tee!(action)             // Side effects in pipeline
```

### Range Traits

```d
isInputRange!(Range)
isForwardRange!(Range)
isBidirectionalRange!(Range)
isRandomAccessRange!(Range)
isOutputRange!(Range, Elem)
hasLength!(Range)
hasSlicing!(Range)
hasAssignableElements!(Range)
hasMobileElements!(Range)
```

### Additional std.algorithm

```d
bringToFront   // Rotate elements
moveAll         // Move elements between ranges
fill            // Assign value to all elements
initializeAll   // Call constructors
uninitializedFill // Fill without destructor
strip/Left/Right // Strip elements

partialSort    // Partial sort (first N sorted)
completeSort   // Full sort from partial
topN           // Nth element (quickselect)
topNCopy       // Copy top N elements
merge          // Merge sorted ranges
multiSort      // Multi-key sort
nextPermutation // Permutation iteration

setDifference  // Set difference
setIntersection // Set intersection
setSymmetricDifference // Symmetric difference
cartesianProduct // Cartesian product

clamp          // Clamp value to range
cmp            // Compare two ranges
levenshteinDistance // String edit distance
predSwitch     // Pattern matching switch

assumeSorted   // Declare range as sorted
only           // Range from list of elements
recurrence     // Define recurrence relation
generate       // Generate values from function
lockstep       // Iterate multiple ranges
transposed     // Transpose range of ranges
refRange       // Reference to range
takeNone/One/Exactly // Exact element count
tee            // Side-effect passthrough
```

## Common Idioms

### Filtering and Transforming

```d
import std.algorithm : filter, map;

auto data = [1, -2, 3, -4, 5];
auto result = data
    .filter!(x => x > 0)
    .map!(x => x * 2);
```

### Reducing to Single Value

```d
import std.algorithm : reduce;

auto data = [1, 2, 3, 4, 5];
auto sum = data.reduce!((a, b) => a + b);
auto max = data.reduce!((a, b) => (a > b) ? a : b);
```

### Searching

```d
import std.algorithm : find, canFind;

auto data = [1, 2, 3, 4, 5];
auto target = 3;

if (data.canFind(target)) {
    auto pos = data.find(target);
}
```

### Grouping

```d
import std.algorithm : group, chunkBy;

auto data = [1, 1, 2, 2, 2, 3, 4, 4];

// Group consecutive identical elements
foreach (value, count; data.group) { }

// Group by property
foreach (chunk; data.chunkBy!((a, b) => a % 2 == b % 2)) { }
```

## References

- [Phobos std.range](https://dlang.org/phobos/std_range.html)
- [Phobos std.algorithm](https://dlang.org/phobos/std_algorithm.html)
- [Range Primitives](https://dlang.org/phobos/std_range_primitives.html)
- [DConf 2015: Introduction to Ranges](http://dconf.org/2015/talks/davis.html)
