# Suffix Array

## Idea

A suffix array stores starting indices of all suffixes in lexicographic order.
The doubling algorithm repeatedly sorts suffixes by the ranks of two halves of
length `2^k`.

## Visual model

For `banana`:

```text
5: a
3: ana
1: anana
0: banana
4: na
2: nana
suffix array = [5, 3, 1, 0, 4, 2]
```

## Classroom board: sort longer prefixes by pairs

```text
after ranking 2-character prefixes, rank[i] describes text[i:i+2]
to rank 4 characters at i, compare:
(rank of text[i:i+2], rank of text[i+2:i+4])
repeat with lengths 1,2,4,8,... until whole suffixes are covered
```

## Steps

1. Give each suffix a rank from its first character.
2. Sort indices by `(rank[i], rank[i + length])`.
3. Compress equal pairs into new ranks.
4. Double `length` until it covers the string.

## First-principles derivation

Sorting full suffix strings repeats long character comparisons. Rank suffixes
first by one character, then by pairs of ranks representing prefixes of length
`2, 4, 8, ...`.

After each round, equal ranks mean equal prefixes of the processed length.

## Classroom board: sorted suffixes of banana

```text
index  suffix
0      banana
1      anana
2      nana
3      ana
4      na
5      a

sorted:
5  a
3  ana
1  anana
0  banana
4  na
2  nana

suffix array = [5,3,1,0,4,2]
```

Doubling ranks distinguishes suffixes without comparing their full text each
round.

## Pattern recognition

Use a suffix array for sorted suffix queries, substring search, repeated
substrings, or many comparisons among suffixes.

## Implementation: clear `O(n log^2 n)` version

### C++

```cpp
std::vector<int> suffixArray(const std::string& text) {
    const int size = text.size();
    std::vector<int> order(size), rank(size), nextRank(size);
    std::iota(order.begin(), order.end(), 0);
    for (int index = 0; index < size; ++index) rank[index] = static_cast<unsigned char>(text[index]);
    for (int length = 1; length < size; length *= 2) {
        std::sort(order.begin(), order.end(), [&](int left, int right) {
            return std::pair{rank[left], left + length < size ? rank[left + length] : -1}
                 < std::pair{rank[right], right + length < size ? rank[right + length] : -1};
        });
        nextRank[order[0]] = 0;
        for (int position = 1; position < size; ++position) {
            int previous = order[position - 1], current = order[position];
            auto previousKey = std::pair{rank[previous], previous + length < size ? rank[previous + length] : -1};
            auto currentKey = std::pair{rank[current], current + length < size ? rank[current + length] : -1};
            nextRank[current] = nextRank[previous] + (previousKey != currentKey);
        }
        rank.swap(nextRank);
    }
    return order;
}
```

### Python

```python
def suffix_array(text: str) -> list[int]:
    size = len(text)
    order = list(range(size))
    rank = [ord(character) for character in text]
    length = 1
    while length < size:
        order.sort(key=lambda index: (rank[index], rank[index + length] if index + length < size else -1))
        next_rank = [0] * size
        for position in range(1, size):
            previous = order[position - 1]
            current = order[position]
            previous_key = (rank[previous], rank[previous + length] if previous + length < size else -1)
            current_key = (rank[current], rank[current + length] if current + length < size else -1)
            next_rank[current] = next_rank[previous] + (previous_key != current_key)
        rank = next_rank
        length *= 2
    return order
```

### Java

```java
static int[] suffixArray(String text) {
    int size = text.length();
    Integer[] order = new Integer[size];
    int[] rank = new int[size];
    for (int index = 0; index < size; index++) {
        order[index] = index;
        rank[index] = text.charAt(index);
    }
    for (int length = 1; length < size; length *= 2) {
        int block = length;
        int[] currentRank = rank;
        Arrays.sort(order, Comparator.<Integer>comparingInt(index -> currentRank[index])
            .thenComparingInt(index -> index + block < size ? currentRank[index + block] : -1));
        int[] nextRank = new int[size];
        for (int position = 1; position < size; position++) {
            int previous = order[position - 1];
            int current = order[position];
            boolean different = rank[previous] != rank[current]
                || (previous + length < size ? rank[previous + length] : -1)
                != (current + length < size ? rank[current + length] : -1);
            nextRank[current] = nextRank[previous] + (different ? 1 : 0);
        }
        rank = nextRank;
    }
    return Arrays.stream(order).mapToInt(Integer::intValue).toArray();
}
```

## Why it works

If ranks correctly order prefixes of length `length`, sorting pairs correctly
orders prefixes of twice that length. Once length covers the string, these are
full suffix orders.

## Complexity

This readable version is `O(n log^2 n)` time and `O(n)` space. Counting-sort
rank pairs reduces it to `O(n log n)`.

## Common mistakes

- Failing on the empty string; define a non-empty contract or return empty.
- Giving out-of-range second halves a rank larger than real ranks.
- Comparing full suffix strings, which can make sorting quadratic.
