# 150. Mahmoud and Ehab and yet another xor task — Codeforces 959F

**Source:** [Codeforces 959F - Mahmoud and Ehab and yet another xor task](https://codeforces.com/problemset/problem/959/F)  
**Difficulty:** 2300

## 1. Problem in plain words

Each query `(length, target)` asks how many subsets of the first `length` array elements have XOR equal to `target`. The empty subset is allowed. Print answers modulo `1_000_000_007`.

## 2. First principles

XOR combinations form a vector space over bits. A linear basis of rank `r` spans exactly `2^r` XOR values. Among `length` input vectors, every spanned XOR has exactly `2^(length-r)` subset representations because the remaining choices form the basis transformation's kernel.

Sort queries by prefix length, insert new values into one basis, and test whether each target reduces to zero.

## 3. Cases that define correctness

- Target zero always has at least the empty subset.
- A linearly dependent inserted value doubles every existing representation count.
- An unrepresentable target has answer zero.
- Equal array values are separate subset choices but usually basis-dependent.

## 4. Brute force

Enumerate every subset of the requested prefix.

```python
MODULO = 1_000_000_007


def prefix_xor_subset_counts_brute_force(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    answers: list[int] = []
    for length, target in queries:
        if not 0 <= length <= len(values) or target < 0:
            raise ValueError("invalid query")
        answer = 0
        for chosen in range(1 << length):
            result = 0
            for index in range(length):
                if chosen >> index & 1:
                    result ^= values[index]
            answer += result == target
        answers.append(answer % MODULO)
    return answers
```

Worst-case time is `O(qn2ⁿ)` and space is `O(1)`.

## 5. Better approach: explicit XOR-state DP

Process queries by prefix length. For every new value, either omit or include it in every existing XOR state.

```python
MODULO = 1_000_000_007


def prefix_xor_subset_counts_dp(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    ordered: list[tuple[int, int, int]] = []
    for index, (length, target) in enumerate(queries):
        if not 0 <= length <= len(values) or target < 0:
            raise ValueError("invalid query")
        ordered.append((length, target, index))
    ordered.sort()

    counts = {0: 1}
    answers = [0] * len(queries)
    processed = 0
    for length, target, query_index in ordered:
        while processed < length:
            value = values[processed]
            next_counts = counts.copy()
            for current_xor, amount in counts.items():
                combined = current_xor ^ value
                next_counts[combined] = (next_counts.get(combined, 0) + amount) % MODULO
            counts = next_counts
            processed += 1
        answers[query_index] = counts.get(target, 0)
    return answers
```

With `s` reachable XOR states, time is `O(ns + q log q)` and space is `O(s + q)`; `s` can be exponential in bit width.

## 6. Expert solution: offline linear basis

Maintain one pivot per highest set bit. Insertion either creates a new pivot and raises the rank or reduces to zero and adds one dependent choice.

```python
MODULO = 1_000_000_007


def prefix_xor_subset_counts(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    ordered: list[tuple[int, int, int]] = []
    maximum = max(values, default=0)
    for index, (length, target) in enumerate(queries):
        if not 0 <= length <= len(values) or target < 0:
            raise ValueError("invalid query")
        ordered.append((length, target, index))
        maximum = max(maximum, target)
    ordered.sort()

    bit_count = max(1, maximum.bit_length())
    basis = [0] * bit_count
    rank = 0

    def insert(value: int) -> None:
        nonlocal rank
        for bit in range(bit_count - 1, -1, -1):
            if value >> bit & 1 == 0:
                continue
            if basis[bit]:
                value ^= basis[bit]
            else:
                basis[bit] = value
                rank += 1
                return

    def representable(value: int) -> bool:
        for bit in range(bit_count - 1, -1, -1):
            if value >> bit & 1:
                if basis[bit] == 0:
                    return False
                value ^= basis[bit]
        return True

    powers_of_two = [1] * (len(values) + 1)
    for exponent in range(1, len(powers_of_two)):
        powers_of_two[exponent] = powers_of_two[exponent - 1] * 2 % MODULO

    answers = [0] * len(queries)
    processed = 0
    for length, target, query_index in ordered:
        while processed < length:
            insert(values[processed])
            processed += 1
        if representable(target):
            answers[query_index] = powers_of_two[length - rank]
    return answers
```

## 7. Why the expert solution is correct

Gaussian elimination over XOR preserves exactly the span of the processed prefix. The target reduces to zero exactly when it lies in that span. A rank-`r` linear map from `length` subset-choice bits has a kernel of size `2^(length-r)`, so every representable target has exactly that many preimages and every other target has none.

Time is `O((n + q)B + q log q)` and space is `O(B + q + n)` for bit width `B`.
