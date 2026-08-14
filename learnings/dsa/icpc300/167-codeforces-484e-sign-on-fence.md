# ICPC300 167: Codeforces 484E - Sign on Fence

**Source:** [Codeforces 484E](https://codeforces.com/problemset/problem/484/E)  
**Pattern:** persistent threshold segment trees with consecutive-run monoids

## Exact contract

Given fence heights and queries `(l,r,w)`, output the greatest height `h` such
that the inclusive range `[l,r]` contains at least `w` consecutive boards whose
heights are all at least `h`.

## First principles

For a threshold `h`, mark position `i` active exactly when `height[i] >= h`.
A segment-tree node stores its active prefix length, suffix length, and longest
active run. These fields merge associatively.

Activate positions in descending height order and save a persistent root after
each distinct height. As the threshold decreases, longest runs can only grow.
For each query, binary-search the first descending threshold version whose
range has a run of length at least `w`; its height is the greatest feasible
answer.

## Cases that decide correctness

- Boards equal to the threshold are active.
- Activate every position of one equal height before saving that version.
- Query merging must preserve left-to-right order for prefix and suffix fields.
- The requested run must lie wholly inside `[l,r]`.
- At the minimum array height all positions are active, so every valid query
  width is feasible.

## Brute force: inspect every candidate window

```python
def sign_on_fence_brute(
    heights: list[int], queries: list[tuple[int, int, int]]
) -> list[int]:
    answers = []
    for left, right, width in queries:
        answer = 0
        for start in range(left - 1, right - width + 1):
            answer = max(answer, min(heights[start : start + width]))
        answers.append(answer)
    return answers
```

The minimum of every length-`w` window is tested directly.

## Better: binary-search heights and scan each range

```python
def sign_on_fence_scanning(
    heights: list[int], queries: list[tuple[int, int, int]]
) -> list[int]:
    candidates = sorted(set(heights))
    answers = []
    for left, right, width in queries:
        low = 0
        high = len(candidates) - 1
        while low < high:
            middle = (low + high + 1) // 2
            threshold = candidates[middle]
            longest = 0
            current = 0
            for height in heights[left - 1 : right]:
                current = current + 1 if height >= threshold else 0
                longest = max(longest, current)
            if longest >= width:
                low = middle
            else:
                high = middle - 1
        answers.append(candidates[low])
    return answers
```

Monotonicity removes candidate windows, but every feasibility check still
scans the queried interval.

## Expert solution: persistent active-run monoids

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    heights = list(map(int, input_stream.readline().split()))

    left_child = [0]
    right_child = [0]
    prefix = [0]
    suffix = [0]
    longest = [0]

    def activate(previous: int, left: int, right: int, position: int) -> int:
        node = len(longest)
        left_child.append(left_child[previous])
        right_child.append(right_child[previous])
        prefix.append(prefix[previous])
        suffix.append(suffix[previous])
        longest.append(longest[previous])
        if right - left == 1:
            prefix[node] = 1
            suffix[node] = 1
            longest[node] = 1
            return node

        middle = (left + right) // 2
        if position < middle:
            left_child[node] = activate(left_child[previous], left, middle, position)
        else:
            right_child[node] = activate(right_child[previous], middle, right, position)

        left_node = left_child[node]
        right_node = right_child[node]
        left_length = middle - left
        right_length = right - middle
        prefix[node] = prefix[left_node]
        if prefix[left_node] == left_length:
            prefix[node] += prefix[right_node]
        suffix[node] = suffix[right_node]
        if suffix[right_node] == right_length:
            suffix[node] += suffix[left_node]
        longest[node] = max(
            longest[left_node],
            longest[right_node],
            suffix[left_node] + prefix[right_node],
        )
        return node

    def merge(
        first: tuple[int, int, int, int],
        second: tuple[int, int, int, int],
    ) -> tuple[int, int, int, int]:
        first_prefix, first_suffix, first_longest, first_length = first
        second_prefix, second_suffix, second_longest, second_length = second
        merged_prefix = first_prefix
        if first_prefix == first_length:
            merged_prefix += second_prefix
        merged_suffix = second_suffix
        if second_suffix == second_length:
            merged_suffix += first_suffix
        return (
            merged_prefix,
            merged_suffix,
            max(first_longest, second_longest, first_suffix + second_prefix),
            first_length + second_length,
        )

    def range_state(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> tuple[int, int, int, int]:
        if query_right <= left or right <= query_left:
            return (0, 0, 0, 0)
        if query_left <= left and right <= query_right:
            return (prefix[node], suffix[node], longest[node], right - left)
        middle = (left + right) // 2
        return merge(
            range_state(left_child[node], left, middle, query_left, query_right),
            range_state(right_child[node], middle, right, query_left, query_right),
        )

    positions_by_height: dict[int, list[int]] = {}
    for position, height in enumerate(heights):
        positions_by_height.setdefault(height, []).append(position)

    thresholds = sorted(positions_by_height, reverse=True)
    roots = []
    current_root = 0
    for height in thresholds:
        for position in positions_by_height[height]:
            current_root = activate(current_root, 0, size, position)
        roots.append(current_root)

    query_count = int(input_stream.readline())
    output = []
    for _ in range(query_count):
        left, right, width = map(int, input_stream.readline().split())
        low = 0
        high = len(thresholds) - 1
        while low < high:
            middle = (low + high) // 2
            state = range_state(roots[middle], 0, size, left - 1, right)
            if state[2] >= width:
                high = middle
            else:
                low = middle + 1
        output.append(str(thresholds[low]))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Each root represents exactly one height threshold. The monoid returns the exact
longest active run inside the query interval, and version feasibility is
monotone, so binary search returns the greatest feasible height.

**Complexity:** `O(n log n)` build time and storage; `O(log^2 n)` per query.
