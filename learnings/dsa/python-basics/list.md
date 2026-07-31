# Python Lists: 120 Questions

All questions are strictly based on concepts 1–12 in [Python List Notes](../../python/notes/collection_framework/list.md).

## Part A: Theory MCQs (1–30)

### 1. What is a Python list?

- A. An ordered mutable sequence
- B. An immutable unordered value
- C. A unique-value-only collection
- D. A number only

**Answer:** A. An ordered mutable sequence

**Reasoning:** Lists preserve order and can change.

### 2. Which property lets a list change?

- A. Immutability
- B. Mutability
- C. Hashing
- D. Sorting

**Answer:** B. Mutability

**Reasoning:** Lists can be updated after creation.

### 3. Can a list hold strings and integers together?

- A. No
- B. Only after sorting
- C. Yes
- D. Only in a tuple

**Answer:** C. Yes

**Reasoning:** Lists are heterogeneous.

### 4. Which expression creates an empty list?

- A. {}
- B. ()
- C. set()
- D. []

**Answer:** D. []

**Reasoning:** Square brackets create a list.

### 5. What does list() return without an argument?

- A. []
- B. {}
- C. None
- D. ()

**Answer:** A. []

**Reasoning:** list() creates an empty list.

### 6. What does list("Hi") return?

- A. ["Hi"]
- B. ["H", "i"]
- C. "Hi"
- D. An error

**Answer:** B. ["H", "i"]

**Reasoning:** Strings are iterable character by character.

### 7. What happens for list(123)?

- A. It returns [123]
- B. It returns 123
- C. It raises TypeError
- D. It returns []

**Answer:** C. It raises TypeError

**Reasoning:** An integer is not iterable.

### 8. What does index 0 select?

- A. The last item
- B. Every item
- C. No item
- D. The first item

**Answer:** D. The first item

**Reasoning:** Python indices start at zero.

### 9. What does index -1 select?

- A. The last item
- B. The first item
- C. The list length
- D. No item

**Answer:** A. The last item

**Reasoning:** Negative index -1 means the final item.

### 10. What happens for an invalid direct index?

- A. It returns None
- B. It raises IndexError
- C. It returns []
- D. It clears the list

**Answer:** B. It raises IndexError

**Reasoning:** Direct access needs an existing item.

### 11. Is the slice end included?

- A. Yes
- B. Only for numbers
- C. No
- D. Only for strings

**Answer:** C. No

**Reasoning:** Slices exclude the end index.

### 12. What happens for an out-of-range slice?

- A. It raises IndexError
- B. It returns None
- C. It clears the list
- D. It returns available items

**Answer:** D. It returns available items

**Reasoning:** Slicing safely limits its bounds.

### 13. How can index 1 be updated?

- A. values[1] = 9
- B. values.append(1)
- C. values.clear()
- D. values.remove(1)

**Answer:** A. values[1] = 9

**Reasoning:** Indexed assignment replaces an item.

### 14. Can slice assignment change list length?

- A. No
- B. Yes
- C. Only for strings
- D. Only for empty lists

**Answer:** B. Yes

**Reasoning:** Replacement length can differ from slice length.

### 15. What does append(value) do?

- A. Adds at the beginning
- B. Removes a value
- C. Adds one final item
- D. Sorts the list

**Answer:** C. Adds one final item

**Reasoning:** append() adds one item at the end.

### 16. What does extend([3, 4]) do?

- A. Adds [3, 4] as one item
- B. Removes 3 and 4
- C. Returns a tuple
- D. Adds 3 and 4 separately

**Answer:** D. Adds 3 and 4 separately

**Reasoning:** extend() adds each iterable item.

### 17. What does insert(1, 9) do?

- A. Places 9 at index 1
- B. Removes index 1
- C. Adds 9 at the end
- D. Sorts the list

**Answer:** A. Places 9 at index 1

**Reasoning:** insert() adds at a requested index.

### 18. What does remove(value) delete?

- A. Every match
- B. The first matching value
- C. The last item
- D. The indexed item only

**Answer:** B. The first matching value

**Reasoning:** remove() stops after its first match.

### 19. What happens when remove() cannot find a value?

- A. It returns False
- B. It returns None
- C. It raises ValueError
- D. It raises IndexError

**Answer:** C. It raises ValueError

**Reasoning:** An absent value is a ValueError.

### 20. What does pop() do without an index?

- A. Returns the first item only
- B. Clears the list
- C. Sorts the list
- D. Removes and returns the last item

**Answer:** D. Removes and returns the last item

**Reasoning:** pop() defaults to the final item.

### 21. What does clear() do?

- A. Removes every item
- B. Deletes the variable
- C. Removes duplicates only
- D. Returns a new list

**Answer:** A. Removes every item

**Reasoning:** clear() empties the existing list.

### 22. After second = first, what is second?

- A. A deep copy
- B. An alias for first
- C. A shallow copy
- D. An empty list

**Answer:** B. An alias for first

**Reasoning:** Both names reference the same list.

### 23. Which creates a shallow copy?

- A. second = values
- B. values.append(1)
- C. values[:]
- D. reversed(values)

**Answer:** C. values[:]

**Reasoning:** A full slice creates a new outer list.

### 24. What does a shallow nested-list copy share?

- A. Nothing
- B. Only its length
- C. Only its outer list
- D. Its inner lists

**Answer:** D. Its inner lists

**Reasoning:** Only the outer list is copied.

### 25. Which creates independent nested lists?

- A. copy.deepcopy(values)
- B. values[:]
- C. list(values)
- D. second = values

**Answer:** A. copy.deepcopy(values)

**Reasoning:** deepcopy() recursively copies nested values.

### 26. What does + do with two lists?

- A. Finds membership
- B. Concatenates them
- C. Sorts them
- D. Removes duplicates

**Answer:** B. Concatenates them

**Reasoning:** + joins list sequences.

### 27. What does in do with a list?

- A. Adds an item
- B. Removes an item
- C. Tests membership
- D. Sorts the list

**Answer:** C. Tests membership

**Reasoning:** in checks whether a value is present.

### 28. Which function returns a new sorted list?

- A. values.sort()
- B. values.reverse()
- C. reversed(values)
- D. sorted(values)

**Answer:** D. sorted(values)

**Reasoning:** sorted() leaves the original unchanged.

### 29. What does index(value) return?

- A. The first matching position
- B. The match count
- C. The value itself
- D. The final position

**Answer:** A. The first matching position

**Reasoning:** index() reports the first match.

### 30. Which loop supplies both index and item?

- A. for value in values
- B. for i, value in enumerate(values)
- C. for i in range(1)
- D. for value in reversed(values)

**Answer:** B. for i, value in enumerate(values)

**Reasoning:** enumerate() yields index-item pairs.

## Part B: Code-Snippet MCQs (31–120)

### 31. What is the result?

~~~python
values = list(range(1))
print(values)

~~~

- A. None
- B. []
- C. [0]
- D. An exception

**Answer:** C. [0]

**Reasoning:** list() materializes the values produced by range().

### 32. What is the result?

~~~python
values = list(range(2))
print(values)

~~~

- A. None
- B. []
- C. An exception
- D. [0, 1]

**Answer:** D. [0, 1]

**Reasoning:** list() materializes the values produced by range().

### 33. What is the result?

~~~python
values = list(range(3))
print(values)

~~~

- A. [0, 1, 2]
- B. None
- C. []
- D. An exception

**Answer:** A. [0, 1, 2]

**Reasoning:** list() materializes the values produced by range().

### 34. What is the result?

~~~python
values = list(range(4))
print(values)

~~~

- A. None
- B. [0, 1, 2, 3]
- C. []
- D. An exception

**Answer:** B. [0, 1, 2, 3]

**Reasoning:** list() materializes the values produced by range().

### 35. What is the result?

~~~python
values = list(range(5))
print(values)

~~~

- A. None
- B. []
- C. [0, 1, 2, 3, 4]
- D. An exception

**Answer:** C. [0, 1, 2, 3, 4]

**Reasoning:** list() materializes the values produced by range().

### 36. What is the result?

~~~python
values = list(range(6))
print(values)

~~~

- A. None
- B. []
- C. An exception
- D. [0, 1, 2, 3, 4, 5]

**Answer:** D. [0, 1, 2, 3, 4, 5]

**Reasoning:** list() materializes the values produced by range().

### 37. What is the result?

~~~python
values = list(range(7))
print(values)

~~~

- A. [0, 1, 2, 3, 4, 5, 6]
- B. None
- C. []
- D. An exception

**Answer:** A. [0, 1, 2, 3, 4, 5, 6]

**Reasoning:** list() materializes the values produced by range().

### 38. What is the result?

~~~python
values = list(range(8))
print(values)

~~~

- A. None
- B. [0, 1, 2, 3, 4, 5, 6, 7]
- C. []
- D. An exception

**Answer:** B. [0, 1, 2, 3, 4, 5, 6, 7]

**Reasoning:** list() materializes the values produced by range().

### 39. What is the result?

~~~python
values = list(range(9))
print(values)

~~~

- A. None
- B. []
- C. [0, 1, 2, 3, 4, 5, 6, 7, 8]
- D. An exception

**Answer:** C. [0, 1, 2, 3, 4, 5, 6, 7, 8]

**Reasoning:** list() materializes the values produced by range().

### 40. What is the result?

~~~python
values = list(range(10))
print(values)

~~~

- A. None
- B. []
- C. An exception
- D. [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

**Answer:** D. [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

**Reasoning:** list() materializes the values produced by range().

### 41. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[0])
~~~

- A. 10
- B. None
- C. []
- D. An exception

**Answer:** A. 10

**Reasoning:** Direct indexing selects one item by position.

### 42. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[1])
~~~

- A. None
- B. 20
- C. []
- D. An exception

**Answer:** B. 20

**Reasoning:** Direct indexing selects one item by position.

### 43. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[2])
~~~

- A. None
- B. []
- C. 30
- D. An exception

**Answer:** C. 30

**Reasoning:** Direct indexing selects one item by position.

### 44. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[3])
~~~

- A. None
- B. []
- C. An exception
- D. 40

**Answer:** D. 40

**Reasoning:** Direct indexing selects one item by position.

### 45. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[4])
~~~

- A. 50
- B. None
- C. []
- D. An exception

**Answer:** A. 50

**Reasoning:** Direct indexing selects one item by position.

### 46. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[0])
~~~

- A. None
- B. 10
- C. []
- D. An exception

**Answer:** B. 10

**Reasoning:** Direct indexing selects one item by position.

### 47. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[1])
~~~

- A. None
- B. []
- C. 20
- D. An exception

**Answer:** C. 20

**Reasoning:** Direct indexing selects one item by position.

### 48. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[2])
~~~

- A. None
- B. []
- C. An exception
- D. 30

**Answer:** D. 30

**Reasoning:** Direct indexing selects one item by position.

### 49. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[3])
~~~

- A. 40
- B. None
- C. []
- D. An exception

**Answer:** A. 40

**Reasoning:** Direct indexing selects one item by position.

### 50. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[4])
~~~

- A. None
- B. 50
- C. []
- D. An exception

**Answer:** B. 50

**Reasoning:** Direct indexing selects one item by position.

### 51. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:1])
~~~

- A. None
- B. []
- C. [10]
- D. An exception

**Answer:** C. [10]

**Reasoning:** A slice excludes its end index.

### 52. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:2])
~~~

- A. None
- B. []
- C. An exception
- D. [10, 20]

**Answer:** D. [10, 20]

**Reasoning:** A slice excludes its end index.

### 53. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:3])
~~~

- A. [10, 20, 30]
- B. None
- C. []
- D. An exception

**Answer:** A. [10, 20, 30]

**Reasoning:** A slice excludes its end index.

### 54. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:4])
~~~

- A. None
- B. [10, 20, 30, 40]
- C. []
- D. An exception

**Answer:** B. [10, 20, 30, 40]

**Reasoning:** A slice excludes its end index.

### 55. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:5])
~~~

- A. None
- B. []
- C. [10, 20, 30, 40, 50]
- D. An exception

**Answer:** C. [10, 20, 30, 40, 50]

**Reasoning:** A slice excludes its end index.

### 56. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:0])
~~~

- A. None
- B. [0]
- C. An exception
- D. []

**Answer:** D. []

**Reasoning:** A slice excludes its end index.

### 57. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:1])
~~~

- A. [10]
- B. None
- C. []
- D. An exception

**Answer:** A. [10]

**Reasoning:** A slice excludes its end index.

### 58. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:2])
~~~

- A. None
- B. [10, 20]
- C. []
- D. An exception

**Answer:** B. [10, 20]

**Reasoning:** A slice excludes its end index.

### 59. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:3])
~~~

- A. None
- B. []
- C. [10, 20, 30]
- D. An exception

**Answer:** C. [10, 20, 30]

**Reasoning:** A slice excludes its end index.

### 60. What is the result?

~~~python
values = [10, 20, 30, 40, 50]
print(values[:4])
~~~

- A. None
- B. []
- C. An exception
- D. [10, 20, 30, 40]

**Answer:** D. [10, 20, 30, 40]

**Reasoning:** A slice excludes its end index.

### 61. What is the result?

~~~python
values = [1, 2]
values.append(1)
print(values)
~~~

- A. [1, 2, 1]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2, 1]

**Reasoning:** append() adds one item at the end.

### 62. What is the result?

~~~python
values = [1, 2]
values.append(2)
print(values)
~~~

- A. None
- B. [1, 2, 2]
- C. []
- D. An exception

**Answer:** B. [1, 2, 2]

**Reasoning:** append() adds one item at the end.

### 63. What is the result?

~~~python
values = [1, 2]
values.append(3)
print(values)
~~~

- A. None
- B. []
- C. [1, 2, 3]
- D. An exception

**Answer:** C. [1, 2, 3]

**Reasoning:** append() adds one item at the end.

### 64. What is the result?

~~~python
values = [1, 2]
values.append(4)
print(values)
~~~

- A. None
- B. []
- C. An exception
- D. [1, 2, 4]

**Answer:** D. [1, 2, 4]

**Reasoning:** append() adds one item at the end.

### 65. What is the result?

~~~python
values = [1, 2]
values.append(5)
print(values)
~~~

- A. [1, 2, 5]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2, 5]

**Reasoning:** append() adds one item at the end.

### 66. What is the result?

~~~python
values = [1, 2]
values.append(6)
print(values)
~~~

- A. None
- B. [1, 2, 6]
- C. []
- D. An exception

**Answer:** B. [1, 2, 6]

**Reasoning:** append() adds one item at the end.

### 67. What is the result?

~~~python
values = [1, 2]
values.append(7)
print(values)
~~~

- A. None
- B. []
- C. [1, 2, 7]
- D. An exception

**Answer:** C. [1, 2, 7]

**Reasoning:** append() adds one item at the end.

### 68. What is the result?

~~~python
values = [1, 2]
values.append(8)
print(values)
~~~

- A. None
- B. []
- C. An exception
- D. [1, 2, 8]

**Answer:** D. [1, 2, 8]

**Reasoning:** append() adds one item at the end.

### 69. What is the result?

~~~python
values = [1, 2]
values.append(9)
print(values)
~~~

- A. [1, 2, 9]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2, 9]

**Reasoning:** append() adds one item at the end.

### 70. What is the result?

~~~python
values = [1, 2]
values.append(10)
print(values)
~~~

- A. None
- B. [1, 2, 10]
- C. []
- D. An exception

**Answer:** B. [1, 2, 10]

**Reasoning:** append() adds one item at the end.

### 71. What is the result?

~~~python
values = [1, 2, 3]
values.remove(2)
print(values)
~~~

- A. None
- B. []
- C. [1, 3]
- D. An exception

**Answer:** C. [1, 3]

**Reasoning:** remove() deletes the first matching value.

### 72. What is the result?

~~~python
values = [1, 2, 3]
removed = values.pop()
print(removed, values)
~~~

- A. None
- B. []
- C. An exception
- D. 3 [1, 2]

**Answer:** D. 3 [1, 2]

**Reasoning:** pop() removes and returns the final item.

### 73. What is the result?

~~~python
values = [1, 2, 3]
values.remove(2)
print(values)
~~~

- A. [1, 3]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 3]

**Reasoning:** remove() deletes the first matching value.

### 74. What is the result?

~~~python
values = [1, 2, 3]
removed = values.pop()
print(removed, values)
~~~

- A. None
- B. 3 [1, 2]
- C. []
- D. An exception

**Answer:** B. 3 [1, 2]

**Reasoning:** pop() removes and returns the final item.

### 75. What is the result?

~~~python
values = [1, 2, 3]
values.remove(2)
print(values)
~~~

- A. None
- B. []
- C. [1, 3]
- D. An exception

**Answer:** C. [1, 3]

**Reasoning:** remove() deletes the first matching value.

### 76. What is the result?

~~~python
values = [1, 2, 3]
removed = values.pop()
print(removed, values)
~~~

- A. None
- B. []
- C. An exception
- D. 3 [1, 2]

**Answer:** D. 3 [1, 2]

**Reasoning:** pop() removes and returns the final item.

### 77. What is the result?

~~~python
values = [1, 2, 3]
values.remove(2)
print(values)
~~~

- A. [1, 3]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 3]

**Reasoning:** remove() deletes the first matching value.

### 78. What is the result?

~~~python
values = [1, 2, 3]
removed = values.pop()
print(removed, values)
~~~

- A. None
- B. 3 [1, 2]
- C. []
- D. An exception

**Answer:** B. 3 [1, 2]

**Reasoning:** pop() removes and returns the final item.

### 79. What is the result?

~~~python
values = [1, 2, 3]
values.remove(2)
print(values)
~~~

- A. None
- B. []
- C. [1, 3]
- D. An exception

**Answer:** C. [1, 3]

**Reasoning:** remove() deletes the first matching value.

### 80. What is the result?

~~~python
values = [1, 2, 3]
removed = values.pop()
print(removed, values)
~~~

- A. None
- B. []
- C. An exception
- D. 3 [1, 2]

**Answer:** D. 3 [1, 2]

**Reasoning:** pop() removes and returns the final item.

### 81. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(1)
print(first, second)
~~~

- A. [1, 2] [1, 2, 1]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2] [1, 2, 1]

**Reasoning:** A full slice makes an independent outer list.

### 82. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(2)
print(first, second)
~~~

- A. None
- B. [1, 2] [1, 2, 2]
- C. []
- D. An exception

**Answer:** B. [1, 2] [1, 2, 2]

**Reasoning:** A full slice makes an independent outer list.

### 83. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(3)
print(first, second)
~~~

- A. None
- B. []
- C. [1, 2] [1, 2, 3]
- D. An exception

**Answer:** C. [1, 2] [1, 2, 3]

**Reasoning:** A full slice makes an independent outer list.

### 84. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(4)
print(first, second)
~~~

- A. None
- B. []
- C. An exception
- D. [1, 2] [1, 2, 4]

**Answer:** D. [1, 2] [1, 2, 4]

**Reasoning:** A full slice makes an independent outer list.

### 85. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(5)
print(first, second)
~~~

- A. [1, 2] [1, 2, 5]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2] [1, 2, 5]

**Reasoning:** A full slice makes an independent outer list.

### 86. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(6)
print(first, second)
~~~

- A. None
- B. [1, 2] [1, 2, 6]
- C. []
- D. An exception

**Answer:** B. [1, 2] [1, 2, 6]

**Reasoning:** A full slice makes an independent outer list.

### 87. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(7)
print(first, second)
~~~

- A. None
- B. []
- C. [1, 2] [1, 2, 7]
- D. An exception

**Answer:** C. [1, 2] [1, 2, 7]

**Reasoning:** A full slice makes an independent outer list.

### 88. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(8)
print(first, second)
~~~

- A. None
- B. []
- C. An exception
- D. [1, 2] [1, 2, 8]

**Answer:** D. [1, 2] [1, 2, 8]

**Reasoning:** A full slice makes an independent outer list.

### 89. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(9)
print(first, second)
~~~

- A. [1, 2] [1, 2, 9]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2] [1, 2, 9]

**Reasoning:** A full slice makes an independent outer list.

### 90. What is the result?

~~~python
first = [1, 2]
second = first[:]
second.append(10)
print(first, second)
~~~

- A. None
- B. [1, 2] [1, 2, 10]
- C. []
- D. An exception

**Answer:** B. [1, 2] [1, 2, 10]

**Reasoning:** A full slice makes an independent outer list.

### 91. What is the result?

~~~python
values = [1, 2, 3]
print(values * 2)
~~~

- A. None
- B. []
- C. [1, 2, 3, 1, 2, 3]
- D. An exception

**Answer:** C. [1, 2, 3, 1, 2, 3]

**Reasoning:** * repeats the list sequence.

### 92. What is the result?

~~~python
values = [1, 2, 3]
print(sum(values))
~~~

- A. None
- B. []
- C. An exception
- D. 6

**Answer:** D. 6

**Reasoning:** sum() adds numeric list items.

### 93. What is the result?

~~~python
values = [1, 2, 3]
print(values * 2)
~~~

- A. [1, 2, 3, 1, 2, 3]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2, 3, 1, 2, 3]

**Reasoning:** * repeats the list sequence.

### 94. What is the result?

~~~python
values = [1, 2, 3]
print(sum(values))
~~~

- A. None
- B. 6
- C. []
- D. An exception

**Answer:** B. 6

**Reasoning:** sum() adds numeric list items.

### 95. What is the result?

~~~python
values = [1, 2, 3]
print(values * 2)
~~~

- A. None
- B. []
- C. [1, 2, 3, 1, 2, 3]
- D. An exception

**Answer:** C. [1, 2, 3, 1, 2, 3]

**Reasoning:** * repeats the list sequence.

### 96. What is the result?

~~~python
values = [1, 2, 3]
print(sum(values))
~~~

- A. None
- B. []
- C. An exception
- D. 6

**Answer:** D. 6

**Reasoning:** sum() adds numeric list items.

### 97. What is the result?

~~~python
values = [1, 2, 3]
print(values * 2)
~~~

- A. [1, 2, 3, 1, 2, 3]
- B. None
- C. []
- D. An exception

**Answer:** A. [1, 2, 3, 1, 2, 3]

**Reasoning:** * repeats the list sequence.

### 98. What is the result?

~~~python
values = [1, 2, 3]
print(sum(values))
~~~

- A. None
- B. 6
- C. []
- D. An exception

**Answer:** B. 6

**Reasoning:** sum() adds numeric list items.

### 99. What is the result?

~~~python
values = [1, 2, 3]
print(values * 2)
~~~

- A. None
- B. []
- C. [1, 2, 3, 1, 2, 3]
- D. An exception

**Answer:** C. [1, 2, 3, 1, 2, 3]

**Reasoning:** * repeats the list sequence.

### 100. What is the result?

~~~python
values = [1, 2, 3]
print(sum(values))
~~~

- A. None
- B. []
- C. An exception
- D. 6

**Answer:** D. 6

**Reasoning:** sum() adds numeric list items.

### 101. What is the result?

~~~python
values = [1, 1, 2]
values.reverse()
print(values)
~~~

- A. [2, 1, 1]
- B. None
- C. []
- D. An exception

**Answer:** A. [2, 1, 1]

**Reasoning:** reverse() changes the list in place.

### 102. What is the result?

~~~python
values = [2, 1, 2]
print(sorted(values))
~~~

- A. None
- B. [1, 2, 2]
- C. []
- D. An exception

**Answer:** B. [1, 2, 2]

**Reasoning:** sorted() returns a sorted new list.

### 103. What is the result?

~~~python
values = [3, 1, 2]
values.reverse()
print(values)
~~~

- A. None
- B. []
- C. [2, 1, 3]
- D. An exception

**Answer:** C. [2, 1, 3]

**Reasoning:** reverse() changes the list in place.

### 104. What is the result?

~~~python
values = [4, 1, 2]
print(sorted(values))
~~~

- A. None
- B. []
- C. An exception
- D. [1, 2, 4]

**Answer:** D. [1, 2, 4]

**Reasoning:** sorted() returns a sorted new list.

### 105. What is the result?

~~~python
values = [5, 1, 2]
values.reverse()
print(values)
~~~

- A. [2, 1, 5]
- B. None
- C. []
- D. An exception

**Answer:** A. [2, 1, 5]

**Reasoning:** reverse() changes the list in place.

### 106. What is the result?

~~~python
values = [6, 1, 2]
print(sorted(values))
~~~

- A. None
- B. [1, 2, 6]
- C. []
- D. An exception

**Answer:** B. [1, 2, 6]

**Reasoning:** sorted() returns a sorted new list.

### 107. What is the result?

~~~python
values = [7, 1, 2]
values.reverse()
print(values)
~~~

- A. None
- B. []
- C. [2, 1, 7]
- D. An exception

**Answer:** C. [2, 1, 7]

**Reasoning:** reverse() changes the list in place.

### 108. What is the result?

~~~python
values = [8, 1, 2]
print(sorted(values))
~~~

- A. None
- B. []
- C. An exception
- D. [1, 2, 8]

**Answer:** D. [1, 2, 8]

**Reasoning:** sorted() returns a sorted new list.

### 109. What is the result?

~~~python
values = [9, 1, 2]
values.reverse()
print(values)
~~~

- A. [2, 1, 9]
- B. None
- C. []
- D. An exception

**Answer:** A. [2, 1, 9]

**Reasoning:** reverse() changes the list in place.

### 110. What is the result?

~~~python
values = [10, 1, 2]
print(sorted(values))
~~~

- A. None
- B. [1, 2, 10]
- C. []
- D. An exception

**Answer:** B. [1, 2, 10]

**Reasoning:** sorted() returns a sorted new list.

### 111. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.count('apple'))
~~~

- A. None
- B. []
- C. 1
- D. An exception

**Answer:** C. 1

**Reasoning:** count() returns the number of matches.

### 112. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.index('banana'))
~~~

- A. None
- B. []
- C. An exception
- D. 1

**Answer:** D. 1

**Reasoning:** index() returns the matching position.

### 113. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.count('apple'))
~~~

- A. 1
- B. None
- C. []
- D. An exception

**Answer:** A. 1

**Reasoning:** count() returns the number of matches.

### 114. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.index('banana'))
~~~

- A. None
- B. 1
- C. []
- D. An exception

**Answer:** B. 1

**Reasoning:** index() returns the matching position.

### 115. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.count('apple'))
~~~

- A. None
- B. []
- C. 1
- D. An exception

**Answer:** C. 1

**Reasoning:** count() returns the number of matches.

### 116. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.index('banana'))
~~~

- A. None
- B. []
- C. An exception
- D. 1

**Answer:** D. 1

**Reasoning:** index() returns the matching position.

### 117. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.count('apple'))
~~~

- A. 1
- B. None
- C. []
- D. An exception

**Answer:** A. 1

**Reasoning:** count() returns the number of matches.

### 118. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.index('banana'))
~~~

- A. None
- B. 1
- C. []
- D. An exception

**Answer:** B. 1

**Reasoning:** index() returns the matching position.

### 119. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.count('apple'))
~~~

- A. None
- B. []
- C. 1
- D. An exception

**Answer:** C. 1

**Reasoning:** count() returns the number of matches.

### 120. What is the result?

~~~python
fruits = ['apple', 'banana', 'mango']
print(fruits.index('banana'))
~~~

- A. None
- B. []
- C. An exception
- D. 1

**Answer:** D. 1

**Reasoning:** index() returns the matching position.
