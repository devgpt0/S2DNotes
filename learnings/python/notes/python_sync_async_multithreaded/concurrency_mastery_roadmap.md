# Python Concurrency - Roadmap

## 1. Core rule

Choose a concurrency model from the work being performed, not from the number
of users or tasks.

| Work | First choice |
| --- | --- |
| short, ordered, simple work | synchronous code |
| many operations waiting on async APIs | `asyncio` |
| blocking I/O libraries | threads or `asyncio.to_thread()` |
| CPU-heavy pure Python | processes |
| existing native code that releases the GIL | measure threads and processes |

## 2. Study order

1. `Synchronous Programming in Python.md`
2. `Async Programming in Python - asyncio Fundamentals.md`
3. `Async Programming in Python - Advanced and Structured Concurrency.md`
4. `Multithreading in Python - Fundamentals.md`
5. `Multithreading in Python - Advanced and ThreadPoolExecutor.md`
6. `multiprocessing_and_process_pools.md`
7. `reliability_timeouts_retries_backpressure.md`
8. `concurrency_design_patterns.md`
9. `async_thread_process_integration.md`
10. `concurrency_debugging_profiling_observability.md`

Use `Sync vs Async vs Multithreading - Interview Decision Guide.md` and
`Python Concurrency Interview Questions and Answers.md` for revision after the
implementation notes.

## 3. Terms

| Term | Meaning |
| --- | --- |
| concurrency | multiple tasks make progress during overlapping time |
| parallelism | multiple tasks execute at the same instant |
| blocking | the current worker cannot make other progress while waiting |
| race condition | result depends on uncontrolled operation order |
| backpressure | producers are slowed or rejected when capacity is full |
| cancellation | a request for cooperative early termination |

## 4. Required design questions

- Is the work CPU-bound or waiting on I/O?
- Is the called API synchronous or asynchronous?
- What is the maximum allowed concurrency and queue size?
- Which task owns each resource and mutable value?
- How do timeout, cancellation, failure, and shutdown propagate?
- Is retry safe for this operation?
- Which metrics reveal saturation or stuck work?

## 5. Safety rules

- Bound workers, tasks, and queues.
- Put timeouts at remote and queue boundaries.
- Share immutable data or use message passing where possible.
- Never block the event-loop thread.
- Protect multiprocessing entry points with `if __name__ == "__main__":`.
- Drain or cancel owned work during shutdown.
- Do not assume cancellation stops a thread or process already running.

## 6. Mental model

```text
workload -> model -> capacity bound -> failure policy -> shutdown -> observability
```

Ownership is the connecting rule: the component that creates a task, worker,
queue, lock, or executor must define how its results are observed and how it is
closed during normal completion, failure, cancellation, and shutdown.
