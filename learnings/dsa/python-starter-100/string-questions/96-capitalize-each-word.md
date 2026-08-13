# 96. Capitalize Each Word

**What you learn:** Building formatted words.

## Problem

Return text with the first character of every word uppercase and the rest lowercase.

## Example

```text
Input: text = "pYTHON dSA"
Output: "Python Dsa"
```

## Simple idea

For each word, uppercase its first character and lowercase the remaining characters.

## Python solution

```python
def capitalize_each_word(text: str) -> str:
    words = text.split()
    result: list[str] = []
    for word in words:
        result.append(word[0].upper() + word[1:].lower())
    return " ".join(result)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
