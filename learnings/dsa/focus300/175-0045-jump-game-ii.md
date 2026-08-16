# Focus300 175: LeetCode 45 - Jump Game II

**Source:** [LeetCode 45](https://leetcode.com/problems/jump-game-ii/)  
**Difficulty:** Medium  
**Pattern:** greedy breadth-first range expansion

## Exact contract

At index `i`, `numbers[i]` is the maximum forward jump length. Starting at
index `0`, return the minimum jumps needed to reach the last index. The source
guarantees the last index is reachable.

## First principles

All indices reachable with the same jump count form a contiguous range. While
scanning that range, compute the farthest index reachable with one more jump.
When the scan reaches the current range end, taking another jump is necessary
and the next range should extend to that farthest index.


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

- A one-element list needs zero jumps.
- Jump lengths are maxima; shorter landings remain available.
- Do not increment the jump count for every index.
- The last range need not be scanned after it already reaches the destination.
- A zero inside the list is harmless when an earlier range jumps over it.

## Brute force: minimum jumps to every index

```python
def jump_brute(numbers: list[int]) -> int:
    if not numbers or any(value < 0 for value in numbers):
        raise ValueError("numbers must be a non-empty list of non-negative integers")

    unreachable = len(numbers) + 1
    jumps = [unreachable] * len(numbers)
    jumps[0] = 0
    for index in range(len(numbers)):
        furthest = min(len(numbers) - 1, index + numbers[index])
        for destination in range(index + 1, furthest + 1):
            jumps[destination] = min(jumps[destination], jumps[index] + 1)
    if jumps[-1] == unreachable:
        raise ValueError("last index is unreachable")
    return jumps[-1]
```

This relaxation takes `O(n^2)` time and `O(n)` space.

## Better transition: aggregate one BFS layer into an interval

Every index in the current reachable interval has the same minimum jump count.
Only their maximum next reach matters; storing individual queue entries repeats
contiguous work.

## Expert solution: greedy layer boundaries

```python
def jump(numbers: list[int]) -> int:
    if not numbers or any(value < 0 for value in numbers):
        raise ValueError("numbers must be a non-empty list of non-negative integers")
    if len(numbers) == 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0
    for index in range(len(numbers) - 1):
        farthest = max(farthest, index + numbers[index])
        if index == current_end:
            if farthest == current_end:
                raise ValueError("last index is unreachable")
            jumps += 1
            current_end = farthest
            if current_end >= len(numbers) - 1:
                return jumps
    raise ValueError("last index is unreachable")
```

Each boundary crossing is one BFS level, so the first level reaching the last
index uses the minimum possible jumps.

**Complexity:** `O(n)` time and `O(1)` space.
