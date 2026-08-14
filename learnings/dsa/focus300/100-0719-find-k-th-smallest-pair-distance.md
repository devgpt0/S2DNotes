# Focus300 100: LeetCode 719 - Find K-th Smallest Pair Distance

**Source:** [LeetCode 719](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)  
**Difficulty:** Hard  
**Pattern:** binary search on distance with sliding-window pair counting

## Exact contract

For an integer array, each index pair `i < j` contributes the absolute distance
`abs(numbers[i] - numbers[j])`. Return the `position`th distance in the sorted
multiset of all `n*(n-1)/2` pair distances. Equal distances from different
pairs occupy separate positions.

## First principles

After sorting a copy of the values, count pairs with distance at most a
candidate `d`. For each right endpoint, advance the left endpoint until the
window difference is at most `d`; all indices from `left` through `right-1`
then form valid pairs with `right`.

That count is monotone in `d`, so the answer is the first distance whose count
reaches `position`.

## Cases that decide correctness

- Duplicate values create zero-distance pairs.
- Pair multiplicity matters; distances are not deduplicated.
- The first position asks for the minimum distance.
- Sorting must not mutate the caller's array.
- Lower-bound binary search is required when the count jumps over `position`.

## Brute force: materialize and sort every pair distance

```python
def kth_pair_distance_brute(numbers: list[int], position: int) -> int:
    if type(numbers) is not list or not 2 <= len(numbers) <= 10_000:
        raise ValueError("numbers length must be between 2 and 10,000")
    if any(type(value) is not int or not 0 <= value <= 1_000_000 for value in numbers):
        raise ValueError("numbers must be integers in the source range")
    pair_count = len(numbers) * (len(numbers) - 1) // 2
    if type(position) is not int or not 1 <= position <= pair_count:
        raise ValueError("position is outside the pair-distance multiset")

    distances = [
        abs(numbers[first] - numbers[second])
        for first in range(len(numbers))
        for second in range(first + 1, len(numbers))
    ]
    distances.sort()
    return distances[position - 1]
```

This costs `O(n^2 log n)` time and `O(n^2)` space.

## Better insight: count pairs no farther apart than a threshold

The sorted two-pointer window counts all qualifying pairs in `O(n)` time. Its
monotonicity converts selection into a binary search over `[0, max-min]`.

## Expert solution: value binary search plus two-pointer counting

```python
def kth_pair_distance(numbers: list[int], position: int) -> int:
    if type(numbers) is not list or not 2 <= len(numbers) <= 10_000:
        raise ValueError("numbers length must be between 2 and 10,000")
    if any(type(value) is not int or not 0 <= value <= 1_000_000 for value in numbers):
        raise ValueError("numbers must be integers in the source range")
    pair_count = len(numbers) * (len(numbers) - 1) // 2
    if type(position) is not int or not 1 <= position <= pair_count:
        raise ValueError("position is outside the pair-distance multiset")

    ordered = sorted(numbers)

    def count_at_most(distance: int) -> int:
        count = 0
        left = 0
        for right, value in enumerate(ordered):
            while value - ordered[left] > distance:
                left += 1
            count += right - left
        return count

    low = 0
    high = ordered[-1] - ordered[0]
    while low < high:
        middle = (low + high) // 2
        if count_at_most(middle) >= position:
            high = middle
        else:
            low = middle + 1
    return low
```

At termination, all smaller distances have too few pairs and `low` has enough,
which is precisely the requested multiset order statistic.

**Complexity:** `O(n log n + n log W)` time for value range `W`, and `O(n)`
space for the sorted copy.
