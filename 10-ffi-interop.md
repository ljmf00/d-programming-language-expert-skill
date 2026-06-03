---
name: d-lang-ffi-interop
description: >-
  D FFI and cross-language interop: extern(C/C++/ObjC) linkage, COM,
  pragma (lib, mangle, inline, msg), C header import via core.stdc.*, 
  Better C mode, calling conventions. Use when calling C/C++/ObjC
  libraries from D or exposing D to other languages.
license: MIT
metadata:
  topics: ffi interop extern-C extern-C++ better-c pragma importc
  order: 10
---

# D FFI & Cross-Language Interop

Comprehensive guide to D's foreign function interface capabilities: calling C/C++/Objective-C libraries, exposing D to other languages, pragma directives, and Better C compilation mode.

## Table of Contents

- [extern(C) — C Language Linkage](#externc--c-language-linkage)
- [extern(C++) — C++ Language Linkage](#externc---c-language-linkage)
- [extern(Objective-C) — Objective-C Interop](#externobjective-c--objective-c-interop)
- [COM Interface Patterns](#com-interface-patterns)
- [pragma(lib) — Library Linking](#pragmalib---library-linking)
- [pragma(mangle) — Custom Symbol Mangling](#pragmamangle---custom-symbol-mangling)
- [pragma(inline) — Inline Hints](#pragmainline---inline-hints)
- [pragma(msg) — Compile-Time Messages](#pragma-msg---compile-time-messages)
- [pragma(startaddress) — Entry Point](#pragmastartaddress---entry-point)
- [C Standard Library via core.stdc.*](#c-standard-library-via-corestdc)
- [POSIX via core.sys.*](#posix-via-coresys)
- [Linux-Specific via core.sys.linux.*](#linux-specific-via-coresyslinux)
- [Better C Mode](#better-c-mode)
- [Calling Conventions](#calling-conventions)
- [Function Pointer Interop](#function-pointer-interop)
- [C Struct Compatibility](#c-struct-compatibility)
- [Quick Reference](#quick-reference)

## extern(C) — C Language Linkage

The `extern(C)` attribute tells the D compiler to use C ABI and C symbol mangling for declarations.

### Declaring C Functions

```d
extern(C) {
    int cPrintf(const(char)* format, ...);
    void* cMalloc(ulong size);
    void cFree(void* ptr);
}
```

### Defining C-Callable Functions

```d
extern(C) int dAdd(int a, int b) {
    return a + b;
}

extern(C) const(char)* dGreeting() {
    return "Hello from D";
}
```

### extern(C) Block Scope

```d
extern(C) {
    int cFuncOne(int x) { return x * 2; }
    int cFuncTwo(int y) { return y + 1; }
}

void main() {
    import std.stdio : writeln;
    writeln(cFuncOne(21));  // 42
    writeln(cFuncTwo(41));  // 42
}
```

### C Function Pointers

```d
extern(C) {
    alias CCallback = int function(int, int);
}

extern(C) int cCompute(int a, int b) {
    return a * b;
}

void main() {
    import std.stdio : writeln;
    CCallback ptr = &cCompute;
    writeln(ptr(6, 7));  // 42
}
```

### C-ABI Struct Layout

```d
extern(C) struct CPoint {
    int xCoord;
    int yCoord;
}

void main() {
    import std.stdio : writeln;
    auto point = CPoint(100, 200);
    writeln(point.xCoord, ", ", point.yCoord);
    static assert(point.xCoord.offsetof == 0);
    static assert(point.yCoord.offsetof == 4);
}
```

### Packed C Structs

```d
extern(C) {
    align(1) struct CFlags {
        byte flagA;
        ushort flagB;
        byte flagC;
    }
}

void main() {
    import std.stdio : writeln;
    // align(1) packs struct: no padding between fields
    auto flags = CFlags(1, 2, 3);
    writeln(flags.flagA, ", ", flags.flagB, ", ", flags.flagC);
}
```

### extern(C) Enum

```d
extern(C) enum CColor {
    redClr = 0,
    greenClr = 1,
    blueClr = 2
}

void main() {
    import std.stdio : writeln;
    CColor clr = CColor.greenClr;
    writeln(cast(int) clr);  // 1
}
```

## extern(C++) — C++ Language Linkage

The `extern(C++)` attribute uses C++ name mangling, enabling direct calls to C++ functions. LDC provides full C++ interop support.

### extern(C++) Function Declarations

```d
extern(C++) {
    void cppFunction(int x);
    double cppCompute(double a, double b);
}
```

### extern(C++) Block

```d
extern(C++) {
    int cppAdd(int a, int b) { return a + b; }
    int cppSub(int c, int d) { return c - d; }
}

void main() {
    import std.stdio : writeln;
    writeln(cppAdd(20, 22));  // 42
    writeln(cppSub(50, 8));   // 42
}
```

### extern(C++, class) — C++ Class Interface

```d
extern(C++, class) class CppString {
    this();
    this(const(char)* data);
    ~this();
    size_t length();
    const(char)* cStr();
}
```

### extern(C++) with Structs

```d
extern(C++) struct CppVector2 {
    double xVec;
    double yVec;

    double magnitudeSq() {
        return xVec * xVec + yVec * yVec;
    }
}

void main() {
    import std.stdio : writeln;
    import std.math : sqrt;
    auto vec = CppVector2(3.0, 4.0);
    writeln(sqrt(vec.magnitudeSq()));  // 5.0
}
```

## extern(Objective-C) — Objective-C Interop

Available on macOS/iOS. Declares Objective-C classes and protocols for use from D.

### Objective-C Class Declaration

```d
version(OSX) {
    extern(Objective-C) class ObjCNSString {
        ObjCNSString alloc();
        ObjCNSString init();
        ObjCNSString initWithUTF8String(const(char)* str);
        const(char)* UTF8String();
        size_t objcLength();
    }
}
```

### Objective-C Protocol

```d
version(OSX) {
    extern(Objective-C) class ObjcObject {}  // id is ObjC's universal object type
    alias id = ObjcObject;
    extern(Objective-C) interface ObjCNSCopying {
        id copyWithZone(id zone);
    }
}
```

### Objective-C Selector

```d
version(OSX) {
    extern(Objective-C) class ObjcObject {}  // id is ObjC's universal object type
    alias id = ObjcObject;
    extern(Objective-C) class ObjCNSObject {
        ObjCNSObject performSelector(id aSelector);
        id description();
    }
}
```

## COM Interface Patterns

D can interface with COM on Windows using `extern(Windows)` and COM-specific attributes.

### COM Guid Struct

```d
struct ComGuid {
    uint comData1;
    ushort comData2;
    ushort comData3;
    byte[8] comData4;
}
```

### COM IUnknown Base Interface

```d
struct ComGuid2 {
    uint comD1;
    ushort comD2;
    ushort comD3;
    byte[8] comD4;
}

extern(Windows) interface IUnknown {
    int queryInterface(ref ComGuid2 iid, void** objPtr);
    ulong addRef();
    ulong release();
}
```

### COM IDispatch Interface

```d
struct ComGuid3 {
    uint comD1;
    ushort comD2;
    ushort comD3;
    byte[8] comD4;
}

extern(Windows) interface IUnknown2 {
    int queryInterface(ref ComGuid3 iid, void** objPtr);
    ulong addRef();
    ulong release();
}

extern(Windows) interface IDispatch : IUnknown2 {
    int getTypeInfoCount(uint* count);
    int getTypeInfo(uint index, uint localeId, void** info);
    int getIDsOfNames(
        void* iid,
        wchar** names,
        uint count,
        uint localeId,
        int* dispIds
    );
}
```

### COM Simple Interface

```d
struct ComGuid4 {
    uint comD1;
    ushort comD2;
    ushort comD3;
    byte[8] comD4;
}

extern(Windows) interface IUnknown3 {
    int queryInterface(ref ComGuid4 iid, void** objPtr);
    ulong addRef();
    ulong release();
}

extern(Windows) interface ISimpleCom : IUnknown3 {
    int getValue(int* result);
    void setValue(int value);
}
```

## pragma(lib) — Library Linking

Automatically adds library links without specifying `-L-l` flags.

### Link System Library

```d
pragma(lib, "m");  // Link with libm on Unix
```

### Multiple Libraries

```d
pragma(lib, "ssl");
pragma(lib, "crypto");
```

### Platform-Specific Linking

```d
version (Windows) {
    pragma(lib, "ws2_32");
    pragma(lib, "advapi32");
} else version (Posix) {
    pragma(lib, "pthread");
}
```

### pragma(lib) with Conditional

```d
debug {
    pragma(lib, "gtest");
}
```

## pragma(mangle) — Custom Symbol Mangling

Override the default symbol name emitted in the object file.

### Override C++ Mangling

```d
pragma(mangle, "_Z13myCppMethodi") int myCppMethod(int x) {
    return x * 2;
}
```

### Custom C Name

```d
pragma(mangle, "my_c_entry_point") void dEntryPoint() {
    import std.stdio : writeln;
    writeln("Entry point called");
}
```

### Underscore-Prefixed Name

```d
pragma(mangle, "_legacy_func") int legacyFunction(int a, int b) {
    return a + b;
}
```

## pragma(inline) — Inline Hints

Control compiler inlining behavior.

### Force Inline

```d
pragma(inline, true) int fastAdd(int x, int y) {
    return x + y;
}
```

### Prevent Inline

```d
pragma(inline, false) int noInline(int a, int b) {
    return a * b + a;
}
```

### Inline with Templates

```d
pragma(inline, true) T templateMax(T)(T a, T b) {
    return a > b ? a : b;
}
```

### Inline in Struct

```d
struct FastMath {
    pragma(inline, true) int square(int x) {
        return x * x;
    }
}

void main() {
    import std.stdio : writeln;
    FastMath math;
    writeln(math.square(7));  // 49
}
```

## pragma(msg) — Compile-Time Messages

Print messages during compilation for debugging templates and conditional compilation.

### Basic Compile-Time Print

```d
pragma(msg, "Module: ", __MODULE__);
pragma(msg, "File: ", __FILE__);
```

### Template Debugging

```d
template TypePrinter(T) {
    enum TypePrinter = T.stringof;
    static {
        pragma(msg, "Instantiated with: ", T.stringof);
    }
}

void main() {
    import std.stdio : writeln;
    writeln(TypePrinter!int);  // "int"
}
```

### Conditional Compilation Messages

```d
version (Windows)
    pragma(msg, "Building for Windows");
else version (Posix)
    pragma(msg, "Building for POSIX");
```

### Version Check Message

```d
pragma(msg, "D version: ", __VERSION__);
```

## pragma(startaddress) — Entry Point

Specify the program entry point (useful for freestanding/Better C builds).

### Custom Entry Point

```d
extern(C) void myStart() {
    import core.stdc.stdio : printf;
    printf("Custom entry\n");
}

pragma(startaddress, myStart);
```

## C Standard Library via core.stdc.*

D provides bindings to the C standard library through `core.stdc.*` modules.

### stdio Bindings

```d
import core.stdc.stdio : printf, fprintf, scanf;

void main() {
    printf("Hello from core.stdc.stdio\\n");
}
```

### stdlib Bindings

```d
import core.stdc.stdlib : malloc, free, atoi, atol;

void main() {
    import std.stdio : writeln;
    auto ptr = malloc(64);
    free(ptr);
    writeln(atoi("42"));    // 42
    writeln(atol("100"));   // 100
}
```

### string Bindings

```d
import core.stdc.string : strlen, strcpy, strcmp, strcat;

void main() {
    import std.stdio : writeln;
    char[20] buf = "Hello\0".dup;
    writeln(strlen(buf.ptr));  // 5
    writeln(strcmp("abc", "abc"));  // 0
}
```

### stdint Bindings

```d
import core.stdc.stdint : int32_t, uint64_t, intptr_t;

void main() {
    import std.stdio : writeln;
    int32_t val32 = 42;
    uint64_t val64 = 9007199254740992;
    writeln(val32, ", ", val64);
}
```

### math Bindings

```d
import core.stdc.math : sin, cos, sqrt, fabs, floor, ceil;

void main() {
    import std.stdio : writeln;
    writeln(sin(0.0));    // 0
    writeln(cos(0.0));    // 1
    writeln(sqrt(16.0));  // 4
    writeln(fabs(-42.5)); // 42.5
}
```

### stdio FILE Operations

```d
import core.stdc.stdio : fopen, fclose, fgets, fputs, FILE;

void main() {
    import std.stdio : writeln;
    auto fp = fopen("/tmp/dlang_test.txt", "w");
    if (fp) {
        fputs("test line\n", fp);
        fclose(fp);
    }
    writeln("File operation done");
}
```

### stddef Bindings

```d
import core.stdc.stdlib : malloc, free;
import std.stdio;

void cMemoryExample() {
    auto p = malloc(64);
    if (p !is null) {
        writeln("Allocated memory");
        free(p);
    }
}
```

## POSIX via core.sys.*

D provides POSIX system call bindings through `core.sys.posix.*`.

### POSIX unistd

```d
import core.sys.posix.unistd : write, read, close, getpid;

void main() {
    import std.stdio : writeln;
    writeln("PID: ", getpid());
}
```

### POSIX fcntl

```d
import core.sys.posix.fcntl : O_RDONLY, O_WRONLY, O_CREAT;
import std.conv : octal;

void main() {
    import std.stdio : writeln;
    import core.sys.posix.fcntl : open;
    import core.sys.posix.unistd : close;
    auto fd = open("/tmp/dlang_test2.txt", O_WRONLY | O_CREAT, octal!"644");
    if (fd >= 0) {
        close(fd);
    }
    writeln("File opened and closed");
}
```

### POSIX errno via core.stdc

```d
import core.stdc.errno : errno;

void main() {
    import std.stdio : writeln;
    int savedErrno = errno;
    writeln("errno: ", savedErrno);
}
```

### POSIX signal

```d
import core.sys.posix.signal : sigaction, SIG_DFL, SIG_IGN;

void main() {
    import std.stdio : writeln;
    writeln("Signal module available");
}
```

### POSIX time

```d
import core.sys.posix.time : time, clock_t, clock;

void main() {
    import std.stdio : writeln;
    auto t = time(null);
    writeln("Time: ", t);
}
```

## Linux-Specific via core.sys.linux.*

### Linux sys/stat via POSIX

```d
import core.sys.posix.sys.stat : stat, fstat;

void main() {
    import std.stdio : writeln;
    writeln("POSIX stat available");
}
```

### Linux sys/socket

```d
import core.sys.linux.sys.socket : socket, bind, listen, accept;

void main() {
    import std.stdio : writeln;
    writeln("Socket functions available");
}
```

### Linux sched

```d
import core.sys.linux.sched : sched_getcpu;

void main() {
    import std.stdio : writeln;
    writeln("sched_getcpu: ", sched_getcpu());
}
```

## Better C Mode

Better C (`-betterC`) compiles D without the runtime: no GC, no exceptions, no RTTI, no typeinfo.

### Basic Better C Program

```d
extern(C) void main() {
    import core.stdc.stdio : printf;
    printf("Better C Hello\\n");
}
```

### Better C Memory Management

```d
extern(C) void main() {
    import core.stdc.stdio : printf;
    import core.stdc.stdlib : malloc, free;

    auto mem = cast(int*) malloc(10 * 4);
    if (mem) {
        mem[0] = 42;
        printf("Value: %d\\n", mem[0]);
        free(mem);
    }
}
```

### Better C with Structs

```d
extern(C) struct BcPoint {
    int bcX;
    int bcY;
}

extern(C) void main() {
    import core.stdc.stdio : printf;
    auto pt = BcPoint(10, 20);
    printf("Point: %d, %d\\n", pt.bcX, pt.bcY);
}
```

### Better C Array Operations

```d
extern(C) void main() {
    import core.stdc.stdio : printf;

    int[5] arr;
    foreach (i, ref elem; arr) {
        elem = cast(int)(i * 10);
    }
    for (size_t idx = 0; idx < arr.length; idx++) {
        printf("%d ", arr[idx]);
    }
    printf("\\n");
}
```

### Better C Templates

```d
T bcMax(T)(T a, T b) {
    return a > b ? a : b;
}

extern(C) void main() {
    import core.stdc.stdio : printf;
    auto mx = bcMax(10, 20);
    printf("Max: %d\\n", mx);
}
```

### Better C with CTFE

```d
enum bcPi = 3.14159265;
enum bcE = 2.71828182;

extern(C) void main() {
    import core.stdc.stdio : printf;
    printf("PI: %f, E: %f\\n", bcPi, bcE);
}
```

## Calling Conventions

D supports multiple calling conventions for FFI compatibility.

### Default D Convention

```d
int dConvention(int a, int b) {
    return a + b;
}
```

### C Calling Convention

```d
extern(C) int cConvention(int x, int y) {
    return x * y;
}
```

### Windows stdcall Convention

```d
extern(Windows) int windowsConvention(int a, int b) {
    return a - b;
}
```

### System Convention

```d
extern(System) int systemConvention(int p, int q) {
    return p + q;
}
```

### Pascal Convention

```d
// Valid linkage identifiers in D:
extern(D) int dFunc();       // D default
extern(C) int cFunc();       // C convention    
extern(Windows) int winFunc(); // Windows stdcall
extern(System) int sysFunc(); // System default
extern(C++) int cppFunc();   // C++ mangling
```

## Function Pointer Interop

### C-Compatible Function Pointer

```d
extern(C) {
    alias CMathFn = int function(int, int);
}

extern(C) int cMultiply(int a, int b) {
    return a * b;
}

void main() {
    import std.stdio : writeln;
    CMathFn fn = &cMultiply;
    writeln(fn(7, 6));  // 42
}
```

### Function Pointer with Context

```d
extern(C) {
    alias CContextFn = int function(void* ctx, int val);
}

extern(C) int contextFunc(void* ctx, int val) {
    return val + 1;
}

void main() {
    import std.stdio : writeln;
    CContextFn fn = &contextFunc;
    writeln(fn(null, 41));  // 42
}
```

### Callback Pattern

```d
extern(C) {
    alias COnComplete = void function(int result);
    void registerCallback(COnComplete callback);
}

extern(C) void onComplete(int result) {
    import std.stdio : writeln;
    writeln("Result: ", result);
}

void main() {
    import std.stdio : writeln;
    writeln("Callback: ", &onComplete);
}
```

## C Struct Compatibility

### extern(C) Struct Alignment

```d
extern(C) struct CData {
    byte cByte;
    int cInt;
    double cDouble;
}

void main() {
    import std.stdio : writeln;
    writeln("Size: ", CData.sizeof);
    writeln("byte offset: ", CData.cByte.offsetof);
    writeln("int offset: ", CData.cInt.offsetof);
    writeln("double offset: ", CData.cDouble.offsetof);
}
```

### Packed Struct for C Interop

```d
extern(C) {
    align(1) struct CPacked {
        byte pByte;
        int pInt;
        short pShort;
    }
}

void main() {
    import std.stdio : writeln;
    // Note: align(1) inside extern(C) may not pack as expected
    auto data = CPacked(1, 2, 3);
    writeln(data.pByte, ", ", data.pInt, ", ", data.pShort);
}
```

### C Union Compatibility

```d
extern(C) union CValue {
    int uInt;
    double uDouble;
    char[8] uChars;
}

void main() {
    import std.stdio : writeln;
    auto val = CValue();
    val.uInt = 42;
    writeln(val.uInt);  // 42
    writeln("Size: ", CValue.sizeof);  // 8 (max of members)
}
```

### extern(C) typedef Alias

```d
extern(C) {
    alias CHandle = void*;
    alias CSize = ulong;
    alias CStatus = int;
}

extern(C) CStatus cInit(CHandle handle) {
    return 0;
}

void main() {
    import std.stdio : writeln;
    CHandle h = null;
    auto status = cInit(h);
    writeln("Status: ", status);
}
```

## Quick Reference

### Linkage Attributes
```d
extern(C)        // C ABI and name mangling
extern(C++)      // C++ name mangling
extern(C++, class) // C++ class interop
extern(Objective-C) // Objective-C interop
extern(Windows)  // Windows stdcall convention
extern(System)   // System default convention
extern(Pascal)   // Pascal calling convention
```

### pragma Summary
```d
// pragma(inline, true) applies to the next function declaration
pragma(inline, true)
int forcedInline(int x) { return x * 2; }

pragma(inline, false)
int noInline(int x) { return x * 3; }

pragma(msg, "Compiling optimization helpers");

void testInline() {
    auto a = forcedInline(5);
    auto b = noInline(5);
}
```

### core.stdc.* Modules
```d
import core.stdc.stdlib : malloc, free, atoi, rand;
import std.string : toStringz;
import std.stdio;

void cStdUsage() {
    auto val = rand() % 100;
    writeln("Random: ", val);
}
```

### core.sys.* Modules
```d
import core.sys.posix.fcntl : open, O_RDONLY, O_CREAT;
// import core.sys.posix.unistd : close, read, write;

// POSIX file operations are available via core.sys.posix.*
// Example: auto fd = open("file.txt", O_RDONLY);
```

### Better C Checklist
```d
// Compile: ldc2 -betterC program.d
// Entry: extern(C) void main()
// No GC, no exceptions, no RTTI, no typeinfo
// Use: malloc/free, core.stdc.*, core.sys.*
// Use: __gshared for global variables
```

## References

- [D Spec: Linking](https://dlang.org/spec/module.html#linking)
- [D Spec: Pragma](https://dlang.org/spec/pragma.html)
- [D Spec: Calling Conventions](https://dlang.org/spec/function.html#calling-conventions)
- [Better C on D Wiki](https://dlang.org/spec/betterc.html)
- [LDC C++ Interop](https://ldc.dlang.org/docs/user-docs.html#d-and-c-interoperability)
- [core.stdc Reference](https://dlang.org/phobos/core/stdc.html)
- [core.sys Reference](https://dlang.org/phobos/core.sys.html)
