# CPython Internals and Performance - Roadmap

## 1. Core rule

Correctness comes first. Measure a representative workload, change the proven
bottleneck, then measure again.

```text
correct program -> representative measurement -> bottleneck -> one change -> verification
```

## 2. Study order

| Order | Note | Responsibility |
| ---: | --- | --- |
| 1 | `cpython-runtime-internals.md` | implementation model and its practical costs |
| 2 | `profiling-and-performance-optimization.md` | CPU, wall-time, memory, and benchmark workflow |
| 3 | `cython-native-extensions.md` | compile measured Python/Cython hot paths |
| 4 | `pybind11-cpp-extensions.md` | expose an existing or justified C++ implementation |

The fundamentals notes own Python's language model. These notes discuss
CPython implementation behavior and optimization choices.

## 3. Decision guide

| Evidence | First action |
| --- | --- |
| slow algorithm | choose a better algorithm or data structure |
| repeated I/O wait | use batching, caching, or an appropriate concurrency model |
| high allocation rate | reduce unnecessary objects and copies |
| hot Python loop | try a built-in operation, then consider Cython |
| existing C++ library | expose a narrow API with pybind11 |
| no measured bottleneck | do not optimize |

## 4. Required evidence

- State the workload, input size, Python version, platform, and dependency versions.
- Use production-like data without exposing sensitive information.
- Record a baseline and multiple runs; a single duration is not evidence.
- Verify output and tests before comparing speed.
- Include build, packaging, deployment, and debugging cost in native-code decisions.

## 5. Completion checklist

You are ready to optimize when you can answer all five questions:

1. Which metric is failing?
2. Which measured function or allocation dominates it?
3. What simpler change was tried first?
4. How will correctness and performance regressions be detected?
5. Is the improvement worth its maintenance cost?

## 6. Mental model

| Stage | Question |
| --- | --- |
| Observe | What is slow or memory-heavy? |
| Locate | Where is the measured cost? |
| Change | What is the smallest correct improvement? |
| Verify | Did results stay correct? |
| Compare | Did the target metric improve consistently? |
