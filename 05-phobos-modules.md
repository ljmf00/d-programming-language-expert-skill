---
name: d-lang-phobos
description: >-
  D Phobos standard library modules: std. (stdio, algorithm, range, conv,
  json, typecons, socket, getopt, checkedint, sumtype, container, digest,
  bigint, uuid, net.curl, uri, csv, mmfile, traits, meta, random).
  Use when working with standard library APIs.
license: MIT
metadata:
  topics: standard-library phobos io json hashing containers networking
  order: 05
---

# D Programming Language - Phobos Standard Library

Comprehensive guide to D's Phobos standard library modules and their common usage patterns.

## Table of Contents
- [std.stdio](#stdstdio)
- [std.algorithm](#stdalgorithm)
- [std.range](#stdrange)
- [std.array](#stdarray)
- [std.string](#stdstring)
- [std.conv](#stdconv)
- [std.format](#stdformat)
- [std.datetime](#stddatetime)
- [std.numeric](#stdnumeric)
- [std.random](#stdrandom)
- [std.typecons](#stdtypecons)
- [std.exception](#stdexception)
- [std.file](#stdfile)
- [std.path](#stdpath)
- [std.process](#stdprocess)
- [std.net.curl](#stdnetcurl)
- [std.json](#stdjson)
- [std.uri](#stduri)
- [std.uuid](#stduuid)
- [std.digest](#stddigest)
- [std.container](#stdcontainer)
- [std.regex](#stdregex)
- [std.sumtype](#stdsumtype)
- [std.bigint](#stdbigint)
- [std.checkedint](#stdcheckedint)
- [std.bitmanip](#stdbitmanip)
- [std.complex](#stdcomplex)
- [std.csv](#stdcsv)
- [std.encoding](#stdencoding)
- [std.getopt](#stdgetopt)
- [std.logger](#stdlogger)
- [std.math](#stdmath)
- [std.mathspecial](#stdmathspecial)
- [std.mmfile](#stdmmfile)
- [std.outbuffer](#stdoutbuffer)
- [std.socket](#stdsocket)
- [std.uni](#stduni)
- [std.utf](#stdutf)
- [std.variant](#stdvariant)
- [std.zip](#stdzip)
- [std.zlib](#stdzlib)
- [std.net.isemail](#stdnetisemail)
- [Quick Reference](#quick-reference)

## std.stdio

## std.stdio

### Basic I/O
```d
import std.stdio;

void main() {
    // Output
    writeln("Hello, World!");
    write("Hello, ");
    writeln("World!");
    writefln("Formatted: %d", 42);
    
    // Input
    readln();
    
    // Formatted output
    writefln("Name: %s, Age: %d", "Alice", 30);
    writefln("Hex: %x, Octal: %o", 255, 255);
    writefln("Float: %.2f", 3.14159);
}
```

### File Operations
```d
import std.stdio;

void readFile(string path) {
    auto file = File(path, "r");
    foreach (line; file.byLine()) {
        writeln(line);
    }
    file.close();
}

void writeFile(string path, string content) {
    auto file = File(path, "w");
    file.write(content);
    file.close();
}

void appendFile(string path, string content) {
    auto file = File(path, "a");
    file.write(content);
    file.close();
}
```

### stdin/stdout/stderr
```d
import std.stdio;

void main() {
    // Read from stdin
    foreach (line; stdin.byLine()) {
        // Process line
    }
    
    // Write to stdout
    stdout.writeln("To stdout");
    
    // Write to stderr
    stderr.writeln("To stderr");
}
```

## std.algorithm

### Searching
```d
import std.algorithm : find, canFind, countUntil, count;

int[] arr = [1, 2, 3, 4, 5];

// Find element
auto result = arr.find(3);

// Check existence
if (arr.canFind(3)) { }

// Count occurrences
auto n = arr.count!(a => a == 3);

// Count until element
auto pos = arr.countUntil(3);  // 2
```

### Sorting
```d
import std.algorithm : sort, isSorted, isPartitioned;

int[] arr = [5, 3, 1, 4, 2];

// Sort
arr.sort();

// Check if sorted
if (arr.isSorted) { }

// Partition
arr.partition!(a => a > 3);
```

### Iteration
```d
import std.algorithm : map, filter, reduce, each;
import std.range : enumerate;

int[] arr = [1, 2, 3, 4, 5];

// Map
auto squared = arr.map!(a => a * a);

// Filter
auto evens = arr.filter!(a => a % 2 == 0);

// Reduce
auto sum = arr.reduce!((a, b) => a + b);

// Each
arr.each!writeln;

// Enumerate
foreach (i, elem; arr.enumerate) {
    writeln(i, ": ", elem);
}
```

### Mutation
```d
import std.algorithm : reverse, fill, copy;
import std.string : strip;

int[] arr = [1, 2, 3, 4, 5];

// Reverse in place
arr.reverse();

// Strip whitespace
string s = "  hello  ";
auto stripped = s.strip();  // "hello"

// Fill with value
arr.fill(0);  // [0, 0, 0, 0, 0]

// Copy
int[] dest = new int[5];
arr.copy(dest);
```

## std.range

### Range Creation
```d
import std.range : iota, repeat, cycle, generate;

// Number sequence
auto seq = iota(1, 11);  // 1 to 10

// Repeat element
auto ones = repeat(1, 5);  // [1, 1, 1, 1, 1]

// Cycle
auto cycled = cycle([1, 2, 3]);  // 1, 2, 3, 1, 2, 3, ...

// Generate
auto gen = generate!(() => 42);
```

### Range Composition
```d
import std.range : chain, zip, lockstep, take, drop;

int[] a = [1, 2, 3];
int[] b = [4, 5, 6];

// Chain
auto combined = chain(a, b);  // [1, 2, 3, 4, 5, 6]

// Zip
foreach (x, y; zip(a, b)) {
    writeln(x, y);
}

// Lockstep (for foreach)
foreach (x, y; lockstep(a, b)) {
    writeln(x, y);
}

// Take
auto first3 = take(a, 3);

// Drop
auto rest = drop(a, 1);  // [2, 3]
```

### Range Primitives
```d
import std.range.primitives : isInputRange, isForwardRange,
                              isBidirectionalRange, isRandomAccessRange;

static assert(isInputRange!(int[]));
static assert(isRandomAccessRange!(int[]));
```

## std.array

### Array Operations
```d
import std.array : appender, array, assocArray, insertInPlace;

// Appender for efficient concatenation
auto app = appender!(int[]);
app.put([1, 2, 3]);
app.put([4, 5, 6]);
auto result = app.data;  // [1, 2, 3, 4, 5, 6]

// Convert to array
import std.range : iota;
auto arr = iota(1, 11).array;  // [1, 2, ..., 10]

// Associative array
int[string] aa = assocArray(["a", "b", "c"], [1, 2, 3]);
// ["a": 1, "b": 2, "c": 3]
```

### Array Manipulation
```d
import std.array : replace, replicate, split;

// Replace
int[] arr = [1, 2, 3, 4, 5];
auto result = arr.replace([2, 3], [9, 9]);  // [1, 9, 9, 4, 5]

// Replicate
auto replicated = replicate([1, 2], 3);  // [1, 2, 1, 2, 1, 2]

// Split
string s = "a,b,c";
auto parts = s.split(',');  // ["a", "b", "c"]
```

## std.string

### String Operations
```d
import std.conv : to;
import std.string : strip;
import std.array : split, join;

// Strip whitespace
auto stripped = "  hello  ".strip;  // "hello"

// Split
auto parts = "a,b,c".split(',');  // ["a", "b", "c"]

// Join
auto joined = ["a", "b", "c"].join(",");  // "a,b,c"
```

### String Searching
```d
import std.string : indexOf;
import std.algorithm : startsWith, endsWith;

string s = "hello world";

// Starts with
if (s.startsWith("hello")) { }

// Ends with
if (s.endsWith("world")) { }

// Index of
auto pos = s.indexOf("world");  // 6
```

## std.conv

### Type Conversion
```d
import std.conv : to;

// Convert to type
int i = to!int("42");
double d = to!double("3.14");
bool b = to!bool("true");

// Convert from type
string s = to!string(42);
string t = to!string(3.14);
```

### Safe Conversion
```d
import std.conv : to;

// Convert using to! (throws on failure)
auto i = to!int("42");  // 42
auto s = to!string(42); // "42"
```

## std.format

### Formatted Output
```d
import std.stdio : writefln, writef;
import std.format : format;

// writefln with format string
writefln("Name: %s, Age: %d", "Alice", 30);
writefln("Hex: %x, Octal: %o", 255, 255);
writefln("Float: %.2f", 3.14159);
writefln("Pad: %10s", "right");
writefln("Align: %-10s", "left");

// format function
string s = format("Name: %s, Age: %d", "Alice", 30);
```

### Range Formatting
```d
import std.stdio : writefln;

int[] arr = [1, 2, 3, 4, 5];

// Format range
writefln("%(%d %)", arr);  // "1 2 3 4 5 "
writefln("%(%d, %)%", arr);  // "1, 2, 3, 4, 5, "
```

## std.datetime

### Date and Time
```d
import std.datetime : DateTime, Date, TimeOfDay;
import core.time : hours, minutes;

// Current date/time
auto now = DateTime(2024, 1, 15, 10, 30, 0);

// Create specific date/time
auto dt = DateTime(2024, 1, 15, 10, 30, 0);

// Date
auto date = Date(2024, 1, 15);

// Time of day
auto time = TimeOfDay(10, 30, 0);

// Duration (using core.time functions)
auto dur = hours(2) + minutes(30);
```

### Date Arithmetic
```d
import std.datetime : DateTime;
import core.time : days;

auto dt = DateTime(2024, 1, 15);
auto nextWeek = dt + days(7);
```

## std.numeric

### Numeric Algorithms
```d
import std.numeric : gcd, lcm;
import std.range : iota;

// Sequence
auto seq = iota(1, 11);  // 1 to 10

// GCD/LCM
auto g = gcd(12, 8);  // 4
auto l = lcm(12, 8);  // 24
```

### Statistics
```d
import std.algorithm : sum;

double[] data = [1, 2, 3, 4, 5];

auto avg = data.sum / data.length;  // 3.0
```

## std.random

### Random Number Generation
```d
import std.random : uniform;

// Random in range
int r1 = uniform(0, 10);  // 0 to 9

// Random double
double d = uniform(0.0, 1.0);
```

### Random Distributions
```d
import std.random : uniform;

// Uniform distribution
int u = uniform(0, 100);  // 0 to 99
```

## std.typecons

### Type Constructors
```d
import std.typecons : Nullable, Tuple;

// Nullable
Nullable!int n = Nullable!int(42);
if (!n.isNull) {
    writeln(n.get);
}

// Tuple
auto t = tuple(42, "hello", 3.14);
writeln(t[0]);  // 42
writeln(t[1]);  // "hello"
```

### Common Types
```d
import std.typecons : Yes, No, Rebindable;

// Rebindable for const-correctness
auto rb = Rebindable!(const int)(42);
rb = 100;
```

## std.exception

### Exception Handling
```d
import std.exception : enforce, assumeUnique;

int val = 42;

// Enforce condition
enforce(val > 0, "Error message");

// Assume unique (for ownership transfer)
auto arr = [1, 2, 3];
auto ptr = assumeUnique(arr);
```

### Custom Exceptions
```d
class MyException : Exception {
    this(string msg, string file = __FILE__, uint line = __LINE__) {
        super(msg, file, line);
    }
}

throw new MyException("Something went wrong");
```

## std.file

### File Operations
```d
import std.file : exists, remove, copy;

// Check if file exists
if (exists("file.txt")) { }

// Copy file
copy("source.txt", "dest.txt");

// Move file
move("source.txt", "dest.txt");

// Remove file
remove("file.txt");
```

### Directory Operations
```d
import std.file : dirEntries, mkdir, rmdir, SpanMode;

// List directory
foreach (entry; dirEntries(".", SpanMode.shallow)) {
    writeln(entry.name);
}

// Create directory
mkdir("newdir");

// Remove directory
rmdir("dir");
```

## std.path

### Path Manipulation
```d
import std.path : dirName, baseName, extension;

// Directory name
string dir = dirName("/path/to/file.txt");  // "/path/to"

// Base name
string base = baseName("/path/to/file.txt");  // "file"

// Extension
string ext = extension("/path/to/file.txt");  // ".txt"
```

## std.process

### Process Execution
```d
import std.process : execute;

// Execute command
auto result = execute(["ls", "-l"]);
writeln(result.output);
writeln(result.status);
```

## std.net.curl

### HTTP Requests
```d
import std.net.curl : get;
```

## std.json

### JSON Parsing
```d
import std.json : parseJSON, JSONValue;

// Parse JSON string
string json = `{"name": "Alice", "age": 30}`;
auto value = parseJSON(json);

// Access fields
auto obj = value.object;
string name = obj["name"].str;
long age = obj["age"].integer;
```

## std.uri

### URI Manipulation
```d
import std.uri : encode, decode;

// Encode/decode
string encoded = encode("hello world");  // "hello%20world"
string decoded = decode("hello%20world");  // "hello world"
```

## std.uuid

### UUID Generation
```d
import std.uuid : UUID, randomUUID;
import std.random : rndGen;

// Generate UUID
auto uuid = randomUUID(rndGen);
writeln(uuid.toString);

// Parse UUID
auto uuid2 = UUID("550e8400-e29b-41d4-a716-446655440000");
```

## std.digest

### Hashing
```d
import std.digest.sha : SHA256, sha256Of;
import std.digest.md : MD5, md5Of;

// SHA256
auto hash = sha256Of("Hello, World!");

// MD5
auto md5hash = md5Of("Hello, World!");
```

## std.container

### Data Structures
```d
import std.container : Array, RedBlackTree;
import std.stdio;

// Dynamic array
auto arr = Array!int(1, 2, 3);

// Red-black tree (sorted set)
auto tree = new RedBlackTree!int();
tree.insert(3);
tree.insert(1);
tree.insert(2);
foreach (i; tree) write(i, " ");
writeln();
```

## std.regex

### Regular Expressions
```d
import std.regex : regex, ctRegex, match;

// Compile regex
auto r = regex(r"\d+");

// Match
string text = "abc123def";
auto m = match(text, r);
if (m.hit) {
    writeln(m.hit);  // "123"
}
```

## std.sumtype

### Tagged Union / Sum Type
```d
import std.sumtype : SumType, tryMatch;

// Create a sum type
alias Value = SumType!(int, double, string);

auto value = Value(42);

// tryMatch with guard
if (auto matched = value.tryMatch!int) {
    writeln("Got an int: ", matched);
}
```

## std.bigint

### Arbitrary-Precision Integers
```d
import std.bigint : BigInt;

// Create BigInt from various sources
auto a = BigInt("123456789012345678901234567890");
auto b = BigInt(42);
auto c = BigInt("0xdeadbeef");

// Arithmetic
auto sum = a + b;
auto diff = a - b;
auto prod = a * b;
auto quot = a / b;
auto rem = a % b;

// Comparison
if (a > b) { }

// Conversions
string s = a.to!string;
long l = a.toLong;  // Truncates if too large
```

## std.checkedint

### Overflow-Checked Integer Types
```d
import std.checkedint : Checked;

// Checked integer with overflow detection
auto a = Checked!int(int.max);
auto b = Checked!int(1);

try {
    auto c = a + b;  // Throws on overflow
} catch (Exception e) {
    writeln("Overflow detected!");
}
```

## std.bitmanip

### Bit Manipulation
```d
import std.bitmanip : BitArray, append;

// BitArray: compact array of bits
BitArray bits;
bits.length = 10;
bits[0] = true;
bits[1] = false;
```
```

## std.complex

### Complex Numbers
```d
import std.complex : Complex, complex;
import std.math : sqrt;

// Create complex numbers
auto c1 = complex(1.0, 2.0);  // 1 + 2i
auto c2 = complex(0.0, 1.0);  // i

// Arithmetic
auto sum = c1 + c2;
auto diff = c1 - c2;
auto prod = c1 * c2;
auto quot = c1 / c2;

// Properties
writeln(c1.re);     // Real part: 1.0
writeln(c1.im);     // Imaginary part: 2.0
auto mag = sqrt(c1.re * c1.re + c1.im * c1.im);  // Magnitude: sqrt(5)
```

## std.csv

### CSV File Processing
```d
import std.csv : csvReader;

// Read CSV from a string
struct Person {
    string name;
    int age;
    string city;
}

string data = "Alice,30,NYC\nBob,25,LA";
auto reader = csvReader!(Person)(data);

foreach (person; reader) {
    writeln(person.name, ", ", person.age);
}
```

## std.encoding

### Character Encoding
```d
// D strings are UTF-8 by default
string s = "Hello";
writeln(s.length);  // number of code units
```

## std.getopt

### Command-Line Argument Parsing
```d
import std.getopt;
import std.stdio;

void main(string[] args) {
    string cfg = "default.conf";
    int port = 8080;
    bool verbose;
    
    getopt(args,
        "cfg", &cfg,
        "port", &port,
        "verbose", &verbose,
    );
    
    writeln("Config: ", cfg);
    writeln("Port: ", port);
}
```

## std.logger

### Logging Framework
```d
import std.logger;

// Global logger
log("Application started");
```

## std.math

### Mathematical Functions
```d
import std.math;

// Trigonometry
double x = sin(PI / 2);  // 1.0

// Exponential and logarithmic
double p = pow(2, 10);          // 1024.0

// Rounding
double c = ceil(3.14);          // 4.0
double f = floor(3.14);         // 3.0
double r = round(3.14);         // 3.0
double a = 3.14, b = 2.0;
double t = trunc(3.14);         // 3.0

// Comparison
double m = fmax(a, b);          // Maximum of a and b
double n = fmin(a, b);          // Minimum
double ab = fabs(a);            // Absolute value
bool eq = approxEqual(a, b);    // Approximate equality with tolerance

// Constants
double pi = PI;

// Floating-point properties
bool nan = isNaN(x);
bool inf = isInfinity(x);
int sign = signbit(x);
```

## std.mathspecial

### Special Mathematical Functions
```d
import std.mathspecial;

double x = 2.5, y = 1.5;

// Gamma functions
double g = gamma(x);             // Gamma function
double lg = logGamma(x);         // Log gamma function
double b = beta(x, y);           // Beta function

// Error function
double e = erf(x);               // Error function
double ec = erfc(x);             // Complementary error function
```

## std.mmfile

### Memory-Mapped Files
```d
import std.mmfile : MmFile;
```

## std.outbuffer

### Binary Data Serialization
```d
import std.outbuffer : OutBuffer;

// Write binary data
auto buf = new OutBuffer();
buf.write(42);              // int
buf.write(3.14);            // double
```

## std.socket

### Network Sockets
```d
import std.socket;
import std.stdio;

// TCP client
void connect() {
    auto socket = new TcpSocket();
    socket.connect(new InternetAddress("example.com", 80));
    socket.send("GET / HTTP/1.0\r\n\r\n");
    
    auto buf = new char[4096];
    auto received = socket.receive(buf);
    writeln(buf[0 .. received]);
    
    socket.close();
}

// TCP server
void serve() {
    auto server = new TcpSocket();
    server.bind(new InternetAddress(InternetAddress.ADDR_ANY, 8080));
    server.listen(10);
    
    auto client = server.accept();
    // Handle client
}
```

## std.uni

### Unicode Algorithms
```d
import std.uni : graphemeStride, byGrapheme,
                 isAlpha, isWhite;

// Grapheme-aware operations
string s = "Hello";
auto stride = graphemeStride(s, 0);  // Size of first grapheme
foreach (grapheme; s.byGrapheme) {
    writeln(grapheme);
}

// Unicode categories
if (isAlpha('A')) { }           // Alphabetic character
if (isWhite(' ')) { }           // Whitespace
auto lower = "HELLO".toLower;   // "hello"
```

## std.utf

### UTF Encoding/Decoding
```d
import std.utf : encode, decode, validate;

// Encode/decode UTF codepoints
dchar cp = '\u00E9';  // Unicode é
char[4] encoded;
auto len = encode(encoded, cp);  // Encode to UTF-8

// Validate UTF-8 string
string s = "Hello";
validate(s);  // throws on invalid
writeln("Valid UTF-8");
```

## std.variant

### Dynamic Typing / Variant
```d
import std.variant : Variant, Algebraic;

// Variant: can hold any type
Variant v;
v = 42;
v = "hello";
v = [1, 2, 3];

// Type checking
int i = v.get!int;  // Throws if wrong type
if (v.type == typeid(int)) { }

// Algebraic: type-safe union
alias MyAlgebraic = Algebraic!(int, double, string);
auto a = MyAlgebraic(42);
```

## std.zip

### Zip Archive Handling
```d
import std.zip : ZipArchive;
```

## std.zlib

### Compression/Decompression
```d
import std.zlib;
import std.stdio;

// Compress data
auto data = "Hello, World!";
auto compressed = compress(cast(ubyte[]) data);

// Decompress
auto decompressed = uncompress(compressed);
writeln("Decompressed: ", cast(string) decompressed);
```

## std.net.isemail

### Email Validation
```d
import std.net.isemail : isEmail;

// Validate email addresses
auto result = isEmail("user@example.com");
writeln("Email valid: ", result);
```

## Quick Reference

### std.stdio
```d
writeln()        // Output with newline
write()          // Output without newline
writefln()       // Formatted output with newline
readln()         // Read line
File(path, mode) // File handle
```

### std.algorithm
```d
filter!(pred)    // Select elements
map!(transform)  // Transform elements
reduce!(op)      // Accumulate values
sort()           // Sort range
find(value)      // Search for element
canFind(value)   // Check existence
each!(action)    // Apply function
reverse()        // Reverse in place
```

### std.range
```d
iota(start, end)     // Number sequence
repeat(value, n)     // Repeat element
chain(r1, r2)        // Concatenate
zip(r1, r2)          // Pair elements
take(range, n)       // First n elements
drop(range, n)       // Skip first n
```

### std.conv
```d
to!T("string")       // Convert to type
toString(value)      // Convert from type
```

### std.format
```d
writefln(fmt, args)  // Formatted output
format(fmt, args)    // Format string
```

### std.datetime
```d
DateTime.now         // Current date/time
DateTime(y, m, d)    // Create date/time
Duration.days(n)     // Duration
```

### std.random
```d
uniform(a, b)        // Random in range
shuffle(arr)         // Shuffle array
```

## Common Idioms

### Reading File Line by Line
```d
import std.stdio;

foreach (line; File("file.txt").byLine()) {
    // Process line
}
```

### Processing with Ranges
```d
import std.algorithm : filter, map, reduce;
import std.range : iota;

auto result = iota(1, 101)
    .filter!(a => a % 2 == 0)
    .map!(a => a * a)
    .reduce!((a, b) => a + b);
```

### Safe Type Conversion
```d
import std.conv : to;

auto value = to!int("42");
```

### JSON Parsing
```d
import std.json : parseJSON;

auto value = parseJSON(`{"name": "Alice"}`);
auto obj = value.object;
auto name = obj["name"].str;
```

## References
- [Phobos Documentation](https://dlang.org/phobos/)
- [std.algorithm](https://dlang.org/phobos/std_algorithm.html)
- [std.range](https://dlang.org/phobos/std_range.html)
- [std.string](https://dlang.org/phobos/std_string.html)
- [std.conv](https://dlang.org/phobos/std_conv.html)
- [std.format](https://dlang.org/phobos/std_format.html)
- [std.datetime](https://dlang.org/phobos/std_datetime.html)
- [std.file](https://dlang.org/phobos/std_file.html)
