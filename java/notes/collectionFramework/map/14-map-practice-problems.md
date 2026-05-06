# 14 - Map Practice Problems

## Beginner

1. Count frequency of characters in a string.
2. Find first non-repeating character.
3. Build `id -> name` map from two arrays.
4. Print key-value pairs sorted by key.

## Intermediate

1. Group words by anagram.
2. Build inverted index (`value -> list of keys`) from a map.
3. Implement `Two Sum` using map.
4. Merge two maps with sum for common keys.
5. Sort entries by value descending.

## Advanced

1. Implement fixed-size LRU cache with `LinkedHashMap`.
2. Build time-based key-value store.
3. Top `k` frequent elements with map + heap.
4. Sliding window substring problems with frequency map.
5. Design thread-safe counter map for high concurrency.

## Expert Challenge

Given list of transactions (`userId`, `category`, `amount`, `status`, `timestamp`):

1. keep only successful transactions
2. group by `userId`
3. inside each user, group by `category`
4. compute total amount per category
5. output top 3 users by total spend

Solve once with loops and once with streams.
