# Focus300 153: LeetCode 5 - Longest Palindromic Substring

**Source:** [LeetCode 5](https://leetcode.com/problems/longest-palindromic-substring/)  
**Difficulty:** Medium  
**Pattern:** expand around every palindrome center

## Exact contract

Given a nonempty string of at most `1_000` ASCII letters and digits, return a
longest contiguous palindromic substring. When several longest answers exist,
any one is valid.

## First principles

Every palindrome has one center: a character for odd length or a gap for even
length. Expanding while the two boundary characters match enumerates the
largest palindrome for that center. Taking the best across all `2*n-1` centers
covers every candidate without storing a substring table.


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

- Both odd and even centers are required.
- One character is always a palindrome.
- The full string may be the answer.
- Equal-length answers need no special tie rule.
- Character case matters.

## Brute force: test every substring

```python
def longest_palindrome_brute(text: str) -> str:
    if (
        type(text) is not str
        or not 1 <= len(text) <= 1_000
        or any(not character.isascii() or not character.isalnum() for character in text)
    ):
        raise ValueError("text must contain 1..1,000 ASCII letters or digits")

    best = text[0]
    for left in range(len(text)):
        for right in range(left + len(best) + 1, len(text) + 1):
            candidate = text[left:right]
            if candidate == candidate[::-1]:
                best = candidate
    return best
```

There are `O(n^2)` substrings and each palindrome test costs `O(n)`, for
`O(n^3)` time.

## Better insight: grow palindromes from their forced midpoint

Once a center is fixed, matching can continue only symmetrically. No other
left/right pairs for that center need consideration.

## Expert solution: expand around odd and even centers

```python
def longest_palindrome(text: str) -> str:
    if (
        type(text) is not str
        or not 1 <= len(text) <= 1_000
        or any(not character.isascii() or not character.isalnum() for character in text)
    ):
        raise ValueError("text must contain 1..1,000 ASCII letters or digits")

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(text) and text[left] == text[right]:
            left -= 1
            right += 1
        return left + 1, right

    best_left = 0
    best_right = 1
    for center in range(len(text)):
        for left, right in (expand(center, center), expand(center, center + 1)):
            if right - left > best_right - best_left:
                best_left = left
                best_right = right
    return text[best_left:best_right]
```

Each returned interval is maximal for its center, and every palindrome belongs
to one examined center.

**Complexity:** `O(n^2)` time and `O(1)` auxiliary space.
