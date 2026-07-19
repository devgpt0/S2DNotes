# Specialized Sequence Types: `array`, `bytes`, `bytearray`, `memoryview`

These are important when performance, binary data, or memory footprint matters.

## 1) `array.array` - Typed Numeric Sequences

```python
from array import array

nums = array("i", [1, 2, 3])  # signed int
nums.append(4)
print(nums.tolist())
```

Why use:
- more compact than Python object-heavy list for numeric primitives.
- useful in low-level I/O and memory-sensitive workloads.

## 2) `bytes` vs `bytearray`

- `bytes`: immutable sequence of integers [0..255]
- `bytearray`: mutable version

```python
raw = b"ABC"          # bytes
buf = bytearray(raw)  # mutable
buf[0] = ord("Z")
print(bytes(buf))     # b'ZBC'
```

## 3) `memoryview` for Zero-Copy Slicing

`memoryview` allows viewing buffer-protocol objects without copying.

```python
data = bytearray(b"abcdefgh")
mv = memoryview(data)
part = mv[2:6]      # no copy
part[0] = ord("X")
print(data)         # bytearray(b'abXdefgh')
```

Use cases:
- binary protocol parsing
- high-throughput file/network processing
- avoiding unnecessary memory copies

## 4) Choosing Between List and Specialized Sequences

- general app logic: `list`
- typed numeric storage: `array.array`
- immutable binary payload: `bytes`
- mutable binary buffer: `bytearray`
- zero-copy view/processing: `memoryview`

## 5) Pitfalls

- mixing text (`str`) and binary (`bytes`) incorrectly.
- assuming `memoryview` makes data immutable (it reflects underlying mutability).
- forgetting type codes in `array.array` constrain element types.
