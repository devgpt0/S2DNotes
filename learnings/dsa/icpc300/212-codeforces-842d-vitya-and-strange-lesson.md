# ICPC300 212: Codeforces 842D - Vitya and Strange Lesson

**Source:** [Codeforces 842D](https://codeforces.com/problemset/problem/842/D)  
**Pattern:** full-subtree binary-trie MEX

## Exact contract

The array is treated as a set of distinct nonnegative integers. Each query
gives `x`; accumulate `xor_mask ^= x` and output the MEX of
`{value xor xor_mask}`.

## First principles

In a binary trie, choose the branch equal to the current mask bit to make the
corresponding MEX bit zero. That branch is usable unless it contains every
possible suffix value. If it is full, the answer bit must be one and traversal
uses the other branch.

Store the number of distinct leaves in every subtree. At bit `b`, one child is
full exactly when its count is `2^b`.

## Cases that decide correctness

- Duplicate input values must be inserted only once.
- XOR queries accumulate rather than replace the mask.
- MEX starts at zero.
- A missing preferred branch immediately permits all remaining answer bits to
  be zero.
- The trie universe must be larger than the number of distinct values.

## Brute force: materialize every transformed set

```python
def strange_lesson_brute(values: list[int], queries: list[int]) -> list[int]:
    distinct = set(values)
    xor_mask = 0
    answers = []
    for value in queries:
        xor_mask ^= value
        transformed = {item ^ xor_mask for item in distinct}
        answer = 0
        while answer in transformed:
            answer += 1
        answers.append(answer)
    return answers
```

This transforms the whole set for every query.

## Better insight: ask whether a zero-bit branch is full

MEX construction is greedy from the highest bit: keep the answer bit zero
whenever at least one suffix is absent from that branch.

## Expert solution: subtree capacities in a binary trie

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    value_count, query_count = map(int, input_stream.readline().split())
    values = set(map(int, input_stream.readline().split()))
    queries = [int(input_stream.readline()) for _ in range(query_count)]

    maximum = max([0, *values, *queries])
    bit_count = max(1, maximum.bit_length())
    while 1 << bit_count <= len(values):
        bit_count += 1

    children = [[-1, -1]]
    count = [0]
    for value in values:
        node = 0
        count[node] += 1
        for bit in range(bit_count - 1, -1, -1):
            direction = value >> bit & 1
            child = children[node][direction]
            if child == -1:
                child = len(children)
                children[node][direction] = child
                children.append([-1, -1])
                count.append(0)
            node = child
            count[node] += 1

    xor_mask = 0
    output = []
    for value in queries:
        xor_mask ^= value
        node = 0
        answer = 0
        for bit in range(bit_count - 1, -1, -1):
            mask_bit = xor_mask >> bit & 1
            preferred = children[node][mask_bit]
            capacity = 1 << bit
            if preferred == -1 or count[preferred] < capacity:
                if preferred == -1:
                    break
                node = preferred
            else:
                answer |= 1 << bit
                node = children[node][mask_bit ^ 1]
                if node == -1:
                    break
        output.append(str(answer))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

At every bit, the chosen prefix is the smallest one whose subtree is not full.
It therefore contains the lexicographically smallest absent transformed value.

**Complexity:** `O((n+q)B)` time and `O(nB)` space for `B` relevant bits.
