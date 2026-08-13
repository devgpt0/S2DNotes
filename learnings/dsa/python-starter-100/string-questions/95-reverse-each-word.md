# 95. Reverse Each Word

**What you learn:** Splitting and joining.

## Problem

Return a sentence where every word is reversed but word order stays the same.

## Example

```text
Input: text = "learn dsa"
Output: "nrael asd"
```

## Simple idea

Split the sentence into words, reverse each word, and join them with one space.

## Python solution

```python
def reverse_each_word(text: str) -> str:
    words = text.split()
    reversed_words: list[str] = []
    for word in words:
        reversed_words.append(word[::-1])
    return " ".join(reversed_words)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
