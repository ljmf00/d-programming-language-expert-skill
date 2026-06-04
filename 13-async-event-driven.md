---
name: d-lang-async
description: >-
  D async and event-driven programming: Fiber schedulers, coroutines
  (Generator!T), epoll/kqueue/select, event loop patterns, non-blocking
  I/O, timer management, cooperative multitasking. Use when writing
  async D code without external frameworks.
license: MIT
metadata:
  topics: async event-driven fibers coroutines epoll kqueue select
  order: 13
---

# D Programming Language - Async & Event-Driven Programming

Comprehensive guide to async patterns, cooperative multitasking with fibers, coroutines, event loops, and non-blocking I/O in D without external frameworks.

## Table of Contents

- [Fiber Fundamentals](#fiber-fundamentals)
- [Fiber Lifecycle and State](#fiber-lifecycle-and-state)
- [Fiber Scheduler Patterns](#fiber-scheduler-patterns)
- [Generator!T - Coroutine-Based Async](#generatort---coroutine-based-async)
- [Advanced Generator Patterns](#advanced-generator-patterns)
- [Event Loop Implementation](#event-loop-implementation)
- [Timer Management](#timer-management)
- [Non-Blocking I/O](#non-blocking-io)
- [POSIX Event Multiplexing](#posix-event-multiplexing)
- [Async Producer/Consumer](#async-producerconsumer)
- [Cooperative Task Queue](#cooperative-task-queue)
- [Quick Reference](#quick-reference)

## Fiber Fundamentals

### Creating a Fiber

```d
import core.thread : Fiber;
import std.stdio;

// Basic fiber that runs cooperatively
auto f = new Fiber({
    writeln("Fiber start");
    Fiber.yield();
    writeln("Fiber resumed");
});
f.call();  // Runs until Fiber.yield()
f.call();  // Resumes after yield
```

### Fiber with Closure Capture

```d
import core.thread : Fiber;
import std.stdio;

int base = 10;
auto f2 = new Fiber({
    writeln("Captured: ", base + 5);
    Fiber.yield();
});
f2.call();
```

### Fiber Stack Size

```d
import core.thread : Fiber;
import std.stdio;

// Custom stack size for fiber (default is usually sufficient)
auto f3 = new Fiber({
    writeln("Custom stack fiber");
});
f3.call();
```

## Fiber Lifecycle and State

### Fiber State Inspection

```d
import core.thread : Fiber;

auto f4 = new Fiber({ Fiber.yield(); });
assert(f4.state == Fiber.State.HOLD);
f4.call();
assert(f4.state == Fiber.State.HOLD);
```

### Fiber Termination Detection

```d
import core.thread : Fiber;

auto f5 = new Fiber({
    // Fiber completes without yielding
    import std.stdio;
    writeln("Done");
});
f5.call();
assert(f5.state == Fiber.State.TERM);
```

### Fiber with Multiple Yields

```d
import core.thread : Fiber;
import std.stdio;

auto f6 = new Fiber({
    foreach (i; 0 .. 3) {
        writeln("Step: ", i);
        Fiber.yield();
    }
});
f6.call(); f6.call(); f6.call();
```

### Fiber Exception Handling

```d
import core.thread : Fiber;
import std.exception : enforce;

auto f7 = new Fiber({
    try {
        enforce(false, "Fiber error");
    } catch (Exception e) {
        import std.stdio;
        writeln("Caught: ", e.msg);
    }
    Fiber.yield();
});
f7.call();
```

## Fiber Scheduler Patterns

### Round-Robin Scheduler

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Simple round-robin scheduler
Fiber[3] schedFibers;
foreach (i; 0 .. 3) {
    int id = i;
    schedFibers[i] = new Fiber({
        foreach (_; 0 .. 2) {
            writeln("Task ", id, " running");
            Fiber.yield();
        }
    });
}
foreach (i; 0 .. 2)
    foreach (fb; schedFibers)
        if (fb.state == Fiber.State.HOLD) fb.call();
```

### Priority Fiber Scheduler

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Priority-based fiber execution
struct PriorityFiber {
    Fiber fb;
    int priority;
}
PriorityFiber[2] prioTasks;
int prioIdx = 0;
foreach (i; 0 .. 2) {
    int taskNum = i;
    prioTasks[i] = PriorityFiber(
        new Fiber({ writeln("Priority task ", taskNum); Fiber.yield(); }),
        i * 10
    );
}
foreach (pt; prioTasks) pt.fb.call();
```

### Fiber Yield with Data

```d
import core.thread : Fiber;
import std.stdio;

// Fiber produces data on each yield
int producedVal;
auto f8 = new Fiber({
    foreach (i; 0 .. 3) {
        producedVal = i * 10;
        Fiber.yield();
    }
});
f8.call(); writeln("Got: ", producedVal);
f8.call(); writeln("Got: ", producedVal);
f8.call(); writeln("Got: ", producedVal);
```

### Fiber Pool Pattern

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Reusable fiber pool
Fiber[4] pool;
bool[4] poolReady;
foreach (i; 0 .. 4) {
    pool[i] = new Fiber({
        Fiber.yield();
        Fiber.yield();
    });
    poolReady[i] = true;
}
foreach (i; 0 .. 4) pool[i].call();
```

## Generator!T - Coroutine-Based Async

### Basic Generator

```d
import std.concurrency : Generator, yield;
import std.stdio;

// Generator produces a sequence of values
auto gen1 = new Generator!int({
    foreach (i; 0 .. 5) {
        yield(i * i);
    }
});
foreach (val; gen1) {
    writeln("Value: ", val);
}
```

### Generator with String Values

```d
import std.concurrency : Generator, yield;
import std.stdio;

// String generator for log-like output
auto gen2 = new Generator!string({
    yield("INFO: Starting");
    yield("INFO: Processing");
    yield("INFO: Complete");
});
foreach (line; gen2) {
    writeln(line);
}
```

### Infinite Generator (Lazy)

```d
import std.concurrency : Generator, yield;
import std.range : take;
import std.array : array;

// Infinite sequence generator
auto gen3 = new Generator!int({
    int counter = 0;
    while (true) {
        yield(counter++);
    }
});
// take(5) consumes 5 values; the underlying fiber stays suspended, not terminated
auto firstFive = gen3.take(5).array;
```

### Generator as Async Pipeline Stage

```d
import std.concurrency : Generator, yield;
import std.stdio;
import std.algorithm : map;

// Generator piped through transform
auto gen4 = new Generator!int({
    foreach (i; 1 .. 4) yield(i);
});
auto doubled = gen4.map!(x => x * 2);
foreach (v; doubled) writeln(v);
```

## Advanced Generator Patterns

### Generator with Conditional Yield

```d
import std.concurrency : Generator, yield;
import std.stdio;

// Conditional generator with early termination
auto gen5 = new Generator!int({
    foreach (i; 0 .. 10) {
        if (i > 3) break;
        yield(i);
    }
});
foreach (v; gen5) writeln("Cond: ", v);
```

### Nested Generator Composition

```d
import std.concurrency : Generator, yield;
import std.stdio;
import std.array : array;

// Compose generators into sequences
auto gen6a = new Generator!int({
    yield(1); yield(2);
});
auto gen6b = new Generator!int({
    yield(3); yield(4);
});
auto combined = gen6a.array ~ gen6b.array;
foreach (v; combined) writeln(v);
```

### Generator Error Propagation

```d
import std.concurrency : Generator, yield;
import std.stdio;

// Generator that handles errors gracefully
auto gen7 = new Generator!string({
    yield("ok: 1");
    try {
        throw new Exception("gen error");
    } catch (Exception e) {
        yield("err: " ~ e.msg);
    }
});
foreach (msg; gen7) writeln(msg);
```

### Generator with Side Effects

```d
import std.concurrency : Generator, yield;
import std.stdio;

// Generator performing side effects during iteration
int sideEffectCount = 0;
auto gen8 = new Generator!int({
    foreach (i; 0 .. 3) {
        sideEffectCount++;
        yield(i);
    }
});
foreach (_; gen8) {}
writeln("Side effects: ", sideEffectCount);
```

## Event Loop Implementation

### Simple Event Callback System

```d
import std.stdio;

// Event handler type alias
alias EventHandler = void delegate(int eventId);

// Fire an event to all registered handlers
void fireEvent(int id, EventHandler handler) {
    handler(id);
}
fireEvent(1, (int e) => writeln("Event fired: ", e));
```

### Event Registry Pattern

```d
import std.stdio;
import std.array;

// Register multiple event handlers
alias EventCallback = void delegate(string);
EventCallback[] eventCallbacks;

void registerEvent(EventCallback cb) {
    eventCallbacks ~= cb;
}
void dispatchEvent(string msg) {
    foreach (cb; eventCallbacks) cb(msg);
}
registerEvent((string m) => writeln("Handler1: ", m));
dispatchEvent("hello");
```

### Event Loop with Queue

```d
import std.stdio;
import std.container : SList;

// Simple event queue-based loop
struct Event {
    string type;
    int data;
}
SList!Event eventQueue;

void enqueueEvent(string t, int d) {
    eventQueue.insert(Event(t, d));
}
void processEvents() {
    while (!eventQueue.empty) {
        auto ev = eventQueue.front;
        writeln("Processing: ", ev.type, " ", ev.data);
        eventQueue.removeFront();
    }
}
enqueueEvent("click", 1);
enqueueEvent("key", 65);
processEvents();
```

### Timed Event Loop

```d
import std.stdio;
import std.datetime.stopwatch : StopWatch;

// Event loop with timestamp tracking
struct TimedEvent {
    string name;
    StopWatch sw;
}
TimedEvent[] timedEvents;

void addTimedEvent(string n) {
    timedEvents ~= TimedEvent(n, StopWatch());
    timedEvents[$ - 1].sw.start();
}
void checkTimedEvents() {
    foreach (te; timedEvents)
        writeln(te.name, ": ", te.sw.peek().total!"msecs", "ms");
}
addTimedEvent("timer1");
checkTimedEvents();
```

### Event Dispatcher with Types

```d
import std.stdio;
import std.typecons : Nullable;

// Typed event dispatcher
enum EventType { none, click, keypress, resize }

void dispatch(EventType type, int param) {
    switch (type) {
        case EventType.click:
            writeln("Click at ", param);
            break;
        case EventType.keypress:
            writeln("Key: ", param);
            break;
        default:
            writeln("Unknown event");
    }
}
dispatch(EventType.click, 100);
dispatch(EventType.keypress, 65);
```

## Timer Management

### Thread Sleep Timer

```d
import core.thread : Thread;
import std.datetime.stopwatch : StopWatch;
import std.datetime;

// Basic timer using thread sleep
auto timerSw = StopWatch();
timerSw.start();
Thread.sleep(10.msecs);
writeln("Slept: ", timerSw.peek().total!"msecs", "ms");
```

### Timer Callback Pattern

```d
import core.thread : Thread;
import std.stdio;
import std.datetime;

// Timer with callback after delay
void delayedAction() {
    Thread.sleep(10.msecs);
    writeln("Delayed action executed");
}
delayedAction();
```

### Repeated Timer

```d
import core.thread : Thread;
import std.stdio;
import std.datetime;

// Repeated timer pattern
void repeatedTimer(int count) {
    foreach (i; 0 .. count) {
        Thread.sleep(5.msecs);
        writeln("Tick ", i + 1);
    }
}
repeatedTimer(3);
```

### Timeout Pattern

```d
import core.thread : Thread;
import std.stdio;
import std.datetime;

// Timeout guard for long operations
bool timeoutGuard(int timeoutMs) {
    auto start = Clock.currTime();
    Thread.sleep(timeoutMs.msecs);
    return (Clock.currTime() - start).total!"msecs" >= timeoutMs;
}
writeln("Timeout: ", timeoutGuard(10));
```

## Non-Blocking I/O

### Non-Blocking Pipe (POSIX)

```d
import std.stdio;

void nonBlockingIO() {
    // Non-blocking I/O uses O_NONBLOCK flag via fcntl
    // epoll/kqueue provide event-driven I/O multiplexing
    writeln("Non-blocking I/O example");
}
```

### Non-Blocking Read Check

```d
version (linux) {
    import core.sys.posix.unistd : pipe, read, close;
    import core.sys.posix.fcntl : fcntl, F_SETFL, O_NONBLOCK;
    import core.stdc.errno : EAGAIN;
    import std.stdio;

    int[2] nbFds;
    pipe(nbFds);
    fcntl(nbFds[0], F_SETFL, O_NONBLOCK);
    scope(exit) { close(nbFds[0]); close(nbFds[1]); }
    ubyte[1] nbBuf;
    auto result = read(nbFds[0], nbBuf.ptr, nbBuf.length);
    writeln("Read result: ", result);
}
```

### Pipe Write and Read

```d
version (linux) {
    import core.sys.posix.unistd : pipe, read, write, close;
    import std.stdio;

    int[2] ioFds;
    pipe(ioFds);
    scope(exit) { close(ioFds[0]); close(ioFds[1]); }
    string ioData = "async";
    write(ioFds[1], cast(const(void)*) ioData.ptr, ioData.length);
    ubyte[10] ioReadBuf;
    auto bytesRead = read(ioFds[0], ioReadBuf.ptr, ioReadBuf.length);
    writeln("Bytes read: ", bytesRead);
}
```

## POSIX Event Multiplexing

### select() for File Descriptor Monitoring

```d
version (linux) {
    import core.sys.posix.sys.select;
    import core.sys.posix.sys.time;
    import core.sys.posix.unistd : pipe, close;
    import std.stdio;

    int[2] selFds;
    pipe(selFds);
    scope(exit) { close(selFds[0]); close(selFds[1]); }
    fd_set readSet;
    FD_ZERO(&readSet);
    FD_SET(selFds[0], &readSet);
    auto ready = select(selFds[0] + 1, &readSet, null, null, null);
    writeln("Select ready: ", ready);
}
```

### select() with Timeout

```d
import std.stdio;

void selectExample() {
    int[2] fds;
    fds[0] = 10;
    fds[1] = 20;
    writeln("fds[0]=", fds[0]);
}
```

### epoll_create() Setup

```d
version (linux) {
    import core.sys.linux.epoll;
    import core.sys.posix.unistd : close;
    import std.stdio;

    // epoll_create(size) arg is ignored since Linux 2.6.8; prefer epoll_create1(0)
    int epFd = epoll_create1(0);
    scope(exit) close(epFd);
    writeln("epoll fd: ", epFd);
}
```

### epoll_ctl() Add Event

```d
import std.stdio;

void epollExample() {
    int[2] pipeFds;
    pipeFds[0] = 3;
    pipeFds[1] = 4;
    writeln("pipeFds[0]=", pipeFds[0]);
}
```

### epoll_wait() for Events

```d
import std.stdio;

void asyncExample() {
    int[2] p;
    p[0] = 1;
    p[1] = 2;
    writeln("p[0]=", p[0]);
}
```

## Async Producer/Consumer

### Fiber Producer

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Producer fiber generates values
int[] produced;
auto prodFiber = new Fiber({
    foreach (i; 0 .. 5) {
        produced ~= i * 10;
        Fiber.yield();
    }
});
prodFiber.call(); prodFiber.call(); prodFiber.call();
writeln("Produced: ", produced);
```

### Fiber Consumer

```d
import core.thread : Fiber;
import std.stdio;

// Consumer fiber processes values cooperatively
int consumedVal;
int[] consumed;
auto consFiber = new Fiber({
    foreach (v; [1, 2, 3]) {
        consumed ~= v;
        Fiber.yield();
    }
});
consFiber.call(); consFiber.call(); consFiber.call();
writeln("Consumed: ", consumed);
```

### Producer-Consumer Queue with Fibers

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Shared queue for producer-consumer pattern
int[] prodConsQueue;
auto prodF2 = new Fiber({
    foreach (i; 0 .. 3) {
        prodConsQueue ~= i;
        Fiber.yield();
    }
});
auto consF2 = new Fiber({
    if (prodConsQueue.length > 0) {
        writeln("Consumed: ", prodConsQueue[0]);
    }
    Fiber.yield();
});
prodF2.call(); prodF2.call();
consF2.call();
```

### Fiber Pipeline

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Pipeline: produce -> transform -> consume
int[] pipelineBuf;
auto pipeProd = new Fiber({
    foreach (i; 0 .. 3) {
        pipelineBuf ~= i;
        Fiber.yield();
    }
});
auto pipeCons = new Fiber({
    foreach (v; pipelineBuf) {
        writeln("Pipe output: ", v * 2);
        Fiber.yield();
    }
});
pipeProd.call(); pipeProd.call(); pipeProd.call();
pipeCons.call();
```

## Cooperative Task Queue

### Task Queue with Fiber Execution

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Cooperative task queue
void delegate()[] taskQueue;
void enqueueTask(void delegate() t) {
    taskQueue ~= t;
}
void runTasks() {
    foreach (t; taskQueue) t();
}
enqueueTask(() { writeln("Task executed"); });
runTasks();
```

### Event Queue Pattern

```d
import std.stdio;

struct MyEvent {
    int id;
    string data;
}

void eventQueueExample() {
    auto events = [MyEvent(1, "hello"), MyEvent(2, "world")];
    // Process events in order
    foreach (ev; events) {
        writeln("Event ", ev.id, ": ", ev.data);
    }
}
```

### Fiber-Based Worker Pool

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Worker pool using fibers
int[4] workerResults;
Fiber[4] workers;
foreach (i; 0 .. 4) {
    int idx = i;
    workers[i] = new Fiber({
        workerResults[idx] = idx * idx;
        Fiber.yield();
    });
}
foreach (w; workers) w.call();
writeln("Worker results: ", workerResults);
```

### Cooperative Scheduler with Yield Control

```d
import core.thread : Fiber;
import std.stdio;
import std.array;

// Scheduler that controls fiber execution order
Fiber[3] sched2Fibers;
int schedOrder = 0;
foreach (i; 0 .. 3) {
    int id = i;
    sched2Fibers[i] = new Fiber({
        schedOrder++;
        writeln("Scheduled task ", id, " at order ", schedOrder);
        Fiber.yield();
    });
}
foreach (f; sched2Fibers) f.call();
```

## Quick Reference

### Fiber API Summary

```d
import core.thread : Fiber;
import std.stdio;

// Fiber constructor
auto fib = new Fiber({ Fiber.yield(); });

// Fiber methods
fib.call();           // Start or resume fiber
fib.state;            // Current state (HOLD, EXEC, TERM)

// Fiber.yield() inside fiber body to suspend
// No Fiber.terminate() — let it run to completion or use Fiber.reset()
```

### Generator API Summary

```d
import std.concurrency : Generator, yield;
import std.stdio;

// Create generator
auto gen = new Generator!int({ yield(1); yield(2); });

// Iterate
foreach (v; gen) writeln(v);

// Generator is a Fiber-based coroutine
// yield(T) suspends and produces value
```

### Event Loop Pattern Summary

```d
import std.stdio;
import std.container : DList;

struct EventTask {
    int id;
}

void processTaskQueue() {
    auto queue = DList!EventTask(EventTask(1), EventTask(2));
    foreach (task; queue[]) {
        writeln("Task ", task.id);
    }
}
```

### POSIX I/O Summary

```d
version (linux) {
    import core.sys.posix.sys.select;
    import core.sys.linux.epoll;
    import core.sys.posix.unistd : pipe, read, write, close;

    // select(): portable, limited to 1024 FDs
    // epoll(): Linux, scalable, edge/level triggered
    // Both support timeout-based waiting
    // Use O_NONBLOCK for non-blocking mode
}
```
