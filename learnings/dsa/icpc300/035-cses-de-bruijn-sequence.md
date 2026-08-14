# ICPC300 035: CSES - De Bruijn Sequence

**Source:** [CSES - De Bruijn Sequence](https://cses.fi/problemset/task/1692/)  
**Pattern:** Euler circuit in an overlap graph

## Exact contract

Input is `n` (`1 <= n <= 15`). Output a shortest binary string in which every
binary string of length `n` occurs exactly once as a contiguous substring. Any
valid answer is accepted.

The required length is `2^n + n - 1`: there are `2^n` required windows, and
every character after the first `n - 1` creates one new window.

## First principles

Use every `(n-1)`-bit string as a graph vertex. Every `n`-bit string is one
directed edge: its prefix is the start vertex, its suffix is the end vertex,
and its last bit labels the edge.

Each vertex has two outgoing and two incoming edges. An Euler circuit uses all
`2^n` edges once, so its edge labels list every `n`-bit string once through
overlapping windows.

## Cases that decide correctness

- For `n = 1`, the graph has one zero-bit vertex and two self-loop edges; the
  generic construction must output both `0` and `1`.
- The prefix contributes exactly `n - 1` zeroes, not `n`.
- Edge labels are collected during Hierholzer backtracking and must be reversed.
- The output is linear, not cyclic, so append the overlap prefix once.

## Brute force: test every candidate of minimum length

```python
from itertools import product


def de_bruijn_brute(order: int) -> str:
    required = {"".join(bits) for bits in product("01", repeat=order)}
    length = (1 << order) + order - 1
    for bits in product("01", repeat=length):
        candidate = "".join(bits)
        windows = {
            candidate[start : start + order] for start in range(length - order + 1)
        }
        if windows == required:
            return candidate
    raise RuntimeError("a binary de Bruijn sequence always exists")
```

**Complexity:** exponential in the already exponential output length.

## Better: backtrack over unseen length-n windows

```python
def de_bruijn_window_backtracking(order: int) -> str:
    word_count = 1 << order
    suffix_mask = (1 << (order - 1)) - 1
    used = [False] * word_count
    used[0] = True
    bits = ["0"] * order

    def search(current_word: int, used_count: int) -> bool:
        if used_count == word_count:
            return True
        suffix = current_word & suffix_mask
        for bit in range(2):
            next_word = (suffix << 1) | bit
            if not used[next_word]:
                used[next_word] = True
                bits.append(str(bit))
                if search(next_word, used_count + 1):
                    return True
                bits.pop()
                used[next_word] = False
        return False

    if not search(0, 1):
        raise RuntimeError("a binary de Bruijn sequence always exists")
    return "".join(bits)
```

This searches for a Hamiltonian traversal of the `n`-bit windows. It avoids
testing arbitrary strings but may still backtrack exponentially.

## Expert solution: iterative Hierholzer construction

```python
import sys


def solve() -> None:
    order = int(sys.stdin.readline())
    vertex_count = 1 << (order - 1)
    vertex_mask = vertex_count - 1
    next_bit = [0] * vertex_count
    stack: list[tuple[int, int]] = [(0, -1)]
    reversed_labels: list[str] = []

    while stack:
        vertex, incoming_bit = stack[-1]
        if next_bit[vertex] < 2:
            bit = next_bit[vertex]
            next_bit[vertex] += 1
            neighbor = ((vertex << 1) | bit) & vertex_mask
            stack.append((neighbor, bit))
        else:
            stack.pop()
            if incoming_bit != -1:
                reversed_labels.append(str(incoming_bit))

    answer = "0" * (order - 1) + "".join(reversed(reversed_labels))
    print(answer)


if __name__ == "__main__":
    solve()
```

Every graph edge is uniquely identified by a vertex and its chosen last bit.
Hierholzer consumes both outgoing edges of every vertex once, hence outputs all
`2^n` windows exactly once.

**Complexity:** `O(2^n)` time and `O(2^n)` space, which is optimal relative to
the output length.
