# 11 - Threads, Channels, Arc, Mutex, Send, and Sync

## Spawn and Join

```rust
use std::thread;

let handle = thread::spawn(|| 21 * 2);
let value = handle.join().expect("worker panicked");
println!("{value}");
// Output: 42
```

`join` waits and returns either the value or panic payload.

## Move Captures

```rust
let course = String::from("Rust");
let handle = thread::spawn(move || println!("{course}"));
handle.join().expect("worker panicked");
// Output: Rust
```

Thread closures normally need owned `'static` data because the thread may outlive the caller.

## Scoped Threads

Scoped threads can borrow local data because the scope waits before returning:

```rust
let values = [1, 2, 3];
thread::scope(|scope| {
    scope.spawn(|| println!("{}", values.iter().sum::<i32>()));
});
// Output: 6
```

## Channels

```rust
use std::sync::mpsc;

let (sender, receiver) = mpsc::channel();
thread::spawn(move || sender.send(String::from("finished")).expect("receiver dropped"));
println!("{}", receiver.recv().expect("sender dropped"));
// Output: finished
```

Sending usually moves ownership, preventing later mutation by the sender.

## Bounded Channel

```rust
let (sender, receiver) = mpsc::sync_channel(2);
```

A bounded channel provides backpressure. Capacity must reflect consumer throughput and memory limits.

## Multiple Producers

Clone senders for producers. The receiver sees closure only after every sender is dropped.

```rust
let sender_two = sender.clone();
```

## Arc

`Arc<T>` is atomically reference-counted shared ownership:

```rust
use std::sync::Arc;

let title = Arc::new(String::from("Rust"));
let worker_title = Arc::clone(&title);
let handle = thread::spawn(move || println!("{worker_title}"));
handle.join().expect("worker panicked");
println!("{title}");
// Output: Rust twice.
```

Arc does not make mutation safe.

## Mutex

```rust
use std::sync::{Arc, Mutex};

let count = Arc::new(Mutex::new(0));
let worker_count = Arc::clone(&count);
let handle = thread::spawn(move || {
    let mut guard = worker_count.lock().expect("mutex poisoned");
    *guard += 1;
});
handle.join().expect("worker panicked");
println!("{}", *count.lock().expect("mutex poisoned"));
// Output: 1
```

The guard unlocks on drop. Keep it out of network calls and callbacks.

## Poisoning

`std::sync::Mutex` becomes poisoned when a thread panics while holding it. The data may violate an invariant. Recover only after validating/repairing state; otherwise fail the operation/process boundary.

## RwLock

`RwLock<T>` permits several readers or one writer. It is not automatically faster; measure contention and starvation behavior.

## Atomics

```rust
use std::sync::atomic::{AtomicU64, Ordering};

let count = AtomicU64::new(0);
count.fetch_add(1, Ordering::Relaxed);
println!("{}", count.load(Ordering::Relaxed));
// Output: 1
```

Relaxed ordering is sufficient only when the counter has no synchronization role. Acquire/Release/SeqCst encode stronger ordering; use them from a proven algorithm, not guesses.

## Send and Sync

- `Send`: ownership can move to another thread
- `Sync`: shared references can be used across threads safely

These are unsafe auto traits. The compiler derives them from fields. `Rc`/`RefCell` are not thread-safe; `Arc`/`Mutex` can be when inner types qualify.

Never manually implement Send/Sync without a complete unsafe invariant proof.

## Worker Pool Shape

```mermaid
flowchart LR
    Producer -->|bounded jobs| Workers
    Workers -->|results| Collector
    Shutdown -.-> Producer
    Shutdown -.-> Workers
```

Define worker count, queue capacity, error propagation, panic behavior, and shutdown.

## Deadlock

Avoid:

- inconsistent lock order
- lock held while joining another thread
- lock held while sending to a bounded channel that needs a locked consumer
- nested unknown callbacks under lock

Document lock order and keep critical sections small.

## Thread Parking

`park`/`unpark`, barriers, condvars, and OnceLock solve specialized coordination. Channels and mutexes are clearer for most application code.

## Final Rules

- ownership before sharing
- bounded channels/workers
- join every owned thread
- propagate shutdown/errors
- Arc is ownership, Mutex is synchronization
- keep guards short
- atomics require memory-order reasoning
- Send/Sync unsafe implementations require expert proof
