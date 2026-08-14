# ICPC300 053: CSES - Pizzeria Queries

**Source:** [CSES - Pizzeria Queries](https://cses.fi/problemset/task/2206/)  
**Pattern:** transformed range minima  
**Goal:** Update pizza prices and answer
`min(price[i] + abs(i - customer))`.

The implementations use zero-based indices. Operations are `(1, index, price)`
and `(2, customer)`.

## 1. First principles

Split candidate pizzerias by which side of the customer they occupy:

```text
i <= customer: price[i] + customer - i
               = customer + (price[i] - i)

i >= customer: price[i] + i - customer
               = -customer + (price[i] + i)
```

The absolute value disappears. Maintain range minima for the transformed
arrays `price[i] - i` and `price[i] + i`.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Pizzeria at the customer | Include it in both sides without changing the minimum. |
| Best pizzeria is left | Add the customer index to `price[i] - i`. |
| Best pizzeria is right | Subtract the customer index from `price[i] + i`. |
| Endpoint customer | One transformed range contains a single endpoint. |
| Price update | Update both transformed values. |

## 3. Brute force: inspect every pizzeria

```python
def pizzeria_queries_brute(
    prices: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not prices:
        raise ValueError("prices must not be empty")

    current = prices.copy()
    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, index, price = operation
            current[index] = price
        elif operation_type == 2:
            _, customer = operation
            answers.append(
                min(
                    price + abs(index - customer) for index, price in enumerate(current)
                )
            )
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(n)` per query, `O(1)` per update, and `O(n)` space.

## 4. Better: square-root range minima

Store block minima for both transformed arrays. A prefix or suffix minimum
uses whole blocks plus at most two partial blocks.

```python
from math import isqrt


def pizzeria_queries_sqrt(
    prices: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not prices:
        raise ValueError("prices must not be empty")

    block_size = isqrt(len(prices)) + 1
    block_count = (len(prices) + block_size - 1) // block_size
    left_values = [price - index for index, price in enumerate(prices)]
    right_values = [price + index for index, price in enumerate(prices)]
    left_minimum = [0] * block_count
    right_minimum = [0] * block_count

    def rebuild(block: int) -> None:
        start = block * block_size
        end = min(start + block_size, len(prices))
        left_minimum[block] = min(left_values[start:end])
        right_minimum[block] = min(right_values[start:end])

    def range_minimum(
        values: list[int], block_minimum: list[int], left: int, right: int
    ) -> int:
        result: int | None = None
        while left <= right and left % block_size != 0:
            result = values[left] if result is None else min(result, values[left])
            left += 1
        while left + block_size - 1 <= right:
            block_value = block_minimum[left // block_size]
            result = block_value if result is None else min(result, block_value)
            left += block_size
        while left <= right:
            result = values[left] if result is None else min(result, values[left])
            left += 1
        if result is None:
            raise RuntimeError("range must be non-empty")
        return result

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, index, price = operation
            left_values[index] = price - index
            right_values[index] = price + index
            rebuild(index // block_size)
        elif operation_type == 2:
            _, customer = operation
            from_left = customer + range_minimum(left_values, left_minimum, 0, customer)
            from_right = -customer + range_minimum(
                right_values, right_minimum, customer, len(prices) - 1
            )
            answers.append(min(from_left, from_right))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(sqrt(n))` per operation and `O(n)` space.

## 5. Expert solution: two segment trees

One tree stores minima of `price[i] - i`; the other stores minima of
`price[i] + i`.

```python
def pizzeria_queries_segment_tree(
    prices: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not prices:
        raise ValueError("prices must not be empty")

    size = 1
    while size < len(prices):
        size *= 2
    infinity = 1 << 62

    def build(transformed: list[int]) -> list[int]:
        tree = [infinity] * (2 * size)
        tree[size : size + len(transformed)] = transformed
        for node in range(size - 1, 0, -1):
            tree[node] = min(tree[2 * node], tree[2 * node + 1])
        return tree

    left_tree = build([price - index for index, price in enumerate(prices)])
    right_tree = build([price + index for index, price in enumerate(prices)])

    def assign(tree: list[int], index: int, value: int) -> None:
        node = size + index
        tree[node] = value
        node //= 2
        while node > 0:
            tree[node] = min(tree[2 * node], tree[2 * node + 1])
            node //= 2

    def range_minimum(tree: list[int], left: int, right: int) -> int:
        left += size
        right += size
        result = infinity
        while left <= right:
            if left % 2 == 1:
                result = min(result, tree[left])
                left += 1
            if right % 2 == 0:
                result = min(result, tree[right])
                right -= 1
            left //= 2
            right //= 2
        return result

    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, index, price = operation
            assign(left_tree, index, price - index)
            assign(right_tree, index, price + index)
        elif operation_type == 2:
            _, customer = operation
            answers.append(
                min(
                    customer + range_minimum(left_tree, 0, customer),
                    -customer + range_minimum(right_tree, customer, len(prices) - 1),
                )
            )
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

### Why the expert code is correct

- The two algebraic transforms exactly equal delivery cost on their respective
  sides of the customer.
- Their queried ranges cover every pizzeria and overlap only at the customer.
- Taking the smaller transformed minimum therefore equals the global minimum
  delivery price.

**Complexity:** `O(n)` construction, `O(log n)` per operation, and `O(n)`
space.

## 6. What to remember

```text
absolute distance -> split left and right
left candidates  store price[i] - i
right candidates store price[i] + i
```
