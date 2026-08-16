# Focus300 119: LeetCode 798 - Smallest Rotation with Highest Score

**Source:** [LeetCode 798](https://leetcode.com/problems/smallest-rotation-with-highest-score/)  
**Difficulty:** Hard  
**Pattern:** circular difference events

## Exact contract

For a nonempty array `nums` of length `n`, every value satisfies
`0 <= nums[i] < n`. Left rotation by `k` scores one point for each rotated
position `i` whose value is at most `i`. Return the smallest `k` in `[0, n)`
that obtains the maximum score. The source length is at most 20,000.

## First principles

As `k` increases by one, an element's new index decreases by one and wraps from
zero to `n - 1`. Its score changes only twice over the full rotation cycle: it
loses a point when its index moves below its value, and gains a point when its
index wraps. Recording those two rotation events for every element yields all
scores with a difference array.


## Classroom board: rank a tiny table

```text
rows = a few records

brute force scans the rows repeatedly.
useful structure: group, sort, or rank once, then read the answer.
```



## Step-by-step transformation

1. Read the table rows and keep only the rows that can still contribute to the answer.
2. Use joins, grouping, ranking, or filtering to turn the raw rows into one intermediate result set.
3. Apply tie rules or ordering rules before selecting the final row or value.
4. Project the requested column(s), which is the final output of the query.

In SQL problems, the database performs the transformation by moving rows through `WHERE`, `JOIN`, `GROUP BY`, window functions, and `ORDER BY` until only the requested result remains.


## Diagram: SQL rows to final answer

```text

            raw table rows
                |
                v
            filter / join / group / rank
                |
                v
            ordered result rows
                |
                v
            requested output column
```

The query turns table rows into one final answer by filtering, combining, and ranking the data in SQL.

## Cases that decide correctness

- Value zero scores at every position; its loss and gain events cancel.
- Rotation zero must be scored explicitly before applying later events.
- Circular event indices use modulo `n`.
- Equal best scores keep the earlier rotation.
- An event at rotation zero describes the wrap from `n - 1` back to zero and
  is not reapplied after initializing rotation zero's score.

## Brute force: score every complete rotation

```python
def best_rotation_brute(numbers: list[int]) -> int:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 20_000:
        raise ValueError("numbers length must be between 1 and 20000")
    if any(not 0 <= value < len(numbers) for value in numbers):
        raise ValueError("every value must be between 0 and len(numbers)-1")

    best_index = 0
    best_score = -1
    for rotation in range(len(numbers)):
        rotated = numbers[rotation:] + numbers[:rotation]
        score = sum(value <= index for index, value in enumerate(rotated))
        if score > best_score:
            best_score = score
            best_index = rotation
    return best_index
```

Building and scoring all `n` rotations takes `O(n^2)` time and `O(n)` space.

## Better approach: add each element's scoring interval

Each element scores over one circular interval of rotations. Splitting wrapped
intervals and adding them to a difference array works directly. Recording the
two score-change events below is the same idea with fewer boundary cases.

## Expert solution: sweep loss and wrap events

```python
def best_rotation(numbers: list[int]) -> int:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 20_000:
        raise ValueError("numbers length must be between 1 and 20000")
    if any(not 0 <= value < len(numbers) for value in numbers):
        raise ValueError("every value must be between 0 and len(numbers)-1")

    length = len(numbers)
    score_change = [0] * length
    for index, value in enumerate(numbers):
        score_change[(index - value + 1) % length] -= 1
        score_change[(index + 1) % length] += 1

    score = sum(value <= index for index, value in enumerate(numbers))
    best_score = score
    best_rotation = 0
    for rotation in range(1, length):
        score += score_change[rotation]
        if score > best_score:
            best_score = score
            best_rotation = rotation
    return best_rotation
```

For original index `i` and value `v`, rotation `(i - v + 1) mod n` moves the
element from scoring index `v` to non-scoring index `v - 1`; rotation
`(i + 1) mod n` wraps it back to a scoring index. The sweep sums exactly these
changes.

**Complexity:** `O(n)` time and `O(n)` space.
