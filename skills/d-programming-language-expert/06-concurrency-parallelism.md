---
name: d-lang-concurrency
description: >-
  D concurrency and parallelism: std.concurrency (spawn, receive, send,
  Generator), std.parallelism (taskPool, parallel, task), threads,
  fibers, synchronization (Mutex, Condition, Semaphore, Barrier,
  ReadWriteMutex), atomic operations (atomicOp, atomicLoad, atomicStore,
  cas), data sharing patterns, thread-local storage.
  Use when writing concurrent or parallel D code.
license: MIT
metadata:
  topics: concurrency parallelism threads fibers message-passing sync
  order: 06
---

# D Programming Language - Concurrency & Parallelism

Comprehensive guide to D's concurrency model, message passing, parallelism, and synchronization primitives.

## Table of Contents

- [Concurrency Model](#concurrency-model)
- [std.concurrency](#stdconcurrency)
- [std.parallelism](#stdparallelism)
- [Threads and Fibers](#threads-and-fibers)
- [Synchronization](#synchronization)
- [Data Sharing](#data-sharing)
- [Common Patterns](#common-patterns)
- [Quick Reference](#quick-reference)

## Concurrency Model

### D's Approach to Concurrency

D embraces the concept of **shared nothing** with message passing as the default concurrency model. Threads do not share mutable state by default; instead, they communicate through messages.

```d
import std.concurrency;
import std.stdio;

// Spawn a new thread
auto tid = spawn({
    receive(
        (string msg) {
            writeln("Got: ", msg);
        }
    );
});

// Send a message to the thread
send(tid, "Hello from main thread");
```

### Immutable Data Sharing

```d
// Immutable (thread-local by default)
int localVar = 42;

// Immutable data is safe to share
immutable int[] sharedData = [1, 2, 3, 4, 5];

// Shared data must be explicitly declared
shared int globalCounter = 0;
```

### Thread Safety Model

```d
// @safe functions cannot share mutable data
int safeFunction() @safe {
    return 42;
}

// @system: required for sharing mutable data
int sharedFunction() @system {
    // Can manipulate shared data
    // Must use proper synchronization
    return 42;
}
```

## std.concurrency

### Spawning Threads

```d
import std.concurrency : spawn, receive, receiveOnly;
import std.stdio;

// Spawn with arguments
auto tidArgs = spawn((string s, int i) {
    writeln("Args: ", s, " ", i);
}, "hello", 42);

// Spawn a delegate
auto tidDelegate = spawn({
    receive(
        (string msg) {
            if (msg == "quit") {
                writeln("Done");
            } else {
                writeln("Worker got: ", msg);
            }
        }
    );
});

// Spawn a function
auto tidFunc = spawn({
    receive(
        (string msg) {
            writeln("Got: ", msg);
        }
    );
});

// Spawn with arguments
auto tid2 = spawn((string s, int i) {
    writeln("Args: ", s, " ", i);
}, "hello", 42);

// Spawn a delegate
auto tid3 = spawn({
    writeln("In spawned thread");
});
```

### Message Passing (Send/Receive)

```d
import std.concurrency;
import std.stdio;

// Sender
void sender(Tid receiver) {
    send(receiver, "Hello!");
    send(receiver, 42);
    send(receiver, 3.14);
}

// Receiver
void receiver() {
    // Receive specific type
    string msg = receiveOnly!(string);

    // Receive multiple types
    receive(
        (string s) { writeln("Got string: ", s); },
        (int i)    { writeln("Got int: ", i); },
        (double d) { writeln("Got double: ", d); }
    );
}
```

### Priority Messages

```d
import std.concurrency;
import std.stdio;

// Priority handling
void worker() {
    bool stop = false;
    while (!stop) {
        receive(
            // High priority: stop message
            (string msg) {
                if (msg == "STOP") stop = true;
            },
            // Medium priority: data messages
            (int i) {
                writeln("Processing: ", i);
            }
        );
    }
}
```

### Owner Receiver

```d
import std.concurrency;
import std.stdio;

// Simple typed message passing
auto tid = spawn({
    receive(
        (int val) {
            writeln("Received int: ", val);
        }
    );
});
send(tid, 42);
writeln("Sent int to worker");
```

### spawnLinked

`spawnLinked(&fn, args)` is the public `std.concurrency` variant of `spawn` that
_links_ the spawned thread to the owner: when the child terminates (normally or
by an uncaught exception), the owner receives a `LinkTerminated` message. Use it
with `receive` to detect worker failure.

```d
import std.concurrency : spawnLinked, receive, LinkTerminated, OwnerTerminated;
import std.stdio : writeln;

static void worker() {
    // ... do work, then return (or throw) ...
}

void main() {
    auto tid = spawnLinked(&worker);
    receive(
        (LinkTerminated lt) { writeln("worker ended: ", lt.tid); },
    );
}
```

## std.parallelism

### Parallel foreach

```d
import std.parallelism : parallel;
import std.range : iota;
import std.array : array;
import std.stdio;

// Parallel foreach
auto arr = iota(0, 100).array;

// `parallel(arr)` yields elements; bind `ref` to mutate in place, and add an
// index variable when you need the position (not `foreach (i; parallel(arr))`,
// which would bind `i` to the element value, not the index).
foreach (i, ref elem; parallel(arr)) {
    elem = cast(int)(i * i);
}

writeln("Done");
```

### taskPool

```d
import std.parallelism;
import std.stdio;

// Use taskPool
auto result = taskPool.map!((i) => i * 2)([1, 2, 3, 4, 5]);
writeln("Result: ", result.front);
```

### Parallel Map

```d
import std.parallelism;
import std.range : iota;
import std.array : array;
import std.stdio;

// Parallel map
auto arr = iota(0, 100).array;
auto result = taskPool.map!((i) => i * i)(arr);
writeln("First result: ", result.front);
```

### amap (eager parallel map)

```d
import std.parallelism;
import std.stdio;

// amap evaluates eagerly and returns an array (unlike taskPool.map which is lazy)
int[] arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
int[] result = taskPool.amap!((i) => i * i)(arr);
writeln("Result: ", result);  // [1, 4, 9, 16, 25, ...]
```

### taskPool.reduce (parallel reduce)

```d
import std.parallelism;
import std.range : iota;
import std.array : array;
import std.stdio;

// Parallel reduce
auto arr = iota(1, 101).array;

// Sum with parallel execution (reduce is a TaskPool method, not a free function)
int sum = taskPool.reduce!((a, b) => a + b)(arr);
writeln("Sum: ", sum);
```

### Future

```d
import std.parallelism;
import std.stdio;

// Create a future using taskPool
auto future = task(() => 42);
future.executeInNewThread();
auto val = future.yieldForce;
writeln("Future result: ", val);
```

### Individual Tasks

```d
import std.parallelism;
import std.stdio;

// Create an individual task
auto t = task(() => 42);
t.executeInNewThread();
auto val = t.yieldForce;
writeln("Task result: ", val);
```

### Parallel foreach with Parallelism

```d
import std.parallelism : parallel;
import std.stdio;

int[] arr = new int[1_000_000];

// Parallel foreach (default) — ref element, index for the position
foreach (i, ref elem; parallel(arr)) {
    elem = cast(int)(i * i);
}

// With work unit size (second arg to parallel)
foreach (ref elem; parallel(arr, 100)) {
    elem = elem * 2;
}
```

## Threads and Fibers

### Thread Class

```d
import core.thread : Thread;
import std.stdio;

// Create and start a thread
auto thread = new Thread({
    writeln("In thread");
});
thread.start();

// Wait for thread to finish
thread.join();

// Thread with work
auto thread2 = new Thread({
    writeln("Thread2 working");
});
thread2.start();
thread2.join();
```

### Fiber (Coroutine)

```d
import core.thread : Fiber;
import std.stdio;

// Create a fiber
auto fiber = new Fiber({
    writeln("In fiber: 1");
    Fiber.yield();
    writeln("In fiber: 2");
    Fiber.yield();
    writeln("In fiber: 3");
});

// Execute fiber
fiber.call();  // Prints "In fiber: 1"
fiber.call();  // Prints "In fiber: 2"
fiber.call();  // Prints "In fiber: 3"

// Fiber with state
auto fiberWithState = new Fiber({
    int counter = 0;
    while (counter < 3) {
        writeln("Counter: ", counter++);
        Fiber.yield();
    }
});

// Fiber with parameters (D features capture by closure)
void fiberExample() {
    int x = 10;
    auto fiber = new Fiber({
        x += 5;  // Captures x from outer scope
        Fiber.yield();
        writeln(x);  // 15
    });
    fiber.call();
}
```

### Fiber Scheduler and Generator

```d
import std.concurrency : Generator, yield;
import core.thread : Fiber;
import std.stdio;

// Generator: produce values via coroutines (std.concurrency.Generator)
auto gen = new Generator!int({
    foreach (i; 0 .. 5) {
        yield(i * i);  // Produce a value, suspend execution
    }
});

// Consume generated values like a range
foreach (val; gen) {
    writeln("Got: ", val);
}

// Custom fiber-based generator
auto genFiber = new Fiber({
    foreach (i; 0 .. 5) {
        writeln("Yielding: ", i * i);
        Fiber.yield();
    }
});
genFiber.call();
genFiber.call();
```

### Atomic Operations (core.atomic)

```d
import core.atomic;
import std.stdio;

// Atomic operations on shared(int)
shared int counter = 0;

void increment() {
    atomicOp!"+="(counter, 1);   // Atomic increment
    atomicOp!"-="(counter, 1);   // Atomic decrement
}

// Atomic load/store
int val = atomicLoad(counter);
atomicStore(counter, 42);

// Compare-and-swap (CAS)
shared int casTarget = 0;
if (cas(&casTarget, 0, 1)) {  // If target == 0, set to 1
    writeln("CAS succeeded");
}
```

### Synchronization Primitives (core.sync)

```d
import core.sync.mutex : Mutex;
import core.sync.condition : Condition;
import core.sync.rwmutex : ReadWriteMutex;
import core.sync.semaphore : Semaphore;
import core.sync.barrier : Barrier;
import std.stdio;

// Mutex with condition variable
auto mutex = new Mutex();
auto cond = new Condition(mutex);

// RWLock
auto rwlock = new ReadWriteMutex();

void reader() {
    rwlock.reader.lock();
    scope(exit) rwlock.reader.unlock();
    // Multiple readers can enter
    writeln("Reading");
}

void writer() {
    rwlock.writer.lock();
    scope(exit) rwlock.writer.unlock();
    // Exclusive access
    writeln("Writing");
}

// Semaphore
auto sem = new Semaphore(3);  // 3 permits max

void worker() {
    sem.wait();
    scope(exit) sem.notify();
    // Access limited resource
    writeln("Accessed resource");
}

// Barrier
auto bar = new Barrier(3);

void parallelWorker(int id) {
    // Phase 1
    writeln("Work phase 1 for ", id);
    bar.wait();  // Wait for all 3 threads

    // Phase 2
    writeln("Work phase 2 for ", id);
    bar.wait();
}
```

### Condition Variable

```d
import core.sync.condition : Condition;
import core.thread : Thread;
import core.sync.mutex : Mutex;
import std.stdio;

// Create condition variable
auto mutex = new Mutex();
auto condition = new Condition(mutex);
bool hasData = false;

// Wait for condition
void consumer() {
    mutex.lock();
    while (!hasData) {
        condition.wait();
    }
    // Process data
    hasData = false;
    mutex.unlock();
    writeln("Processed data");
}

// Signal condition
void producer() {
    mutex.lock();
    hasData = true;
    condition.notify();
    mutex.unlock();
    writeln("Produced data");
}
```

## Synchronization

### synchronized Statement

```d
import core.sync.mutex : Mutex;
import std.stdio;

// Synchronized block
auto mutex = new Mutex();

void criticalSection() {
    mutex.lock();
    scope(exit) mutex.unlock();

    writeln("In critical section");
}

// Shared atomic counter
import core.atomic : atomicOp;
shared int atomicCounter = 0;

void threadFunction() {
    atomicOp!"+="(atomicCounter, 1);
}
```

### Atomic Operations

```d
import core.atomic : atomicOp, atomicLoad, atomicStore;

// Atomic operations
shared int counter = 0;

void threadFunction() {
    atomicOp!"+="(counter, 1);  // Atomic increment
    int value = atomicLoad(counter);  // Atomic read
    atomicStore(counter, 0);  // Atomic write
}
```

### Read-Write Lock

```d
import core.sync.rwmutex : ReadWriteMutex;

auto rwLock = new ReadWriteMutex();

void readOperation() {
    rwLock.reader.lock();
    scope(exit) rwLock.reader.unlock();
    // Multiple readers allowed concurrently
}

void writeOperation() {
    rwLock.writer.lock();
    scope(exit) rwLock.writer.unlock();
    // Exclusive write access
}
```

### Semaphore

```d
import core.sync.semaphore : Semaphore;
import std.stdio;

// Create semaphore with max 3 permits
auto sem = new Semaphore(3);

void limitedResource() {
    sem.wait();  // Acquire a permit
    scope(exit) sem.notify();  // Release permit

    // Access resource
    writeln("Accessed resource");
}
```

### Barrier

```d
import core.sync.barrier : Barrier;

auto barrier = new Barrier(3);  // Wait for 3 participants

void workerFunction() {
    // Do work...
    barrier.wait();  // Wait for all participants

    // Continue with synchronized work
}
```

## Data Sharing

### shared Keyword

```d
// Shared data requires synchronization
shared int g_counter = 0;

void threadFunction() {
    import core.atomic : atomicOp;
    atomicOp!"+="(g_counter, 1);
}

// Using synchronized for shared data
string sharedToString(shared int value) {
    int local = value;  // Copy to local
    return to!string(local);
}
```

### Mutable Data Sharing

```d
import core.sync.mutex : Mutex;
import std.stdio;

// Shared data must be synchronized
class ChatHistory {
    private string[] messages;
    private Mutex mutex;

    this() {
        mutex = new Mutex();
    }

    void addMessage(string msg) {
        mutex.lock();
        scope(exit) mutex.unlock();
        messages ~= msg;
    }

    string[] getMessages() {
        mutex.lock();
        scope(exit) mutex.unlock();
        return messages;
    }
}

auto history = new ChatHistory();
```

### Thread-Local Storage

```d
// Thread-local data (default for globals in D)
__gshared int globalCount = 0;  // Shared across all threads
int threadLocalCount = 0;  // Each thread has its own copy

void threadFunction() {
    threadLocalCount++;  // Only modifies this thread's copy
}
```

### Immutable Sharing

```d
// Immutable data is safe to share
immutable string config = "config content";

// Can be read by multiple threads
// without synchronization
void readerThread() {
    writeln(config);  // Safe
}
```

## Common Patterns

### Worker Pool

```d
import std.concurrency;
import std.stdio;

// Simple worker pool
auto worker = spawn({
    while (true) {
        receive(
            (int work) {
                writeln("Processing: ", work);
                send(ownerTid, work * 2);
            },
            (string stop) {
                if (stop == "STOP") {
                    writeln("Stopping");
                    ownerTid.send("DONE");
                }
            }
        );
    }
});

// Send work
foreach (i; 0 .. 5) {
    send(worker, i);
}

// Signal stop
send(worker, "STOP");
```

### Producer-Consumer

```d
import std.concurrency;
import std.stdio;

auto consumer = spawn({
    bool done = false;
    while (!done) {
        receive(
            (int item) {
                writeln("Processing: ", item);
            },
            (string msg) {
                if (msg == "SHUTDOWN") {
                    done = true;
                    writeln("Shutting down");
                }
            }
        );
    }
});

// Produce
foreach (i; 0 .. 10) {
    send(consumer, i);
}

// Signal shutdown
send(consumer, "SHUTDOWN");
```

### Pipeline

```d
import std.concurrency;
import std.stdio;

// Pipeline example with chained threads
auto stage1 = spawn({
    foreach (i; 0 .. 5) {
        send(ownerTid, i);
    }
    send(ownerTid, "DONE");
});

auto stage2 = spawn({
    bool pipelineDone = false;
    while (!pipelineDone) {
        receive(
            (int val) {
                send(ownerTid, val * 2);
            },
            (string msg) {
                if (msg == "DONE") {
                    pipelineDone = true;
                    send(ownerTid, "ALL_DONE");
                }
            }
        );
    }
});
```

## Quick Reference

### Concurrency Primitives

```d
// Message passing
spawn(&function)           // Spawn new thread
send(tid, message)         // Send message
receiveOnly!T()            // Receive specific type
receive(handlers...)       // Receive with handlers
receiveTimeout(dur, ...)   // Receive with timeout
ownerTid                   // Parent thread's ID
thisTid                    // Current thread's ID
```

### Parallelism

```d
parallel(range)            // Parallel foreach
taskPool.amap!func(range)  // Parallel eager map (TaskPool method)
taskPool.reduce!op(range)  // Parallel reduce (TaskPool method)
taskPool                   // Task scheduler
```

### Parallelization

```d
parallel(range)            // Parallel foreach
taskPool.amap!func(range)  // Parallel eager map (TaskPool method)
taskPool.reduce!op(range)  // Parallel reduce (TaskPool method)
taskPool                   // Task scheduler
task!func(args)            // Create individual task
asyncBuf(range, size)      // Async buffered range
```

### Synchronization

```d
Mutex                      // Mutual exclusion
synchronized               // Method/block synchronization
atomicOp                   // Atomic operations
cas(ptr, old, new)         // Compare-and-swap
Condition                  // Conditional variable
ReadWriteMutex             // Read-write lock
Semaphore                  // Counting semaphore
Barrier                    // Thread barrier
```

### Thread Primitives

```d
core.thread.Thread         // Thread class
core.thread.Fiber          // Coroutine class
core.thread.thread_prio    // Thread priority
core.thread.duration       // Thread duration
Fiber.State.{HOLD, EXEC, TERM}  // Fiber states
Generator!T                // Coroutine generator
```

### Message Passing

```
send(tid, msg)             // Send message
receiveOnly!T()            // Receive specific type
receive(handlers...)       // Receive with handlers
receiveTimeout(dur, ...)   // Receive with timeout
prioritySend(tid, msg)     // Priority message
ownerTid                   // Parent thread ID
thisTid                    // Current thread ID
spawn(&func)               // Spawn thread
spawnLinked(&func)         // Spawn linked: owner gets LinkTerminated on exit
```

### Data Sharing

```d
shared int x;              // Shared data (needs sync)
immutable int y;           // Immutable data (thread-safe)
__gshared int z;           // Global shared data (no TLS)
int t;                     // Thread-local (default)
```

## References

- [std.concurrency](https://dlang.org/phobos/std_concurrency.html)
- [std.parallelism](https://dlang.org/phobos/std_parallelism.html)
- [core.thread](https://dlang.org/phobos/core_thread.html)
- [core.sync](https://dlang.org/phobos/core_sync.html)
- [Concurrent D Article](http://www.informit.com/articles/article.aspx?p=1609144)
