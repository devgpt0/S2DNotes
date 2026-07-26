# Power 30: Core DSA Problems

This set is ordered from foundational array/string patterns to advanced graph
and dynamic-programming techniques. Every problem begins with a concrete
example and visual model, develops a direct first solution with code and
complexity, and then shows exactly which repeated work is removed to derive the
optimal approach. Each note ends with patterns to remember, common mistakes,
and optimized implementations in C++, Python, Java, and Go.

## Problem index

1. [Two Sum](01-two-sum.md)
2. [Best Time to Buy and Sell Stock](02-best-time-to-buy-and-sell-stock.md)
3. [Product of Array Except Self](03-product-of-array-except-self.md)
4. [Maximum Subarray](04-maximum-subarray.md)
5. [Subarray Sum Equals K](05-subarray-sum-equals-k.md)
6. [3Sum](06-3sum.md)
7. [Trapping Rain Water](07-trapping-rain-water.md)
8. [Longest Substring Without Repeating Characters](08-longest-substring-without-repeating-characters.md)
9. [Minimum Window Substring](09-minimum-window-substring.md)
10. [Sliding Window Maximum](10-sliding-window-maximum.md)
11. [Search in Rotated Sorted Array](11-search-in-rotated-sorted-array.md)
12. [Median of Two Sorted Arrays](12-median-of-two-sorted-arrays.md)
13. [LRU Cache](13-lru-cache.md)
14. [Largest Rectangle in Histogram](14-largest-rectangle-in-histogram.md)
15. [Find Median from Data Stream](15-find-median-from-data-stream.md)
16. [Lowest Common Ancestor of a Binary Tree](16-lowest-common-ancestor-of-a-binary-tree.md)
17. [Binary Tree Maximum Path Sum](17-binary-tree-maximum-path-sum.md)
18. [Number of Islands](18-number-of-islands.md)
19. [Course Schedule](19-course-schedule.md)
20. [Word Ladder](20-word-ladder.md)
21. [Alien Dictionary](21-alien-dictionary.md)
22. [Network Delay Time](22-network-delay-time.md)
23. [Critical Connections in a Network](23-critical-connections-in-a-network.md)
24. [Redundant Connection](24-redundant-connection.md)
25. [Combination Sum](25-combination-sum.md)
26. [N-Queens](26-n-queens.md)
27. [Longest Common Subsequence](27-longest-common-subsequence.md)
28. [Edit Distance](28-edit-distance.md)
29. [Burst Balloons](29-burst-balloons.md)
30. [Minimum Cost to Connect All Points](30-minimum-cost-to-connect-all-points.md)

## How to use this set

1. Read the problem and articulate the brute-force solution first.
2. Identify the invariant used by the CP approach.
3. Implement the CP version without looking at the code.
4. Compare time and space complexity before moving on.

## Learning flow used in every note

```text
Problem and example
        |
        v
Visualization and observation
        |
        v
Solution 1: direct / brute-force thinking
        |
        v
Identify repeated or unnecessary work
        |
        v
Derive the optimized and competitive-programming approach
        |
        v
Remember the reusable pattern
```

## 1. Two Sum — Hash Map

**Problem:** Return the indices of two distinct elements whose sum is `target`.

- **Brute force:** Check every pair. `O(n^2)` time, `O(1)` space.
- **Better:** Sort `(value, index)` pairs and use two pointers. `O(n log n)` time, `O(n)` space.
- **CP approach:** Store `value -> index` while scanning. For `value`, look up `target - value` before storing it. `O(n)` expected time, `O(n)` space.
- **Invariant:** The map contains exactly the elements to the left of the current index.

## 2. Best Time to Buy and Sell Stock — Greedy

**Problem:** Choose one buy day before one sell day to maximize profit.

- **Brute force:** Evaluate all buy/sell pairs. `O(n^2)` time, `O(1)` space.
- **CP approach:** Track the lowest price seen so far and update the best profit for every price. `O(n)` time, `O(1)` space.
- **Invariant:** `minPrice` is the cheapest valid buy price before today.

## 3. Product of Array Except Self — Prefix/Suffix

**Problem:** Return `answer[i]`, the product of every value except `nums[i]`, without division.

- **Brute force:** Multiply all values except each index. `O(n^2)` time, `O(1)` extra space.
- **Better:** Store complete prefix and suffix arrays. `O(n)` time, `O(n)` space.
- **CP approach:** Write prefixes into the result, then multiply a rolling suffix product. `O(n)` time, `O(1)` extra space (excluding output).
- **Invariant:** Before the suffix pass reaches `i`, `answer[i]` contains the product strictly left of `i`.

## 4. Maximum Subarray — Kadane's Algorithm

**Problem:** Return the largest sum of a non-empty contiguous subarray.

- **Brute force:** Sum every subarray. `O(n^2)` with a running sum, `O(1)` space.
- **CP approach:** At each value, either extend the previous subarray or start a new one. `O(n)` time, `O(1)` space.
- **Invariant:** `current` is the best sum of a subarray ending at the current index.

## 5. Subarray Sum Equals K — Prefix Sum + Hash Map

**Problem:** Count subarrays whose sum equals `k`; values may be negative.

- **Brute force:** Test every subarray with a running sum. `O(n^2)` time, `O(1)` space.
- **CP approach:** For prefix sum `sum`, add the number of earlier prefixes equal to `sum - k`. `O(n)` expected time, `O(n)` space.
- **Invariant:** The frequency map counts all prefix sums before the current element. Initialize `0 -> 1`.

## 6. 3Sum — Sorting + Two Pointers

**Problem:** Return all unique triplets that sum to zero.

- **Brute force:** Enumerate triplets and deduplicate them. `O(n^3)` time.
- **CP approach:** Sort, fix the first value, then solve Two Sum with two pointers while skipping duplicates. `O(n^2)` time, `O(1)` extra space apart from output/sort.
- **Invariant:** With a fixed first value, moving left increases the sum and moving right decreases it.

## 7. Trapping Rain Water — Two Pointers

**Problem:** Compute how much water is trapped between non-negative bar heights.

- **Brute force:** For every bar, scan both sides for maximum height. `O(n^2)` time.
- **Better:** Precompute left and right maximum arrays. `O(n)` time, `O(n)` space.
- **CP approach:** Advance the shorter boundary and maintain maxima. `O(n)` time, `O(1)` space.
- **Invariant:** Water above the shorter side is determined by its own maximum, because the opposite boundary is at least as high.

## 8. Longest Substring Without Repeating Characters — Sliding Window

**Problem:** Return the maximum length of a substring with all distinct characters.

- **Brute force:** Test every substring for duplicates. `O(n^3)` time.
- **CP approach:** Keep the last index of each character and move the left boundary past a duplicate. `O(n)` time, `O(min(n, alphabet))` space.
- **Invariant:** The active window always has unique characters.

## 9. Minimum Window Substring — Sliding Window

**Problem:** Return the shortest substring of `s` containing every character of `t` with multiplicity.

- **Brute force:** Enumerate windows and count characters. `O(n^2)` time or worse.
- **CP approach:** Expand until valid, then shrink while valid; track missing required characters. `O(n)` time, `O(alphabet)` space.
- **Invariant:** `missing == 0` means the current window covers every required occurrence.

## 10. Sliding Window Maximum — Monotonic Queue

**Problem:** Return the maximum in every window of size `k`.

- **Brute force:** Scan each window. `O(nk)` time.
- **CP approach:** Keep indices in decreasing value order; discard expired and smaller trailing indices. `O(n)` time, `O(k)` space.
- **Invariant:** The deque front is always the maximum index for the current window.

## 11. Search in Rotated Sorted Array — Binary Search

**Problem:** Find a target in a rotated, strictly increasing array or return `-1`.

- **Brute force:** Linear scan. `O(n)` time.
- **CP approach:** One half of each binary-search interval is sorted; decide whether the target lies in it. `O(log n)` time, `O(1)` space.
- **Invariant:** The target, if present, remains inside `[left, right]`.

## 12. Median of Two Sorted Arrays — Binary Search

**Problem:** Return the median of two sorted arrays in `O(log(min(m, n)))` time.

- **Brute force:** Merge and then take the middle. `O(m + n)` time, `O(m + n)` space.
- **Better:** Merge only until the median. `O(m + n)` time, `O(1)` space.
- **CP approach:** Partition the shorter array so both left partitions contain half the values. `O(log(min(m, n)))` time, `O(1)` space.
- **Invariant:** A valid partition satisfies `leftA <= rightB` and `leftB <= rightA`.

## 13. LRU Cache — Hash Map + Doubly Linked List

**Problem:** Support `get` and `put` in `O(1)` while evicting the least recently used item.

- **Brute force:** Use a list and linearly find/move keys. `O(n)` per operation.
- **CP approach:** Map keys to linked-list nodes; keep most-recent items next to a head sentinel and evict the node next to a tail sentinel. `O(1)` average time, `O(capacity)` space.
- **Invariant:** List order is most recently used to least recently used, and every map node is linked once.

## 14. Largest Rectangle in Histogram — Monotonic Stack

**Problem:** Return the largest rectangle area in a histogram.

- **Brute force:** Choose a range and its minimum height. `O(n^2)` time.
- **CP approach:** Use an increasing stack of indices; when a lower bar arrives, finalize rectangles for taller bars. `O(n)` time, `O(n)` space.
- **Invariant:** Heights indexed by the stack are non-decreasing.

## 15. Find Median from Data Stream — Two Heaps

**Problem:** Add numbers and query the median at any time.

- **Brute force:** Store values and sort on every query. `O(n log n)` query time.
- **Better:** Keep a sorted list, but insertion remains `O(n)`.
- **CP approach:** A max-heap stores the lower half and a min-heap stores the upper half. `O(log n)` add, `O(1)` median, `O(n)` space.
- **Invariant:** Heap sizes differ by at most one and every lower value is at most every upper value.

## 16. Lowest Common Ancestor of a Binary Tree — Tree DFS

**Problem:** Return the lowest node having both `p` and `q` as descendants (a node can be its own descendant).

- **Brute force:** Store root-to-node paths, then compare paths. `O(n)` time and space.
- **CP approach:** DFS returns `p`, `q`, or the LCA found below. `O(n)` time, `O(h)` recursion space.
- **Invariant:** A node is the LCA exactly when one target is found in each subtree, or it is one target and the other appears below.

## 17. Binary Tree Maximum Path Sum — Tree DP

**Problem:** Return the maximum sum of any non-empty path in a binary tree.

- **Brute force:** Consider paths through every pair of nodes. Superlinear time.
- **CP approach:** DFS returns the best downward gain and updates a global result with both positive child gains. `O(n)` time, `O(h)` space.
- **Invariant:** The returned gain uses at most one child because a parent path cannot branch twice.

## 18. Number of Islands — DFS / BFS

**Problem:** Count 4-directionally connected components of land in a grid.

- **Brute force:** Re-scan from every land cell without marking. Redundant and potentially `O((mn)^2)`.
- **CP approach:** Start DFS/BFS at each unvisited land cell and mark its whole component. `O(mn)` time, `O(mn)` worst-case space.
- **Invariant:** Every visited land cell belongs to exactly one counted island.

## 19. Course Schedule — Topological Sort

**Problem:** Determine whether all courses can be completed given prerequisite pairs.

- **Brute force:** Search for a cycle from each course repeatedly. `O(V(V+E))` time.
- **CP approach:** Kahn's algorithm repeatedly removes zero-indegree courses. `O(V+E)` time and space.
- **Invariant:** A course is ready exactly when all prerequisite edges have been removed.

## 20. Word Ladder — BFS

**Problem:** Find the shortest transformation sequence between equal-length words, changing one letter at a time.

- **Brute force:** Build all pairwise edges, then BFS. `O(n^2L)` time.
- **CP approach:** BFS and generate the `25 * L` one-letter neighbors of each word. `O(nL^2 * alphabet)` worst-case time, `O(n)` space.
- **Invariant:** BFS explores transformations in non-decreasing number of steps.

## 21. Alien Dictionary — Topological Sort

**Problem:** Infer a valid character order from a sorted alien-word dictionary.

- **Brute force:** Try every character permutation. `O(V!)` time.
- **CP approach:** Compare adjacent words to create the first differing-character edge, then topologically sort. `O(total characters + V + E)` time.
- **Invariant:** Every directed edge must appear in the final order; an invalid prefix or cycle has no answer.

## 22. Network Delay Time — Dijkstra's Algorithm

**Problem:** Return how long a signal needs to reach all nodes from a source, or `-1`.

- **Brute force:** Repeatedly relax every edge until stable. `O(VE)` time.
- **CP approach:** Use an adjacency list and min-heap Dijkstra for non-negative weights. `O((V+E) log V)` time, `O(V+E)` space.
- **Invariant:** The first non-stale distance popped from the heap is final.

## 23. Critical Connections in a Network — Tarjan's Algorithm

**Problem:** Return all bridges: edges whose removal disconnects an undirected graph.

- **Brute force:** Remove each edge and test connectivity. `O(E(V+E))` time.
- **CP approach:** DFS discovery times and low-link values identify a bridge when `low[child] > discovery[parent]`. `O(V+E)` time and space.
- **Invariant:** `low[u]` is the smallest discovery time reachable from `u`'s DFS subtree using at most one back edge.

## 24. Redundant Connection — Union-Find (DSU)

**Problem:** Given a tree plus one edge, return the edge that creates a cycle.

- **Brute force:** For each edge, DFS to see whether endpoints are already connected. `O(n^2)` time.
- **CP approach:** Union endpoints; the first failed union is the redundant edge. `O(n alpha(n))` time, `O(n)` space.
- **Invariant:** Each DSU component represents exactly the graph connectivity formed by processed edges.

## 25. Combination Sum — Backtracking

**Problem:** Return all combinations of distinct candidate choices that sum to a target; a candidate may be reused.

- **Brute force:** Generate unrestricted sequences and deduplicate. Exponential time and duplicate-heavy.
- **CP approach:** Backtrack with a non-decreasing candidate start index and prune when a sorted candidate exceeds the remainder. Exponential output-sensitive time.
- **Invariant:** The current path is non-decreasing, so each combination is generated once.

## 26. N-Queens — Backtracking

**Problem:** Place `n` queens on an `n x n` board so none attack another.

- **Brute force:** Try every board configuration. `O(n^(2n))` or worse.
- **CP approach:** Place one queen per row and track used columns and diagonals. `O(n!)` search time, `O(n)` auxiliary state excluding output.
- **Invariant:** Before each recursive call, the partial board has no attacking queens.

## 27. Longest Common Subsequence — Dynamic Programming

**Problem:** Return the length of the longest sequence shared by two strings without requiring contiguity.

- **Brute force:** Enumerate subsequences. Exponential time.
- **CP approach:** `dp[i][j]` is the LCS length for suffixes starting at `i` and `j`. `O(mn)` time and space.
- **Invariant:** Equal characters extend the diagonal; otherwise discard one leading character optimally.

## 28. Edit Distance — Dynamic Programming

**Problem:** Return the minimum insertions, deletions, and replacements to transform one string into another.

- **Brute force:** Recursively try all edits. Exponential time.
- **CP approach:** `dp[i][j]` is the minimum cost to convert prefixes of length `i` and `j`. `O(mn)` time and space.
- **Invariant:** Each state ends in match, insertion, deletion, or replacement.

## 29. Burst Balloons — Interval Dynamic Programming

**Problem:** Choose burst order to maximize coins from adjacent remaining balloons.

- **Brute force:** Try every burst order. `O(n!)` time.
- **CP approach:** Choose the last balloon burst in each interval; pad both ends with `1`. `O(n^3)` time, `O(n^2)` space.
- **Invariant:** When balloon `k` is last in `(left, right)`, its neighbors are fixed at `left` and `right`.

## 30. Minimum Cost to Connect All Points — Minimum Spanning Tree

**Problem:** Connect all points with minimum Manhattan-distance cost.

- **Brute force:** Enumerate spanning trees. Exponential time.
- **CP approach:** Dense Prim's algorithm adds the cheapest point and relaxes Manhattan distances to every unvisited point. `O(n^2)` time, `O(n)` space.
- **Invariant:** `minDistance[i]` is the cheapest edge from the current MST to unvisited point `i`.
