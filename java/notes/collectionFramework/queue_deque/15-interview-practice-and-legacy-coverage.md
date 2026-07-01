# 15 - Interview, Practice, and Legacy Coverage

## 1) High-Frequency Interview Questions

1. Difference between `offer/poll/peek` and `add/remove/element`.
2. Why prefer `ArrayDeque` over `Stack`?
3. Difference between `PriorityQueue` and FIFO queues.
4. `ArrayBlockingQueue` vs `LinkedBlockingQueue`.
5. `ConcurrentLinkedQueue` vs `BlockingQueue`.

## 2) Solved Practice: Sliding Window Maximum (Deque)

Concept taught: Monotonic deque for `O(n)` window max.

```java
int[] nums = {1, 3, -1, -3, 5, 3, 6, 7};
int k = 3;
Deque<Integer> dq = new ArrayDeque<>();
List<Integer> out = new ArrayList<>();

for (int i = 0; i < nums.length; i++) {
    while (!dq.isEmpty() && dq.peekFirst() <= i - k) dq.pollFirst();
    while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
    dq.offerLast(i);
    if (i >= k - 1) out.add(nums[dq.peekFirst()]);
}
System.out.println(out);
```

Expected output:

```text
[3, 3, 5, 5, 6, 7]
```

## 3) Solved Practice: Top-K Smallest Using PriorityQueue

Concept taught: Max-heap of size `k` for streaming top-k.

```java
int[] arr = {9, 4, 7, 1, 3, 6};
int k = 3;
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
for (int x : arr) {
    maxHeap.offer(x);
    if (maxHeap.size() > k) maxHeap.poll();
}
List<Integer> ans = new ArrayList<>(maxHeap);
Collections.sort(ans);
System.out.println(ans);
```

Expected output:

```text
[1, 3, 4]
```

## 4) Practice Set

1. Implement circular task scheduler with deque.
2. Build producer-consumer with graceful shutdown.
3. Task prioritizer with dynamic priority updates.
4. Time-delayed retry queue.
5. Queue using two stacks, stack using one queue.

## 5) Legacy to Modern Mapping

- `Stack` -> `ArrayDeque` stack methods
- manual thread wait/notify queues -> `BlockingQueue`
- ad-hoc priority list sorting -> `PriorityQueue`

## 6) Module Coverage Map

- basics and hierarchy -> `01`
- queue methods -> `02`
- deque methods -> `03`
- major non-concurrent implementations -> `04-06`
- blocking and concurrent implementations -> `07-12`
- performance and bug handling -> `13-14`
- interview and algorithmic practice -> `15`

## 7) Summary

Queue/deque mastery means understanding ordering semantics, blocking behavior, and implementation tradeoffs under load.
