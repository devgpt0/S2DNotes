# Focus300 154: LeetCode 6 - Zigzag Conversion

**Source:** [LeetCode 6](https://leetcode.com/problems/zigzag-conversion/)  
**Difficulty:** Medium  
**Pattern:** periodic row traversal

## Exact contract

Write a nonempty string in a zigzag across `num_rows`, moving vertically down
and diagonally up, then read the rows from top to bottom. Return that converted
string. The row count is positive and may exceed the string length.

## First principles

For more than one row, row movement repeats every
`cycle = 2*num_rows - 2` characters. An index with cycle offset `o` belongs to
row `o` while descending and row `cycle-o` while ascending. Alternatively,
simulate that same row direction and append directly to row buffers.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- One row returns the input unchanged.
- At least as many rows as characters also returns the input.
- Top and bottom rows occur once per cycle; middle rows occur twice.
- Punctuation is preserved as an ordinary character.
- Empty padding cells never appear in the result.

## Brute force: rescan every index for every output row

```python
def zigzag_convert_brute(text: str, row_count: int) -> str:
    if (
        type(text) is not str
        or not 1 <= len(text) <= 1_000
        or any(
            not character.isascii() or not (character.isalpha() or character in ",.")
            for character in text
        )
    ):
        raise ValueError("text must contain 1..1,000 source-valid characters")
    if type(row_count) is not int or not 1 <= row_count <= 1_000:
        raise ValueError("row_count must be an integer between 1 and 1,000")
    if row_count == 1 or row_count >= len(text):
        return text

    cycle = 2 * row_count - 2
    output: list[str] = []
    for wanted_row in range(row_count):
        for index, character in enumerate(text):
            offset = index % cycle
            actual_row = offset if offset < row_count else cycle - offset
            if actual_row == wanted_row:
                output.append(character)
    return "".join(output)
```

This uses constant structural space but scans the text `row_count` times.

## Better insight: route each character to its final row in one pass

Maintain the current row and reverse direction only at the top or bottom. The
row buffers already have final within-row order.

## Expert solution: directional row buffers

```python
def zigzag_convert(text: str, row_count: int) -> str:
    if (
        type(text) is not str
        or not 1 <= len(text) <= 1_000
        or any(
            not character.isascii() or not (character.isalpha() or character in ",.")
            for character in text
        )
    ):
        raise ValueError("text must contain 1..1,000 source-valid characters")
    if type(row_count) is not int or not 1 <= row_count <= 1_000:
        raise ValueError("row_count must be an integer between 1 and 1,000")
    if row_count == 1 or row_count >= len(text):
        return text

    rows = [[] for _ in range(row_count)]
    row = 0
    direction = 1
    for character in text:
        rows[row].append(character)
        if row == 0:
            direction = 1
        elif row == row_count - 1:
            direction = -1
        row += direction
    return "".join(character for values in rows for character in values)
```

The direction invariant reproduces the source layout, and concatenating buffers
is exactly the required row-wise read.

**Complexity:** `O(n)` time and `O(n)` output-buffer space.
