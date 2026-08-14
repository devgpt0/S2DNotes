# ICPC300 258: Codeforces 1245F - Daniel and Spring Cleaning

**Source:** [Codeforces 1245F - Daniel and Spring Cleaning](https://codeforces.com/problemset/problem/1245/F)  
**Rating:** 2200  
**Pattern:** two-number tight bit DP with symmetry reduction  
**Goal:** For each range `[left, right]`, count pairs
`left <= first <= second <= right` such that `first + second = first XOR second`.

## 1. First principles

Binary addition equals XOR exactly when it creates no carries:

```text
first + second = first XOR second  <=>  first & second = 0
```

Digit-DP over two upper bounds counts ordered pairs with no position choosing
bit one for both numbers. Inclusion-exclusion restricts both numbers to the
requested range. Symmetry converts ordered pairs to `first <= second`; the only
valid equal pair is `(0, 0)`.

## 2. Cases that decide correctness

- Range endpoints are inclusive and nonnegative.
- Bit pair `(1, 1)` is forbidden at every position.
- Ordered unequal pairs occur in symmetric pairs.
- The diagonal contributes once only when zero lies in the range.
- Negative upper bounds contribute zero during inclusion-exclusion.

## 3. Brute force: inspect every unordered pair

```python
def spring_cleaning_counts_brute(
    ranges: list[tuple[int, int]],
) -> list[int]:
    for left, right in ranges:
        if not 0 <= left <= right:
            raise ValueError("ranges must be nonnegative and ordered")
    return [
        sum(
            first & second == 0
            for first in range(left, right + 1)
            for second in range(first, right + 1)
        )
        for left, right in ranges
    ]
```

**Complexity:** `O(sum of squared range lengths)` time and `O(1)` space.

## 4. Better transition: count a bounded rectangle of bit pairs

The no-carry condition is local to each bit. Two tight flags record whether the
constructed numbers still equal their respective upper-bound prefixes, giving
a constant number of states per bit.

## 5. Expert solution: rectangle digit DP and symmetry

```python
from functools import lru_cache


def spring_cleaning_counts(ranges: list[tuple[int, int]]) -> list[int]:
    for left, right in ranges:
        if not 0 <= left <= right:
            raise ValueError("ranges must be nonnegative and ordered")

    def ordered_pairs(first_limit: int, second_limit: int) -> int:
        if first_limit < 0 or second_limit < 0:
            return 0
        bit_count = max(1, first_limit.bit_length(), second_limit.bit_length())

        @lru_cache(maxsize=None)
        def count(position: int, first_tight: bool, second_tight: bool) -> int:
            if position < 0:
                return 1
            first_bound = (first_limit >> position) & 1 if first_tight else 1
            second_bound = (second_limit >> position) & 1 if second_tight else 1
            answer = 0
            for first_bit in range(first_bound + 1):
                for second_bit in range(second_bound + 1):
                    if first_bit & second_bit:
                        continue
                    answer += count(
                        position - 1,
                        first_tight and first_bit == first_bound,
                        second_tight and second_bit == second_bound,
                    )
            return answer

        return count(bit_count - 1, True, True)

    answers: list[int] = []
    for left, right in ranges:
        ordered = (
            ordered_pairs(right, right)
            - ordered_pairs(left - 1, right)
            - ordered_pairs(right, left - 1)
            + ordered_pairs(left - 1, left - 1)
        )
        diagonal = int(left == 0)
        answers.append((ordered + diagonal) // 2)
    return answers
```

### Why the expert code is correct

The bit DP enumerates exactly the ordered bounded pairs without a shared one
bit, which is equivalent to carry-free addition. Rectangle inclusion-exclusion
keeps both values inside `[left,right]`. Every valid unequal unordered pair is
counted twice in ordered form, while `(0,0)` is the sole valid diagonal pair and
is added once before halving.

**Complexity:** `O(32)` DP states per rectangle call and `O(32)` cache space.

## 6. What to remember

```text
sum equals xor -> no carry -> bitwise AND is zero
two bounded numbers -> two tight flags
unordered pair count -> ordered symmetry plus diagonal correction
```
