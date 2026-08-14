# ICPC300 288: Codeforces 855E - Salazar Slytherin's Locket

**Source:** [Codeforces 855E - Salazar Slytherin's Locket](https://codeforces.com/problemset/problem/855/E)  
**Rating:** 2300  
**Pattern:** base-dependent digit parity DP  
**Goal:** For every `(base, left, right)` query, count positive integers in the
inclusive range whose base-`base` representation uses every digit an even
number of times.

## 1. First principles

Only the parity of each digit count matters. Reading digit `d` toggles bit `d`
of a mask, and a number is valid exactly when the final mask is zero. Precompute
how many fixed-length digit strings realize every parity mask for each base.

## 2. Cases that decide correctness

- Bases range from 2 through 10.
- Leading zeros are not representation digits.
- Zeros after the first nonzero digit do toggle digit zero.
- Both range endpoints are inclusive and positive.
- Shorter representations must be counted before matching the limit's length.

## 3. Brute force: convert every number

```python
def locket_query_counts_brute(
    queries: list[tuple[int, int, int]],
) -> list[int]:
    if not queries or any(
        not 2 <= base <= 10 or not 1 <= left <= right for base, left, right in queries
    ):
        raise ValueError("invalid query")

    answers: list[int] = []
    for base, left, right in queries:
        answer = 0
        for value in range(left, right + 1):
            parity = 0
            remaining = value
            while remaining:
                parity ^= 1 << (remaining % base)
                remaining //= base
            answer += parity == 0
        answers.append(answer)
    return answers
```

**Complexity:** `O(sum(range length * log_base right))` time.

## 4. Better transition: precompute suffix parity counts

Let `ways[length][mask]` count length-`length` digit strings, including leading
zeros inside the suffix, whose parity is `mask`. While scanning a limit, trying
a smaller current digit leaves a suffix whose required parity is known.

## 5. Expert solution: prefix counting with parity tables

```python
def locket_query_counts(queries: list[tuple[int, int, int]]) -> list[int]:
    if not queries or any(
        not 2 <= base <= 10 or not 1 <= left <= right for base, left, right in queries
    ):
        raise ValueError("invalid query")

    maximum_length: dict[int, int] = {}

    def digits_of(value: int, base: int) -> list[int]:
        digits: list[int] = []
        while value:
            digits.append(value % base)
            value //= base
        return digits[::-1]

    for base, _left, right in queries:
        maximum_length[base] = max(
            maximum_length.get(base, 0), len(digits_of(right, base))
        )

    tables: dict[int, list[list[int]]] = {}
    for base, length_limit in maximum_length.items():
        ways = [[0] * (1 << base) for _ in range(length_limit + 1)]
        ways[0][0] = 1
        for length in range(1, length_limit + 1):
            previous = ways[length - 1]
            current = ways[length]
            for mask in range(1 << base):
                current[mask] = sum(
                    previous[mask ^ (1 << digit)] for digit in range(base)
                )
        tables[base] = ways

    def count_up_to(limit: int, base: int) -> int:
        if limit <= 0:
            return 0
        digits = digits_of(limit, base)
        ways = tables[base]
        answer = 0
        for length in range(1, len(digits)):
            for first_digit in range(1, base):
                answer += ways[length - 1][1 << first_digit]

        parity = 0
        for position, current_digit in enumerate(digits):
            minimum = 1 if position == 0 else 0
            remaining = len(digits) - position - 1
            for digit in range(minimum, current_digit):
                required_suffix = parity ^ (1 << digit)
                answer += ways[remaining][required_suffix]
            parity ^= 1 << current_digit
        return answer + (parity == 0)

    return [
        count_up_to(right, base) - count_up_to(left - 1, base)
        for base, left, right in queries
    ]
```

### Why the expert code is correct

The precomputed table counts every possible suffix by its exact parity mask.
The prefix scan partitions numbers below the limit at their first smaller
digit, then requests the only suffix parity that cancels the chosen prefix.
Shorter lengths and the limit itself are handled separately, with no leading
zero representation counted.

**Complexity:** `O(sum_base(L * base * 2^base) + q * L * base)` time and
`O(sum_base(L * 2^base))` space.

## 6. What to remember

```text
even occurrence of every digit -> parity mask zero
many queries per base -> precompute suffix masks once
bounded count -> first smaller digit plus a free suffix
```
