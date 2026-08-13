# Cython Native Extensions

## 1. Use Cython only for a measured hot path

Cython translates Python-like source into C and builds a native extension.
Static Cython types can remove Python object and dispatch overhead, but an
untyped `.pyx` file is not automatically faster.

Keep validation and orchestration in Python unless profiling identifies them as
hot. Compile the smallest stable computation boundary.

## 2. Minimal project

```text
fastsum/
|-- pyproject.toml
|-- setup.py
`-- fastsum.pyx
```

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools", "Cython"]
build-backend = "setuptools.build_meta"
```

`setup.py`:

```python
from setuptools import setup

from Cython.Build import cythonize

setup(
    name="fastsum",
    ext_modules=cythonize("fastsum.pyx", language_level="3"),
)
```

`fastsum.pyx`:

```cython
def sum_integers(list values):
    cdef Py_ssize_t index
    cdef long total = 0

    for index in range(len(values)):
        total += values[index]
    return total
```

Build in the project directory:

```bash
python -m pip install .
```

The compiler and installer output and the extension filename are
platform-dependent. A successful build installs an importable `fastsum` module.

After installation:

```python
from fastsum import sum_integers

print(sum_integers([1, 2, 3, 4]))
```

Output:

```text
10
```

This import example is contextual; it requires the preceding build.

## 3. Type the hot variables

`cdef` declares Cython-only implementation variables. `def` keeps a normal
Python-callable boundary. Use `cpdef` only when the function needs both Python
and efficient Cython dispatch.

Typed memoryviews accept compatible buffer objects without requiring a Python
object operation for every element.

```cython
def sum_doubles(const double[:] values):
    cdef Py_ssize_t index
    cdef double total = 0.0

    for index in range(values.shape[0]):
        total += values[index]
    return total
```

The `const` view prevents writes through this view; it does not make the source
buffer globally immutable.

## 4. Validate at the boundary

Python callers can still supply invalid types, shapes, or values. Define the
public contract and fail immediately with a specific exception.

```cython
def positive_sum(const long[:] values):
    cdef Py_ssize_t index
    cdef long total = 0

    for index in range(values.shape[0]):
        if values[index] < 0:
            raise ValueError("values must be non-negative")
        total += values[index]
    return total
```

Do not silently cast arbitrary external input merely to satisfy a C type.

## 5. Releasing the GIL is a correctness decision

Code in a `nogil` region cannot freely use Python objects or Python APIs.
Release the GIL only around independent C-level work, then verify thread safety
for every accessed native resource.

```cython
cdef long square(long value) noexcept nogil:
    return value * value
```

`nogil` does not create a thread, schedule work, or make shared state safe.

## 6. Failure and maintenance rules

- Pin compatible build dependencies for reproducible releases.
- Build wheels for every supported Python version, ABI, and platform.
- Run tests against the built wheel, not only an in-place extension.
- Keep a Python reference implementation when it materially improves testing.
- Benchmark end-to-end behavior; Python-to-native conversion can dominate small work.
- Treat compiler warnings and sanitizer failures as release blockers.

## 7. Decision guide

| Situation | Choice |
| --- | --- |
| hot numeric loop in Python-like code | consider Cython |
| existing C++ library | prefer pybind11 |
| bottleneck is I/O or algorithm choice | fix that first |
| tiny infrequent operation | keep Python |
| team cannot own native builds | use a maintained native library or keep Python |

## 8. Mental model

```text
profile -> isolate hot loop -> add narrow types -> build -> test -> benchmark
```
