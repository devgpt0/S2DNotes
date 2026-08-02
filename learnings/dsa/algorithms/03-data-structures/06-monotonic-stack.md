# Monotonic Stack

## Idea

A monotonic stack keeps values in increasing or decreasing order. When a new
value breaks the order, popped items have just found their nearest answer.

## Visual model

```text
decreasing stack of unresolved indices
new larger value -> pop smaller indices -> their next greater is known
```

## Classroom board: next greater values

```text
values = [2, 1, 4]

read 2 -> unresolved stack [2]
read 1 -> 1 is not greater than 2; stack [2,1]
read 4 -> pop 1: its next greater is 4
          pop 2: its next greater is 4
          push 4
answer = [4,4,-1]
```

The stack contains only values still waiting for an answer.

## Steps

1. Store indices whose answer is still unknown.
2. While the current value answers the top index, pop and record it.
3. Push the current index.
4. Unpopped indices keep the default “not found” answer.

## First-principles derivation

For each item, scanning backward for the first greater value repeats work.
Remove earlier candidates as soon as a new value proves they can never help a
future query.

The stack keeps unresolved candidates in monotone order; each index enters and
leaves at most once.

## Pattern recognition

Look for nearest greater/smaller values, histogram rectangles, visible people,
or removing dominated candidates in one direction.

## Implementation: next greater value

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

## Why it works

An index is popped by the first later value larger than it. Earlier candidates
were not large enough, so this value is exactly its next greater value.

## Complexity

Time is `O(n)` because every index is pushed and popped once. Space is `O(n)`.

## Common mistakes

- Storing values when the answer needs indices or distances.
- Using `<` instead of `<=` incorrectly when duplicates matter.
- Forgetting whether the required neighbor is previous or next.
