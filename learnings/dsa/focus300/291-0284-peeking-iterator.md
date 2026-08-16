# Focus300 291: LeetCode 284 - Peeking Iterator

**Source:** [LeetCode 284](https://leetcode.com/problems/peeking-iterator/)  
**Difficulty:** Easy  
**Pattern:** iterator wrapper with cached lookahead

## Exact contract

Implement an iterator that can peek at the next element without consuming it.

## First principles

Peeking only requires remembering one upcoming value. Cache that value when needed, and serve it again until `next` consumes it.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- Calling `peek` repeatedly should not advance the iterator.
- A finished iterator has no next value.
- The wrapper should preserve the original iteration order.
- The lookahead cache is at most one element deep.

## Brute force

```python
class PeekingIteratorBrute:
    def __init__(self, iterator):
        self.values = list(iterator)
        self.index = 0

    def peek(self):
        return self.values[self.index]

    def next(self):
        value = self.values[self.index]
        self.index += 1
        return value

    def hasNext(self):
        return self.index < len(self.values)
```

Advance the underlying iterator every time `peek` is called and try to push the value back.

## Better insight

Store one cached value and only fetch from the source iterator when the cache is empty.

## Expert solution

```python
class PeekingIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self._advance()

    def _advance(self):
        self._has_next = self.iterator.hasNext()
        self._next = self.iterator.next() if self._has_next else None

    def peek(self):
        return self._next

    def next(self):
        value = self._next
        self._advance()
        return value

    def hasNext(self):
        return self._has_next
```

Use a single lookahead slot that `peek` fills and `next` consumes.

**Complexity:** O(1) time per operation and O(1) extra space.
