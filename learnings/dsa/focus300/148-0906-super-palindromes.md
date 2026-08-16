# Focus300 148: LeetCode 906 - Super Palindromes

**Source:** [LeetCode 906](https://leetcode.com/problems/super-palindromes/)  
**Difficulty:** Hard  
**Pattern:** generate palindromic square roots

## Exact contract

An integer is a super-palindrome when it is a palindrome and its positive
integer square root is also a palindrome. Given decimal strings `left` and
`right` with `1 <= left <= right <= 10^18`, return the number of
super-palindromes in that inclusive range.

## First principles

A qualifying square must come from a palindromic root no larger than `10^9`.
Generate roots by mirroring a prefix into odd- and even-length palindromes, then
square each root and test the square. This visits about `10^5` prefixes instead
of up to one billion roots.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- Both range endpoints are inclusive.
- Use integer square roots; floating-point rounding near `10^18` is unsafe.
- Root `1` and square `1` are valid.
- Odd and even root lengths require different mirroring.
- Stop only when both mirrored roots exceed `isqrt(right)`.

## Brute force: inspect every root in the range

```python
from math import isqrt


def superpalindromes_in_range_brute(left: str, right: str) -> int:
    if (
        not left.isdigit()
        or not right.isdigit()
        or str(int(left)) != left
        or str(int(right)) != right
    ):
        raise ValueError("bounds must be canonical positive decimal strings")
    lower = int(left)
    upper = int(right)
    if not 1 <= lower <= upper <= 10**18:
        raise ValueError("bounds must satisfy 1 <= left <= right <= 1e18")

    first_root = isqrt(lower)
    if first_root * first_root < lower:
        first_root += 1
    answer = 0
    for root in range(first_root, isqrt(upper) + 1):
        root_text = str(root)
        square_text = str(root * root)
        if root_text == root_text[::-1] and square_text == square_text[::-1]:
            answer += 1
    return answer
```

The source range can require checking nearly `10^9` roots.

## Better transition: a palindrome is determined by half its digits

Mirroring each positive prefix produces every positive palindrome exactly once
for each parity. Only the resulting square still needs a palindrome test.

## Expert solution: enumerate mirrored roots

```python
from math import isqrt


def superpalindromes_in_range(left: str, right: str) -> int:
    if (
        not left.isdigit()
        or not right.isdigit()
        or str(int(left)) != left
        or str(int(right)) != right
    ):
        raise ValueError("bounds must be canonical positive decimal strings")
    lower = int(left)
    upper = int(right)
    if not 1 <= lower <= upper <= 10**18:
        raise ValueError("bounds must satisfy 1 <= left <= right <= 1e18")

    root_limit = isqrt(upper)
    answer = 0
    prefix = 1
    while True:
        text = str(prefix)
        odd_root = int(text + text[-2::-1])
        even_root = int(text + text[::-1])
        if odd_root > root_limit and even_root > root_limit:
            break
        for root in (odd_root, even_root):
            if root > root_limit:
                continue
            square = root * root
            square_text = str(square)
            if square >= lower and square_text == square_text[::-1]:
                answer += 1
        prefix += 1
    return answer
```

Every palindromic root appears as exactly one odd or even mirror. Testing its
square completes both conditions without duplicate counting.

**Complexity:** `O(10^(d/2) * d)` time for `d <= 9` root digits and `O(d)`
space per generated value.
