# 65. Run-Length Encoding

**What you learn:** Counting consecutive characters.

## Problem

Replace each consecutive character run with the character followed by its count.

## Example

```text
Input: text = "aaabbc"
Output: "a3b2c1"
```

## Simple idea

Count equal neighbouring characters. Save the run when the character changes.

## Python solution

```python
def run_length_encode(text: str) -> str:
    if text == "":
        return ""

    parts: list[str] = []
    current = text[0]
    count = 1

    for character in text[1:]:
        if character == current:
            count = count + 1
        else:
            parts.append(current + str(count))
            current = character
            count = 1

    parts.append(current + str(count))
    return "".join(parts)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
