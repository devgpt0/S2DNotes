# Z Algorithm

## Idea

`z[i]` is the length of the longest substring starting at `i` that matches the
whole string's prefix. A remembered matching window avoids comparing the same
characters again.

## Visual model

```text
string prefix:  a b a ...
at position i:  a b a ... -> z[i] >= 3
```

## Classroom board: prefix match at every start

```text
text = "ababa"
start 0: convention z[0]=0
start 1: "b..." differs from prefix "a..." -> 0
start 2: "aba" matches prefix "aba"       -> 3
start 4: "a" matches prefix "a"           -> 1
z = [0,0,3,0,1]
```

## Steps

1. Maintain a rightmost matched interval `[left, right)`.
2. If `i` is inside it, copy the safe part of a previous Z value.
3. Compare forward to extend the match.
4. Update the rightmost interval when extension goes farther.

## First-principles derivation

For every position, the Z value asks how long the suffix starting there matches
the whole string's prefix. Previously matched intervals can supply an initial
answer instead of comparing from scratch.

The active Z-box `[left,right)` is a region already known to match the prefix.

## Classroom board: Z values for ababa

```text
string: a b a b a
index:  0 1 2 3 4
Z:      0 0 3 0 1

index 1: b != a                     -> 0
index 2: aba matches prefix aba     -> 3, box [2,5)
index 3: inside box; prefix[1]=b
         but text[3]=b starts against prefix[0]=a -> 0
index 4: a matches prefix a         -> 1
```

A copied value is capped by the current box; comparisons extend only beyond
what is already known.

## Pattern recognition

Use Z values for prefix matching at every position, pattern search via
`pattern + separator + text`, borders, and periods.

## Implementation

### C++

```cpp
std::vector<int> zFunction(const std::string& text) {
    std::vector<int> z(text.size(), 0);
    int left = 0, right = 0;
    for (int index = 1; index < static_cast<int>(text.size()); ++index) {
        if (index < right) z[index] = std::min(right - index, z[index - left]);
        while (index + z[index] < static_cast<int>(text.size()) && text[z[index]] == text[index + z[index]]) ++z[index];
        if (index + z[index] > right) {
            left = index;
            right = index + z[index];
        }
    }
    return z;
}
```

### Python

```python
def z_function(text: str) -> list[int]:
    z = [0] * len(text)
    left = right = 0
    for index in range(1, len(text)):
        if index < right:
            z[index] = min(right - index, z[index - left])
        while index + z[index] < len(text) and text[z[index]] == text[index + z[index]]:
            z[index] += 1
        if index + z[index] > right:
            left, right = index, index + z[index]
    return z
```

### Java

```java
static int[] zFunction(String text) {
    int[] z = new int[text.length()];
    int left = 0;
    int right = 0;
    for (int index = 1; index < text.length(); index++) {
        if (index < right) z[index] = Math.min(right - index, z[index - left]);
        while (index + z[index] < text.length()
            && text.charAt(z[index]) == text.charAt(index + z[index])) z[index]++;
        if (index + z[index] > right) {
            left = index;
            right = index + z[index];
        }
    }
    return z;
}
```

## Why it works

Inside a known match window, the string equals its prefix. A copied Z value is
safe until the window boundary; only characters beyond it need new comparisons.

## Complexity

Time and space are `O(n)`.

## Common mistakes

- Mixing inclusive and exclusive right boundaries.
- Choosing a separator that occurs in the pattern or text.
- Assuming `z[0]` has one universal convention; here it is `0`.
