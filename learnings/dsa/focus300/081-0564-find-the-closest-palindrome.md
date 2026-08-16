# Focus300 081: LeetCode 564 - Find the Closest Palindrome

**Source:** [LeetCode 564](https://leetcode.com/problems/find-the-closest-palindrome/)  
**Difficulty:** Hard  
**Pattern:** decimal mirroring and boundary candidates

## Exact contract

Given the decimal representation of a positive integer, return the different
palindromic integer with minimum absolute difference. If both sides are equally
close, return the smaller one. The input has no leading zero and fits the
source limit of at most 18 digits.

## First principles

A nearest palindrome normally keeps the leading half close to the input's
leading half. Mirroring that half is one candidate; changing the half by one
covers the nearest carry and borrow. Powers of ten are the exception, so the
all-nine number below and `1...001` above must also be considered.


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

- The answer must differ from the input, even when the input is a palindrome.
- `10`, `100`, and similar values need the shorter all-nine candidate.
- `9`, `99`, and similar values need the longer `1...001` candidate.
- Odd lengths mirror every prefix digit except its last digit.
- Equal distances choose the numerically smaller palindrome.

## Brute force: search outward by distance

```python
def nearest_palindrome_brute(number: str) -> str:
    if type(number) is not str or not number.isascii() or not number.isdigit():
        raise TypeError("number must be an ASCII decimal string")
    if number == "0" or (len(number) > 1 and number[0] == "0"):
        raise ValueError(
            "number must represent a positive integer without leading zero"
        )
    if len(number) > 18:
        raise ValueError("number must contain at most 18 digits")

    value = int(number)
    distance = 1
    while True:
        lower = value - distance
        if lower >= 0 and str(lower) == str(lower)[::-1]:
            return str(lower)
        upper = value + distance
        if str(upper) == str(upper)[::-1]:
            return str(upper)
        distance += 1
```

Searching the lower value first implements the tie rule. The time is
proportional to the answer's distance and each test costs `O(d)` for `d`
digits.

## Better approach: enumerate palindromes near the prefix

Instead of examining every integer, mirror the original leading half and a
small neighborhood of that half. This reduces the candidate set to a constant
size. The remaining complication is a carry or borrow that changes the number
of digits.

## Expert solution: five structural candidates

```python
def nearest_palindrome(number: str) -> str:
    if type(number) is not str or not number.isascii() or not number.isdigit():
        raise TypeError("number must be an ASCII decimal string")
    if number == "0" or (len(number) > 1 and number[0] == "0"):
        raise ValueError(
            "number must represent a positive integer without leading zero"
        )
    if len(number) > 18:
        raise ValueError("number must contain at most 18 digits")

    value = int(number)
    digit_count = len(number)
    prefix_length = (digit_count + 1) // 2
    prefix = int(number[:prefix_length])
    candidates = {10 ** (digit_count - 1) - 1, 10**digit_count + 1}

    for nearby_prefix in (prefix - 1, prefix, prefix + 1):
        if nearby_prefix < 0:
            continue
        left = str(nearby_prefix)
        if digit_count % 2:
            candidate = int(left + left[-2::-1])
        else:
            candidate = int(left + left[::-1])
        candidates.add(candidate)

    candidates.discard(value)
    return str(
        min(candidates, key=lambda candidate: (abs(candidate - value), candidate))
    )
```

Every non-boundary nearest palindrome is determined by one of the three
nearest prefixes. The two explicit boundary candidates cover digit-count
changes, so the minimum under `(distance, value)` is the required answer.

**Complexity:** `O(d)` time and `O(d)` temporary space for at most five
`d`-digit candidates.
