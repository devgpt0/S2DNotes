# Focus300 058: LeetCode 381 - Insert Delete GetRandom O(1), Duplicates Allowed

**Source:** [LeetCode 381 - Insert Delete GetRandom O(1) - Duplicates allowed](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/)  
**Difficulty:** Hard  
**Pattern:** dense occurrence array plus value-to-index sets  

## Exact contract

Maintain a multiset with `insert(value)`, `remove(value)`, and `get_random()`.
Insertion returns whether the value was previously absent; removal deletes one
copy and returns whether one existed. Random selection is uniform over stored
occurrences. Empty random selection raises `IndexError` in these Python models.

## First principles

An array provides uniform random occurrence selection. Deleting an arbitrary
array position becomes constant time by moving the last occurrence into the
hole. A dictionary of index sets locates one occurrence of each value and must
be updated for that swap.


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

- Duplicate insertion returns `False` but appends another occurrence.
- Removing a missing value returns `False`.
- Moving the final occurrence of the same value still updates its index set.
- Empty index sets must be removed from the dictionary.
- Randomness is over occurrences, so duplicates have proportional probability.

## Brute force: store only the occurrence list

```python
from collections.abc import Callable
from secrets import randbelow


class RandomizedCollectionBrute:
    def __init__(self, choose_index: Callable[[int], int] = randbelow) -> None:
        self._values: list[int] = []
        self._choose_index = choose_index

    def insert(self, value: int) -> bool:
        if type(value) is not int:
            raise ValueError("value must be an integer")
        was_absent = value not in self._values
        self._values.append(value)
        return was_absent

    def remove(self, value: int) -> bool:
        if type(value) is not int:
            raise ValueError("value must be an integer")
        try:
            self._values.remove(value)
        except ValueError:
            return False
        return True

    def get_random(self) -> int:
        if not self._values:
            raise IndexError("collection is empty")
        return self._values[self._choose_index(len(self._values))]
```

**Complexity:** `O(n)` insertion membership and removal, `O(1)` random access.

## Better approach: no separate genuine intermediate

A frequency dictionary makes membership constant but cannot identify an array
position to delete. The index-set design is the necessary bridge to constant
expected time for every operation.

## Expert solution: swap-delete with occurrence index sets

```python
from collections.abc import Callable
from secrets import randbelow


class RandomizedCollection:
    def __init__(self, choose_index: Callable[[int], int] = randbelow) -> None:
        self._values: list[int] = []
        self._indices: dict[int, set[int]] = {}
        self._choose_index = choose_index

    def insert(self, value: int) -> bool:
        if type(value) is not int:
            raise ValueError("value must be an integer")
        was_absent = value not in self._indices
        self._indices.setdefault(value, set()).add(len(self._values))
        self._values.append(value)
        return was_absent

    def remove(self, value: int) -> bool:
        if type(value) is not int:
            raise ValueError("value must be an integer")
        positions = self._indices.get(value)
        if not positions:
            return False
        remove_index = positions.pop()
        last_index = len(self._values) - 1
        last_value = self._values[last_index]
        if remove_index != last_index:
            self._values[remove_index] = last_value
            last_positions = self._indices[last_value]
            last_positions.remove(last_index)
            last_positions.add(remove_index)
        self._values.pop()
        if not positions:
            del self._indices[value]
        return True

    def get_random(self) -> int:
        if not self._values:
            raise IndexError("collection is empty")
        return self._values[self._choose_index(len(self._values))]
```

The dictionary contains exactly every current array index for its value. A
swap-delete changes at most one moved occurrence index, preserving the invariant
and the dense array needed for uniform sampling.

**Complexity:** `O(1)` expected time per operation and `O(n)` space.

