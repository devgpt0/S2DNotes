# ICPC300 217: Codeforces 1272F - Two Bracket Sequences

**Source:** [Codeforces 1272F](https://codeforces.com/problemset/problem/1272/F)  
**Pattern:** shortest-path DP over two subsequence positions and balance

## Exact contract

Given two parenthesis strings, output a shortest regular bracket sequence that
contains both input strings as subsequences. Any shortest answer is accepted.

## First principles

A state `(i,j,b)` has consumed prefixes of lengths `i` and `j` and currently
has balance `b`. Appending one parenthesis advances each input position whose
next character matches it. Opening increases balance; closing is allowed only
when balance is positive.

Every transition appends one character, so breadth-first search finds the
shortest state path to `(len(first),len(second),0)`. Predecessor states recover
the answer.

## Cases that decide correctness

- Both inputs are subsequences, not substrings.
- No prefix of the output may have negative balance.
- The final balance must be zero.
- One appended character can advance both input positions.
- Extra parentheses may be required after both inputs are consumed.

## Brute force: BFS with tuple states

```python
from collections import deque


def two_brackets_brute(first: str, second: str) -> str:
    start: tuple[int, int, int] = (0, 0, 0)
    queue: deque[tuple[tuple[int, int, int], str]] = deque([(start, "")])
    visited: set[tuple[int, int, int]] = {start}
    while queue:
        (first_index, second_index, balance), answer = queue.popleft()
        if first_index == len(first) and second_index == len(second) and balance == 0:
            return answer
        for character, difference in (("(", 1), (")", -1)):
            new_balance = balance + difference
            if not 0 <= new_balance <= len(first) + len(second):
                continue
            new_first = first_index + int(
                first_index < len(first) and first[first_index] == character
            )
            new_second = second_index + int(
                second_index < len(second) and second[second_index] == character
            )
            state = (new_first, new_second, new_balance)
            if state not in visited:
                visited.add(state)
                queue.append((state, answer + character))
    raise RuntimeError("a balanced common supersequence always exists")
```

This stores a complete output string in every queue entry.

## Better insight: encode states and store one predecessor

The state graph has a fixed rectangular index space. Compact integer arrays
avoid per-state tuples and reconstruct only the final shortest path.

## Expert solution: compact BFS with predecessor states

```python
import sys
from array import array


def solve() -> None:
    input_stream = sys.stdin.buffer
    first = input_stream.readline().strip().decode()
    second = input_stream.readline().strip().decode()
    first_width = len(first) + 1
    second_width = len(second) + 1
    balance_width = len(first) + len(second) + 1
    state_count = first_width * second_width * balance_width

    def encode(first_index: int, second_index: int, balance: int) -> int:
        return (first_index * second_width + second_index) * balance_width + balance

    def decode(state: int) -> tuple[int, int, int]:
        pair, balance = divmod(state, balance_width)
        first_index, second_index = divmod(pair, second_width)
        return first_index, second_index, balance

    start = encode(0, 0, 0)
    target = encode(len(first), len(second), 0)
    predecessor = array("i", [-1]) * state_count
    predecessor[start] = start
    queue = array("i", [start])
    head = 0
    while head < len(queue) and predecessor[target] == -1:
        state = queue[head]
        head += 1
        first_index, second_index, balance = decode(state)
        for character, difference in (("(", 1), (")", -1)):
            new_balance = balance + difference
            if not 0 <= new_balance < balance_width:
                continue
            new_first = first_index + int(
                first_index < len(first) and first[first_index] == character
            )
            new_second = second_index + int(
                second_index < len(second) and second[second_index] == character
            )
            next_state = encode(new_first, new_second, new_balance)
            if predecessor[next_state] == -1:
                predecessor[next_state] = state
                queue.append(next_state)

    answer = []
    state = target
    while state != start:
        previous = predecessor[state]
        _, _, balance = decode(state)
        _, _, previous_balance = decode(previous)
        answer.append("(" if balance > previous_balance else ")")
        state = previous
    print("".join(reversed(answer)))


if __name__ == "__main__":
    solve()
```

BFS guarantees minimum length; transition guards guarantee every prefix and
the final output satisfy the regular-bracket invariant.

**Complexity:** `O(nm(n+m))` time and compact integer storage of the same order.
