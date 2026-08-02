# Longest Common Prefix Array (Kasai's Algorithm)

## Idea

Given a suffix array, `lcp[i]` is the common-prefix length of suffixes at
positions `i` and `i-1` in suffix order. Kasai builds all values in linear time.

## Visual model

```text
suffix order neighbors are the only candidates needed for many repeated-
substring questions
```

## Classroom board: reuse one fewer character

```text
suffix starting at i matches another suffix for k=5 characters
remove the first character from both
suffix starting at i+1 has at least k-1=4 known matching characters
start the next comparison from 4, not 0
```

## Steps

1. Build `rank[start]`, the suffix-array position of each suffix.
2. For suffix `start`, compare it with the previous suffix in sorted order.
3. Reuse the previous match length minus one.
4. Store the new length, then decrease it by one before the next start.

## First-principles derivation

Adjacent suffixes in suffix-array order contain all information needed for
many repeated-substring questions. When moving from suffix `i` to `i+1`,
their known common prefix loses at most its first character.

Kasai's algorithm reuses that length, so total character decrements and
increments are linear.

## Classroom board: LCP values for banana

```text
rank  suffix       LCP with previous
0     a            0
1     ana          1   ("a")
2     anana        3   ("ana")
3     banana       0
4     na           0
5     nana         2   ("na")

suffix array = [5,3,1,0,4,2]
LCP          = [0,1,3,0,0,2]
```

The largest LCP is `3`, so `"ana"` is a longest repeated substring.

## Pattern recognition

Use LCP with a suffix array for longest repeated substring, distinct substring
counts, or range-minimum queries between suffixes.

## Implementation

### C++

```cpp
std::vector<int> lcpArray(const std::string& text, const std::vector<int>& suffixArray) {
    const int size = text.size();
    std::vector<int> rank(size), lcp(size, 0);
    for (int position = 0; position < size; ++position) rank[suffixArray[position]] = position;
    int length = 0;
    for (int start = 0; start < size; ++start) {
        int position = rank[start];
        if (position == 0) continue;
        int other = suffixArray[position - 1];
        while (start + length < size && other + length < size && text[start + length] == text[other + length]) ++length;
        lcp[position] = length;
        if (length > 0) --length;
    }
    return lcp;
}
```

### Python

```python
def lcp_array(text: str, suffix_array: list[int]) -> list[int]:
    rank = [0] * len(text)
    for position, start in enumerate(suffix_array):
        rank[start] = position
    lcp = [0] * len(text)
    length = 0
    for start in range(len(text)):
        position = rank[start]
        if position == 0:
            continue
        other = suffix_array[position - 1]
        while start + length < len(text) and other + length < len(text) and text[start + length] == text[other + length]:
            length += 1
        lcp[position] = length
        length = max(0, length - 1)
    return lcp
```

### Java

```java
static int[] lcpArray(String text, int[] suffixArray) {
    int[] rank = new int[text.length()];
    for (int position = 0; position < suffixArray.length; position++) rank[suffixArray[position]] = position;
    int[] lcp = new int[text.length()];
    int length = 0;
    for (int start = 0; start < text.length(); start++) {
        int position = rank[start];
        if (position == 0) continue;
        int other = suffixArray[position - 1];
        while (start + length < text.length() && other + length < text.length()
            && text.charAt(start + length) == text.charAt(other + length)) length++;
        lcp[position] = length;
        if (length > 0) length--;
    }
    return lcp;
}
```

## Why it works

Moving from suffix `i` to `i+1` removes one leading character, so a previous
common prefix of length `k` guarantees at least `k-1` reusable comparisons.

## Complexity

Time and space are `O(n)` after the suffix array is known.

## Common mistakes

- Confusing text index with suffix-array position.
- Defining `lcp[i]` against the next suffix in code that uses the previous one.
- Forgetting to decrease the reused length.
