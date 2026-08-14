# ICPC300 093: CSES - Nim Game I

**Source:** [CSES - Nim Game I](https://cses.fi/problemset/task/1730/)  
**Pattern:** Sprague-Grundy xor for ordinary Nim

## Exact contract

Input gives `t` games. Each game gives a heap count and the positive size of
each heap. Players alternate choosing one heap and removing any positive number
of sticks. The player unable to move loses. Output `first` or `second` for each
game under optimal play.

## First principles

A heap of size `x` can move to every Grundy value `0..x-1`, so its Grundy value
is `x`. Independent impartial games combine by xor. The position is losing
exactly when the xor of all heap sizes is zero.

## Cases that decide correctness

- One nonempty heap is always winning.
- Equal heap sizes can cancel in xor.
- Ordinary addition is irrelevant; only bitwise xor determines the outcome.
- Games are independent and produce one output line each.

## Brute force: search every legal removal

```python
def nim_first_wins_brute(heaps: tuple[int, ...]) -> bool:
    if not any(heaps):
        return False
    for heap_index, heap_size in enumerate(heaps):
        for remaining in range(heap_size):
            next_heaps = list(heaps)
            next_heaps[heap_index] = remaining
            if not nim_first_wins_brute(tuple(next_heaps)):
                return True
    return False
```

The un-memoized game tree is exponential.

## Better: derive each heap's Grundy number by mex

```python
def nim_first_wins_grundy(heaps: list[int]) -> bool:
    maximum = max(heaps, default=0)
    grundy = [0] * (maximum + 1)
    for heap_size in range(1, maximum + 1):
        reachable = {grundy[remaining] for remaining in range(heap_size)}
        value = 0
        while value in reachable:
            value += 1
        grundy[heap_size] = value

    nim_sum = 0
    for heap_size in heaps:
        nim_sum ^= grundy[heap_size]
    return nim_sum != 0
```

This is polynomial but spends `O(H^2)` work rediscovering the simple pattern
`grundy[x] = x`.

## Expert solution: xor heap sizes directly

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
            nim_sum ^= heap_size
        offset += heap_count
        answers.append("first" if nim_sum else "second")
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The xor theorem characterizes all losing Nim positions. A nonzero highest xor
bit always identifies a heap move that makes the xor zero; from zero, every
move makes it nonzero.

**Complexity:** `O(total heaps)` time and `O(1)` extra space.

