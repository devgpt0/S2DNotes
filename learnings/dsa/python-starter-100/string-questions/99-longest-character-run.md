# 99. Find the Longest Run of One Character

**What you learn:** Running counts.

## Problem

Return `(character, length)` for the first longest consecutive character run in a non-empty string.

## Example

```text
Input: text = "aaabbccccd"
Output: ('c', 4)
```

## Simple idea

Count the current run. Save it whenever it becomes longer than the best run.

## Python solution

```python
def longest_character_run(text: str) -> tuple[str, int]:
    if len(text) == 0:
        raise ValueError("text must not be empty")

    best_character = text[0]
    best_length = 1
    current_character = text[0]
    current_length = 1

    for character in text[1:]:
        if character == current_character:
            current_length += 1
        else:
            current_character = character
            current_length = 1

        if current_length > best_length:
            best_character = current_character
            best_length = current_length

    return best_character, best_length
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
