# Cython Native Extensions

Cython compiles Python-like source into C or C++ extension modules. It is useful when profiling identifies a stable CPU-heavy loop or when a C library must be wrapped.

Do not begin with Cython. First improve the algorithm and try clear built-ins or appropriate maintained libraries.

## 1. What Cython Changes

```text
.pyx source -> Cython generates C/C++ -> native compiler -> platform extension module
```

Ordinary dynamic Python operations can remain dynamic. Static Cython declarations allow selected operations to use C representations and loops.

## 2. Complete Project

This example calculates the mean of a contiguous `array('d')` without copying its data.

```text
cython-stats/
|-- pyproject.toml
|-- setup.py
|-- src/
|   `-- fast_stats.pyx
`-- tests/
    `-- test_fast_stats.py
```

## 3. `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=75", "wheel", "Cython>=3.0"]
build-backend = "setuptools.build_meta"

[project]
name = "cython-stats-example"
version = "0.1.0"
requires-python = ">=3.12"
```

The build requirements belong in an isolated build environment. An application should constrain exact versions through its reviewed dependency process; a published library normally declares compatible ranges.

## 4. `setup.py`

```python
from setuptools import Extension, setup

from Cython.Build import cythonize


extensions = [
    Extension(
        name="fast_stats",
        sources=["src/fast_stats.pyx"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "boundscheck": True,
            "language_level": 3,
            "wraparound": False,
        },
    )
)
```

`boundscheck` remains enabled in this first implementation. Disabling it can turn an indexing bug into memory corruption. Remove safety checks only when tests, invariants, and profiling justify the risk.

`wraparound=False` rejects reliance on negative indexing in generated C-level indexing paths.

## 5. `src/fast_stats.pyx`

```cython
cdef double _sum_values(const double[::1] values) noexcept nogil:
    cdef Py_ssize_t index
    cdef double total = 0.0

    for index in range(values.shape[0]):
        total += values[index]

    return total


cpdef double mean(const double[::1] values):
    cdef Py_ssize_t count = values.shape[0]
    cdef double total

    if count == 0:
        raise ValueError("values must not be empty")

    with nogil:
        total = _sum_values(values)

    return total / count
```

Read the declarations:

- `double[::1]` is a typed, one-dimensional, contiguous memory view;
- `const` prevents mutation through this view;
- `Py_ssize_t` is the correct signed index-size type for Python containers;
- `cdef` creates Cython/C-level declarations;
- `cpdef` creates a Python-callable function with a Cython-callable entry;
- `nogil` means the helper can execute without the CPython GIL;
- `noexcept` says the helper does not raise Python exceptions.

The wrapper validates emptiness while holding the GIL. Only the numeric loop releases it.

## 6. `tests/test_fast_stats.py`

```python
from array import array

import pytest

from fast_stats import mean


def test_mean_returns_expected_value() -> None:
    values = array("d", [10.0, 20.0, 30.0])

    assert mean(values) == 20.0


def test_mean_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        mean(array("d"))
```

The tests verify behavior through the Python API. Add numerical-tolerance tests when floating-point rounding is relevant.

## 7. Build and Test

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install build pytest
.venv\Scripts\python -m build
.venv\Scripts\python -m pip install --force-reinstall (Get-ChildItem dist\*.whl | Select-Object -First 1)
.venv\Scripts\python -m pytest
```

Build tools need a compatible C compiler. On Windows, that normally means the supported Microsoft C/C++ Build Tools for the target Python release.

## 8. Use It

```python
from array import array

from fast_stats import mean

values = array("d", [2.0, 4.0, 6.0])
print(mean(values))
```

Output:

```text
4.0
```

A Python list does not expose the same contiguous double buffer. The API rejects incompatible input instead of silently converting and hiding a copy.

## 9. Python Objects Versus C Values

```cython
def dynamic_sum(values: object) -> object:
    total = 0
    for value in values:
        total += value
    return total
```

This remains mostly dynamic Python behavior even though Cython compiles it.

```cython
cpdef long long integer_sum(const long long[::1] values):
    cdef Py_ssize_t index
    cdef long long total = 0

    for index in range(values.shape[0]):
        total += values[index]

    return total
```

The second version uses C integers, but signed overflow becomes a design concern. Native speed also introduces native correctness responsibilities.

## 10. GIL Rules

Code running `nogil` must not use Python objects or Python APIs unless it reacquires the GIL.

Usually safe without the GIL:

- arithmetic on C values;
- indexing a valid typed memory view under proven bounds;
- calling a declared `nogil` C function;
- loops that cannot raise Python exceptions.

Requires the GIL:

- creating or modifying Python objects;
- reference-count operations;
- raising a Python exception;
- most Python attribute or container operations;
- calling ordinary Python functions.

Releasing the GIL enables parallel native work; it does not make shared memory thread-safe.

## 11. Exception Contracts

A Cython C-level function needs a clear exception contract. An exception check inside a tight loop can force GIL interaction and reduce performance.

Validate at the Python boundary, keep the kernel small, and use `noexcept` only when the function genuinely cannot fail through Python exceptions.

## 12. Memory-View Lifetime

The exported memory view keeps its base object alive for the call. Never retain a raw pointer beyond the base object's valid lifetime. If native work continues asynchronously, define and enforce ownership explicitly.

## 13. Wrapping a C Library

Declare only the required external API:

```cython
cdef extern from "math.h":
    double sqrt(double value) nogil


cpdef double root(double value):
    if value < 0:
        raise ValueError("value must be non-negative")
    return sqrt(value)
```

The external header and ABI must be available for every build target. Validate domain rules before calling C.

## 14. Benchmark Correctly

Compare:

- the same algorithm and input representation;
- a warmed installed release wheel;
- several representative sizes;
- total boundary-conversion cost;
- single-threaded and intended parallel workloads;
- correctness results before timing.

If converting a Python list into a native buffer costs more than the loop saves, the extension is not a win for that call shape.

## 15. Distribution

A compiled extension wheel is platform-, architecture-, and Python-ABI-specific. Build wheels in clean CI environments for each supported target.

Use platform tooling such as `cibuildwheel` when a project genuinely supports a target matrix. Test each produced wheel in a clean environment. Do not upload an untested local compiler artifact.

## 16. Debugging

- keep a small pure-Python reference implementation;
- test boundary sizes: empty, one item, maximum expected input;
- run native sanitizers where supported;
- generate annotated Cython output to identify Python interaction;
- retain symbols in diagnostic builds;
- treat crashes as native memory bugs, not catchable Python exceptions.

Generate an annotation report:

```powershell
cython -a src\fast_stats.pyx
```

Yellow regions in the HTML report indicate Python C-API interaction. They are investigation targets, not automatic defects.

## Final Rules

- profile before introducing Cython;
- type the hot kernel rather than translating the whole application;
- validate at the Python boundary;
- keep bounds checks until proven safe to remove;
- release the GIL only around Python-free work;
- include conversion and allocation cost in benchmarks;
- keep a tested reference implementation;
- build and test wheels for every supported platform.
