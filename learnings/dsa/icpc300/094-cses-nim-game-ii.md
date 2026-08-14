# ICPC300 094: CSES - Nim Game II

**Source:** [CSES - Nim Game II](https://cses.fi/problemset/task/1098/)  
**Pattern:** periodic Grundy values

## Exact contract

Input gives `t` games. Each game consists of several nonempty heaps. A move
chooses one heap and removes one, two, or three sticks. The player unable to
move loses. Output `first` or `second` for each game under optimal play.

## First principles

For one heap, Grundy values repeat `0,1,2,3`: from size `x`, the reachable
values are those at `x-1`, `x-2`, and `x-3`, whose mex is `x mod 4`. Multiple
heaps combine by xor, so xor all `heap_size mod 4`.

## Cases that decide correctness

- A heap divisible by four contributes zero but may still contain sticks.
- Removing at most three is the defining difference from ordinary Nim.
- Equal residues can cancel through xor.
- Only the residues are needed, even for very large heap sizes.

## Brute force: search all one-to-three removals

```python
def nim_two_first_wins_brute(heaps: tuple[int, ...]) -> bool:
    if not any(heaps):
        return False
    for heap_index, heap_size in enumerate(heaps):
        for removed in range(1, min(3, heap_size) + 1):
            next_heaps = list(heaps)
            next_heaps[heap_index] -= removed
            if not nim_two_first_wins_brute(tuple(next_heaps)):
                return True
    return False
```

**Complexity:** exponential in the total number of sticks.

## Better: tabulate heap Grundy values

```python
def nim_two_first_wins_grundy(heaps: list[int]) -> bool:
    maximum = max(heaps, default=0)
    grundy = [0] * (maximum + 1)
    for heap_size in range(1, maximum + 1):
        reachable = {
            grundy[heap_size - removed] for removed in range(1, min(3, heap_size) + 1)
        }
        value = 0
        while value in reachable:
            value += 1
        grundy[heap_size] = value

    nim_sum = 0
    for heap_size in heaps:
        nim_sum ^= grundy[heap_size]
    return nim_sum != 0
```

This is linear in the largest heap but stores values whose period is only four.

## Expert solution: xor modulo-four residues

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    test_count = data[0]
    offset = 1
    answers = []

    for _ in range(test_count):
        heap_count = data[offset]
        offset += 1
        nim_sum = 0
        for heap_size in data[offset : offset + heap_count]:
            nim_sum ^= heap_size % 4
        offset += heap_count
        answers.append("first" if nim_sum else "second")
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The four-value Grundy cycle follows directly by mex induction. The xor theorem
then makes zero exactly the losing combined position.

**Complexity:** `O(total heaps)` time and `O(1)` extra space.

