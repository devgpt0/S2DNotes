# 12 - Interview and Practice

## 1) Interview Theory Questions

1. Difference between `ArrayList` and `LinkedList`
2. Why `CopyOnWriteArrayList` is costly for writes
3. Difference between `List.of`, `Arrays.asList`, `new ArrayList<>(...)`
4. Why `Vector`/`Stack` are legacy in modern Java
5. What causes `ConcurrentModificationException`

## 2) Coding Questions

1. Remove duplicates from list while preserving order.
2. Find top `k` frequent elements from list.
3. Rotate list by `k` positions.
4. Merge two sorted lists into one sorted list.
5. Partition list into chunks of size `n`.
6. Group strings by length.
7. Sort list of objects by two fields.
8. Reverse every alternate block of `k` elements.

## 3) Expert Practice Challenge

Given list of transactions (`userId`, `amount`, `status`, `timestamp`):

1. keep only successful transactions
2. group by user
3. calculate total amount per user
4. sort users by total desc
5. return top 5 user IDs

Try one solution with loops, one with streams.

