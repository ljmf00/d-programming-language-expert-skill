---
name: d-lang-performance
description: >-
  D performance optimization: core.simd types, LDC optimization
  attributes and flags, profile-guided optimization, cache-friendly
  data layout (SoA vs AoS), memory alignment, loop optimizations,
  @inline/@noinline. Use when optimizing D code for speed.
license: MIT
metadata:
  topics: performance optimization simd ldc cache-friendly pgo alignment
  order: 11
---

# D Programming Language - Performance Optimization

Comprehensive guide to D performance optimization: SIMD vector types, compiler pragmas, data layout patterns, memory alignment, loop transformations, and LDC-specific optimization techniques.

## Table of Contents

- [core.simd Types](#coresimd-types)
- [@inline / @noinline Pragmas](#inline--noinline-pragmas)
- [Cache-Friendly Data Layout](#cache-friendly-data-layout)
- [Memory Alignment](#memory-alignment)
- [Loop Optimization Patterns](#loop-optimization-patterns)
- [Const and Immutable for Optimization](#const-and-immutable-for-optimization)
- [Allocation Strategies](#allocation-strategies)
- [Bounds Check Elimination](#bounds-check-elimination)
- [LDC Optimization Flags](#ldc-optimization-flags)
- [Profile-Guided Optimization (PGO)](#profile-guided-optimization-pgo)
- [Link-Time Optimization (LTO)](#link-time-optimization-lto)
- [Quick Reference](#quick-reference)

## core.simd Types

D provides built-in SIMD vector types through `core.simd` for explicit vectorization. These map directly to hardware SIMD registers (SSE/AVX on x86, NEON on ARM) and support element-wise arithmetic operations.

### float4 Vector Operations

```d
import core.simd;

void float4Demo() {
    float4 a = [1.0f, 2.0f, 3.0f, 4.0f];
    float4 b = [5.0f, 6.0f, 7.0f, 8.0f];
    float4 c = a + b;  // [6, 8, 10, 12] - element-wise
    float4 d = a * b;  // [5, 12, 21, 32]
}
```

### int4 and short8 Vectors

```d
import core.simd;

void intSimdDemo() {
    int4 ia = [10, 20, 30, 40];
    int4 ib = [1, 2, 3, 4];
    int4 ic = ia + ib;        // [11, 22, 33, 44]
    short8 sa = cast(short8) [1, 2, 3, 4, 5, 6, 7, 8];
    short8 sb = cast(short8) [8, 7, 6, 5, 4, 3, 2, 1];
    short8 sc = sa + sb;
}
```

### double2 Vector Operations

```d
import core.simd;

void double2Demo() {
    double2 da = [1.5, 2.5];
    double2 db = [3.5, 4.5];
    double2 dc = da * db;    // [5.25, 11.25]
    double2 dd = dc + da;    // [6.75, 13.75]
}
```

### Vector Load and Store

```d
import core.simd;

void vectorLoadStore() {
    float[4] src = [1.0f, 2.0f, 3.0f, 4.0f];
    float4 v = *cast(float4*)&src;     // Load via pointer cast
    float factor = 2.0f;
    float4 scaled = v * factor;        // Broadcast scalar multiply
    float[4] dst = scaled.array;       // Store to array
}
```

### Vector Reduction Helpers

```d
import core.simd;
import std.stdio;

float horizontalSum(float4 v) {
    return v[0] + v[1] + v[2] + v[3];
}

void reductionDemo() {
    float4 vals = [1.0f, 2.0f, 3.0f, 4.0f];
    float total = horizontalSum(vals);
    writeln(total);  // 10.0
}
```

## @inline / @noinline Pragmas

D offers fine-grained control over function inlining via `pragma(inline, bool)`. LDC also supports `@llvmAttr` for backend-specific hints.

### Force Inline

```d
pragma(inline, true) int square(int x) {
    return x * x;
}

void inlineTest() {
    int result = square(5);  // Always inlined, no call overhead
}
```

### Prevent Inlining

```d
pragma(inline, false) int debugTrace(int val) {
    return val + 1;  // Never inlined (useful for breakpoints)
}

void noinlineTest() {
    int x = debugTrace(42);
}
```

### Selective Inlining with Templates

```d
import std.traits : isScalarType;

pragma(inline, isScalarType!T) T identity(T)(T val) {
    return val;
}

void templateInlineTest() {
    int a = identity(10);   // Inlined (scalar)
    // struct S {} auto b = identity(S());  // Not inlined
}
```

### LDC Cold Attribute

```d
import ldc.attributes : llvmAttr;

@llvmAttr("cold") void errorRecovery() {
    // Rarely-called path kept out of hot code
}

void coldPathTest() {
    errorRecovery();
}
```

## Cache-Friendly Data Layout

Data layout dramatically affects cache performance. The choice between AoS (Array of Structs) and SoA (Struct of Arrays) depends on access patterns.

### Array of Structs (AoS)

```d
struct AosParticle {
    float x, y, z;        // All fields together in memory
    float vx, vy, vz;
}

void aosDemo() {
    auto ps = [AosParticle(1,2,3,0,0,0), AosParticle(4,5,6,0,0,0)];
    foreach (ref p; ps) { p.x += p.vx; p.y += p.vy; p.z += p.vz; }
}
```

### Struct of Arrays (SoA)

```d
struct SoaParticles {
    float[] xs, ys, zs;   // Each field stored contiguously
    float[] vxs, vys, vzs;
}

void soaDemo(SoaParticles p, size_t idx) {
    p.xs[idx] += p.vxs[idx];  // Cache-friendly for bulk updates
    p.ys[idx] += p.vys[idx];
    p.zs[idx] += p.vzs[idx];
}
```

### Cache Line Padding

```d
struct PaddedCounter {
    align(64) size_t count;  // Occupies own cache line
}

void counterDemo() {
    PaddedCounter[4] counters;  // Each on separate cache line
    counters[0].count = 1;      // No false sharing
    counters[1].count = 2;
}
```

### Hot/Cold Field Splitting

```d
struct Entity {
    int id;
    float x, y;            // Frequently accessed (hot)
    // Cold: large, rarely used data
    byte[256] metadata;    // Placed last to avoid polluting cache
}

void entityDemo() {
    auto ents = [Entity(1, 0.0f, 0.0f), Entity(2, 5.0f, 5.0f)];
}
```

## Memory Alignment

Explicit alignment ensures data starts at memory boundaries that match cache line and SIMD register requirements.

### Struct Alignment

```d
struct AlignedBuffer {
    align(16) float x, y, z, w;  // SSE register size alignment
}

void alignDemo() {
    auto buf = AlignedBuffer(1.0f, 2.0f, 3.0f, 4.0f);
}
```

### Class Alignment

```d
align(64) class CacheAlignedClass {
    int payload;
    long timestamp;
    this(int p, long t) { payload = p; timestamp = t; }
}

void classAlignDemo() {
    auto obj = new CacheAlignedClass(5, 100);
}
```

### Aligned Stack Variables

```d
void stackAlignDemo() {
    align(16) int[4] vec = [1, 2, 3, 4];  // Stack vector aligned to 16 bytes
}
```

### Aligned Heap Allocation

```d
import core.memory : GC;
import std.stdio;

void alignedHeapDemo() {
    void* raw = GC.calloc(1024, cast(uint) GC.BlkAttr.NONE);
    // For non-GC aligned alloc use core.stdc.stdlib.aligned_alloc
    writeln(raw !is null);
}
```

## Loop Optimization Patterns

Small transformations to loops can yield significant speedups by improving cache locality, reducing branch mispredictions, and enabling auto-vectorization.

### Sum Reduction Loop

```d
float sumArray(const float[] arr) {
    float result = 0.0f;
    foreach (val; arr) { result += val; }
    return result;
}

void reductionLoopDemo() {
    float[] data = [1.0f, 2.0f, 3.0f, 4.0f, 5.0f];
    float t = sumArray(data);
}
```

### Loop Fusion

```d
void loopFusion(const float[] a, const float[] b, float[] dest) {
    foreach (i; 0 .. a.length) {
        dest[i] = a[i] + b[i];        // Single pass: add + scale
        dest[i] *= 2.0f;
    }
}

void fusionDemo() {
    float[] x = [1.0f, 2.0f, 3.0f];
    float[] y = [4.0f, 5.0f, 6.0f];
    float[] z = new float[3];
    loopFusion(x, y, z);
}
```

### Hoisting Invariant Computations

```d
import std.math : sqrt;

void hoistDemo(float[] arr) {
    float threshold = sqrt(2.0f);         // Invariant: computed once
    foreach (ref val; arr) {
        if (val > threshold) val = threshold;  // Loop body is lean
    }
}
```

### Strength Reduction

```d
void strengthReduction(const int[] arr, int[] outArr) {
    foreach (i; 0 .. arr.length) {
        outArr[i] = (arr[i] << 3) + (arr[i] << 1);  // x*8 + x*2 = x*10
    }
}

void strengthDemo() {
    int[] src = [1, 2, 3, 4];
    int[] dst = new int[4];
    strengthReduction(src, dst);
}
```

### Unroll Hint via Static Foreach

```d
float unrolledSum(float a, float b, float c, float d) {
    float acc = 0.0f;
    foreach (x; [a, b, c, d]) { acc += x; }
    return acc;
}

void unrollDemo() {
    float t = unrolledSum(1.0f, 2.0f, 3.0f, 4.0f);
}
```

### Auto-Vectorization Friendly Loop

```d
void vecFriendlyLoop(float[] a, const float[] b, const float[] c) {
    foreach (i; 0 .. a.length) {
        a[i] = b[i] * c[i] + b[i];  // Simple pattern LDC can auto-vectorize
    }
}

void vecDemo() {
    float[] x = new float[8];
    float[] y = [1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f];
    float[] z = [8.0f, 7.0f, 6.0f, 5.0f, 4.0f, 3.0f, 2.0f, 1.0f];
    vecFriendlyLoop(x, y, z);
}
```

## Const and Immutable for Optimization

Marking data as `const` or `immutable` enables the compiler to perform alias analysis and more aggressive optimizations, since it guarantees data won't change.

### Const Parameters Enable Aliasing Analysis

```d
int sumConstRange(const int[] arr) {
    int total = 0;
    foreach (val; arr) total += val;  // Compiler knows arr won't change
    return total;
}

void constParamDemo() {
    int result = sumConstRange([1, 2, 3, 4, 5]);
}
```

### Immutable Data in Hot Paths

```d
immutable float[4] lut = [0.0f, 0.25f, 0.5f, 0.75f];  // Read-only lookup

float lookupImmutable(size_t idx) {
    return lut[idx];  // Compiler can inline/constant-fold
}

void immutDemo() {
    float val = lookupImmutable(2);
}
```

### Const Locals Help CSE

```d
import std.math : sin;

void constLocalDemo(float[] outArr) {
    const float coeff = sin(1.0f);  // Common subexpression
    foreach (i; 0 .. outArr.length) {
        outArr[i] = coeff * cast(float) i;
    }
}
```

## Allocation Strategies

Smart allocation reduces GC pressure and improves data locality.

### Pre-Allocated Stack Arrays

```d
void stackAllocDemo() {
    float[256] buffer;           // Stack allocation, no GC
    foreach (i; 0 .. 256) { buffer[i] = cast(float) i * 0.5f; }
}
```

### Pre-size Dynamic Arrays

```d
void preSizeDemo() {
    int[] arr;
    arr.reserve(1024);           // Single allocation, avoid reallocs
    foreach (i; 0 .. 1024) { arr ~= cast(int) i; }
}
```

### Reuse Buffers

```d
void reuseBuffer(float[] buffer, size_t n) {
    buffer.length = n;            // No alloc if capacity >= n
    foreach (i; 0 .. n) { buffer[i] = 0.0f; }
}

void reuseDemo() {
    auto buf = new float[512];    // Allocate once
    reuseBuffer(buf, 256);        // Reuse, no new allocation
    reuseBuffer(buf, 128);
}
```

### Stack Class via scope

```d
class TempCalc {
    int value;
    this(int v) { value = v; }
    int compute() { return value * value; }
}

void scopeClassDemo() {
    scope tc = new TempCalc(5);   // Allocates on stack (LDC with -d-scope)
    int result = tc.compute();
}
```

## Bounds Check Elimination

D arrays are bounds-checked by default. Several techniques eliminate checks in hot loops while preserving safety elsewhere.

### Pointer Arithmetic Bypasses Bounds Checks

```d
void ptrLoopDemo(const float[] src, float[] dst) {
    auto s = src.ptr;
    auto d = dst.ptr;
    foreach (i; 0 .. src.length) {
        d[i] = s[i] * 2.0f;        // LDC often elides checks when .ptr used
    }
}
```

### Compile-Time Assert for Safe Offsets

```d
void knownSize(const float[64] arr) {
    float sum = 0.0f;
    foreach (i; 0 .. 64) {
        sum += arr[i];             // Static bounds: checks elided
    }
}

void knownSizeDemo() {
    float[64] data = 0.0f;
    knownSize(data);
}
```

### Pointer Indexing to Skip Bounds Checks

Indexing through the raw `.ptr` (a pointer, not the slice) is not bounds-checked,
so the loop below skips per-element checks regardless of `-boundscheck`. It is
therefore `@trusted` — you are asserting `i` stays in range. (To drop bounds
checks globally instead, compile with `-boundscheck=off`.)

```d
void unsafeButFast(float[] arr) @trusted {
    auto p = arr.ptr;
    foreach (i; 0 .. arr.length) {
        p[i] += 1.0f;  // no bounds check — indexing a pointer, not the slice
    }
}

void fastLoopDemo() {
    auto data = new float[100];
    unsafeButFast(data);
}
```

## LDC Optimization Flags

LDC provides extensive optimization flags for production builds. These are not D code — they are command-line arguments passed to the compiler.

### Basic Optimization Levels

```
-O0          No optimization (fast compile, slow code)
-O1          Basic optimizations
-O2          Standard optimizations (good balance)
-O3          Aggressive optimizations (auto-vectorization, loop unrolling)
-Os          Optimize for size
-Oz          Aggressively optimize for size
```

### Floating Point Optimization

```
--ffast-math        Enable aggressive FP optimizations (may break IEEE compliance)
--fno-fast-math     Disable fast-math (IEEE 754 compliant, default)
--fsingle-precision-constant  Treat FP literals as float, not double
```

### Target-Specific Optimizations

```
-mcpu=native        Target current CPU (enables all ISA extensions)
-mcpu=core2         Target specific microarchitecture
-mattr=+sse4.2      Enable specific ISA features
-mattr=-avx2        Disable specific ISA features
```

### Recommended Release Flags

```
ldc2 -O3 -release -boundscheck=off -mcpu=native -flto=thin source.d
```

### Diagnostics and Analysis

```
--print-before-llvm-optimization  Print IR before optimization passes
--print-after-llvm-optimization   Print IR after optimization passes
-fsave-optimization-record        Save optimization remarks to YAML
-foptimization-record-file=FILE   Specify output file for remarks
-Rremarks                          Emit optimization remarks to stderr
```

## Profile-Guided Optimization (PGO)

PGO is a two-phase compilation process that uses runtime profiling data to guide optimizations. It improves branch prediction, inlining decisions, and code layout.

### Instrumented Build (Phase 1)

```
# Compile with instrumentation
ldc2 -fprofile-instr-generate -O2 source.d -o=program-instr

# Run with representative workload to generate profile data
./program-instr
# This produces default.profraw (or use LLVM_PROFILE_FILE to name it)
```

### Merge Profile Data

```
# Convert raw profile to processed format
ldc-profdata merge -output=program.profdata default.profraw
```

### Optimized Build (Phase 2)

```
# Compile using the collected profile data
ldc2 -fprofile-instr-use=program.profdata -O3 -release source.d -o=program-opt
```

### PGO with Multiple Runs

```
# Collect multiple profiles
LLVM_PROFILE_FILE="run1.profraw" ./program-instr workload1
LLVM_PROFILE_FILE="run2.profraw" ./program-instr workload2

# Merge all profiles
ldc-profdata merge -output=program.profdata run1.profraw run2.profraw

# Build optimized binary
ldc2 -fprofile-instr-use=program.profdata -O3 source.d -o=program-opt
```

### Environment Variables for PGO

```
LLVM_PROFILE_FILE="%p_%m.profraw"   # %p=pid, %m=sig for multi-process
```

## Link-Time Optimization (LTO)

LTO enables cross-module optimizations by deferring code generation to link time. LDC supports both full and thin LTO.

### Thin LTO (Recommended)

```
# Compile to LLVM bitcode, link with thin LTO
ldc2 -flto=thin -O2 -c module_a.d
ldc2 -flto=thin -O2 -c module_b.d
ldc2 -flto=thin -O2 module_a.o module_b.o -o=program
```

### Full LTO

```
# Full LTO merges all IR into a single module (higher memory, more optimization)
ldc2 -flto=full -O3 -release source.d -o=program
```

### LTO with PGO

```
# Combine PGO and LTO for maximum optimization
ldc2 -flto=thin -fprofile-instr-use=program.profdata -O3 source.d -o=program
```

### Checking LTO Effectiveness

```
# List symbols to verify cross-module inlining occurred
nm program | grep -c ' T '   # Count defined text symbols

# Check binary size impact
ls -lh program
```

## Quick Reference

```
# LDC Release Build
ldc2 -O3 -release -boundscheck=off -mcpu=native -flto=thin source.d

# PGO Instrumented
ldc2 -fprofile-instr-generate -O2 source.d -o=prog-instr && ./prog-instr

# PGO Optimized
ldc-profdata merge -output=code.profdata default.profraw
ldc2 -fprofile-instr-use=code.profdata -O3 source.d -o=prog

# SIMD Types
float4, double2, int4, short8, byte16

# Inline Control
pragma(inline, true)           # Force inline
pragma(inline, false)          # Prevent inline
@llvmAttr("cold")              # Cold function hint

# Alignment
align(16), align(64)           # Struct/field alignment

# Cache-Friendly
SoA over AoS for bulk processing
Cache-line padding for shared counters
Hot fields first, cold fields last
```
