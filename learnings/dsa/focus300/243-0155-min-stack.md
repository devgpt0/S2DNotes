# Focus300 243: LeetCode 155 - Min Stack

**Source:** [LeetCode 155](https://leetcode.com/problems/min-stack/)  
**Difficulty:** Easy  
**Pattern:** stack with tracked minimum

## Exact contract

Implement a stack that can return the current minimum element in constant time.

## First principles

The stack needs to remember the minimum value seen so far for every prefix. Storing a parallel minimum snapshot makes `getMin` constant-time instead of rescanning.

## Cases that decide correctness

- Pushing a smaller value updates the minimum.
- Popping can reveal an older minimum from deeper in the stack.
- The current minimum must be available even after many operations.
- All core operations should stay constant-time.

## Brute force

```python
class MinStackBrute:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return min(self.stack)
```

Scan the stack whenever the minimum is requested.

## Better insight

Store either a parallel minimum stack or a paired value with each push.

## Expert solution

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val):
        self.stack.append(val)
        self.mins.append(val if not self.mins else min(val, self.mins[-1]))

    def pop(self):
        self.stack.pop()
        self.mins.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.mins[-1]
```

Track the current minimum alongside each stack state so push, pop, and top remain O(1).

**Complexity:** O(1) time per operation and O(n) space.
