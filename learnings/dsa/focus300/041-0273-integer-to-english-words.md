# Focus300 041: LeetCode 273 - Integer to English Words

**Source:** [LeetCode 273](https://leetcode.com/problems/integer-to-english-words/)  
**Difficulty:** Hard  
**Pattern:** three-digit chunks and scale words

## Exact contract

Given an integer from `0` through `2^31 - 1`, return its English representation
using the LeetCode vocabulary and capitalization. Separate words with one
space, omit zero-valued chunks, do not use `and`, and return `"Zero"` for zero.

## First principles

English names repeat every three decimal digits. Convert each nonzero chunk
from 1 through 999, then append its scale: `Thousand`, `Million`, or `Billion`.
Inside a chunk, process hundreds, the special values below 20, and tens.


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

- Zero is the only value whose zero chunk is spoken.
- Values 10 through 19 use dedicated words.
- Exact hundreds and scales have no trailing words.
- Zero chunks between nonzero chunks are skipped.
- Output contains neither commas nor doubled spaces.

## Brute force: decompose each three-digit chunk explicitly

```python
def number_to_words_brute(number: int) -> str:
    if not 0 <= number <= 2**31 - 1:
        raise ValueError("number must be a 32-bit nonnegative integer")
    if number == 0:
        return "Zero"

    below_twenty = [
        "",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Eleven",
        "Twelve",
        "Thirteen",
        "Fourteen",
        "Fifteen",
        "Sixteen",
        "Seventeen",
        "Eighteen",
        "Nineteen",
    ]
    tens = [
        "",
        "",
        "Twenty",
        "Thirty",
        "Forty",
        "Fifty",
        "Sixty",
        "Seventy",
        "Eighty",
        "Ninety",
    ]
    scales = ["", "Thousand", "Million", "Billion"]

    def chunk_words(value: int) -> list[str]:
        words: list[str] = []
        hundreds, value = divmod(value, 100)
        if hundreds:
            words.extend((below_twenty[hundreds], "Hundred"))
        if value < 20:
            if value:
                words.append(below_twenty[value])
        else:
            ten, one = divmod(value, 10)
            words.append(tens[ten])
            if one:
                words.append(below_twenty[one])
        return words

    groups: list[int] = []
    while number:
        number, group = divmod(number, 1000)
        groups.append(group)
    answer: list[str] = []
    for scale_index in range(len(groups) - 1, -1, -1):
        if groups[scale_index] == 0:
            continue
        answer.extend(chunk_words(groups[scale_index]))
        if scales[scale_index]:
            answer.append(scales[scale_index])
    return " ".join(answer)
```

The explicit chunk cases are constant-time but repeat the decimal hierarchy.

## Better transition: recurse by the largest language unit

A value is named by its quotient before the largest applicable unit, the unit
word itself, then its remainder. The same function handles billions, millions,
thousands, hundreds, tens, and one-word values.

## Expert solution: recursive scale conversion

```python
def number_to_words(number: int) -> str:
    if not 0 <= number <= 2**31 - 1:
        raise ValueError("number must be a 32-bit nonnegative integer")
    if number == 0:
        return "Zero"

    words = [
        (1_000_000_000, "Billion"),
        (1_000_000, "Million"),
        (1_000, "Thousand"),
        (100, "Hundred"),
        (90, "Ninety"),
        (80, "Eighty"),
        (70, "Seventy"),
        (60, "Sixty"),
        (50, "Fifty"),
        (40, "Forty"),
        (30, "Thirty"),
        (20, "Twenty"),
        (19, "Nineteen"),
        (18, "Eighteen"),
        (17, "Seventeen"),
        (16, "Sixteen"),
        (15, "Fifteen"),
        (14, "Fourteen"),
        (13, "Thirteen"),
        (12, "Twelve"),
        (11, "Eleven"),
        (10, "Ten"),
        (9, "Nine"),
        (8, "Eight"),
        (7, "Seven"),
        (6, "Six"),
        (5, "Five"),
        (4, "Four"),
        (3, "Three"),
        (2, "Two"),
        (1, "One"),
    ]

    def convert(value: int) -> list[str]:
        for unit, word in words:
            if value < unit:
                continue
            quotient, remainder = divmod(value, unit)
            result = convert(quotient) if unit >= 100 else []
            result.append(word)
            if remainder:
                result.extend(convert(remainder))
            return result
        return []

    return " ".join(convert(number))
```

The first applicable unit is the unique largest language unit in the value.
Its quotient and remainder are both smaller, so recursion terminates and emits
the canonical words in descending place-value order.

**Complexity:** `O(log number)` emitted-word steps and recursion space.
