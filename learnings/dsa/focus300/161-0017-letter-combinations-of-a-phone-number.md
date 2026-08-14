# Focus300 161: LeetCode 17 - Letter Combinations of a Phone Number

**Source:** [LeetCode 17](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)  
**Difficulty:** Medium  
**Pattern:** Cartesian-product backtracking

## Exact contract

Map each digit from `2` through `9` to its telephone keypad letters and return
every string formed by choosing one mapped letter per input digit, in digit
order. The digit string has length at most four; an empty input returns an empty
list.

## First principles

Each output is a root-to-leaf path in a decision tree. Level `i` chooses one
letter from the mapping of `digits[i]`. A path is complete after exactly
`len(digits)` choices, so no output can be missing, duplicated, or have the
wrong order.

## Cases that decide correctness

- Empty digits returns `[]`, not a list containing an empty string.
- Digits `7` and `9` each contribute four choices.
- Digits `0` and `1` are outside the source contract.
- Repeated digits create independent positions.
- Output ordering is not semantically significant.

## Brute force: materialize the Cartesian product

```python
from itertools import product


DIGIT_LETTERS = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations_brute(digits: str) -> list[str]:
    if (
        type(digits) is not str
        or len(digits) > 4
        or any(digit not in DIGIT_LETTERS for digit in digits)
    ):
        raise ValueError("digits must contain at most four characters from 2 through 9")
    if not digits:
        return []
    return [
        "".join(letters)
        for letters in product(*(DIGIT_LETTERS[digit] for digit in digits))
    ]
```

The library product stores each result tuple before joining it.

## Better insight: construct one output path in place

Backtracking reuses a length-`n` buffer. At each depth, only the letters for the
corresponding digit are legal choices.

## Expert solution: depth-first generation

```python
DIGIT_LETTERS = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits: str) -> list[str]:
    if (
        type(digits) is not str
        or len(digits) > 4
        or any(digit not in DIGIT_LETTERS for digit in digits)
    ):
        raise ValueError("digits must contain at most four characters from 2 through 9")
    if not digits:
        return []

    answer: list[str] = []
    path = [""] * len(digits)

    def build(index: int) -> None:
        if index == len(digits):
            answer.append("".join(path))
            return
        for letter in DIGIT_LETTERS[digits[index]]:
            path[index] = letter
            build(index + 1)

    build(0)
    return answer
```

The recursion invariant fixes exactly the first `index` output positions, and
the loop explores every legal next choice once.

**Complexity:** `O(n * output_count)` time for constructing strings and `O(n)`
auxiliary recursion space, excluding output.
