# ICPC300 063: CSES - Finding Borders

**Source:** [CSES - Finding Borders](https://cses.fi/problemset/task/1732/)  
**Pattern:** prefix function and border chain  
**Goal:** Output in increasing order every length that is both a nonempty
proper prefix and a suffix of the string.

## 1. Problem in plain words

For `abcababcab`, lengths `2` and `5` are borders because `ab` and `abcab`
occur at both ends. The full string is not a proper border and is not output.

Borders may nest: every border of a border is also a border of the whole
string.

## 2. First principles

The prefix function `pi[i]` is the length of the longest proper prefix of
`text[:i+1]` that is also its suffix. Therefore `pi[-1]` is the longest border
of the full string.

If that border has length `b`, its next smaller border has length `pi[b-1]`.
Following these links reaches every border once, from largest to smallest.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| No proper border | Output no lengths. |
| All characters equal | Output every length `1..n-1`. |
| Nested borders | Follow the entire prefix-function chain. |
| Border also occurs internally | It is still output once. |
| Whole string | Exclude it because the border must be proper. |

## 4. Brute force: compare every prefix with its suffix

```python
def border_lengths_brute_force(text: str) -> list[int]:
    if not text:
        raise ValueError("text must be nonempty")
    return [length for length in range(1, len(text)) if text[:length] == text[-length:]]
```

**Complexity:** `O(n^2)` character work and `O(n)` output memory.

## 5. Better: find borders from the Z-function

`z[i]` is the longest prefix matching the suffix that begins at `i`. A length
`b` is a border exactly when `z[n-b] >= b`.

```python
def border_lengths_z_function(text: str) -> list[int]:
    if not text:
        raise ValueError("text must be nonempty")

    length = len(text)
    z = [0] * length
    left = 0
    right = 0
    for index in range(1, length):
        if index < right:
            z[index] = min(right - index, z[index - left])
        while index + z[index] < length and text[z[index]] == text[index + z[index]]:
            z[index] += 1
        if index + z[index] > right:
            left = index
            right = index + z[index]

    return [border for border in range(1, length) if z[length - border] >= border]
```

**Complexity:** `O(n)` time and `O(n)` memory.

## 6. Expert solution: follow prefix-function border links

The Z-function scan checks all possible lengths. The prefix-function chain
visits only actual borders after the same linear preprocessing.

```python
def border_lengths(text: str) -> list[int]:
    if not text:
        raise ValueError("text must be nonempty")

    prefix = [0] * len(text)
    for index in range(1, len(text)):
        matched = prefix[index - 1]
        while matched and text[index] != text[matched]:
            matched = prefix[matched - 1]
        if text[index] == text[matched]:
            matched += 1
        prefix[index] = matched

    borders: list[int] = []
    border = prefix[-1]
    while border:
        borders.append(border)
        border = prefix[border - 1]
    borders.reverse()
    return borders
```

### Why the expert code is correct

- `prefix[-1]` is, by definition, the longest proper border of the full string.
- Any smaller full-string border must also be a border of that longest border;
  `prefix[border-1]` gives the longest such smaller one.
- Repeating this argument enumerates every nested border and terminates at zero.
- Reversing converts the chain's decreasing order to the source's increasing
  output order.

**Complexity:** `O(n)` time and `O(n)` memory.

## 7. What to remember

Borders form a parent chain in the prefix-function array: start at `pi[n-1]`
and repeatedly move to `pi[length-1]`.
