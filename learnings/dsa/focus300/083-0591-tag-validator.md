# Focus300 083: LeetCode 591 - Tag Validator

**Source:** [LeetCode 591](https://leetcode.com/problems/tag-validator/)  
**Difficulty:** Hard  
**Pattern:** deterministic parsing with a tag stack

## Exact contract

Return whether `code` is exactly one closed outer tag. A tag name contains one
to nine uppercase ASCII letters. Tag content may contain text, nested valid
tags, or `<![CDATA[...]]>` sections; CDATA is legal only inside an open tag and
ends at the first `]]>`. No characters may appear before or after the root tag.

## First principles

At any position beginning with `<`, the next construct is determined by its
prefix: CDATA, a closing tag, or an opening tag. A stack records which opening
tags still require matching closes. Plain text is legal only while that stack
is nonempty, and the root closing tag must be the final input construct.


## Classroom board: keep only the useful unfinished work

```text
a stack stores the part of the state that can still matter after the next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- An empty string or plain text without a root tag is invalid.
- Tag names reject lowercase letters, digits, empty names, and length above 9.
- CDATA text is opaque, including apparent tags, but must have a closing `]]>`.
- A closing tag must match the most recent unmatched opening tag.
- A second root or any suffix after the root closes is invalid.

## Brute force: recursive descent over nested tags

```python
def is_valid_tag_code_brute(code: str) -> bool:
    if type(code) is not str:
        raise TypeError("code must be a string")

    def valid_name(name: str) -> bool:
        return 1 <= len(name) <= 9 and all(
            "A" <= character <= "Z" for character in name
        )

    def parse_tag(start: int) -> int | None:
        if not code.startswith("<", start) or code.startswith("</", start):
            return None
        open_end = code.find(">", start + 1)
        if open_end == -1:
            return None
        name = code[start + 1 : open_end]
        if not valid_name(name):
            return None

        index = open_end + 1
        closing = f"</{name}>"
        while index < len(code):
            if code.startswith(closing, index):
                return index + len(closing)
            if code.startswith("<![CDATA[", index):
                cdata_end = code.find("]]>", index + 9)
                if cdata_end == -1:
                    return None
                index = cdata_end + 3
            elif code[index] == "<":
                nested_end = parse_tag(index)
                if nested_end is None:
                    return None
                index = nested_end
            else:
                index += 1
        return None

    return parse_tag(0) == len(code)
```

Recursive descent follows the grammar directly. Repeated substring searches
can rescan input, giving `O(n^2)` worst-case time and `O(n)` recursion space.

## Better approach: tokenize once, then validate nesting

A lexer can emit text, CDATA, open-tag, and close-tag tokens, followed by a
stack pass. The token list is unnecessary storage because each token can be
validated immediately while scanning.

## Expert solution: one-pass stack parser

```python
def is_valid_tag_code(code: str) -> bool:
    if type(code) is not str:
        raise TypeError("code must be a string")

    def valid_name(name: str) -> bool:
        return 1 <= len(name) <= 9 and all(
            "A" <= character <= "Z" for character in name
        )

    stack: list[str] = []
    index = 0
    while index < len(code):
        if index > 0 and not stack:
            return False
        if code.startswith("<![CDATA[", index):
            if not stack:
                return False
            end = code.find("]]>", index + 9)
            if end == -1:
                return False
            index = end + 3
        elif code.startswith("</", index):
            end = code.find(">", index + 2)
            if end == -1:
                return False
            name = code[index + 2 : end]
            if not valid_name(name) or not stack or stack[-1] != name:
                return False
            stack.pop()
            index = end + 1
        elif code[index] == "<":
            end = code.find(">", index + 1)
            if end == -1:
                return False
            name = code[index + 1 : end]
            if not valid_name(name):
                return False
            stack.append(name)
            index = end + 1
        else:
            if not stack:
                return False
            index += 1
    return not stack and index > 0
```

Each construct is consumed once and stack order enforces proper nesting. The
empty-stack guard ensures that the first opening tag is the only root.

**Complexity:** `O(n)` time and `O(d)` space for nesting depth `d`.
