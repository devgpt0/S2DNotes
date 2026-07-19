# Python Programming - Beginner to Expert Roadmap

This roadmap connects Python syntax, runtime internals, concurrency, typing, packaging, performance, and native extensions into one learning path.

## How to Study

For every example:

1. predict the output;
2. run it with Python 3.12 or newer;
3. explain each object, reference, call, and failure path;
4. change one input and predict the new result;
5. run the relevant formatter, linter, type checker, and tests.

```text
syntax -> object model -> protocols -> runtime internals -> concurrency
       -> profiling -> native optimization -> packaging and delivery
```

## Phase 1 - Python Fundamentals

Start with the [Python fundamentals roadmap](python_fundamentals/00_python_fundamentals_mastery_roadmap.md).

It covers variables, objects, data types, control flow, functions, errors, iterators, generators, context managers, imports, typing, files, and packaging.

## Phase 2 - Object-Oriented Python

Continue with the [OOP and clean-code roadmap](oops_and_clean_code/00_oops_clean_code_mastery_roadmap.md).

It covers classes, encapsulation, composition, inheritance, protocols, SOLID, object lifecycle, descriptors, class creation, and metaclasses.

## Phase 3 - Concurrency

Continue with the [concurrency roadmap](python_sync_async_multithreaded/00_concurrency_mastery_roadmap.md).

It covers:

- synchronous execution;
- asyncio and structured concurrency;
- multithreading and the GIL;
- multiprocessing and process pools;
- timeouts, cancellation, backpressure, debugging, and shutdown.

## Phase 4 - CPython and Performance

Finish with the [CPython internals and performance roadmap](python_internals_and_performance/00-cpython-performance-roadmap.md).

It covers:

- CPython compilation, bytecode, frames, and evaluation;
- reference counting, cyclic garbage collection, allocators, and the GIL;
- profiling and evidence-based optimization;
- Cython native compilation;
- pybind11 C++ extensions.

## Requested Topic Coverage

| Topic | Primary note |
|---|---|
| Python internals | [CPython runtime internals](python_internals_and_performance/01-cpython-runtime-internals.md) |
| CPython implementation | [CPython runtime internals](python_internals_and_performance/01-cpython-runtime-internals.md) |
| Memory management | [Python memory model](python_fundamentals/MemoryModel.md) |
| GIL | [CPython runtime internals](python_internals_and_performance/01-cpython-runtime-internals.md) and [threading fundamentals](python_sync_async_multithreaded/Multithreading%20in%20Python%20-%20Fundamentals.md) |
| Asyncio | [Asyncio fundamentals](python_sync_async_multithreaded/Async%20Programming%20in%20Python%20-%20asyncio%20Fundamentals.md) |
| Multiprocessing | [Multiprocessing and process pools](python_sync_async_multithreaded/10_multiprocessing_and_process_pools.md) |
| Multithreading | [Multithreading fundamentals](python_sync_async_multithreaded/Multithreading%20in%20Python%20-%20Fundamentals.md) |
| Generators and iterators | [Iterators, generators, and context managers](python_fundamentals/11_iterators_generators_context_managers.md) |
| Decorators | [Functions and decorators](python_fundamentals/function.md) |
| Context managers | [Iterators, generators, and context managers](python_fundamentals/11_iterators_generators_context_managers.md) |
| Metaclasses | [Class creation, descriptors, and metaclasses](oops_and_clean_code/15_class_creation_descriptors_and_metaclasses.md) |
| Profiling | [Profiling and optimization](python_internals_and_performance/02-profiling-and-performance-optimization.md) |
| Performance optimization | [Profiling and optimization](python_internals_and_performance/02-profiling-and-performance-optimization.md) |
| Cython | [Cython](python_internals_and_performance/03-cython-native-extensions.md) |
| pybind11 | [pybind11](python_internals_and_performance/04-pybind11-cpp-extensions.md) |
| Type hints | [Type hints and static analysis](python_fundamentals/13_type_hints_static_analysis_mastery.md) |
| Ruff and mypy | [Type hints and static analysis](python_fundamentals/13_type_hints_static_analysis_mastery.md) |
| Packaging | [Modern Python packaging](python_fundamentals/15_modern_packaging_pyproject_wheels.md) |

## Completion Standard

You can explain how source becomes executed bytecode, trace object lifetime, choose the correct concurrency model, design typed APIs, profile before optimizing, build native extensions only when justified, and publish a reproducible wheel without relying on hidden local state.

