# Focus300 060: LeetCode 403 - Frog Jump

**Source:** [LeetCode 403 - Frog Jump](https://leetcode.com/problems/frog-jump/)  
**Difficulty:** Hard  
**Pattern:** reachable last-jump states at stone positions  

## Exact contract

Stones have strictly increasing positions and start at zero. The first jump
must be one unit. After a positive jump of length `k`, the next jump must have
positive length `k-1`, `k`, or `k+1`. Return whether the last stone is reachable.

## First principles

Position alone is not a complete state because legal next moves depend on the
previous jump. Store every reachable `(stone position, last jump)` pair and
propagate its three possible positive next jumps.


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

- One starting stone is already the destination.
- With multiple stones, the second stone must be at position one.
- Zero-length and negative jumps are forbidden.
- Different last jumps at the same stone are distinct states.
- Missing landing positions terminate that transition immediately.

## Brute force: recursively enumerate jump sequences

```python
def can_cross_brute(stones: list[int]) -> bool:
    if (
        not stones
        or any(type(stone) is not int or stone < 0 for stone in stones)
        or stones[0] != 0
        or any(stones[index] >= stones[index + 1] for index in range(len(stones) - 1))
    ):
        raise ValueError(
            "stones must be strictly increasing nonnegative integers from zero"
        )
    positions = set(stones)
    destination = stones[-1]

    def search(position: int, last_jump: int) -> bool:
        if position == destination:
            return True
        for jump in (last_jump - 1, last_jump, last_jump + 1):
            if jump > 0 and position + jump in positions:
                if search(position + jump, jump):
                    return True
        return False

    return search(0, 0)
```

**Complexity:** exponential time and `O(n)` recursion depth.

## Better approach: memoized state search

Caching `(position, last_jump)` prevents repeated suffix searches and gives
`O(n^2)` states. The iterative expert solution has the same bound without
recursion depth risk.

## Expert solution: propagate reachable jumps stone by stone

```python
def can_cross(stones: list[int]) -> bool:
    if (
        not stones
        or any(type(stone) is not int or stone < 0 for stone in stones)
        or stones[0] != 0
        or any(stones[index] >= stones[index + 1] for index in range(len(stones) - 1))
    ):
        raise ValueError(
            "stones must be strictly increasing nonnegative integers from zero"
        )
    if len(stones) == 1:
        return True
    if stones[1] != 1:
        return False

    jumps_at = {stone: set() for stone in stones}
    jumps_at[0].add(0)
    for stone in stones:
        for last_jump in jumps_at[stone]:
            for jump in (last_jump - 1, last_jump, last_jump + 1):
                if jump > 0 and stone + jump in jumps_at:
                    jumps_at[stone + jump].add(jump)
    return bool(jumps_at[stones[-1]])
```

Every stored jump corresponds to one legal path reaching that stone. Each
transition applies exactly the source's three next lengths, so induction over
increasing stone positions proves the final set is nonempty exactly when the
frog can arrive.

**Complexity:** `O(n^2)` time and space in the worst case.

