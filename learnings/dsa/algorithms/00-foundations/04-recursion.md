# Recursion and the Call Stack

## Idea

Recursion solves a problem by solving smaller instances of the same shape.
Every recursive design needs:

- a base case that returns directly;
- a transition to a strictly smaller state;
- a clear meaning for the returned value.

## Steps

1. State what one call returns.
2. Handle the smallest state directly.
3. Call only strictly smaller states.
4. Combine their answers and return.

## First-principles derivation

Recursion is ordinary problem solving with a promise: assume a smaller call
returns the correct answer, then show how to build the current answer.

```text
current problem -> strictly smaller problem(s)
                -> returned answers
                -> combine
base case stops the chain
```

A call must have one precise meaning and every path must move toward a base
case.

## Classroom board: returns rebuild the answer

For `[2, 1, 3, 4]`:

```text
sum[0,4)
├─ sum[0,2)
│  ├─ sum[0,1) = 2
│  └─ sum[1,2) = 1
│  returns 3
└─ sum[2,4)
   ├─ sum[2,3) = 3
   └─ sum[3,4) = 4
   returns 7

root returns 3 + 7 = 10
```

The leaves solve the smallest ranges; every parent combines two already
correct smaller answers.

## Pattern recognition

Use recursion for trees, divide and conquer, and backtracking when the natural
state becomes smaller and maximum depth is safe.

## Example: divide-and-conquer range sum

```text
sum [0, 8)
   /       \
[0, 4)    [4, 8)
```

### C++

```cpp
long long rangeSum(const std::vector<int>& values, int left, int right) {
    if (right - left == 1) {
        return values[left];
    }
    const int middle = left + (right - left) / 2;
    return rangeSum(values, left, middle) + rangeSum(values, middle, right);
}
```

### Python

```python
def range_sum(values: list[int], left: int, right: int) -> int:
    if right - left == 1:
        return values[left]
    middle = left + (right - left) // 2
    return range_sum(values, left, middle) + range_sum(values, middle, right)
```

### Java

```java
static long rangeSum(int[] values, int left, int right) {
    if (right - left == 1) {
        return values[left];
    }
    int middle = left + (right - left) / 2;
    return rangeSum(values, left, middle) + rangeSum(values, middle, right);
}
```

## Complexity

Time is `O(n)`, and stack space is `O(log n)` because the recursion is
balanced. A one-by-one recursion would use `O(n)` stack space.

> [!WARNING]
> Python and Java can overflow the call stack on deep paths. C++ is not immune.
> Prefer iterative DFS for adversarial graphs with up to hundreds of thousands
> of vertices.

## Recursion versus dynamic programming

Draw the recursion tree. If the same state appears multiple times, memoize it
or compute states bottom-up. If states never repeat, memoization adds no value.

## Common mistakes

- A base case that excludes a valid smallest input.
- Changing shared mutable state without undoing it during backtracking.
- Copying a large array into every call.
- Assuming tail recursion is automatically optimized; these languages do not
  guarantee that here.
