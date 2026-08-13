# Multiprocessing and Process Pools

## 1. Processes provide isolated interpreters

Each process has its own Python interpreter and memory. This permits CPU
parallelism at the cost of startup, serialization, and inter-process
communication.

Use processes for sufficiently large, independent CPU-bound work. They are
usually wasteful for tiny operations or ordinary network waiting.

## 2. Protect the entry point

Worker code must be importable, and process creation belongs behind the main
guard. This is required for spawn-based execution and keeps imports from
recursively starting more workers.

```python
from concurrent.futures import ProcessPoolExecutor


def square(value: int) -> int:
    return value * value


def main() -> None:
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(square, [1, 2, 3, 4]))
    print(results)


if __name__ == "__main__":
    main()
```

Output:

```text
[1, 4, 9, 16]
```

`map()` preserves input order even when workers finish in another order.

## 3. Arguments and results must cross a process boundary

Pool work is serialized. Prefer top-level functions and small, serializable
values. Open files, locks, local functions, and many live service clients are
not valid portable work items.

```python
payload = {"record_id": 7, "values": [2, 3]}
print(payload["record_id"])
print(payload["values"])
```

Output:

```text
7
[2, 3]
```

The executor serializes supported values internally. Never deserialize untrusted
pickle data; pickle can execute attacker-controlled code.

## 4. Submit work and handle each failure explicitly

`Future.result()` returns the value or re-raises the worker exception.

```python
from concurrent.futures import ProcessPoolExecutor


def divide(pair: tuple[int, int]) -> float:
    left, right = pair
    return left / right


def main() -> None:
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(divide, pair) for pair in [(6, 2), (1, 0)]]
        for future in futures:
            try:
                print(future.result())
            except ZeroDivisionError as error:
                print(type(error).__name__)


if __name__ == "__main__":
    main()
```

Output:

```text
3.0
ZeroDivisionError
```

Catch only failures the caller can handle. Unexpected worker failures should
remain visible.

## 5. Size work to dominate overhead

Process startup and serialization can cost more than the calculation.

- Reuse a pool instead of creating one per item.
- Batch small records into meaningful units.
- Use `chunksize` with `map()` only after measuring representative data.
- Send identifiers or compact inputs instead of large object graphs.
- Avoid returning huge intermediate results when they can be reduced in workers.

## 6. Shared state is an explicit tradeoff

`multiprocessing.Queue`, pipes, shared memory, managers, and synchronization
primitives solve different problems. Prefer independent inputs and returned
results; shared mutable state adds coordination and cleanup risk.

Shared memory avoids copies but requires exact ownership, bounds, data-layout,
and unlinking rules.

## 7. Timeout, cancellation, and shutdown

- A timeout on `future.result(timeout=...)` stops waiting; it does not reliably
  stop a function already executing.
- `future.cancel()` succeeds only before the work starts.
- Exiting an executor context waits for submitted work by default.
- Design long-running computations as bounded chunks when cooperative stopping
  is required.
- On worker crashes, surface the broken-pool error and rebuild state explicitly.

## 8. Start methods and portability

Available start methods and their defaults depend on Python version and
platform. Do not force a start method inside a reusable library. Application
entry points may select one once, after verifying dependency compatibility.

Test the packaged application on every supported platform; interactive shells
and notebooks can behave differently because workers must import definitions.

## 9. Decision guide

| Situation | Choice |
| --- | --- |
| independent CPU-heavy Python calls | process pool |
| one long process with message protocol | `multiprocessing.Process` |
| blocking I/O | threads |
| many async I/O calls | `asyncio` |
| large shared numeric buffer | consider shared memory after measuring copies |
| tiny CPU task | synchronous code or batching |

## 10. Mental model

```text
parent -> serialize input -> worker interpreter -> compute -> serialize result -> parent
```
