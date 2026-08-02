# Time and Space Complexity

## Idea

Complexity describes growth as input becomes large. It ignores machine-level
constants but preserves the dominant work.

## Steps

1. Choose the input-size variables.
2. Count how often the dominant operation runs.
3. Include hidden copying, sorting, hashing, and recursion.
4. Keep the fastest-growing term and state auxiliary space separately.

## The main rules

- Consecutive blocks add: `O(n) + O(n log n) = O(n log n)`.
- Nested independent loops multiply: `n` by `n` is `O(n^2)`.
- A pointer that only moves forward across the whole algorithm contributes
  `O(n)`, even if it appears inside another loop.
- Halving a search range gives `O(log n)` iterations.
- Recursion cost equals states times work per state, not merely recursion depth.

```text
O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)
```

## Amortized analysis

An individual dynamic-array append can cost `O(n)` during resizing, but a
sequence of `n` appends costs `O(n)`. Therefore append is `O(1)` amortized.
The same reasoning proves a monotonic stack is linear: each item is pushed
once and popped once.

## First-principles derivation

Complexity comes from counting operations, not from counting visible loops.

```text
input size -> number of states visited
           x work per state
           + preprocessing
           + hidden copies
```

Drop constants only after deriving the full count. A loop inside another loop
can still be linear when the inner pointer moves forward at most `n` times in
total.

## Classroom board: compare growth

```text
n               10       100       1,000
O(n)            10       100       1,000
O(n log2 n)     ~33      ~664      ~9,966
O(n^2)          100      10,000    1,000,000
O(2^n)          1,024    impossible impossible
```

Doubling `n` roughly doubles linear work, quadruples quadratic work, and can
make exponential work unusable immediately.

## Pattern recognition

Analyze complexity whenever constraints are given, loops share moving pointers,
recursion repeats states, or a convenient language operation may copy data.

## Space

Count auxiliary memory separately from output. A recursive DFS on a path of
`n` vertices uses `O(n)` call-stack space even if it allocates no collection.

## Example: linear despite a nested loop

Each value enters and leaves the stack at most once.

### C++

```cpp
std::vector<int> nextGreater(const std::vector<int>& values) {
    std::vector<int> answer(values.size(), -1);
    std::vector<int> stack;
    for (int index = 0; index < static_cast<int>(values.size()); ++index) {
        while (!stack.empty() && values[stack.back()] < values[index]) {
            answer[stack.back()] = values[index];
            stack.pop_back();
        }
        stack.push_back(index);
    }
    return answer;
}
```

### Python

```python
def next_greater(values: list[int]) -> list[int]:
    answer = [-1] * len(values)
    stack: list[int] = []
    for index, value in enumerate(values):
        while stack and values[stack[-1]] < value:
            answer[stack.pop()] = value
        stack.append(index)
    return answer
```

### Java

```java
static int[] nextGreater(int[] values) {
    int[] answer = new int[values.length];
    Arrays.fill(answer, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int index = 0; index < values.length; index++) {
        while (!stack.isEmpty() && values[stack.peekLast()] < values[index]) {
            answer[stack.removeLast()] = values[index];
        }
        stack.addLast(index);
    }
    return answer;
}
```

## Complexity of the example

Time is `O(n)` and auxiliary space is `O(n)`.

## Common mistakes

- Calling sorting “linear” because the visible loop is linear.
- Forgetting string slicing or copying costs.
- Treating hash operations as worst-case `O(1)`; they are expected `O(1)`.
- Ignoring the recursion stack or a copied input parameter.
- Multiplying loops when the inner pointer never moves backward.
