# 06 - Coding, Algorithms, and Complexity

## Complexity Foundation

Know Big-O time and auxiliary space for array/list traversal, hashing, sorting, binary search, heap operations, tree traversal, and graph traversal. Discuss average and worst case where they differ.

## Recurring Patterns

- two pointers: sorted pairs, palindrome, partition
- sliding window: longest/shortest contiguous range
- hash lookup: counts, complements, grouping
- prefix sum: range sums and subarray counts
- stack: balanced brackets, monotonic next-greater problems
- queue/BFS: shortest unweighted path and level traversal
- heap: top-K and merging sorted sources
- binary search: sorted values or monotonic answer space
- DFS/backtracking: combinations, paths, constraint search
- dynamic programming: overlapping subproblems and optimal substructure
- union-find: connectivity

## Sliding Window Example

```java
static int maximumSum(int[] values, int windowSize) {
    if (windowSize <= 0 || windowSize > values.length) {
        throw new IllegalArgumentException("invalid windowSize");
    }
    int sum = Arrays.stream(values, 0, windowSize).sum();
    int maximum = sum;
    for (int right = windowSize; right < values.length; right++) {
        sum += values[right] - values[right - windowSize];
        maximum = Math.max(maximum, sum);
    }
    return maximum;
}
System.out.println(maximumSum(new int[] {2, 1, 5, 1, 3}, 2));
// Output: 6
```

Time is O(n), auxiliary space O(1).

## Interview Method

1. Restate inputs, outputs, constraints, duplicates, ordering, and failure behavior.
2. Work a small example.
3. Explain brute force and complexity.
4. Derive the improved data structure/pattern.
5. Code with clear names and validation.
6. Test normal, boundary, empty, duplicate, overflow, and invalid cases.
7. State complexity and tradeoffs.
