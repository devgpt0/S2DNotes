# 86. Count Consonants

**What you learn:** Character checks.

## Problem

Return how many alphabetic characters are not vowels.

## Example

```text
Input: text = "Data Structures"
Output: 9
```

## Simple idea

Count a character only when it is a letter and not in the vowel list.

## Python solution

```python
def count_consonants(text: str) -> int:
    vowels = "aeiou"
    count = 0
    for character in text.lower():
        if character.isalpha() and character not in vowels:
            count += 1
    return count
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
