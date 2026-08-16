# Focus300 069: LeetCode 466 - Count The Repetitions

**Source:** [LeetCode 466](https://leetcode.com/problems/count-the-repetitions/)  
**Difficulty:** Hard  
**Pattern:** cycle detection at repeated-block boundaries

## Exact contract

Let `S1` be `s1` repeated `n1` times and `S2` be `s2` repeated `n2` times.
Return the largest integer `m` such that `S2` repeated `m` times is a
subsequence of `S1`.

## First principles

Scan each `s1` block while tracking the next index needed in `s2` and how many
complete `s2` copies have matched. At an `s1` block boundary, that `s2` index
fully determines future behavior.

When the same index reappears, the blocks and completed copies between visits
form a cycle. Skip as many whole cycles as fit, then scan the short remainder.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- If `s2` contains a character absent from `s1`, the answer is zero.
- Matching is a subsequence, not a substring.
- A completed `s2` immediately restarts at index zero.
- Cycle state is recorded only at complete `s1` block boundaries.
- The final count is divided by `n2` with floor semantics.

## Brute force: scan every repeated source character

```python
def get_max_repetitions_brute(s1: str, n1: int, s2: str, n2: int) -> int:
    if n1 == 0:
        return 0
    target_index = 0
    completed = 0
    for character in s1 * n1:
        if character == s2[target_index]:
            target_index += 1
            if target_index == len(s2):
                target_index = 0
                completed += 1
    return completed // n2
```

This takes `O(n1*|s1|)` time and materializes the repeated source string.

## Better insight: block-boundary matching state is finite

There are only `|s2|` possible next-character indices at a boundary. A repeated
state proves that all later block transitions repeat periodically.

## Expert solution: skip cycles of repeated block states

```python
def get_max_repetitions(s1: str, n1: int, s2: str, n2: int) -> int:
    if n1 == 0 or not set(s2).issubset(s1):
        return 0
    block = 0
    target_index = 0
    completed = 0
    seen = {0: (0, 0)}

    while block < n1:
        for character in s1:
            if character == s2[target_index]:
                target_index += 1
                if target_index == len(s2):
                    target_index = 0
                    completed += 1
        block += 1

        previous = seen.get(target_index)
        if previous is None:
            seen[target_index] = (block, completed)
            continue
        previous_block, previous_completed = previous
        cycle_blocks = block - previous_block
        cycle_completed = completed - previous_completed
        cycles = (n1 - block) // cycle_blocks
        block += cycles * cycle_blocks
        completed += cycles * cycle_completed

    return completed // n2
```

Cycle skipping preserves both the next target character and the exact number of
completed target copies added by every skipped block group.

**Complexity:** `O((|s2|+remainder_blocks)*|s1|)` time and `O(|s2|)` space.
