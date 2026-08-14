# Focus300 158: LeetCode 12 - Integer to Roman

**Source:** [LeetCode 12](https://leetcode.com/problems/integer-to-roman/)  
**Difficulty:** Medium  
**Pattern:** canonical place-value encoding

## Exact contract

Convert an integer from `1` through `3999` to its canonical Roman numeral using
`I, V, X, L, C, D, M` and the subtractive forms `IV, IX, XL, XC, CD, CM`.

## First principles

Roman notation is canonical independently at each decimal place. The only
non-additive digits are `4` and `9`, represented by a smaller symbol before the
next one or five value. A table per place or a descending list containing those
subtractive tokens both encode the same greedy invariant.

## Cases that decide correctness

- `4` and `9` at every place require subtractive notation.
- A symbol may repeat at most three times in canonical output.
- `3999` is the largest supported value.
- Zero and negative numbers have no representation in this contract.
- Output uses uppercase symbols only.

## Brute force: choose the representation of each decimal digit

```python
def integer_to_roman_brute(number: int) -> str:
    if type(number) is not int or not 1 <= number <= 3_999:
        raise ValueError("number must be an integer from 1 through 3,999")

    thousands = ("", "M", "MM", "MMM")
    hundreds = ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM")
    tens = ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC")
    ones = ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX")
    return "".join(
        (
            thousands[number // 1_000],
            hundreds[number // 100 % 10],
            tens[number // 10 % 10],
            ones[number % 10],
        )
    )
```

The finite lookup is direct but duplicates the same digit pattern four times.

## Better insight: include subtractive forms in descending token order

After adding `900`, `400`, `90`, `40`, `9`, and `4` as indivisible tokens, the
canonical numeral is simply the greedy decomposition by the largest token.

## Expert solution: descending greedy tokens

```python
def integer_to_roman(number: int) -> str:
    if type(number) is not int or not 1 <= number <= 3_999:
        raise ValueError("number must be an integer from 1 through 3,999")

    tokens = (
        (1_000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )
    output: list[str] = []
    remaining = number
    for value, symbol in tokens:
        count, remaining = divmod(remaining, value)
        output.append(symbol * count)
    return "".join(output)
```

At each step the largest legal canonical prefix is forced; the remainder is a
smaller instance with the same token ordering.

**Complexity:** `O(1)` time and output space under the fixed `1..3999` contract.
