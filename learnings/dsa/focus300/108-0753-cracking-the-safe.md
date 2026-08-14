# Focus300 108: LeetCode 753 - Cracking the Safe

**Source:** [LeetCode 753](https://leetcode.com/problems/cracking-the-safe/)  
**Difficulty:** Hard  
**Pattern:** De Bruijn graph Eulerian cycle

## Exact contract

Given code length `n` and alphabet size `k`, return any shortest string that
contains every length-`n` code over digits `0` through `k - 1` as a substring.
Source bounds are `1 <= n <= 4`, `1 <= k <= 10`, and `k^n <= 4096`.

## First principles

Treat each length-`n` code as a directed edge. Its first `n - 1` digits are the
source node and its last `n - 1` digits are the destination. Every node has the
same in-degree and out-degree, so an Eulerian cycle uses every code exactly once.
Writing the traversed edge digits yields a shortest De Bruijn sequence.

## Cases that decide correctness

- `k = 1` returns exactly `n` zeroes.
- `n = 1` must contain every alphabet digit once.
- Every one of the `k^n` codes must occur; repeats cannot shorten the answer.
- The minimum possible length is `k^n + n - 1`.
- Any valid shortest sequence is accepted; its lexicographic order is irrelevant.

## Brute force: backtrack over unused codes

```python
def crack_safe_brute(code_length: int, alphabet_size: int) -> str:
    if not 1 <= code_length <= 4:
        raise ValueError("code_length must be between 1 and 4")
    if not 1 <= alphabet_size <= 10 or alphabet_size**code_length > 4096:
        raise ValueError("alphabet_size must satisfy source bounds")

    digits = tuple(str(digit) for digit in range(alphabet_size))
    target = alphabet_size**code_length
    start = "0" * code_length
    used = {start}

    def extend(sequence: str) -> str | None:
        if len(used) == target:
            return sequence
        prefix = sequence[-(code_length - 1) :] if code_length > 1 else ""
        for digit in digits:
            code = prefix + digit
            if code in used:
                continue
            used.add(code)
            answer = extend(sequence + digit)
            if answer is not None:
                return answer
            used.remove(code)
        return None

    answer = extend(start)
    if answer is None:
        raise RuntimeError("a De Bruijn sequence must exist")
    return answer
```

This searches paths through unused codes and may backtrack exponentially.

## Better transition: use every code as one graph edge

The backtracking state already exposes the overlap graph. In that graph, the
balanced degrees guarantee an Eulerian cycle, so Hierholzer's algorithm never
needs to reconsider an edge choice.

## Expert solution: iterative Hierholzer traversal

```python
def crack_safe(code_length: int, alphabet_size: int) -> str:
    if not 1 <= code_length <= 4:
        raise ValueError("code_length must be between 1 and 4")
    if not 1 <= alphabet_size <= 10 or alphabet_size**code_length > 4096:
        raise ValueError("alphabet_size must satisfy source bounds")

    start = "0" * (code_length - 1)
    next_digit: dict[str, int] = {}
    node_stack = [start]
    edge_stack: list[str] = []
    reversed_edge_digits: list[str] = []

    while node_stack:
        node = node_stack[-1]
        digit = next_digit.get(node, 0)
        if digit < alphabet_size:
            next_digit[node] = digit + 1
            label = str(digit)
            node_stack.append((node + label)[1:])
            edge_stack.append(label)
        else:
            node_stack.pop()
            if edge_stack:
                reversed_edge_digits.append(edge_stack.pop())

    return "".join(reversed_edge_digits) + start
```

Each node's counter emits every outgoing edge once. Appending an edge label when
backtracking records an Eulerian cycle; the final `n - 1` start digits expose the
last edge windows. The iterative form safely handles all `4096` edges without
Python recursion-depth changes.

**Complexity:** `O(k^n)` time and space.
