# ICPC300 045: CSES - Longest Palindrome

**Source:** [CSES - Longest Palindrome](https://cses.fi/problemset/task/1111/)  
**Pattern:** Manacher's algorithm  
**Goal:** Output any longest contiguous substring that reads the same forward
and backward.

## 1. Problem in plain words

The answer must be a substring, so its characters are consecutive. For
`bananas`, one longest palindrome is `anana`.

Odd palindromes have a character center; even palindromes have a gap center.
Both forms must be checked.

## 2. First principles

Expanding around every center repeats comparisons. Manacher's algorithm keeps
the rightmost palindrome found so far. When a new center lies inside it, the
mirror center provides a radius that is already known to match, capped by the
current right boundary. Expansion starts only beyond that guaranteed region.

Maintain separate radius arrays:

- `odd[i]`: number of characters from center `i` through one side, including
  the center; palindrome length `2*odd[i]-1`;
- `even[i]`: number of matched pairs around the gap before `i`; palindrome
  length `2*even[i]`.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| One character | Return that character. |
| All characters equal | Return the whole string. |
| Longest palindrome has even length | Check gap centers. |
| Several longest palindromes | Return any one. |
| Palindrome touches either end | Stop expansion at the boundary. |

## 4. Brute force: test every substring

```python
def longest_palindrome_brute_force(text: str) -> str:
    if not text:
        raise ValueError("text must be nonempty")

    best = text[0]
    for left in range(len(text)):
        for right in range(left + 1, len(text) + 1):
            candidate = text[left:right]
            if len(candidate) > len(best) and candidate == candidate[::-1]:
                best = candidate
    return best
```

**Complexity:** `O(n^3)` time because each of `O(n^2)` substrings takes up to
`O(n)` time to reverse and compare.

## 5. Better: expand around every center

Expansion avoids constructing and testing non-palindromic substrings. It is
still quadratic on a string such as `aaaa...`, but uses constant extra memory.

```python
def longest_palindrome_expand_centers(text: str) -> str:
    if not text:
        raise ValueError("text must be nonempty")

    best_left = 0
    best_right = 1

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(text) and text[left] == text[right]:
            left -= 1
            right += 1
        return left + 1, right

    for center in range(len(text)):
        for left, right in (
            expand(center, center),
            expand(center - 1, center),
        ):
            if right - left > best_right - best_left:
                best_left = left
                best_right = right

    return text[best_left:best_right]
```

**Complexity:** `O(n^2)` time and `O(1)` auxiliary memory.

## 6. Expert solution: odd and even Manacher passes

```python
def longest_palindrome(text: str) -> str:
    if not text:
        raise ValueError("text must be nonempty")

    length = len(text)
    best_start = 0
    best_length = 1

    odd = [0] * length
    left = 0
    right = -1
    for center in range(length):
        radius = (
            1 if center > right else min(odd[left + right - center], right - center + 1)
        )
        while (
            center - radius >= 0
            and center + radius < length
            and text[center - radius] == text[center + radius]
        ):
            radius += 1
        odd[center] = radius

        palindrome_length = 2 * radius - 1
        if palindrome_length > best_length:
            best_length = palindrome_length
            best_start = center - radius + 1
        if center + radius - 1 > right:
            left = center - radius + 1
            right = center + radius - 1

    even = [0] * length
    left = 0
    right = -1
    for center in range(length):
        radius = (
            0
            if center > right
            else min(even[left + right - center + 1], right - center + 1)
        )
        while (
            center - radius - 1 >= 0
            and center + radius < length
            and text[center - radius - 1] == text[center + radius]
        ):
            radius += 1
        even[center] = radius

        palindrome_length = 2 * radius
        if palindrome_length > best_length:
            best_length = palindrome_length
            best_start = center - radius
        if center + radius - 1 > right:
            left = center - radius
            right = center + radius - 1

    return text[best_start : best_start + best_length]
```

### Why the expert code is correct

- Each radius starts with a region already proven equal by mirror symmetry,
  never assuming characters beyond the known right boundary.
- The following while-loop extends until the first mismatch or string edge, so
  the stored radius is exact.
- Odd and even passes cover every possible palindrome center.
- Tracking the largest exact radius therefore returns a globally longest
  palindromic substring.

**Complexity:** `O(n)` time and `O(n)` memory. The maintained right boundary
only moves right, so total successful expansion work is linear.

## 7. What to remember

Center expansion becomes linear when a palindrome inside the current rightmost
palindrome reuses its mirror's already-proven radius.
