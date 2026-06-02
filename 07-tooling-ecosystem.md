---
name: d-lang-tooling
description: >-
  D tooling and ecosystem: DMD reference compiler, LDC LLVM-based compiler,
  GDC GCC-based compiler, dub package manager and build system, DDoc
  documentation generator, libdparse code analysis library, DustMite
  test-case reducer, IDE support, debugging with GDB/LLDB, profiling.
  Use when setting up builds or debugging D projects.
license: MIT
metadata:
  topics: compilers dub ddoc build-system debugging profiling
  order: 07
---

# D Programming Language - Tooling & Ecosystem

Comprehensive guide to D's compilers, package manager, build system, development tools, and ecosystem.

## Table of Contents
- [DMD - Reference Compiler](#dmd---reference-compiler)
- [LDC - LLVM-Based Compiler](#ldc---llvm-based-compiler)
- [GDC - GCC-Based Compiler](#gdc---gcc-based-compiler)
- [DUB - Package Manager](#dub---package-manager)
- [Build Configuration](#build-configuration)
- [DDoc - Documentation Generator](#ddoc---documentation-generator)
- [Development Tools](#development-tools)
- [Build System & DUB Ecosystem](#build-system--dub-ecosystem)
- [Testing and Debugging](#testing-and-debugging)
- [IDE and Editor Support](#ide-and-editor-support)
- [Quick Reference](#quick-reference)

## DMD - Reference Compiler

### Overview
DMD (Digital Mars D) is the reference compiler for D. It's implemented in D itself and provides fast compilation times.

### Basic Usage
```bash
# Compile a single file
dmd main.d

# Compile with output name
dmd -of=myprogram main.d

# Compile multiple files
dmd main.d helper.d utils.d

# Compile with debug symbols
dmd -g main.d

# Compile with optimization
dmd -O main.d

# Compile with all warnings
dmd -w main.d
```

### Common Flags
```bash
# Compilation
-c              # Compile only, no link
-of=<name>      # Output file name
-od=<dir>       # Output directory
-I=<path>       # Include path
-J=<path>       # String import path

# Optimization
-O              # Enable optimizations
-inline         # Enable function inlining
-O2             # More aggressive optimizations
-O3             # Maximum optimizations (experimental)

# Debugging
-g              # Generate debug symbols
-gs             # Generate debug info for source
-v              # Verbose compilation
-vtls           # Show thread-local storage info

# Warnings
-w              # Enable warnings
-wi             # Enable informational warnings
-de            # Enable deprecation warnings

# Safety
-check         # Enable contracts and asserts
-check=on      # Enable runtime checks
-check=off     # Disable runtime checks

# Special
-run           # Compile and run
-dry-run       # Show what would be compiled
-cov           # Enable code coverage
-unittest      # Enable unit tests
```

### DMD Environment
```bash
# Set DMD home directory
export DMD_HOME=/path/to/dmd

# Library search path
export DFLAGS="-L-L/path/to/libs"

# Configuration file
# ~/.dmdrc or /etc/dmdrc
```

### DMD Subcommands
```bash
dmd -run main.d        # Compile and run immediately
dmd -unittest main.d   # Compile with unit tests enabled
dmd -debug main.d      # Enable debug mode
dmd -version=MyVersion # Set version identifier
dmd -check main.d      # Enable runtime checks
dmd -cov main.d        # Enable code coverage
dmd -profile main.d    # Enable profiling
dmd -vgc main.d        # Show GC allocations
```

#### Better C Mode
```bash
# Compile in Better C mode (no D runtime needed)
dmd -betterC main.d
ldc2 -betterC main.d

# Better C creates smaller, standalone binaries
# without GC, exceptions, or TypeInfo

# Set entry point as extern(C)
dmd -betterC -extern-std=c++ main.d
```

### Code Coverage
```bash
# Enable code coverage
dmd -cov main.d
./main
# Produces main.lst with coverage data

# With DUB
dub build --build=coverage
./myapp
# Results in *.lst files showing coverage

# View coverage
# Lines executed: 85% of 200 lines
```

### Profiling
```bash
# Profile with DMD
dmd -profile main.d
./myapp
# Produces trace.log with execution counts

# Profile with LDC
ldc2 -profile main.d
./myapp
# More detailed profiling with LLVM infrastructure
```

## Integration with Other Languages
```bash
# Link with C libraries
dmd main.d -L-lm      # Link with math library
dmd main.d -L-lz      # Link with zlib

# Link with C++ libraries
dmd main.d -L-lstdc++ -L-lboost

# Mixed C/D compilation
dmd main.d clib.o     # Link with C object files
```

## LDC - LLVM-Based Compiler

### Overview
LDC is a D compiler based on LLVM. It provides better optimization and targeting of multiple architectures.

### Basic Usage
```bash
# Compile a single file
ldc2 main.d

# Compile with optimization
ldc2 -O2 main.d

# Compile with LLVM-specific flags
ldc2 -O3 -mcpu=native main.d  # Optimize for current CPU

# Cross-compilation
ldc2 -mtriple=aarch64-linux-gnu main.d

# Generate LLVM IR
ldc2 -output-ll main.d

# Generate assembly
ldc2 -output-s main.d
```

### LDC Performance Flags
```bash
# Optimization levels
-O0  # No optimization (fast compile)
-O1  # Light optimization
-O2  # Standard optimization
-O3  # Heavy optimization
-O5  # Max optimization (may increase code size)

# Architecture-specific
-mcpu=native        # Optimize for current CPU
-mattr=+sse2        # Enable specific CPU features

# Code generation
-enable-inlining    # Enable inlining
-flto=full         # Full link-time optimization
-flto=thin         # Thin link-time optimization

# Debug info
-g                 # Generate debug symbols
-gline-tables-only  # Minimal debug info
```

### LDC vs DMD Features
```d
// DMD-specific features
version(D_Version2) { }

// LDC-specific features
version(LDC) { }

// Check compiler
static if (__traits(compiles, __VERSION__)) {
    // This is DMD
} else {
    // This is LDC or GDC
}
```

### LDC Configuration
```bash
# LDC configuration file
# /etc/ldc2.conf or ~/.ldc2.conf

# Example ldc2.conf
{
    "switches": [
        "-O2",
        "-mcpu=native",
        "-flto=full"
    ],
    "libDirs": ["/path/to/libs"],
    "rpath": "/path/to/libs"
}
```

## GDC - GCC-Based Compiler

### Overview
GDC uses the GCC backend for D compilation. It provides good performance and integration with GCC tools.

### Basic Usage
```bash
# Compile
gdc main.d

# With optimization
gdc -O2 main.d

# With GCC-specific features
gdc -fversion=MyVersion main.d
```

## DUB - Package Manager

### Overview
DUB is the official package manager and build system for D. It handles dependencies, builds, and package management.

### Basic Commands
```bash
# Initialize a new project
dub init myproject
dub init myproject --type=minimal

# Build project
dub build
dub build --config=release
dub build --build=debug
dub build --compiler=ldc2

# Run project
dub run
dub run -- --args "for program"

# Run with compiler flags
dub run --compiler=ldc2 -b=release

# Add dependency
dub add dependency_name

# Update dependencies
dub upgrade
dub upgrade --dry-run  # Show what would be updated

# Generate documentation
dub describe

# Get help
dub help
dub help build

# List available commands
dub --help
```

### Project initialization
```bash
# Interactive
dub init

# Quick init
dub init myproject --type=library
dub init myproject --type=executable
dub init myproject --type=minimal

# With template
dub init myproject --format=sdl  # Simple Declarative Language
dub init myproject --format=json # JSON format
```

### Dependency Management
```bash
# Search for packages
dub search term

# Add dependency
dub add vibe-d
dub add "vibe-d@>=0.9.0"

# Remove dependency
dub remove vibe-d

# List dependencies
dub list

# Show outdated packages
dub outdated
```

### Build Cache
```bash
# Clear build cache
dub clean

# Clear all caches
dub clean-all

# Build with cache disabled
dub build --force
```

## Build Configuration

### dub.json Format
```json
{
    "name": "myproject",
    "description": "My D project",
    "authors": ["Author Name"],
    "license": "BSL-1.0",
    "targetType": "executable",
    "sourcePaths": ["source"],
    "importPaths": ["source", "views"],
    "stringImportPaths": ["views"],
    "dependencies": {
        "vibe-d": "~>0.9.0",
        "arsd-official:http2": "~>2.0"
    },
    "buildTypes": {
        "debug": {
            "buildOptions": ["debugMode", "debugInfo"]
        },
        "release": {
            "buildOptions": ["releaseMode", "optimize"],
            "lflags": ["-O2"]
        }
    },
    "configurations": [
        {
            "name": "library",
            "targetType": "library"
        },
        {
            "name": "executable",
            "targetType": "executable",
            "mainSourceFile": "source/app.d"
        }
    ],
    "dflags-ldc": ["-mcpu=native"],
    "lflags": ["-L-lm"],
    "libs": ["m"]
}
```

### dub.sdl Format
```sdl
name "myproject"
description "My D project"
authors "Author Name"
license "BSL-1.0"
targetType "executable"
sourcePaths "source"
importPaths "source" "views"
stringImportPaths "views"

dependency "vibe-d" version="~>0.9.0"
dependency "arsd-official:http2" version="~>2.0"

buildType "debug"
    buildOptions "debugMode" "debugInfo"

buildType "release"
    buildOptions "releaseMode" "optimize"
```

### Build Options
```json
// Common build options
"buildOptions": [
    "debugMode",           // Add debug code
    "debugInfo",           // Generate debug info
    "releaseMode",         // Release mode
    "optimize",            // Enable optimizations
    "syntaxOnly",          // Syntax check only
    "warnings",            // Enable warnings
    "warningsAsErrors",    // Treat warnings as errors
    "coverage",            // Code coverage
    "profile",             // Profiling
    "unittests",           // Enable unit tests
    "noAssert",           // Disable assertions
    "noBoundsCheck",       // Disable bounds checking
    "noSetSignals",        // Don't set signal handlers
    "noStrip",             // Don't strip symbols
    "strip",               // Strip symbols
    "verbose",             // Verbose output
    "docDir",              // Documentation directory
    "noDoc",               // Don't generate docs
    "noLibrary",           // Don't create library
    "usePIC",              // Position-independent code
    "enableDynamic"        // Dynamic libraries
]
```

### Compilation with DUB
```bash
# Build specific configuration
dub build --config=library
dub build --config=executable

# Build for specific platform
dub build --arch=x86_64
dub build --arch=x86

# Build with specific compiler
dub build --compiler=dmd
dub build --compiler=ldc2
dub build --compiler=gdc

# Build with custom flags
dub build --override-config=vibe-d:core     # Example
dub build --with-debug-info=codeview
dub build --combined
```

## DDoc - Documentation Generator

### DDoc Comments
```d
/**
 * Brief description of the function.
 *
 * Detailed description that can span multiple lines.
 *
 * Parameters:
 *   param1 = Description of first parameter
 *   param2 = Description of second parameter
 *
 * Returns:
 *   Description of return value
 *
 * Throws:
 *   ExceptionType = When the exception is thrown
 *
 * Examples:
 * ---
 * auto result = myFunction(42);
 * assert(result == 100);
 * ---
 */
int myFunction(int param1, string param2) { }

// Inline doc
/// Brief documentation
int myFunction2() { }

// Section-level docs
// $(SECTION Name, Content)  // DDoc macro, not D code
```

### Using DDoc
```bash
# Generate documentation
dub build --build=docs

# Manual generation with DMD
dmd -D main.d

# With custom path
dmd -Dd=docs/ main.d

# With DUB
dub build --build=docs
```

### DDoc Macros
```d
// Common macros
$(D ...)          // D code inline
$(I ...)          // Italic
$(B ...)          // Bold
$(LINK2 url, text) // Link
$(REF name, module) // Reference to module
$(DDOC_COMMENT ...) // Comment
$(SECTION Name, Content) // Section
$(SUBREF module, name) // Submodule reference
```

## Development Tools

### Code Formatting (dfmt)
```bash
# Format a file
dfmt --in-place source.d

# Format directory
dfmt --in-place source/

# Check formatting
dfmt source.d

# With custom config
dfmt --in-place --config=dfmt.json source.d
```

### Create dfmt Configuration
```json
{
    "braceStyle": "allman",
    "softMaxLineLength": 80,
    "indentSize": 4,
    "selectiveImportSpace": true,
    "spaceAfterCast": true,
    "spaceAfterKeyword": true,
    "spaceBeforeParentheses": false,
    "tabs": false,
    "alignParallelAssignments": true,
    "alignSections": true,
    "operatorsBlockStartAtLineEnd": true,
    "importWrap": false,
    "maxLineLength": 120
}
```

### Linting (D-Scanner)
```bash
# Run linter
dscanner --styleCheck source.d

# Check all files
dscanner --styleCheck source/

# With DUB
dub run dscanner -- --styleCheck source/

# Report all issues
dscanner --report source.d
```

### DCD (Code Completion)
```bash
# Start DCD server
dcd-server

# Get completions at a specific position
dcd-client -c 10 path/to/file.d

# Get symbol information
dcd-client -s SymbolName

# Shutdown DCD server
dcd-client --shutdown
```

### dfix (Automatic Fixes)
```bash
# Fix common issues
dfix source.d

# Apply fixes in directory
dfix source/

# Dry-run (show what would be changed)
dfix --dry-run source.d

# With custom config
dfix --config=dfix.json source.d
```

### rdmd (Script Runner)
```bash
# Run D script directly (shebang compatible)
rdmd my_script.d

# Pass arguments
rdmd my_script.d -- --args "for program"

# As shebang (put on first line of .d file):
#!/usr/bin/env rdmd

# With dependencies
rdmd --force my_script.d
rdmd --build-only my_script.d
```

### htod (C/C++ Header to D)
```bash
# Convert C header to D
htod header.h > header.d

# Convert with custom options
htod -o header.d header.h

# Output D import file
htod -i header.h
```

### ddemangle (Symbol Demangling)
```bash
# Demangle D symbols
ddemangle _D3std5stdio7__T5writelnTAhZ

# Pipe from compiler output
dmd -c file.d 2>&1 | ddemangle
```

### DDox (API Documentation Generator)
```bash
# Generate API docs with DDox
dub build --build=ddox

# Manual invocation
dub run ddox -- --project-name=myproject --project-version=1.0.0

# Generate with custom config
dub run ddox -- --file-ignore=*.private.d
```

### libdparse (D Source Parsing)
```d
import libdparse;
import std.stdio;

// Parse D source code
auto source = readText("myfile.d");
auto lexer = Lexer(source);

// Iterate tokens
foreach (token; lexer) {
    writeln(token.text);
}

// Parse modules
auto caches = StringCache();
auto parsed = parseModule(caches, source);
```

### unit-threaded (Testing Framework)
```bash
# Install via DUB
dub add unit-threaded

# Run tests
dub run unit-threaded -- -f myproject

# Run with specific test file
dub run unit-threaded -- -f source/myapp.d

# Generate test report
dub run unit-threaded -- -f source/ --report
```

### undeaD (Dead Code Removal)
```bash
# Find dead code
undeaD myproject/

# With DUB project
undeaD -- dub
```

### DustMite (Test Case Reducer)
```bash
# Minimize test case
./dustmite source.d "dmd -c source.d 2>&1"

# With test script
./dustmite testDir/ "bash test.sh"
```

## Build System & DUB Ecosystem

D's build system and package ecosystem provide comprehensive tooling for project management, continuous integration, and dependency handling.

### Build System & CI

DUB (D's Unified Build system) serves as both build tool and package manager. It supports multiple target types, pre/post build commands, cross-compilation, and integrates with CI systems.

```json
{
    "name": "myapp",
    "description": "A D application",
    "authors": ["You"],
    "license": "MIT",
    "targetType": "executable",
    "dependencies": {
        "vibe-d": "~>0.9"
    }
}
```

```d
// Build types in DUB
import std.stdio;
void testDUBBuildTypes() {
    // DUB supports: executable, sourceLibrary, staticLibrary, dynamicLibrary
    // Configure in dub.json: "targetType": "executable"
    writeln("DUB build types: executable, sourceLibrary, staticLibrary, dynamicLibrary");
}
```

```json
"preBuildCommands": ["python3 generate_code.d"],
"postBuildCommands": ["cp myapp dist/"]
```

```d
// Cross-compilation with DUB
import std.stdio;
void testDUBCrossCompile() {
    // dub build --arch=x86_64 --build=release
    // dub build --arch=aarch64-linux-gnu --build=release
    writeln("DUB cross-compilation via --arch flag");
}
```

```d
// Coverage analysis
import std.stdio;
void testDUBCoverage() {
    // ldc2 -cov -run myapp.d   (line coverage)
    // dub test --coverage      (via DUB)
    // Profiling: ldc2 -profile -run myapp.d
    writeln("Coverage and profiling tools");
}
```

```d
// GitHub Actions for D
import std.stdio;
void testDUBCI() {
    /*
    name: D CI
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: dlang-community/setup-dlang@v1
          - run: dub test
    */
    writeln("CI configuration for D projects");
}
```

### DUB Commands Reference

```d
import std.stdio;
void testDUBCommandRef() {
    // dub init myapp         - Create new project
    // dub build              - Build project
    // dub run                - Build and run
    // dub test               - Run tests
    // dub clean              - Clean build artifacts
    // dub describe           - Show dependency tree
    // dub upgrade            - Upgrade dependencies
    // dub list               - List installed packages
    writeln("Common DUB commands");
}
```

### DUB Package Ecosystem

The DUB package registry at [code.dlang.org](https://code.dlang.org) hosts thousands of packages. Dependencies are specified with semantic versioning and support various source types.

```d
import std.stdio;
void testDUBPackageSpec() {
    // code.dlang.org - Package registry
    // Package specification: "name": "~>version"
    // Semantic versioning: ~>1.2.3 (>=1.2.3 <1.3.0)
    // Exact: "1.2.3"
    // Path: {"path": "../mylib"}
    // Git: {"repository": "https://github.com/user/repo.git", "version": "main"}
    writeln("Package dependency specification");
}
```

```d
import std.stdio;
void testDUBSubPackages() {
    /*
    {
        "name": "mylib",
        "subPackages": [
            {
                "name": "extra",
                "targetType": "library",
                "sourcePaths": ["extra/"]
            }
        ]
    }
    */
    writeln("SubPackages allow splitting a package into optional components");
}
```

```d
// Locking dependencies
import std.stdio;
void testDUBLocking() {
    // dub.selections.json - locks all dependency versions
    // dub upgrade --lock    - upgrade and update lock file
    // Check in dub.selections.json to VCS for reproducible builds
    writeln("dub.selections.json for reproducible builds");
}
```

## Testing and Debugging

### Unit Tests
```d
// Unit tests
unittest {
    auto result = 42;
    assert(result == 42);
}

// Compile and run
void main() {
    // Main program
    import std.stdio;
    writeln("Hello, World!");
}
```

### Running Tests
```bash
# Run unit tests with DMD
dmd -unittest main.d && ./main

# Run unit tests with DUB
dub test

# Run unit tests with specific configuration
dub test --config=library

# Run specific test
dub test -- --single path/to/test.d

# Run with code coverage
dub test --build=coverage
```

### Debugging
```bash
# Compile with debug symbols
dmd -g -debug main.d

# Debug with GDB
gdb ./myprogram
(gdb) break main
(gdb) run

# Debug with LLDB
lldb ./myprogram
(lldb) break set -n main
(lldb) run
```

### Profiling
```bash
# Profile with DMD
dmd -profile main.d

# Profile with LDC
ldc2 -profile main.d

# Use GPerfTools
dub run --profile

# Custom profiling
import std.datetime.stopwatch : benchmark;

auto results = benchmark!({
    // Function to benchmark
})(1000);  // Number of iterations

writeln("Mean: ", results[0].total!"msecs");
```

### Cross-Compilation with LDC

```bash
# Cross-compile for ARM
ldc2 -mtriple=arm-linux-gnueabihf main.d

# Cross-compile for AArch64
ldc2 -mtriple=aarch64-linux-gnu main.d

# For iOS
ldc2 -mtriple=arm64-apple-ios main.d

# For Android
ldc2 -mtriple=aarch64-linux-android main.d

# With custom sysroot
ldc2 -mtriple=arm-linux-gnueabihf --sysroot=/path/to/sysroot main.d
```

### Language Changelogs

D releases follow a predictable schedule with versions like 2.100.0, 2.101.0, etc. Each release includes:

```bash
# View changes between versions
# Available at: https://dlang.org/changelog/

# Track new features per version
dmd --version  # Show compiler version
```

Key recent milestones:
- **2.100.0** - DIP 1000 (scope), improvements to import
- **2.105.0** - DIP 1030 (named arguments), DIP 1043 (shortened methods)
- **2.110.0** - DIP 1052 (editions), DIP 1051 (bitfields)
- **Pending** - DIP 1048, DIP 1049, DIP 1053 (tuple unpacking), DIP 1054

## IDE and Editor Support

### VS Code
```bash
# Install extension
code --install-extension laurenttrudel:code-d

# Features provided:
# - Syntax highlighting
# - Code completion
# - Hover information
# - Go to definition
# - Find references
# - Rename symbol
# - Debugging support
```

### Visual D (Visual Studio)
```bash
# Features:
# - Integrated with Visual Studio
# - Project wizard for DUB and DMD/LDC
# - Debugger integration
# - Code completion
# - Refactoring support
# - Profiling integration
```

### Mono-D (MonoDevelop/Xamarin Studio)
```bash
# Features:
# - Cross-platform IDE
# - DUB integration
# - Debugger support
# - Code completion
# - Package management
```

### Vim/Neovim
```vim
" D syntax highlighting
syntax on

" D completion
Plug 'd-language/DCD'
Plug 'd-language/d-tools'
```

### Emacs
```elisp
;; D mode
(require 'd-mode)

;; DCD integration
(require 'dcd)
(dcd-setup)
```

## Quick Reference

### Compiler Quick Comparison
| Feature | DMD | LDC | GDC |
|---------|-----|-----|-----|
| Compilation speed | Fastest | Fast | Moderate |
| Optimization | Good | Best | Very good |
| Target support | Limited | Extensive | Extensive |
| Debug info | Good | Excellent | Good |
| Cross-compilation | Basic | Advanced | Advanced |

### DUB Command Summary
```bash
dub init           # Initialize project
dub build          # Build project
dub run            # Run project
dub test           # Run unit tests
dub clean          # Clean build cache
dub upgrade        # Update dependencies
dub search         # Search packages
dub describe       # Show project info
```

### Compiler Flags Summary
```bash
dmd file.d         # Basic compilation
dmd -O file.d      # With optimization
dmd -g file.d      # Debug symbols
dmd -w file.d      # Warnings
dmd -unittest      # Unit tests
dmd -cov file.d    # Code coverage
dmd -profile       # Profiling
dmd -run file.d    # Run immediately
```

### Development Tools
```bash
dfmt --in-place file.d         # Format code
dscanner --styleCheck file.d   # Lint code
dcd-server                     # Code completion
dfix file.d                    # Auto-fix issues
dustmite file.d script.sh      # Reduce test cases
```

### Build Configuration
```json
// dub.json
{
    "name": "project",
    "targetType": "executable",
    "dependencies": {
        "vibe-d": "~>0.9.0"
    }
}
```

### Documentation Generation
```bash
dub build --build=docs    # Generate documentation
dmd -D file.d             # Generate DDoc
dmd -Dd=docs/ file.d      # Custom output directory
```

## Resources

- [DMD Download](https://dlang.org/download.html)
- [LDC GitHub](https://github.com/ldc-developers/ldc)
- [GDC Repository](https://github.com/D-Programming-GDC/GDC)
- [DUB Website](https://code.dlang.org)
- [DUB GitHub](https://github.com/dlang/dub)
- [D Tools](https://github.com/dlang/tools)
- [dfmt GitHub](https://github.com/dlang/dfmt)
- [DCD GitHub](https://github.com/dlang/DCD)
- [D-Scanner GitHub](https://github.com/dlang-community/D-Scanner)
- [D Wiki](https://wiki.dlang.org)
- [D Blog](https://dlang.org/blog)
- [D Forum](https://forum.dlang.org)
