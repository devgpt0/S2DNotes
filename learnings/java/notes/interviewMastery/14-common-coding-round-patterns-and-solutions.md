# 14 - Common Java Coding-Round Patterns and Solutions

## 1) Two Sum

```java
static int[] twoSum(int[] values, int target) {
    Map<Integer, Integer> indexByValue = new HashMap<>();
    for (int index = 0; index < values.length; index++) {
        int needed = target - values[index];
        Integer match = indexByValue.get(needed);
        if (match != null) return new int[] {match, index};
        indexByValue.put(values[index], index);
    }
    throw new IllegalArgumentException("no solution");
}
System.out.println(Arrays.toString(twoSum(new int[] {2, 7, 11, 15}, 9)));
// Output: [0, 1]
```

Complexity: O(n) time, O(n) space. Clarify whether one solution is guaranteed.

## 2) Longest Substring Without Repeating Characters

```java
static int longestUnique(String value) {
    Map<Character, Integer> lastSeen = new HashMap<>();
    int left = 0;
    int maximum = 0;
    for (int right = 0; right < value.length(); right++) {
        char character = value.charAt(right);
        left = Math.max(left, lastSeen.getOrDefault(character, -1) + 1);
        lastSeen.put(character, right);
        maximum = Math.max(maximum, right - left + 1);
    }
    return maximum;
}
System.out.println(longestUnique("abcabcbb"));
// Output: 3
```

Pattern: sliding window. Complexity: O(n) time, O(k) space.

## 3) Balanced Brackets

```java
static boolean balanced(String value) {
    Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');
    Deque<Character> stack = new ArrayDeque<>();
    for (char character : value.toCharArray()) {
        if (pairs.containsValue(character)) stack.push(character);
        else if (pairs.containsKey(character)
                && (stack.isEmpty() || stack.pop() != pairs.get(character))) return false;
    }
    return stack.isEmpty();
}
System.out.println(balanced("{[()]}") + ", " + balanced("([)]"));
// Output: true, false
```

Complexity: O(n) time and O(n) worst-case space.

## 4) Binary Search

```java
static int binarySearch(int[] sorted, int target) {
    int left = 0;
    int right = sorted.length - 1;
    while (left <= right) {
        int middle = left + (right - left) / 2;
        if (sorted[middle] == target) return middle;
        if (sorted[middle] < target) left = middle + 1;
        else right = middle - 1;
    }
    return -1;
}
System.out.println(binarySearch(new int[] {1, 3, 5, 7}, 5));
// Output: 2
```

Complexity: O(log n). Input must be sorted according to the same comparison.

## 5) Merge Overlapping Intervals

```java
record Interval(int start, int end) {
    Interval {
        if (start > end) throw new IllegalArgumentException("start after end");
    }
}
static List<Interval> merge(List<Interval> input) {
    List<Interval> sorted = input.stream().sorted(Comparator.comparingInt(Interval::start)).toList();
    List<Interval> result = new ArrayList<>();
    for (Interval current : sorted) {
        if (result.isEmpty() || result.getLast().end() < current.start()) result.add(current);
        else {
            Interval previous = result.removeLast();
            result.add(new Interval(previous.start(), Math.max(previous.end(), current.end())));
        }
    }
    return result;
}
System.out.println(merge(List.of(new Interval(1, 3), new Interval(2, 6), new Interval(8, 10))));
// Output: [Interval[start=1, end=6], Interval[start=8, end=10]]
```

Complexity: O(n log n) time due to sorting.

## 6) Maximum Sum Fixed Window

```java
static int maxWindowSum(int[] values, int size) {
    if (size <= 0 || size > values.length) throw new IllegalArgumentException("invalid size");
    int sum = Arrays.stream(values, 0, size).sum();
    int maximum = sum;
    for (int right = size; right < values.length; right++) {
        sum += values[right] - values[right - size];
        maximum = Math.max(maximum, sum);
    }
    return maximum;
}
System.out.println(maxWindowSum(new int[] {2, 1, 5, 1, 3, 2}, 3));
// Output: 9
```

Complexity: O(n) time and O(1) space.

## 7) Top K Frequent Values

```java
static List<Integer> topKFrequent(int[] values, int k) {
    Map<Integer, Integer> counts = new HashMap<>();
    for (int value : values) counts.merge(value, 1, Integer::sum);
    PriorityQueue<Integer> heap = new PriorityQueue<>(Comparator.comparingInt(counts::get));
    for (int value : counts.keySet()) {
        heap.offer(value);
        if (heap.size() > k) heap.poll();
    }
    List<Integer> result = new ArrayList<>(heap);
    result.sort(Comparator.comparingInt(counts::get).reversed());
    return result;
}
System.out.println(topKFrequent(new int[] {1, 1, 1, 2, 2, 3}, 2));
// Output: [1, 2]
```

Complexity: O(n + d log k) for d distinct values.

## 8) Breadth-First Search Shortest Distance

```java
static int distance(Map<String, List<String>> graph, String start, String target) {
    Queue<String> queue = new ArrayDeque<>();
    Map<String, Integer> distance = new HashMap<>();
    queue.add(start);
    distance.put(start, 0);
    while (!queue.isEmpty()) {
        String node = queue.remove();
        if (node.equals(target)) return distance.get(node);
        for (String next : graph.getOrDefault(node, List.of())) {
            if (!distance.containsKey(next)) {
                distance.put(next, distance.get(node) + 1);
                queue.add(next);
            }
        }
    }
    return -1;
}
Map<String, List<String>> graph = Map.of("A", List.of("B", "C"), "B", List.of("D"), "C", List.of(), "D", List.of());
System.out.println(distance(graph, "A", "D"));
// Output: 2
```

Complexity: O(V + E). BFS finds shortest path length in an unweighted graph.

## Most-Asked Coding Patterns

- hash lookup: two sum, frequency, anagrams
- two pointers: sorted pairs, palindrome, deduplication
- sliding window: substring/subarray constraints
- stack: brackets, next greater, expression parsing
- queue/BFS: levels and shortest unweighted path
- heap: top K, merge sorted sources, running median
- binary search: sorted lookup and monotonic answer
- intervals: merge, meeting rooms, scheduling
- DFS/backtracking: combinations, permutations, grids
- dynamic programming: climbing stairs, coin change, longest subsequence
- trees: traversals, height, lowest common ancestor
- graphs: cycle, connectivity, topological sort

## Coding-Round Answer Template

Clarify constraints -> demonstrate brute force -> derive pattern -> code cleanly -> test boundaries -> state time/space complexity -> discuss tradeoffs.
