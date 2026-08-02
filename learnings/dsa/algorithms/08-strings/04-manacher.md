# Manacher's Algorithm

## Idea

Manacher finds palindrome radii around every center in linear time. It mirrors
known radii inside the rightmost palindrome and compares only beyond its edge.

## Visual model

For odd palindromes, `radius[i]` includes the center:

```text
text:    a b a c a b a
center:        c
radius:        4          palindrome spans center-radius+1 .. center+radius-1
```

## Classroom board: mirror a known palindrome

```text
known palindrome: "abacaba" centered at c
positions equally far left/right of c have mirrored known matches
copy the safe radius up to the known boundary
compare characters only beyond that boundary
```

## Steps

1. Maintain the rightmost palindrome interval `[left, right)`.
2. If the center is inside it, initialize from its mirror.
3. Expand while outside characters match.
4. Update the rightmost interval when this palindrome reaches farther.

## First-principles derivation

Expanding around every center repeats comparisons inside palindromes already
found. Manacher keeps the palindrome reaching farthest right and mirrors a
known radius across its center.

The mirrored radius is only a safe lower bound when it reaches the current
right boundary; expansion verifies anything beyond it.

## Classroom board: odd radii of abacaba

Radius counts the center itself.

```text
index:   0 1 2 3 4 5 6
char:    a b a c a b a
radius:  1 2 1 4 1 2 1

center 3:
c
aca
bacab
abacaba
radius = 4

center 5 mirrors center 1 around center 3,
so it starts with radius 2 without rechecking the inside.
```

## Pattern recognition

Use it when all palindrome centers, longest palindrome, or many palindrome
queries are needed in true `O(n)` preprocessing.

## Implementation: odd-length radii

### C++

```cpp
std::vector<int> oddPalindromeRadii(const std::string& text) {
    std::vector<int> radius(text.size());
    int left = 0, right = 0;
    for (int center = 0; center < static_cast<int>(text.size()); ++center) {
        int current = center < right ? std::min(radius[left + right - center - 1], right - center) : 1;
        while (center - current >= 0 && center + current < static_cast<int>(text.size())
               && text[center - current] == text[center + current]) ++current;
        radius[center] = current;
        if (center + current > right) {
            left = center - current + 1;
            right = center + current;
        }
    }
    return radius;
}
```

### Python

```python
def odd_palindrome_radii(text: str) -> list[int]:
    radius = [0] * len(text)
    left = right = 0
    for center in range(len(text)):
        current = min(radius[left + right - center - 1], right - center) if center < right else 1
        while center - current >= 0 and center + current < len(text) and text[center - current] == text[center + current]:
            current += 1
        radius[center] = current
        if center + current > right:
            left, right = center - current + 1, center + current
    return radius
```

### Java

```java
static int[] oddPalindromeRadii(String text) {
    int[] radius = new int[text.length()];
    int left = 0;
    int right = 0;
    for (int center = 0; center < text.length(); center++) {
        int current = center < right ? Math.min(radius[left + right - center - 1], right - center) : 1;
        while (center - current >= 0 && center + current < text.length()
            && text.charAt(center - current) == text.charAt(center + current)) current++;
        radius[center] = current;
        if (center + current > right) {
            left = center - current + 1;
            right = center + current;
        }
    }
    return radius;
}
```

## Why it works

Positions mirrored inside a known palindrome match until either their own
radius ends or the known boundary is reached. Only expansion beyond that
boundary performs new comparisons.

## Complexity

Time and space are `O(n)`.

## Common mistakes

- Mixing radius definitions and interval endpoints.
- Forgetting even-length palindromes; run the even variant or transform the
  string with separators.
- Using rolling hash when deterministic palindrome results are required.
