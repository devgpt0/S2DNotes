# Focus300 008: LeetCode 41 - First Missing Positive

**Source:** [LeetCode 41](https://leetcode.com/problems/first-missing-positive/)  
**Difficulty:** Hard  
**Pattern:** use the input array as an index-addressed presence table

## Exact contract

Return the smallest missing positive integer from an unsorted integer array.
The required solution uses `O(n)` time and `O(1)` auxiliary space. Mutating the
array is allowed.

## First principles

For length `n`, the answer lies in `[1,n+1]`: if all `1..n` occur, it is `n+1`.
Therefore only values in `1..n` matter. Place each such value `v` at index
`v-1`. After placement, the first index not holding `index+1` reveals the
answer.

Each swap puts at least one value into its final slot, bounding all inner loops
by `O(n)` total swaps.

## Cases that decide correctness

- Zero and negative values are irrelevant.
- Values greater than `n` are irrelevant.
- Duplicate values must not cause an infinite swap loop.
- An empty array returns one.
- The expert solution intentionally mutates the array.

## Brute force: repeated membership scans

```python
def first_missing_positive_brute(values: list[int]) -> int:
    candidate = 1
    while candidate in values:
        candidate += 1
    return candidate
```

This is `O(n^2)` time in the worst case and `O(1)` auxiliary space.

## Better approach: explicit presence set

```python
def first_missing_positive_set(values: list[int]) -> int:
    present = set(values)
    for candidate in range(1, len(values) + 2):
        if candidate not in present:
            return candidate
    raise RuntimeError("finite scan must find an answer")
```

This is `O(n)` expected time and `O(n)` space.

## Expert solution: cyclic placement in the input

```python
def first_missing_positive(values: list[int]) -> int:
    size = len(values)
    for index in range(size):
        while 1 <= values[index] <= size and values[values[index] - 1] != values[index]:
            destination = values[index] - 1
            values[index], values[destination] = values[destination], values[index]
    for index, value in enumerate(values):
        if value != index + 1:
            return index + 1
    return size + 1
```

The duplicate guard stops only when the destination already proves that value
present; every other swap makes permanent progress.

**Complexity:** `O(n)` time and `O(1)` auxiliary space.
