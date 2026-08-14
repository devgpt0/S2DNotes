# ICPC300 157: Codeforces 446C - DZY Loves Fibonacci Numbers

**Source:** [Codeforces 446C - DZY Loves Fibonacci Numbers](https://codeforces.com/problemset/problem/446/C)  
**Rating:** 2400  
**Pattern:** lazy segment tree with shifted Fibonacci sequences  
**Goal:** Support range updates that add `F1, F2, ...` from the left endpoint
and range-sum queries modulo `1_000_000_009`, where `F1 = F2 = 1`.

The code uses zero-based inclusive ranges; subtract one from the source input.

## 1. First principles

A Fibonacci update does not add one constant to a covered segment. It adds a
sequence whose first two terms determine every later term. If a lazy tag begins
with `(first, second)`, then its term at zero-based offset `k` is

```text
k = 0: first
k > 0: F[k-1] * first + F[k] * second
```

The sum of its first `length` terms is

```text
F[length] * first + (F[length+1] - 1) * second
```

Therefore a segment-tree node needs only two lazy numbers. The right child gets
the same sequence shifted by the left child's length.

## 2. Cases that decide correctness

- Every update restarts with `F1 = 1` at its own left endpoint.
- A fully covered node away from that endpoint receives a shifted pair.
- Overlapping lazy updates add their two starting pairs componentwise.
- A one-element update adds exactly one.
- All stored sums and lazy terms are reduced modulo `1_000_000_009`.

## 3. Brute force: write every Fibonacci term

```python
MODULO = 1_000_000_009


def fibonacci_ranges_brute(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must be nonempty")
    for kind, left, right in operations:
        if kind not in (1, 2) or not 0 <= left <= right < len(values):
            raise ValueError("invalid operation")

    fibonacci = [0, 1]
    for _ in range(len(values) + 1):
        fibonacci.append((fibonacci[-1] + fibonacci[-2]) % MODULO)

    current = [value % MODULO for value in values]
    answers: list[int] = []
    for kind, left, right in operations:
        if kind == 1:
            for index in range(left, right + 1):
                offset = index - left + 1
                current[index] = (current[index] + fibonacci[offset]) % MODULO
        else:
            answers.append(sum(current[left : right + 1]) % MODULO)
    return answers
```

**Complexity:** `O(n + sum of operation lengths)` time and `O(n+q)` space.

## 4. Better transition: make a sequence a lazy value

A constant range-add tag is one number because every position receives the
same value. A Fibonacci range-add tag is two numbers because a second-order
recurrence is fixed by its first two values. Sequence addition and sequence
shifting preserve that representation, so no larger per-node state is needed.

## 5. Expert solution: two-term lazy segment tree

```python
MODULO = 1_000_000_009


def fibonacci_ranges_segment_tree(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must be nonempty")
    for kind, left, right in operations:
        if kind not in (1, 2) or not 0 <= left <= right < len(values):
            raise ValueError("invalid operation")

    size = len(values)
    fibonacci = [0, 1]
    for _ in range(size + 2):
        fibonacci.append((fibonacci[-1] + fibonacci[-2]) % MODULO)

    tree = [0] * (4 * size)
    lazy_first = [0] * (4 * size)
    lazy_second = [0] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            tree[node] = values[left] % MODULO
            return
        middle = (left + right) // 2
        build(2 * node, left, middle)
        build(2 * node + 1, middle + 1, right)
        tree[node] = (tree[2 * node] + tree[2 * node + 1]) % MODULO

    def shifted(first: int, second: int, distance: int) -> tuple[int, int]:
        if distance == 0:
            return first, second
        shifted_first = (
            fibonacci[distance - 1] * first + fibonacci[distance] * second
        ) % MODULO
        shifted_second = (
            fibonacci[distance] * first + fibonacci[distance + 1] * second
        ) % MODULO
        return shifted_first, shifted_second

    def apply(
        node: int,
        length: int,
        first: int,
        second: int,
    ) -> None:
        added_sum = (
            fibonacci[length] * first + (fibonacci[length + 1] - 1) * second
        ) % MODULO
        tree[node] = (tree[node] + added_sum) % MODULO
        lazy_first[node] = (lazy_first[node] + first) % MODULO
        lazy_second[node] = (lazy_second[node] + second) % MODULO

    def push(node: int, left: int, right: int) -> None:
        first = lazy_first[node]
        second = lazy_second[node]
        if left == right or first == second == 0:
            return
        middle = (left + right) // 2
        left_length = middle - left + 1
        apply(2 * node, left_length, first, second)
        right_first, right_second = shifted(first, second, left_length)
        apply(
            2 * node + 1,
            right - middle,
            right_first,
            right_second,
        )
        lazy_first[node] = 0
        lazy_second[node] = 0

    def update(
        node: int,
        left: int,
        right: int,
        update_left: int,
        update_right: int,
    ) -> None:
        if update_left <= left and right <= update_right:
            offset = left - update_left
            apply(
                node,
                right - left + 1,
                fibonacci[offset + 1],
                fibonacci[offset + 2],
            )
            return
        push(node, left, right)
        middle = (left + right) // 2
        if update_left <= middle:
            update(2 * node, left, middle, update_left, update_right)
        if update_right > middle:
            update(
                2 * node + 1,
                middle + 1,
                right,
                update_left,
                update_right,
            )
        tree[node] = (tree[2 * node] + tree[2 * node + 1]) % MODULO

    def query(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_left <= left and right <= query_right:
            return tree[node]
        push(node, left, right)
        middle = (left + right) // 2
        answer = 0
        if query_left <= middle:
            answer += query(2 * node, left, middle, query_left, query_right)
        if query_right > middle:
            answer += query(
                2 * node + 1,
                middle + 1,
                right,
                query_left,
                query_right,
            )
        return answer % MODULO

    build(1, 0, size - 1)
    answers: list[int] = []
    for kind, left, right in operations:
        if kind == 1:
            update(1, 0, size - 1, left, right)
        else:
            answers.append(query(1, 0, size - 1, left, right))
    return answers
```

### Why the expert code is correct

Each lazy pair represents the exact recurrence-aligned sequence pending at a
node's left boundary. The closed-form prefix sum updates the node aggregate.
Pushing gives the left child the unchanged pair and the right child its exact
shift, so both children receive the same position values as a direct update.
Range sums are therefore preserved after every update and query.

**Complexity:** `O((n+q) log n)` time and `O(n+q)` space.

## 6. What to remember

```text
order-two recurrence -> two lazy values
right child -> shift by left-child length
node aggregate -> closed-form sum of the tagged sequence
```
