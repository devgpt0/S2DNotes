# Concurrency Debugging and Observability

## 1. Observe work by stable identifiers

Concurrent logs interleave. Attach a non-sensitive operation identifier and an
event name so records can be grouped without depending on output order.

```python
import logging
import sys

logging.basicConfig(format="%(message)s", level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

operation_id = "job-7"
logger.info("operation=%s event=started", operation_id)
logger.info("operation=%s event=completed", operation_id)
```

Output:

```text
operation=job-7 event=started
operation=job-7 event=completed
```

Logging normally writes to standard error. Never log secrets, payload bodies,
or personal data merely to debug concurrency.

## 2. Measure saturation, not only failures

Useful signals include:

- active and configured workers;
- queue depth and queue-wait duration;
- task duration and end-to-end latency percentiles;
- timeout, cancellation, rejection, and retry counts;
- event-loop lag;
- process restarts and broken-pool errors;
- deadlock or stuck-work watchdog events.

Counters must have bounded label cardinality. Do not use request IDs as metric
labels.

## 3. Make task results observable

Un-awaited tasks can hide failures. Structured concurrency owns child tasks and
propagates errors.

```python
import asyncio


async def calculate(value: int) -> int:
    await asyncio.sleep(0)
    return value * 2


async def main() -> None:
    async with asyncio.TaskGroup() as group:
        task = group.create_task(calculate(4), name="calculate-4")

    print(task.get_name())
    print(task.result())


asyncio.run(main())
```

Output:

```text
calculate-4
8
```

Names aid diagnosis but are not authorization or uniqueness mechanisms.

## 4. Enable asyncio diagnostics in development

Run a development or test workload with debug mode:

```bash
PYTHONASYNCIODEBUG=1 python app.py
```

On PowerShell:

```powershell
$env:PYTHONASYNCIODEBUG = "1"
python app.py
```

Warnings and timing details depend on the program. Debug mode adds overhead and
does not replace application metrics.

## 5. Diagnose stuck threads

`faulthandler.dump_traceback_later()` can emit all thread stacks after a delay.
Use it in a controlled diagnostic environment because stack traces may contain
sensitive values or paths.

```python
import faulthandler

faulthandler.dump_traceback_later(30, repeat=False)
# Run the suspected operation.
faulthandler.cancel_dump_traceback_later()
```

This contextual fragment intentionally has no fixed output: output occurs only
if the timeout expires.

For deadlocks, map which thread owns each lock and which lock it is waiting for.
A thread dump shows the symptom; consistent lock ordering fixes the design.

## 6. Profile the correct resource

| Symptom | Evidence |
| --- | --- |
| high CPU | process and function CPU profile |
| slow with low CPU | I/O timing, queue wait, dependency latency |
| event loop stalls | event-loop lag and blocking stack |
| growing memory | queue depth, task count, allocation snapshots |
| poor process scaling | serialization size, worker CPU, task duration |

Measure with representative concurrency. A single-user profile can miss lock
contention, pool saturation, and queue growth.

## 7. Reproduce races deliberately

- Remove unrelated work and keep the failing shared state.
- Use barriers or events to force the suspected ordering in a test.
- Repeat the test, but never treat repetition alone as proof of safety.
- Assert invariants after every synchronization boundary.
- Fix ownership or synchronization; do not add arbitrary sleeps.

## 8. Incident checklist

1. Confirm impact and stop unbounded admission.
2. Capture queue, worker, task, dependency, and resource metrics.
3. Capture sanitized task or thread stacks.
4. Identify the owner that failed to complete or release a resource.
5. Reproduce with controlled ordering.
6. Fix the ownership, bound, timeout, or synchronization rule.
7. Add a regression test and an alert for the earliest reliable symptom.

## 9. Mental model

```text
stable context + bounded metrics + owned tasks + captured stacks -> explainable failure
```
