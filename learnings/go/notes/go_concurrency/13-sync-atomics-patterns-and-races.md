# 13 - Mutexes, Atomics, Concurrency Patterns, and Races

## Data Race

A race occurs when goroutines access the same memory concurrently, at least one access writes, and synchronization does not order them.

```go
// Unsafe:
count := 0
go func() { count++ }()
go func() { count++ }()
```

The final result is not reliable.

## Mutex

```go
type Counter struct {
	mu    sync.Mutex
	value int
}

func (counter *Counter) Increment() {
	counter.mu.Lock()
	defer counter.mu.Unlock()
	counter.value++
}

func (counter *Counter) Value() int {
	counter.mu.Lock()
	defer counter.mu.Unlock()
	return counter.value
}
```

The mutex protects the invariant across every access. Do not copy a mutex after use.

## Read-Write Mutex

`sync.RWMutex` permits several readers or one writer. It can be slower than `Mutex` and should be chosen from measured contention/read patterns.

## Atomics

```go
var count atomic.Int64
count.Add(1)
fmt.Println(count.Load())
// Output: 1
```

Atomics suit simple independent counters/flags and carefully designed algorithms. They do not automatically protect multi-field invariants.

## `sync.Once`

```go
var once sync.Once
var configuration Config

func Configuration() Config {
	once.Do(func() {
		configuration = loadConfig()
	})
	return configuration
}
```

If initialization can fail or needs reset, explicit startup construction is usually clearer.

## `sync.Map`

Use `sync.Map` for its documented specialized patterns, not as a default replacement for `map` plus mutex. Typed maps are clearer and often faster for ordinary workloads.

## Condition Variables

`sync.Cond` coordinates goroutines waiting for a condition under a lock. Channels are usually simpler for event/data flow. Always wait in a loop because wake-up means “recheck,” not “condition guaranteed.”

## Semaphore

A buffered channel can limit concurrent work:

```go
sem := make(chan struct{}, 4)

run := func(ctx context.Context, job Job) error {
	select {
	case sem <- struct{}{}:
		defer func() { <-sem }()
	case <-ctx.Done():
		return ctx.Err()
	}
	return process(ctx, job)
}
```

Capacity must come from downstream limits and measurements.

## Fan-Out/Fan-In

- fan-out: several workers read jobs
- fan-in: results combine into one stream

Ensure one goroutine closes the result channel after all workers finish.

## Errgroup Pattern

For related goroutines that should cancel after one failure, a maintained errgroup implementation from the Go ecosystem is commonly used. The standard design principles remain: first error, shared cancellation, wait for all goroutines, bounded concurrency.

## Deadlock

Deadlock can result from:

- inconsistent lock order
- sending with no receiver
- receiving forever
- waiting on yourself
- holding a lock while calling unknown blocking code

Keep lock order documented and critical sections small.

## Livelock and Starvation

- livelock: goroutines keep reacting but make no progress
- starvation: one goroutine rarely gets a resource

Fairness is not automatically guaranteed. Measure latency distributions and contention.

## Race Detector

```powershell
go test -race ./...
go run -race .
```

It observes executed paths. Add concurrent stress tests around real shared state.

## Memory Model

Synchronization establishes happens-before relationships. Important examples include channel send/receive, channel close observation, mutex unlock/lock, atomic operations, and goroutine start rules.

Do not reason from wall-clock timing or `time.Sleep`.

## Ownership Decision

```text
One owner goroutine? -> channels/messages
Small shared invariant? -> mutex
Single counter/flag? -> atomic if contract fits
Immutable snapshot? -> atomic pointer/value or locked replacement
```

## Final Rules

- race-free is a correctness requirement
- protect complete invariants
- no sleeps for synchronization
- no locks across network/user callbacks
- bound goroutines and queues
- profile contention before choosing specialized primitives
- test cancellation and shutdown
