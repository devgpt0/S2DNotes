# CPython Internals and Performance Roadmap

Read this section after Python fundamentals. Native extensions are the final step, not the first performance tool.

1. [CPython runtime internals](01-cpython-runtime-internals.md)
2. [Profiling and performance optimization](02-profiling-and-performance-optimization.md)
3. [Cython native extensions](03-cython-native-extensions.md)
4. [pybind11 C++ extensions](04-pybind11-cpp-extensions.md)

## Learning Flow

```text
source -> AST -> bytecode -> frames -> objects -> measured bottleneck
       -> Python optimization -> native boundary only when evidence requires it
```

## Ready-to-Continue Checks

Before Cython or pybind11, you should be able to:

- identify the hot function with a profiler;
- describe its input and output types exactly;
- write correctness tests and a benchmark;
- explain whether the bottleneck is CPU, allocation, I/O, locking, or an external dependency;
- show that a simpler algorithm or built-in operation is insufficient.

[Return to the Python programming roadmap](../00-python-programming-mastery-roadmap.md)

