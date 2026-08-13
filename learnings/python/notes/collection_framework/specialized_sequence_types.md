# Specialized Sequence Types
## 1. Core truth

These sequence types are for situations where plain `list` is not the best fit.
Use them when you need compact numeric storage, binary data, or zero-copy access.

```python
from array import array

nums = array("i", [1, 2, 3])
nums.append(4)
print(nums.tolist())
```

Output:

```text
[1, 2, 3, 4]
```

`array("i")` stores signed integers, and `append(4)` adds one more value to the sequence.

## 2. Binary and numeric sequence foundations

### `array.array` stores one numeric type efficiently

```python
from array import array

nums = array("i", [1, 2, 3])
nums.append(4)

print(nums.tolist())
```

Output:

```text
[1, 2, 3, 4]
```

The type code `"i"` means signed integer, so the array accepts integers and keeps them in a compact form.

Practical takeaway: use `array` when you need a compact numeric sequence and all items share one type.

### `bytes` is immutable, `bytearray` is mutable

```python
raw = b"ABC"
buf = bytearray(raw)
buf[0] = ord("Z")

print(raw)
print(bytes(buf))
```

Output:

```text
b'ABC'
b'ZBC'
```

`bytes` cannot be changed in place, but `bytearray` can.

Practical takeaway: use `bytes` for read-only payloads and `bytearray` when you need to edit the data.

### `memoryview` lets you view data without copying it

```python
data = bytearray(b"abcdefgh")
part = memoryview(data)[2:6]
part[0] = ord("X")

print(data)
print(bytes(part))
```

Output:

```text
bytearray(b'abXdefgh')
b'Xdef'
```

`memoryview` points at the original buffer, so changing the slice changes the original data too.

Practical takeaway: use `memoryview` when you want to avoid unnecessary copies.

## 3. Specialized sequence APIs

### `array.array`

- `append()` adds one typed item.
- `extend()` adds many typed items.
- `tolist()` converts to a regular list for display or debugging.

### `bytes`

- Slicing returns another `bytes` object.
- Concatenation creates a new immutable value.

### `bytearray`

- `append()` and `extend()` mutate the buffer.
- Item assignment changes a single byte.

### `memoryview`

- Slicing usually creates another view, not a copy.
- The view reflects changes in the underlying buffer.

```python
buf = bytearray(b"hi")
buf.extend(b"!")
print(buf)
```

Output:

```text
bytearray(b'hi!')
```

## 4. Practical binary-data patterns

### Example 1: Store integers compactly

```python
from array import array

values = array("i", [10, 20, 30])
values.append(40)

print(values.tolist())
```

Output:

```text
[10, 20, 30, 40]
```

### Example 2: Edit binary data safely

```python
payload = bytearray(b"HELLO")
payload[1] = ord("A")

print(bytes(payload))
```

Output:

```text
b'HALLO'
```

### Example 3: Read a slice without copying

```python
data = bytearray(b"abcdefgh")
window = memoryview(data)[3:6]

print(bytes(window))
```

Output:

```text
b'def'
```

- Use `array` for numeric data where memory matters.
- Use `bytes` for file contents, protocol packets, and other read-only binary payloads.
- Use `bytearray` when you need to build or modify binary content.
- Use `memoryview` when you want to inspect or edit a slice without copying.

## 5. Type and mutation mistakes

### Mistake 1: Mixing text and binary data

`str` is text. `bytes` is binary. They are not interchangeable.

### Mistake 2: Treating `bytes` like a mutable sequence

```python
from typing import Any

payload = b"ABC"
unsafe_payload: Any = payload

try:
    unsafe_payload[0] = 90
except TypeError as error:
    print(f"{type(error).__name__}: {error}")
```

Output:

```text
TypeError: 'bytes' object does not support item assignment
```

Correct approach:

```python
payload = bytearray(b"ABC")
payload[0] = 90
print(bytes(payload))
```

Output:

```text
b'ZBC'
```

### Mistake 3: Assuming `memoryview` makes a copy

It usually does not. It points at the original buffer.

### Mistake 4: Forgetting that `array` has a type code

The type code decides what kind of values the array can store.

## 6. Sequence decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| General-purpose sequence | `list` | Flexible and familiar | You need compact numeric storage |
| Compact numbers of one type | `array.array` | Lower overhead for typed data | Your items are mixed types |
| Read-only binary payload | `bytes` | Immutable and safe to share | You need in-place edits |
| Mutable binary payload | `bytearray` | Easy to modify | You need an immutable value |
| No-copy slice into data | `memoryview` | Avoids extra allocation | You need a completely independent copy |

Selection rule:

- Start with `list` for general app logic.
- Move to `array` for compact numeric data.
- Use `bytes` for immutable binary content.
- Use `bytearray` when the content must change.
- Use `memoryview` when copying would be wasteful.

## 7. Performance and safety

| Type | Strength | Limitation |
| --- | --- | --- |
| `array` | Compact numeric storage | One type only |
| `bytes` | Immutable and hashable | Cannot be edited in place |
| `bytearray` | Mutable binary buffer | Still a binary type, not text |
| `memoryview` | Zero-copy access | The underlying data still controls mutability |

Best practices:

- Convert to text only with an explicit encoding step.
- Use `bytes` when sharing read-only binary data.
- Use `bytearray` when you need repeated edits.
- Use `memoryview` for performance-sensitive binary processing.

## 8. Buffer protocol behavior

### Buffer sharing

`memoryview` is powerful because it lets multiple objects refer to the same underlying data.
That is useful in parsers, file readers, and networking code where copying large payloads would be expensive.

### Type codes in `array`

The type code controls the item type, so choose it carefully.

## 9. Mental model

| Need | Use | Remember |
| --- | --- | --- |
| Compact numeric data | `array` | One fixed type |
| Immutable binary data | `bytes` | Safe to share |
| Mutable binary data | `bytearray` | Editable in place |
| No-copy slice | `memoryview` | Views the same buffer |

## 10. Memory layout and casting

`memoryview.cast()` reinterprets the same contiguous bytes with a compatible
element format; it does not convert numeric values.

```python
from array import array

values = array("I", [1, 2])
view = memoryview(values)
byte_view = view.cast("B")

print(view.contiguous)
print(byte_view.nbytes == view.nbytes)
```

Output:

```text
True
True
```

Element size, byte order, alignment, shape, and contiguity are part of the
binary contract. Copy with `tobytes()` when a stable independent snapshot is
required, and release long-lived views before resizing the underlying buffer.
