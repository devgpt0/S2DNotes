# 146. Sasha and Array — Codeforces 718C

**Source:** [Codeforces 718C - Sasha and Array](https://codeforces.com/problemset/problem/718/C)  
**Difficulty:** 2500

## 1. Problem in plain words

Maintain a positive-integer array. Operation `1 left right x` adds `x` to every value in the range. Operation `2 left right` asks for the sum of Fibonacci numbers `F[value]` over that range, modulo `1_000_000_007`.

The functions use zero-based inclusive endpoints.

## 2. First principles

Use the Fibonacci state vector `[F(a), F(a+1)]`. Adding `x` to `a` multiplies this vector by the Fibonacci transition matrix `Q^x`. Matrix multiplication distributes over addition, so a whole segment's summed vector can be transformed at once.

A lazy segment tree stores the two vector sums and a pending transition matrix.

## 3. Cases that define correctness

- An addition of zero is the identity transition.
- Several pending additions compose by matrix multiplication.
- Query output uses only the first component, `sum F(a)`.
- Exponents can be large, so transitions use logarithmic fast doubling.

## 4. Brute force

Update every value directly and evaluate Fibonacci numbers by fast doubling on each query.

```python
MODULO = 1_000_000_007


def sasha_array_brute_force(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    def fibonacci_pair(index: int) -> tuple[int, int]:
        if index == 0:
            return 0, 1
        first, second = fibonacci_pair(index // 2)
        doubled = first * ((2 * second - first) % MODULO) % MODULO
        adjacent = (first * first + second * second) % MODULO
        if index % 2:
            return adjacent, (doubled + adjacent) % MODULO
        return doubled, adjacent

    data = values.copy()
    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (3, 4):
            raise ValueError("invalid operation")
        kind, left, right = operation[:3]
        if not 0 <= left <= right < len(data):
            raise ValueError("invalid interval")
        if kind == 1 and len(operation) == 4:
            increment = operation[3]
            if increment < 0:
                raise ValueError("increment must be nonnegative")
            for index in range(left, right + 1):
                data[index] += increment
        elif kind == 2 and len(operation) == 3:
            answers.append(
                sum(fibonacci_pair(data[index])[0] for index in range(left, right + 1))
                % MODULO
            )
        else:
            raise ValueError("invalid operation")
    return answers
```

Worst-case time is `O(qn log A)` and space is `O(n + log A)`.

## 5. Better approach: block decomposition

Each block stores its summed Fibonacci vector plus one pending numeric addition. Full-block updates transform the vector; boundary fragments are materialized and rebuilt.

```python
from math import isqrt

MODULO = 1_000_000_007


def sasha_array_blocks(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    def fibonacci_pair(index: int) -> tuple[int, int]:
        if index == 0:
            return 0, 1
        first, second = fibonacci_pair(index // 2)
        doubled = first * ((2 * second - first) % MODULO) % MODULO
        adjacent = (first * first + second * second) % MODULO
        if index % 2:
            return adjacent, (doubled + adjacent) % MODULO
        return doubled, adjacent

    def shift(vector: tuple[int, int], amount: int) -> tuple[int, int]:
        current, following = fibonacci_pair(amount)
        previous = (following - current) % MODULO
        first, second = vector
        return (
            (previous * first + current * second) % MODULO,
            (current * first + following * second) % MODULO,
        )

    size = len(values)
    block_size = isqrt(size) + 1
    block_count = (size + block_size - 1) // block_size
    data = values.copy()
    lazy = [0] * block_count
    sums = [(0, 0)] * block_count

    def rebuild(block: int) -> None:
        left = block * block_size
        right = min(size, left + block_size)
        first_sum = 0
        second_sum = 0
        for index in range(left, right):
            first, second = fibonacci_pair(data[index])
            first_sum += first
            second_sum += second
        sums[block] = first_sum % MODULO, second_sum % MODULO

    def materialize(block: int) -> None:
        amount = lazy[block]
        if amount == 0:
            return
        left = block * block_size
        right = min(size, left + block_size)
        for index in range(left, right):
            data[index] += amount
        lazy[block] = 0

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (3, 4):
            raise ValueError("invalid operation")
        kind, left, right = operation[:3]
        if not 0 <= left <= right < size:
            raise ValueError("invalid interval")
        if kind == 1 and len(operation) == 4:
            amount = operation[3]
            if amount < 0:
                raise ValueError("increment must be nonnegative")
            first_block = left // block_size
            last_block = right // block_size
            for block in range(first_block, last_block + 1):
                block_left = block * block_size
                block_right = min(size, block_left + block_size) - 1
                if left <= block_left and block_right <= right:
                    sums[block] = shift(sums[block], amount)
                    lazy[block] += amount
                else:
                    materialize(block)
                    for index in range(
                        max(left, block_left), min(right, block_right) + 1
                    ):
                        data[index] += amount
                    rebuild(block)
        elif kind == 2 and len(operation) == 3:
            answer = 0
            index = left
            while index <= right:
                block = index // block_size
                block_left = block * block_size
                block_right = min(size, block_left + block_size) - 1
                if index == block_left and block_right <= right:
                    answer += sums[block][0]
                    index = block_right + 1
                else:
                    answer += fibonacci_pair(data[index] + lazy[block])[0]
                    index += 1
            answers.append(answer % MODULO)
        else:
            raise ValueError("invalid operation")
    return answers
```

Each operation costs `O(sqrt(n) log A)` worst case and space is `O(n)`.

## 6. Expert solution: lazy Fibonacci-vector segment tree

Store `(sum F(a), sum F(a+1))` per node. Range addition applies `Q^x` to that pair and composes the same matrix into the lazy tag.

```python
MODULO = 1_000_000_007
IDENTITY: tuple[int, int, int, int] = (1, 0, 0, 1)


def sasha_array(values: list[int], operations: list[tuple[int, ...]]) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    def fibonacci_pair(index: int) -> tuple[int, int]:
        if index == 0:
            return 0, 1
        first, second = fibonacci_pair(index // 2)
        doubled = first * ((2 * second - first) % MODULO) % MODULO
        adjacent = (first * first + second * second) % MODULO
        if index % 2:
            return adjacent, (doubled + adjacent) % MODULO
        return doubled, adjacent

    def transition(amount: int) -> tuple[int, int, int, int]:
        current, following = fibonacci_pair(amount)
        return (following - current) % MODULO, current, current, following

    def multiply(
        first: tuple[int, int, int, int], second: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:
        a, b, c, d = first
        e, f, g, h = second
        return (
            (a * e + b * g) % MODULO,
            (a * f + b * h) % MODULO,
            (c * e + d * g) % MODULO,
            (c * f + d * h) % MODULO,
        )

    size = len(values)
    first_sum = [0] * (4 * size)
    second_sum = [0] * (4 * size)
    lazy = [IDENTITY] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            first_sum[node], second_sum[node] = fibonacci_pair(values[left])
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle + 1, right)
        first_sum[node] = (first_sum[node * 2] + first_sum[node * 2 + 1]) % MODULO
        second_sum[node] = (second_sum[node * 2] + second_sum[node * 2 + 1]) % MODULO

    def apply(node: int, matrix: tuple[int, int, int, int]) -> None:
        a, b, c, d = matrix
        old_first = first_sum[node]
        old_second = second_sum[node]
        first_sum[node] = (a * old_first + b * old_second) % MODULO
        second_sum[node] = (c * old_first + d * old_second) % MODULO
        lazy[node] = multiply(matrix, lazy[node])

    def push(node: int) -> None:
        if lazy[node] != IDENTITY:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = IDENTITY

    def update(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        matrix: tuple[int, int, int, int],
    ) -> None:
        if query_left <= left and right <= query_right:
            apply(node, matrix)
            return
        push(node)
        middle = (left + right) // 2
        if query_left <= middle:
            update(node * 2, left, middle, query_left, query_right, matrix)
        if middle < query_right:
            update(node * 2 + 1, middle + 1, right, query_left, query_right, matrix)
        first_sum[node] = (first_sum[node * 2] + first_sum[node * 2 + 1]) % MODULO
        second_sum[node] = (second_sum[node * 2] + second_sum[node * 2 + 1]) % MODULO

    def query(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> int:
        if query_left <= left and right <= query_right:
            return first_sum[node]
        push(node)
        middle = (left + right) // 2
        answer = 0
        if query_left <= middle:
            answer += query(node * 2, left, middle, query_left, query_right)
        if middle < query_right:
            answer += query(node * 2 + 1, middle + 1, right, query_left, query_right)
        return answer % MODULO

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (3, 4):
            raise ValueError("invalid operation")
        kind, left, right = operation[:3]
        if not 0 <= left <= right < size:
            raise ValueError("invalid interval")
        if kind == 1 and len(operation) == 4:
            amount = operation[3]
            if amount < 0:
                raise ValueError("increment must be nonnegative")
            update(1, 0, size - 1, left, right, transition(amount))
        elif kind == 2 and len(operation) == 3:
            answers.append(query(1, 0, size - 1, left, right))
        else:
            raise ValueError("invalid operation")
    return answers
```

## 7. Why the expert solution is correct

Every leaf stores the exact Fibonacci state of its value, and internal nodes sum those states. Adding `x` applies `Q^x` to each leaf; linearity makes applying it once to the node sum equivalent. Lazy matrices compose the same transitions in chronological order, so queried first components are exactly the requested Fibonacci sums.

Time is `O(n log A + q(log n + log A))`, including Fibonacci transition construction, and space is `O(n)`.
