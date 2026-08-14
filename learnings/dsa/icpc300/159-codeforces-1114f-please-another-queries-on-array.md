# ICPC300 159: Codeforces 1114F - Please, another Queries on Array

**Source:** [Codeforces 1114F - Please, another Queries on Array](https://codeforces.com/problemset/problem/1114/F)  
**Rating:** 2400  
**Pattern:** lazy product segment tree with prime-factor bitmasks  
**Goal:** Support `MULTIPLY left right x` and return Euler's totient of the
product on a `TOTIENT left right` range, modulo `1_000_000_007`. Initial values
and multipliers are between `1` and `300`.

The code uses zero-based inclusive ranges; subtract one from the source input.

## 1. First principles

Euler's product formula separates the range product from its distinct primes:

```text
phi(product) = product * product_over_distinct_primes((p - 1) / p)
```

There are only 62 primes at most 300, so their presence fits in one integer
bitmask. Segment concatenation multiplies products and ORs masks. Multiplying a
segment of length `length` by `x` changes its product by `x^length` and ORs in
the mask of `x`.

## 2. Cases that decide correctness

- Repeated occurrences of a prime affect the product but set only one mask bit.
- Multiplication by one changes neither aggregate.
- `phi(1) = 1`.
- Range endpoints are inclusive.
- Products, powers, and modular inverses use `1_000_000_007`, but masks do not.

## 3. Brute force: keep exact integers

```python
from math import prod


MODULO = 1_000_000_007


def range_totients_brute(
    values: list[int],
    operations: list[tuple[str, int, int] | tuple[str, int, int, int]],
) -> list[int]:
    if not values or any(not 1 <= value <= 300 for value in values):
        raise ValueError("values must be integers from 1 through 300")

    current = values.copy()
    answers: list[int] = []
    for operation in operations:
        command = operation[0]
        if command == "multiply":
            if len(operation) != 4:
                raise ValueError("multiply requires left, right, and value")
            left, right, multiplier = operation[1:]
            if not 0 <= left <= right < len(current) or not 1 <= multiplier <= 300:
                raise ValueError("invalid multiply operation")
            for index in range(left, right + 1):
                current[index] *= multiplier
        elif command == "totient":
            if len(operation) != 3:
                raise ValueError("totient requires left and right")
            left, right = operation[1:]
            if not 0 <= left <= right < len(current):
                raise ValueError("invalid totient range")
            product = prod(current[left : right + 1])
            answer = product
            remaining = product
            factor = 2
            while factor * factor <= remaining:
                if remaining % factor == 0:
                    answer -= answer // factor
                    while remaining % factor == 0:
                        remaining //= factor
                factor += 1
            if remaining > 1:
                answer -= answer // remaining
            answers.append(answer % MODULO)
        else:
            raise ValueError("unknown operation")
    return answers
```

**Complexity:** Unbounded big-integer growth plus trial division makes this
exponential in the accumulated input bit length.

## 4. Better: bounded per-element products and masks

```python
MODULO = 1_000_000_007


def range_totients_scan(
    values: list[int],
    operations: list[tuple[str, int, int] | tuple[str, int, int, int]],
) -> list[int]:
    if not values or any(not 1 <= value <= 300 for value in values):
        raise ValueError("values must be integers from 1 through 300")

    primes: list[int] = []
    for candidate in range(2, 301):
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)

    def prime_mask(value: int) -> int:
        mask = 0
        for bit, prime in enumerate(primes):
            if value % prime == 0:
                mask |= 1 << bit
        return mask

    products = [value % MODULO for value in values]
    masks = [prime_mask(value) for value in values]
    totient_factors = [
        (prime - 1) * pow(prime, MODULO - 2, MODULO) % MODULO for prime in primes
    ]
    answers: list[int] = []
    for operation in operations:
        command = operation[0]
        if command == "multiply":
            if len(operation) != 4:
                raise ValueError("multiply requires left, right, and value")
            left, right, multiplier = operation[1:]
            if not 0 <= left <= right < len(values) or not 1 <= multiplier <= 300:
                raise ValueError("invalid multiply operation")
            multiplier_mask = prime_mask(multiplier)
            for index in range(left, right + 1):
                products[index] = products[index] * multiplier % MODULO
                masks[index] |= multiplier_mask
        elif command == "totient":
            if len(operation) != 3:
                raise ValueError("totient requires left and right")
            left, right = operation[1:]
            if not 0 <= left <= right < len(values):
                raise ValueError("invalid totient range")
            product = 1
            mask = 0
            for index in range(left, right + 1):
                product = product * products[index] % MODULO
                mask |= masks[index]
            for bit, factor in enumerate(totient_factors):
                if mask >> bit & 1:
                    product = product * factor % MODULO
            answers.append(product)
        else:
            raise ValueError("unknown operation")
    return answers
```

**Complexity:** `O(n + sum of operation lengths + 62q)` time and `O(n+q)`
space, with every integer bounded.

## 5. Expert solution: product-and-mask lazy tree

```python
MODULO = 1_000_000_007


def range_totients_segment_tree(
    values: list[int],
    operations: list[tuple[str, int, int] | tuple[str, int, int, int]],
) -> list[int]:
    if not values or any(not 1 <= value <= 300 for value in values):
        raise ValueError("values must be integers from 1 through 300")

    primes: list[int] = []
    for candidate in range(2, 301):
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)

    def prime_mask(value: int) -> int:
        mask = 0
        for bit, prime in enumerate(primes):
            if value % prime == 0:
                mask |= 1 << bit
        return mask

    size = len(values)
    product_tree = [1] * (4 * size)
    mask_tree = [0] * (4 * size)
    lazy_product = [1] * (4 * size)
    lazy_mask = [0] * (4 * size)

    def merge(node: int) -> None:
        product_tree[node] = (
            product_tree[2 * node] * product_tree[2 * node + 1]
        ) % MODULO
        mask_tree[node] = mask_tree[2 * node] | mask_tree[2 * node + 1]

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            product_tree[node] = values[left] % MODULO
            mask_tree[node] = prime_mask(values[left])
            return
        middle = (left + right) // 2
        build(2 * node, left, middle)
        build(2 * node + 1, middle + 1, right)
        merge(node)

    def apply(
        node: int,
        length: int,
        multiplier: int,
        multiplier_mask: int,
    ) -> None:
        product_tree[node] = (
            product_tree[node] * pow(multiplier, length, MODULO)
        ) % MODULO
        mask_tree[node] |= multiplier_mask
        lazy_product[node] = lazy_product[node] * multiplier % MODULO
        lazy_mask[node] |= multiplier_mask

    def push(node: int, left: int, right: int) -> None:
        multiplier = lazy_product[node]
        multiplier_mask = lazy_mask[node]
        if left == right or (multiplier == 1 and multiplier_mask == 0):
            return
        middle = (left + right) // 2
        apply(2 * node, middle - left + 1, multiplier, multiplier_mask)
        apply(
            2 * node + 1,
            right - middle,
            multiplier,
            multiplier_mask,
        )
        lazy_product[node] = 1
        lazy_mask[node] = 0

    def update(
        node: int,
        left: int,
        right: int,
        update_left: int,
        update_right: int,
        multiplier: int,
        multiplier_mask: int,
    ) -> None:
        if update_left <= left and right <= update_right:
            apply(
                node,
                right - left + 1,
                multiplier,
                multiplier_mask,
            )
            return
        push(node, left, right)
        middle = (left + right) // 2
        if update_left <= middle:
            update(
                2 * node,
                left,
                middle,
                update_left,
                update_right,
                multiplier,
                multiplier_mask,
            )
        if update_right > middle:
            update(
                2 * node + 1,
                middle + 1,
                right,
                update_left,
                update_right,
                multiplier,
                multiplier_mask,
            )
        merge(node)

    def query(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> tuple[int, int]:
        if query_left <= left and right <= query_right:
            return product_tree[node], mask_tree[node]
        push(node, left, right)
        middle = (left + right) // 2
        product = 1
        mask = 0
        if query_left <= middle:
            left_product, left_mask = query(
                2 * node,
                left,
                middle,
                query_left,
                query_right,
            )
            product = product * left_product % MODULO
            mask |= left_mask
        if query_right > middle:
            right_product, right_mask = query(
                2 * node + 1,
                middle + 1,
                right,
                query_left,
                query_right,
            )
            product = product * right_product % MODULO
            mask |= right_mask
        return product, mask

    build(1, 0, size - 1)
    totient_factors = [
        (prime - 1) * pow(prime, MODULO - 2, MODULO) % MODULO for prime in primes
    ]
    answers: list[int] = []
    for operation in operations:
        command = operation[0]
        if command == "multiply":
            if len(operation) != 4:
                raise ValueError("multiply requires left, right, and value")
            left, right, multiplier = operation[1:]
            if not 0 <= left <= right < size or not 1 <= multiplier <= 300:
                raise ValueError("invalid multiply operation")
            update(
                1,
                0,
                size - 1,
                left,
                right,
                multiplier,
                prime_mask(multiplier),
            )
        elif command == "totient":
            if len(operation) != 3:
                raise ValueError("totient requires left and right")
            left, right = operation[1:]
            if not 0 <= left <= right < size:
                raise ValueError("invalid totient range")
            product, mask = query(1, 0, size - 1, left, right)
            for bit, factor in enumerate(totient_factors):
                if mask >> bit & 1:
                    product = product * factor % MODULO
            answers.append(product)
        else:
            raise ValueError("unknown operation")
    return answers
```

### Why the expert code is correct

Every node stores the product of its interval and exactly the union of its
prime divisors. The merge operations are multiplication and bitwise OR, and a
lazy multiplication updates both aggregates exactly for the node's length.
Euler's product formula then converts the queried pair into `phi(product)`;
all listed primes are invertible modulo `1_000_000_007`.

**Complexity:** `O(log^2 n)` per multiply, `O(log n + 62)` per totient query,
and `O(n+q)` space.

## 6. What to remember

```text
phi(x) -> product value plus set of distinct prime divisors
values at most 300 -> prime set fits one bitmask
range multiply -> x^length for product, OR mask for divisors
```
