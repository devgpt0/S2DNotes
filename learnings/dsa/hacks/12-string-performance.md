# Fast String Construction and Parsing

## First principles

Python strings are immutable. Every apparent modification creates a new string.
Repeatedly growing a long string can copy the already-built prefix many times;
collect pieces and join once.

## Why it matters

Strings are immutable. Repeated concatenation can copy an ever-growing prefix
and become quadratic.

## Technique

Collect pieces, then join once:

```python
pieces: list[str] = []
for value in values:
    pieces.append(str(value))
answer = ','.join(pieces)
```

For character edits, use a list:

```python
characters = list(text)
characters[index] = replacement
text = ''.join(characters)
```

Parse tokens as bytes when decoding is unnecessary:

```python
tokens = sys.stdin.buffer.read().split()
if tokens[0] == b'YES':
    ...
```

## Pattern recognition

Watch string costs in builders, recursive substring algorithms, hashing, and
large output formatting.

## Performance rules

- `text[left:right]` creates a new string in `O(length)`.
- `separator.join(parts)` is linear in final output size.
- `startswith`/`endswith` avoid manual slices.
- Iterating a string yields one-character strings; iterating bytes yields ints.

## Visual worked example: avoid repeated copying

```text
result += "a"   copies length 0
result += "b"   copies length 1
result += "c"   copies length 2
...
total copied work can grow like 1+2+...+n

pieces.append("a")
pieces.append("b")
pieces.append("c")
"".join(pieces) -> allocate final length once
```

For a handful of pieces, direct concatenation is fine; the issue is repeated
growth inside a large loop.

## Traps

- Building output with `answer += piece` in a large loop.
- Passing sliced strings into every recursive call instead of indices.
- Mixing `bytes` and `str` in comparisons or joins.
- Using regex for simple token splitting when `split()` is clearer and faster.
