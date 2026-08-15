# Focus300 289: LeetCode 275 - H-Index II

**Source:** [LeetCode 275](https://leetcode.com/problems/h-index-ii/)  
**Difficulty:** Medium  
**Pattern:** count-based rank thresholding

## Exact contract

Return the largest `h` such that at least `h` papers have citations of at least `h`.

## First principles

The answer depends only on how many papers reach each citation threshold. Once the papers are sorted or bucketed, the threshold search becomes direct.

## Cases that decide correctness

- All zero citations yield zero.
- High outliers should not distort the rank threshold.
- Duplicates still count as separate papers.
- The result is bounded by the number of papers.

## Brute force

```python
def h_index_brute(citations):
    left, right = 0, len(citations) - 1
    while left <= right:
        mid = (left + right) // 2
        if citations[mid] >= len(citations) - mid:
            right = mid - 1
        else:
            left = mid + 1
    return len(citations) - left
```

Sort the citations and test every possible threshold.

## Better insight

Use sorting or counting to locate the highest rank that still has enough supporting papers.

## Expert solution

```python
def h_index(citations):
    left, right = 0, len(citations) - 1
    n = len(citations)
    while left <= right:
        mid = (left + right) // 2
        if citations[mid] >= n - mid:
            right = mid - 1
        else:
            left = mid + 1
    return n - left
```

Find the boundary where the number of papers with citations at least that boundary meets or exceeds the boundary itself.

**Complexity:** O(n log n) with sorting or O(n) with counting/bucket approaches.
