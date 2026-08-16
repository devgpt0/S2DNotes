# Focus300 036: LeetCode 220 - Contains Duplicate III

**Source:** [LeetCode 220 - Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/)  
**Difficulty:** Hard  
**Pattern:** fixed-width value buckets in an index window  

## Exact contract

Return whether distinct indices `i` and `j` exist with both
`abs(i - j) <= index_limit` and
`abs(values[i] - values[j]) <= value_limit`.

## First principles

Only the previous `index_limit` values can pair with the current value. Divide
the number line into buckets of width `value_limit + 1`. Two values close
enough must occupy the same bucket or adjacent buckets; one active value per
bucket is sufficient because two in one bucket would already be an answer.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- A nonpositive index limit cannot contain distinct eligible indices.
- A negative value limit makes the inequality impossible.
- Equal values are found when the value limit is zero.
- Negative values need mathematical floor buckets; Python `//` provides them.
- Remove the value that leaves the window after testing the current value.

## Brute force: compare every eligible recent pair

```python
def contains_nearby_almost_duplicate_brute(
    values: list[int], index_limit: int, value_limit: int
) -> bool:
    if (
        any(type(value) is not int for value in values)
        or type(index_limit) is not int
        or type(value_limit) is not int
    ):
        raise ValueError("values and limits must be integers")
    if index_limit <= 0 or value_limit < 0:
        return False
    for right, value in enumerate(values):
        for left in range(max(0, right - index_limit), right):
            if abs(value - values[left]) <= value_limit:
                return True
    return False
```

**Complexity:** `O(n * index_limit)` time and `O(1)` space.

## Better approach: ordered active window

A balanced search tree can find the predecessor of `value + value_limit` and
test it against `value - value_limit` in `O(log index_limit)` time. Python's
standard library has no logarithmic ordered multiset.

## Expert solution: constant-neighborhood bucket lookup

```python
def contains_nearby_almost_duplicate(
    values: list[int], index_limit: int, value_limit: int
) -> bool:
    if (
        any(type(value) is not int for value in values)
        or type(index_limit) is not int
        or type(value_limit) is not int
    ):
        raise ValueError("values and limits must be integers")
    if index_limit <= 0 or value_limit < 0:
        return False

    width = value_limit + 1
    buckets: dict[int, int] = {}
    for index, value in enumerate(values):
        bucket = value // width
        if bucket in buckets:
            return True
        if bucket - 1 in buckets and value - buckets[bucket - 1] <= value_limit:
            return True
        if bucket + 1 in buckets and buckets[bucket + 1] - value <= value_limit:
            return True
        buckets[bucket] = value
        if index >= index_limit:
            expired = values[index - index_limit]
            del buckets[expired // width]
    return False
```

Same-bucket values differ by at most `value_limit`; nonadjacent buckets are too
far apart. The dictionary contains exactly the eligible previous index window,
so the three bucket tests are necessary and sufficient.

**Complexity:** `O(n)` expected time and `O(index_limit)` space.

