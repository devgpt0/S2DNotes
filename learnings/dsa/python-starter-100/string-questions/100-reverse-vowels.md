# 100. Reverse Vowels in a String

**What you learn:** Two pointers.

## Problem

Return text with only its vowels reversed.

## Example

```text
Input: text = "hello"
Output: "holle"
```

## Simple idea

Move one pointer from each end. Swap when both pointers point to vowels.

## Python solution

```python
def reverse_vowels(text: str) -> str:
    characters = list(text)
    vowels = set("aeiouAEIOU")
    left = 0
    right = len(characters) - 1

    while left < right:
        while left < right and characters[left] not in vowels:
            left += 1
        while left < right and characters[right] not in vowels:
            right -= 1

        if left < right:
            characters[left], characters[right] = characters[right], characters[left]
            left += 1
            right -= 1

    return "".join(characters)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
