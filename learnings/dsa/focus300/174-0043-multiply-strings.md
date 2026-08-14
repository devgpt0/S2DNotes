# Focus300 174: LeetCode 43 - Multiply Strings

**Source:** [LeetCode 43](https://leetcode.com/problems/multiply-strings/)  
**Difficulty:** Medium  
**Pattern:** manual decimal arithmetic

## Exact contract

Given canonical decimal strings `first` and `second` representing non-negative
integers, return their product as a canonical decimal string. Do not convert the
whole inputs to integers and do not use arbitrary-precision numeric libraries.

## First principles

Multiplying digits at positions `i` and `j` contributes to output columns
`i + j` and `i + j + 1`. Accumulate every digit product in a fixed array, then
propagate carries from right to left. At most `m + n` output digits are needed.

## Cases that decide correctness

- If either input is `"0"`, return exactly `"0"`.
- Inputs have no leading zero unless the number itself is zero.
- Carry from one column may exceed nine before propagation.
- Every pair of input digits contributes exactly once.
- Strip only unused leading result zeroes, never meaningful internal zeroes.

## Brute force: repeated decimal addition per multiplier digit

```python
def multiply_strings_brute(first: str, second: str) -> str:
    if (
        not first
        or not second
        or any(character not in "0123456789" for character in first + second)
        or (len(first) > 1 and first[0] == "0")
        or (len(second) > 1 and second[0] == "0")
    ):
        raise ValueError("inputs must be canonical non-negative decimal strings")

    def add(left: str, right: str) -> str:
        left_index = len(left) - 1
        right_index = len(right) - 1
        carry = 0
        reversed_digits: list[str] = []
        while left_index >= 0 or right_index >= 0 or carry:
            left_digit = ord(left[left_index]) - ord("0") if left_index >= 0 else 0
            right_digit = ord(right[right_index]) - ord("0") if right_index >= 0 else 0
            carry, digit = divmod(left_digit + right_digit + carry, 10)
            reversed_digits.append(chr(ord("0") + digit))
            left_index -= 1
            right_index -= 1
        return "".join(reversed(reversed_digits))

    result = "0"
    for character in second:
        result = result + "0" if result != "0" else result
        for _ in range(ord(character) - ord("0")):
            result = add(result, first)
    return result
```

This performs up to nine full decimal additions for every digit of `second`.

## Better transition: accumulate all partial products by column

Grade-school multiplication does not need to construct shifted partial strings.
One array holds their column sums, and one right-to-left pass normalizes carries.

## Expert solution: digit-product array

```python
def multiply_strings(first: str, second: str) -> str:
    if (
        not first
        or not second
        or any(character not in "0123456789" for character in first + second)
        or (len(first) > 1 and first[0] == "0")
        or (len(second) > 1 and second[0] == "0")
    ):
        raise ValueError("inputs must be canonical non-negative decimal strings")
    if first == "0" or second == "0":
        return "0"

    digits = [0] * (len(first) + len(second))
    for first_index in range(len(first) - 1, -1, -1):
        first_digit = ord(first[first_index]) - ord("0")
        for second_index in range(len(second) - 1, -1, -1):
            second_digit = ord(second[second_index]) - ord("0")
            low = first_index + second_index + 1
            high = low - 1
            total = digits[low] + first_digit * second_digit
            digits[low] = total % 10
            digits[high] += total // 10

    start = 0
    while start < len(digits) - 1 and digits[start] == 0:
        start += 1
    return "".join(chr(ord("0") + digit) for digit in digits[start:])
```

Each pair is accumulated into its two positional columns. Processing from right
to left ensures any carry added to a higher column is handled by later pairs or
already remains a valid leading digit.

**Complexity:** `O(mn)` time and `O(m + n)` space.
