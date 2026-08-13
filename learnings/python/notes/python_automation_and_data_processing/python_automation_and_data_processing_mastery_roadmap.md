# Python Automation and Data Processing - Roadmap

## 1. Core rule

Automation must be safe to rerun, explicit at external boundaries, bounded in
resource use, and observable when it fails.

```text
validate input -> plan -> dry run -> bounded execution -> atomic output -> report
```

## 2. Study order

| Order | Note | Responsibility |
| ---: | --- | --- |
| 1 | `iterators.md` | iteration protocol and one-pass state |
| 2 | `generators.md` | lazy producers, delegation, and cleanup |
| 3 | `json.md` | structured interchange and strict validation |
| 4 | `csv.md` | streaming tables and schema conversion |
| 5 | `pathlib.md` | readable path and file operations |
| 6 | `os_module.md` | environment, descriptors, and OS boundaries |
| 7 | `datetime.md` | aware time, zones, durations, and serialization |
| 8 | `basic_scripting_and_automation.md` | command boundaries and repeatable changes |

Collections and file-handling fundamentals should be understood before this
series. Concurrency notes own parallel execution and backpressure across workers.

## 3. Data-flow decisions

| Need | First choice |
| --- | --- |
| reusable in-memory values | collection |
| one-pass transformation | iterator or generator |
| nested interoperable record | JSON |
| flat tabular interchange | CSV |
| very large JSON document | newline-delimited JSON or a streaming parser |
| path manipulation | `pathlib` |
| low-level OS operation | `os` |
| civil-time rule | aware `datetime` plus `zoneinfo` |
| elapsed duration | monotonic clock |

## 4. Production checklist

- Validate types and values without implicit coercion.
- Bound file size, row count, field size, nesting, memory, and execution time.
- Use explicit encodings and newline rules.
- Reject path traversal and define symlink behavior.
- Keep secrets out of logs, process arguments, and generated files.
- Make changes idempotent; use dry runs for destructive plans.
- Write outputs atomically and define partial-failure behavior.
- Preserve row, item, or operation context in actionable errors.

## 5. Failure model

| Failure | Required behavior |
| --- | --- |
| invalid record | fail with record location and exact contract |
| malformed configuration | stop before changing state |
| missing permission | surface the specific OS error |
| partial output | discard temporary output or resume from a documented checkpoint |
| duplicate execution | converge through idempotency or reject through a lock |
| external command timeout | terminate according to policy and report captured context safely |

## 6. Completion standard

You understand the series when you can design a script that streams large input,
validates every boundary, previews changes, writes atomically, handles time zones
correctly, and produces the same intended state after a safe rerun.
