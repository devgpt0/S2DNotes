# Greedy Algorithms and Exchange Arguments

## Idea

A greedy algorithm makes the best-looking safe choice now and never changes
it. It is correct only when a proof shows that this local choice can belong to
an optimal answer.

## Visual model

For maximum non-overlapping activities, choose the activity that ends first:

```text
earliest finish -> leaves the most remaining time -> repeat
```

## Classroom board: choose the earliest finish

```text
activities: A[1,4], B[2,3], C[3,5]
choose B because it finishes at 3
C starts at 3, so choose C
result B,C has 2 activities; choosing A would leave only 1
```

Finishing earlier leaves at least as much room as any other first choice.

## Steps

1. Sort activities by finish time.
2. Take the first activity.
3. Take each later activity whose start is at least the last chosen finish.

## First-principles derivation

A greedy algorithm commits to one local choice without revisiting it. That is
safe only when any optimal solution can exchange its first different choice
for the greedy choice without becoming worse.

The exchange argument proves the discarded alternatives are unnecessary; the
code alone does not.

## Pattern recognition

Greedy often appears with intervals, repeated cheapest/smallest choices, or a
matroid-like “choose items while valid” rule. Never infer correctness from the
word “minimum” alone.

## Implementation: maximum activity count

Each activity must satisfy `start < finish`. Activities touching at an endpoint
are compatible.

### C++

```cpp
int maximumActivities(std::vector<std::pair<int, int>> activities) {
    std::sort(activities.begin(), activities.end(), [](const auto& left, const auto& right) {
        return left.second < right.second;
    });
    int count = 0;
    int lastFinish = std::numeric_limits<int>::min();
    for (auto [start, finish] : activities) {
        if (start >= lastFinish) {
            ++count;
            lastFinish = finish;
        }
    }
    return count;
}
```

### Python

```python
def maximum_activities(activities: list[tuple[int, int]]) -> int:
    count = 0
    last_finish = -10**30
    for start, finish in sorted(activities, key=lambda activity: activity[1]):
        if start >= last_finish:
            count += 1
            last_finish = finish
    return count
```

### Java

```java
static int maximumActivities(int[][] activities) {
    Arrays.sort(activities, Comparator.comparingInt(activity -> activity[1]));
    int count = 0;
    int lastFinish = Integer.MIN_VALUE;
    for (int[] activity : activities) {
        if (activity[0] >= lastFinish) {
            count++;
            lastFinish = activity[1];
        }
    }
    return count;
}
```

## Why it works: exchange argument

Take any optimal schedule. Replacing its first activity with the earliest-
finishing activity cannot reduce room for later activities. Repeat this
exchange after every choice; an optimal schedule can match the greedy one.

## Complexity

Time is `O(n log n)` for sorting and extra space depends on the sort.

## Common mistakes

- Choosing the earliest start or shortest duration without a proof.
- Using `>` when touching intervals are allowed.
- Applying this rule to weighted activities; that problem needs DP.
