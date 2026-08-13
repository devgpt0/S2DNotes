# 56. Count Vowels

**What you learn:** String membership.

## Problem

Count the vowels in a string. Accept uppercase and lowercase vowels.

## Example

```text
Input: text = "Education"
Output: 5
```

## Simple idea

Visit each character and check whether it appears in the vowel string.

## Python solution

```python
def count_vowels(text: str) -> int:
    vowels = "aeiouAEIOU"
    count = 0

    for character in text:
        if character in vowels:
            count = count + 1

    return count
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

