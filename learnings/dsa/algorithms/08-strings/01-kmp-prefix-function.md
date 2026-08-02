# KMP and the Prefix Function

## Idea

The prefix function `prefix[i]` is the length of the longest proper prefix of
`text[0..i]` that is also a suffix. KMP reuses this information after a
mismatch instead of restarting the match.

## Visual model

```text
matched prefix: ababa
mismatch next:  fall back to its longest border "aba", then continue
```

## Classroom board: do not restart after mismatch

```text
pattern "abab", matched "aba", next text character is "a"
full continuation fails, but suffix "a" is also pattern prefix "a"
fall back to length 1 instead of length 0; reuse that known match
```

## Steps

1. Build prefix values for the pattern.
2. Scan the text while tracking matched pattern length.
3. On mismatch, fall back through earlier prefix values.
4. On a full match, record its start and fall back to allow overlaps.

## First-principles derivation

A naive matcher restarts after a mismatch and compares characters that were
already known to match. The prefix function records the longest proper prefix
that is also a suffix, so matching can fall back to the next possible border.

The invariant is that `matched` characters of the pattern equal the current
text suffix.

## Classroom board: build prefix values for ababaca

```text
index:  0 1 2 3 4 5 6
char:   a b a b a c a
pi:     0 0 1 2 3 0 1

at index 4, "aba" is both prefix and suffix -> pi[4] = 3

at index 5, compare c with pattern[3]=b -> mismatch
fall back pi[2]=1, compare c with pattern[1]=b -> mismatch
fall back 0 -> pi[5] = 0

at index 6, a matches pattern[0] -> pi[6] = 1
```

Fallback changes the candidate border without moving backward in the text.

## Pattern recognition

Use KMP for exact pattern matching, borders, string periods, or repeated
prefix/suffix structure in linear time.

## Implementation: all match positions

### C++

```cpp
std::vector<int> kmpSearch(const std::string& text, const std::string& pattern) {
    std::vector<int> prefix(pattern.size(), 0);
    for (int index = 1; index < static_cast<int>(pattern.size()); ++index) {
        int length = prefix[index - 1];
        while (length > 0 && pattern[index] != pattern[length]) length = prefix[length - 1];
        if (pattern[index] == pattern[length]) ++length;
        prefix[index] = length;
    }
    std::vector<int> matches;
    int length = 0;
    for (int index = 0; index < static_cast<int>(text.size()); ++index) {
        while (length > 0 && text[index] != pattern[length]) length = prefix[length - 1];
        if (text[index] == pattern[length]) ++length;
        if (length == static_cast<int>(pattern.size())) {
            matches.push_back(index - length + 1);
            length = prefix[length - 1];
        }
    }
    return matches;
}
```

### Python

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    prefix = [0] * len(pattern)
    for index in range(1, len(pattern)):
        length = prefix[index - 1]
        while length and pattern[index] != pattern[length]:
            length = prefix[length - 1]
        if pattern[index] == pattern[length]:
            length += 1
        prefix[index] = length
    matches: list[int] = []
    length = 0
    for index, character in enumerate(text):
        while length and character != pattern[length]:
            length = prefix[length - 1]
        if character == pattern[length]:
            length += 1
        if length == len(pattern):
            matches.append(index - length + 1)
            length = prefix[length - 1]
    return matches
```

### Java

```java
static List<Integer> kmpSearch(String text, String pattern) {
    int[] prefix = new int[pattern.length()];
    for (int index = 1; index < pattern.length(); index++) {
        int length = prefix[index - 1];
        while (length > 0 && pattern.charAt(index) != pattern.charAt(length)) length = prefix[length - 1];
        if (pattern.charAt(index) == pattern.charAt(length)) length++;
        prefix[index] = length;
    }
    List<Integer> matches = new ArrayList<>();
    int length = 0;
    for (int index = 0; index < text.length(); index++) {
        while (length > 0 && text.charAt(index) != pattern.charAt(length)) length = prefix[length - 1];
        if (text.charAt(index) == pattern.charAt(length)) length++;
        if (length == pattern.length()) {
            matches.add(index - length + 1);
            length = prefix[length - 1];
        }
    }
    return matches;
}
```

## Why it works

After a mismatch, every longer border is impossible. The prefix table jumps to
the longest remaining prefix that already matches the text suffix.

## Complexity

Time is `O(text length + pattern length)` and space is `O(pattern length)`.

## Common mistakes

- Passing an empty pattern to code whose contract requires non-empty input.
- Falling back to `prefix[length]` instead of `prefix[length - 1]`.
- Resetting to zero after a match and missing overlaps.
