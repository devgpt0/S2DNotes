# Python List Worksheet Answers

Source Worksheet: `python/assignement/worksheets/collection_framwork/list.md`

## Level 1 Answers

### Tricky Predict the Output Solutions (50)

1.
```python
a = [10, 20, 30, 40, 50]
print(a[0], a[-1])
```

Correct Output:
```text
10 50
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

2.
```python
a = [10, 20, 30, 40, 50]
print(a[1:4])
```

Correct Output:
```text
[20, 30, 40]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

3.
```python
a = [10, 20, 30, 40, 50]
print(a[:3])
```

Correct Output:
```text
[10, 20, 30]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

4.
```python
a = [10, 20, 30, 40, 50]
print(a[2:])
```

Correct Output:
```text
[30, 40, 50]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

5.
```python
a = [10, 20, 30, 40, 50]
print(a[::-1])
```

Correct Output:
```text
[50, 40, 30, 20, 10]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

6.
```python
a = [10, 20, 30, 40, 50]
print(a[::2])
```

Correct Output:
```text
[10, 30, 50]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

7.
```python
a = [10, 20, 30, 40, 50]
print(a[1::2])
```

Correct Output:
```text
[20, 40]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

8.
```python
a = [10, 20, 30, 40, 50]
print(a[-3:])
```

Correct Output:
```text
[30, 40, 50]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

9.
```python
a = [10, 20, 30, 40, 50]
print(a[3:100])
```

Correct Output:
```text
[40, 50]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

10.
```python
a = ['a', 'b', 'c', 'd']
print(a[-4], a[-2])
```

Correct Output:
```text
a c
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

11.
```python
a = [1, 2, 3, 4, 5, 6]
print(a[5:1:-2])
```

Correct Output:
```text
[6, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

12.
```python
a = [1, 2, 3, 4, 5, 6]
print(a[-2::-2])
```

Correct Output:
```text
[5, 3, 1]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

13.
```python
a = [1, 2, 3, 4, 5]
print(a[:])
```

Correct Output:
```text
[1, 2, 3, 4, 5]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

14.
```python
a = [1, 2, 3, 4, 5]
print(a[:: -2])
```

Correct Output:
```text
[5, 3, 1]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

15.
```python
a = [1, 2, 3, 4, 5]
print(a[1:1])
```

Correct Output:
```text
[]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

16.
```python
a = ['apple', 'banana', 'cherry']
a[1] = 'blueberry'
print(a)
```

Correct Output:
```text
['apple', 'blueberry', 'cherry']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

17.
```python
a = ['apple', 'banana', 'cherry']
a[1:3] = ['pear', 'kiwi']
print(a)
```

Correct Output:
```text
['apple', 'pear', 'kiwi']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

18.
```python
a = [1, 2, 3]
a.append(4)
print(a)
```

Correct Output:
```text
[1, 2, 3, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

19.
```python
a = [1, 2]
a.append([3, 4])
print(a)
```

Correct Output:
```text
[1, 2, [3, 4]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

20.
```python
a = [1, 2]
a.extend([3, 4])
print(a)
```

Correct Output:
```text
[1, 2, 3, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

21.
```python
a = [1, 2, 3]
a.insert(1, 99)
print(a)
```

Correct Output:
```text
[1, 99, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

22.
```python
a = ['x', 'y', 'z']
a.remove('y')
print(a)
```

Correct Output:
```text
['x', 'z']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

23.
```python
a = ['x', 'y', 'z']
print(a.pop())
print(a)
```

Correct Output:
```text
z
['x', 'y']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

24.
```python
a = ['x', 'y', 'z']
print(a.pop(0))
print(a)
```

Correct Output:
```text
x
['y', 'z']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

25.
```python
a = [1, 2, 3, 4]
del a[1]
print(a)
```

Correct Output:
```text
[1, 3, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

26.
```python
a = [1, 2, 3, 4, 5]
del a[1:4]
print(a)
```

Correct Output:
```text
[1, 5]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

27.
```python
a = [1, 2, 3]
a.clear()
print(a)
```

Correct Output:
```text
[]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

28.
```python
a = [1, 2, 3]
print(a.count(2), a.index(3))
```

Correct Output:
```text
1 2
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

29.
```python
a = ['apple', 'banana', 'apple', 'orange']
print(a.index('apple', 1))
```

Correct Output:
```text
2
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

30.
```python
a = [1, 2, 3]
print(2 in a, 9 not in a)
```

Correct Output:
```text
True True
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

31.
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)
```

Correct Output:
```text
[1, 2, 3, 4] [1, 2, 3, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

32.
```python
a = [1, 2, 3]
b = a[:]
b[0] = 99
print(a, b)
```

Correct Output:
```text
[1, 2, 3] [99, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

33.
```python
a = [[1, 2], [3, 4]]
b = a[:]
b[0][0] = 99
print(a)
```

Correct Output:
```text
[[99, 2], [3, 4]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

34.
```python
import copy
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0][0] = 99
print(a)
print(b)
```

Correct Output:
```text
[[1, 2], [3, 4]]
[[99, 2], [3, 4]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

35.
```python
a = [1, 2, 3]
b = [4, 5]
print(a + b)
```

Correct Output:
```text
[1, 2, 3, 4, 5]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

36.
```python
a = [1, 2, 3]
print(a * 2)
```

Correct Output:
```text
[1, 2, 3, 1, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

37.
```python
a = [1, 2]
b = [3]
a += b
print(a)
```

Correct Output:
```text
[1, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

38.
```python
a = [1, 2]
b = [3]
a = a + b
print(a)
```

Correct Output:
```text
[1, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

39.
```python
a = [1, 2, 3]
print(len(a), min(a), max(a), sum(a))
```

Correct Output:
```text
3 1 3 6
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

40.
```python
names = ['Alice', 'Bob', 'Charlie']
print(min(names), max(names))
```

Correct Output:
```text
Alice Charlie
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

41.
```python
a = [3, 1, 2]
a.sort()
print(a)
```

Correct Output:
```text
[1, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

42.
```python
a = [3, 1, 2]
print(sorted(a))
print(a)
```

Correct Output:
```text
[1, 2, 3]
[3, 1, 2]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

43.
```python
a = [-10, 5, -3, 2, -1]
a.sort(key=abs)
print(a)
```

Correct Output:
```text
[-1, 2, -3, 5, -10]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

44.
```python
a = [-10, 5, -3, 2, -1]
a.sort(key=abs, reverse=True)
print(a)
```

Correct Output:
```text
[-10, 5, -3, 2, -1]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

45.
```python
a = [1, 2, 3]
a.reverse()
print(a)
```

Correct Output:
```text
[3, 2, 1]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

46.
```python
a = [1, 2, 3]
print(list(reversed(a)))
print(a)
```

Correct Output:
```text
[3, 2, 1]
[1, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

47.
```python
a = ['Alice', 'ALice', 'Charlie']
a.sort(key=str.lower, reverse=True)
print(a)
```

Correct Output:
```text
['Charlie', 'Alice', 'ALice']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

48.
```python
a = [10, 20, 30]
for x in a:
    print(x, end=' ')
print()
```

Correct Output:
```text
10 20 30 
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

49.
```python
a = ['x', 'y', 'z']
for i in range(len(a)):
    print(i, a[i])
```

Correct Output:
```text
0 x
1 y
2 z
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

50.
```python
a = ['x', 'y', 'z']
for i, v in enumerate(a):
    print(i, v)
```

Correct Output:
```text
0 x
1 y
2 z
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

### MCQ Theory Answer Key (50)

1. Lists in Python are:
Answer: **A**
Reason: `Ordered and mutable` is correct for this list concept based on Python behavior and the worksheet notes.

2. Best empty list syntax:
Answer: **A**
Reason: `[]` is correct for this list concept based on Python behavior and the worksheet notes.

3. `list("Ada")` produces:
Answer: **A**
Reason: `['A','d','a']` is correct for this list concept based on Python behavior and the worksheet notes.

4. `list(range(4))` gives:
Answer: **A**
Reason: `[0,1,2,3]` is correct for this list concept based on Python behavior and the worksheet notes.

5. Index `-1` means:
Answer: **A**
Reason: `last element` is correct for this list concept based on Python behavior and the worksheet notes.

6. Slicing upper bound in `a[1:4]` is:
Answer: **A**
Reason: `exclusive` is correct for this list concept based on Python behavior and the worksheet notes.

7. Out-of-range slicing typically:
Answer: **A**
Reason: `returns available slice` is correct for this list concept based on Python behavior and the worksheet notes.

8. Out-of-range direct indexing raises:
Answer: **A**
Reason: `IndexError` is correct for this list concept based on Python behavior and the worksheet notes.

9. `append(x)` does:
Answer: **A**
Reason: `adds one item at end` is correct for this list concept based on Python behavior and the worksheet notes.

10. `extend(iterable)` does:
Answer: **A**
Reason: `adds each iterable item` is correct for this list concept based on Python behavior and the worksheet notes.

11. `insert(i,x)` does:
Answer: **A**
Reason: `places x before index i` is correct for this list concept based on Python behavior and the worksheet notes.

12. `remove(x)` removes:
Answer: **A**
Reason: `first matching value` is correct for this list concept based on Python behavior and the worksheet notes.

13. `pop()` returns and removes:
Answer: **A**
Reason: `last element by default` is correct for this list concept based on Python behavior and the worksheet notes.

14. `del a[i]` is:
Answer: **A**
Reason: `statement-based deletion` is correct for this list concept based on Python behavior and the worksheet notes.

15. `clear()` on list:
Answer: **A**
Reason: `empties it in-place` is correct for this list concept based on Python behavior and the worksheet notes.

16. Aliasing `b=a` means:
Answer: **A**
Reason: `same object reference` is correct for this list concept based on Python behavior and the worksheet notes.

17. `a[:]` is commonly used as:
Answer: **A**
Reason: `shallow copy` is correct for this list concept based on Python behavior and the worksheet notes.

18. Nested list shallow copy risk:
Answer: **A**
Reason: `inner lists still shared` is correct for this list concept based on Python behavior and the worksheet notes.

19. Deep copy module is:
Answer: **A**
Reason: `copy` is correct for this list concept based on Python behavior and the worksheet notes.

20. `a + b` for lists:
Answer: **A**
Reason: `creates new concatenated list` is correct for this list concept based on Python behavior and the worksheet notes.

21. `a * 3` for list:
Answer: **A**
Reason: `repeats sequence` is correct for this list concept based on Python behavior and the worksheet notes.

22. Membership `x in list` is usually:
Answer: **A**
Reason: `O(n)` is correct for this list concept based on Python behavior and the worksheet notes.

23. `len([1,2,3,[4]])` equals:
Answer: **A**
Reason: `4` is correct for this list concept based on Python behavior and the worksheet notes.

24. `sorted(lst)` returns:
Answer: **A**
Reason: `new sorted list` is correct for this list concept based on Python behavior and the worksheet notes.

25. `lst.sort()` returns:
Answer: **A**
Reason: `None` is correct for this list concept based on Python behavior and the worksheet notes.

26. `reverse()` on list:
Answer: **A**
Reason: `in-place reverse` is correct for this list concept based on Python behavior and the worksheet notes.

27. `reversed(lst)` returns:
Answer: **A**
Reason: `iterator` is correct for this list concept based on Python behavior and the worksheet notes.

28. Case-insensitive sort key often:
Answer: **A**
Reason: `str.lower` is correct for this list concept based on Python behavior and the worksheet notes.

29. `index(x)` if missing:
Answer: **A**
Reason: `raises ValueError` is correct for this list concept based on Python behavior and the worksheet notes.

30. `count(x)` returns:
Answer: **A**
Reason: `occurrence frequency` is correct for this list concept based on Python behavior and the worksheet notes.

31. `list()` requires input to be:
Answer: **A**
Reason: `iterable` is correct for this list concept based on Python behavior and the worksheet notes.

32. `list(123)` causes:
Answer: **A**
Reason: `TypeError` is correct for this list concept based on Python behavior and the worksheet notes.

33. `[[0]*3]*3` pitfall:
Answer: **A**
Reason: `shared inner references` is correct for this list concept based on Python behavior and the worksheet notes.

34. Safe matrix creation:
Answer: **A**
Reason: `[[0 for _ in range(3)] for _ in range(3)]` is correct for this list concept based on Python behavior and the worksheet notes.

35. `sum([1,2,3])` gives:
Answer: **A**
Reason: `6` is correct for this list concept based on Python behavior and the worksheet notes.

36. `max(["Alice","Bob"])` uses:
Answer: **A**
Reason: `lexicographic comparison` is correct for this list concept based on Python behavior and the worksheet notes.

37. `ord("A")` returns:
Answer: **A**
Reason: `ASCII/Unicode code point integer` is correct for this list concept based on Python behavior and the worksheet notes.

38. `append([1,2])` vs `extend([1,2])`:
Answer: **A**
Reason: `nested vs flattened add` is correct for this list concept based on Python behavior and the worksheet notes.

39. `del a[1:3]` does:
Answer: **A**
Reason: `delete slice range` is correct for this list concept based on Python behavior and the worksheet notes.

40. `a[:: -1]` and `a[::-1]`:
Answer: **A**
Reason: `both reverse via slicing` is correct for this list concept based on Python behavior and the worksheet notes.

41. `for x in lst` yields:
Answer: **A**
Reason: `elements` is correct for this list concept based on Python behavior and the worksheet notes.

42. `for i in range(len(lst))` yields:
Answer: **A**
Reason: `indices` is correct for this list concept based on Python behavior and the worksheet notes.

43. `enumerate(lst)` yields:
Answer: **A**
Reason: `index-value pairs` is correct for this list concept based on Python behavior and the worksheet notes.

44. Lists can store:
Answer: **A**
Reason: `mixed datatypes` is correct for this list concept based on Python behavior and the worksheet notes.

45. List is best described as:
Answer: **A**
Reason: `dynamic array-like sequence` is correct for this list concept based on Python behavior and the worksheet notes.

46. `a[1:1]` result is usually:
Answer: **A**
Reason: `empty list` is correct for this list concept based on Python behavior and the worksheet notes.

47. `a[1:100]` with short list:
Answer: **A**
Reason: `no error slicing` is correct for this list concept based on Python behavior and the worksheet notes.

48. `copy.deepcopy` is needed when:
Answer: **A**
Reason: `nested mutable structures must be independent` is correct for this list concept based on Python behavior and the worksheet notes.

49. Interview best practice for list pitfalls:
Answer: **A**
Reason: `test aliasing and edge indices explicitly` is correct for this list concept based on Python behavior and the worksheet notes.

50. Which operation is safest when original list must remain unchanged while sorting?
Answer: **B**
Reason: `sorted(lst)` is correct for this list concept based on Python behavior and the worksheet notes.

## Level 2 Answers

### Tricky Predict the Output Solutions (50)

1.
```python
a = [1, 2, 3, 4]
print([x*x for x in a])
```

Correct Output:
```text
[1, 4, 9, 16]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

2.
```python
a = [1, 2, 3, 4]
print([x for x in a if x % 2 == 0])
```

Correct Output:
```text
[2, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

3.
```python
a = [1, 2, 3, 4]
print(["even" if x % 2 == 0 else "odd" for x in a])
```

Correct Output:
```text
['odd', 'even', 'odd', 'even']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

4.
```python
a = [1, 2, 3, 4]
print([x*10 for x in a if x > 2])
```

Correct Output:
```text
[30, 40]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

5.
```python
a = [1, 2, 3]
print(list(map(lambda x: x + 5, a)))
```

Correct Output:
```text
[6, 7, 8]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

6.
```python
a = [1, 2, 3, 4, 5]
print(list(filter(lambda x: x % 2, a)))
```

Correct Output:
```text
[1, 3, 5]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

7.
```python
a = [1, 2, 3, 4]
print(any(x > 3 for x in a), all(x > 0 for x in a))
```

Correct Output:
```text
True True
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

8.
```python
a = [0, 0, 1]
print(any(a), all(a))
```

Correct Output:
```text
True False
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

9.
```python
a = [1, 2, 3]
print(sum(x*x for x in a))
```

Correct Output:
```text
14
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

10.
```python
a = ['apple', 'banana', 'mango']
print(next((x for x in a if x.startswith('m')), None))
```

Correct Output:
```text
mango
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

11.
```python
a = ['apple', 'banana', 'mango']
print(next((x for x in a if x.startswith('z')), 'NA'))
```

Correct Output:
```text
NA
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

12.
```python
a = [1, 2, 3, 4, 5]
print([i for i, x in enumerate(a) if x % 2 == 1])
```

Correct Output:
```text
[0, 2, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

13.
```python
a = [1, 2, 3]
print([*a, 4, 5])
```

Correct Output:
```text
[1, 2, 3, 4, 5]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

14.
```python
a = [1, 2]
b = [3, 4]
print([*a, *b])
```

Correct Output:
```text
[1, 2, 3, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

15.
```python
a = [1, 2, 3]
first, *mid, last = a
print(first, mid, last)
```

Correct Output:
```text
1 [2] 3
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

16.
```python
a = [1, 2, 3, 4]
*head, tail = a
print(head, tail)
```

Correct Output:
```text
[1, 2, 3] 4
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

17.
```python
a = ['1', '2', '3']
print(list(map(int, a)))
```

Correct Output:
```text
[1, 2, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

18.
```python
a = [1, 2, 3]
print(list(map(str, a)))
```

Correct Output:
```text
['1', '2', '3']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

19.
```python
a = [1, 2, 3, 4]
print([x for x in a if not x % 2])
```

Correct Output:
```text
[2, 4]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

20.
```python
a = [1, 2, 3, 4]
print([x for x in a if x % 2])
```

Correct Output:
```text
[1, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

21.
```python
m = [[1, 2], [3, 4], [5, 6]]
print([x for row in m for x in row])
```

Correct Output:
```text
[1, 2, 3, 4, 5, 6]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

22.
```python
m = [[1, 2], [3, 4], [5, 6]]
print([row[0] for row in m])
```

Correct Output:
```text
[1, 3, 5]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

23.
```python
m = [[1, 2, 3], [4, 5, 6]]
print([sum(row) for row in m])
```

Correct Output:
```text
[6, 15]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

24.
```python
m = [[1, 2, 3], [4, 5, 6]]
print([m[r][c] for c in range(3) for r in range(2)])
```

Correct Output:
```text
[1, 4, 2, 5, 3, 6]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

25.
```python
grid = [[0 for _ in range(2)] for _ in range(2)]
grid[0][0] = 1
print(grid)
```

Correct Output:
```text
[[1, 0], [0, 0]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

26.
```python
bad = [[0] * 2] * 2
bad[0][0] = 1
print(bad)
```

Correct Output:
```text
[[1, 0], [1, 0]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

27.
```python
a = [[1], [2]]
b = a.copy()
b.append([3])
print(a, b)
```

Correct Output:
```text
[[1], [2]] [[1], [2], [3]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

28.
```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
print(a, b)
```

Correct Output:
```text
[[1, 9], [2]] [[1, 9], [2]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

29.
```python
import copy
a = [[1], [2]]
b = copy.deepcopy(a)
b[0].append(9)
print(a, b)
```

Correct Output:
```text
[[1], [2]] [[1, 9], [2]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

30.
```python
m = [[1, 2], [3, 4]]
print(list(zip(*m)))
```

Correct Output:
```text
[(1, 3), (2, 4)]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

31.
```python
m = [[1, 2], [3, 4]]
print([list(col) for col in zip(*m)])
```

Correct Output:
```text
[[1, 3], [2, 4]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

32.
```python
rows = [[1, 2], [3, 4]]
rows[1][1] = 99
print(rows)
```

Correct Output:
```text
[[1, 2], [3, 99]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

33.
```python
a = [1, 2, [3, 4]]
print(len(a), len(a[2]))
```

Correct Output:
```text
3 2
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

34.
```python
a = [[1,2],[3,4],[5,6]]
print(a[2][1], a[-1][-2])
```

Correct Output:
```text
6 5
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

35.
```python
a = [[1,2],[3,4],[5,6]]
print(a[-2:])
```

Correct Output:
```text
[[3, 4], [5, 6]]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

36.
```python
a = ['banana', 'an', 'cherry']
print(sorted(a, key=len))
```

Correct Output:
```text
['an', 'banana', 'cherry']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

37.
```python
a = ['banana', 'an', 'cherry']
print(sorted(a, key=len, reverse=True))
```

Correct Output:
```text
['banana', 'cherry', 'an']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

38.
```python
a = ['Alice', 'alice', 'Bob']
a.sort(key=str.lower)
print(a)
```

Correct Output:
```text
['Alice', 'alice', 'Bob']
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

39.
```python
a = [(1, 'b'), (1, 'a'), (2, 'c')]
print(sorted(a))
```

Correct Output:
```text
[(1, 'a'), (1, 'b'), (2, 'c')]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

40.
```python
a = [(1, 'b'), (1, 'a'), (2, 'c')]
print(sorted(a, key=lambda x: (x[0], x[1])))
```

Correct Output:
```text
[(1, 'a'), (1, 'b'), (2, 'c')]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

41.
```python
a = [3, 1, 2]
a.sort()
print(a is None)
```

Correct Output:
```text
False
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

42.
```python
a = [3, 1, 2]
print(sorted(a))
print(a)
```

Correct Output:
```text
[1, 2, 3]
[3, 1, 2]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

43.
```python
a = [1, 2, 3]
b = [10, 20]
print(list(zip(a, b)))
```

Correct Output:
```text
[(1, 10), (2, 20)]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

44.
```python
from itertools import zip_longest
a = [1, 2, 3]
b = [10, 20]
print(list(zip_longest(a, b, fillvalue=0)))
```

Correct Output:
```text
[(1, 10), (2, 20), (3, 0)]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

45.
```python
a = ['x', 'y', 'z']
print(list(enumerate(a, start=1)))
```

Correct Output:
```text
[(1, 'x'), (2, 'y'), (3, 'z')]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

46.
```python
a = ['a', 'b', 'c']
print('-'.join(a))
```

Correct Output:
```text
a-b-c
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

47.
```python
a = [1, 2, 3]
print(a.__contains__(2), a.__contains__(9))
```

Correct Output:
```text
True False
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

48.
```python
a = []
try:
    a.pop()
except Exception as e:
    print(type(e).__name__)
```

Correct Output:
```text
IndexError
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

49.
```python
a = [1, 2, 3]
try:
    a.remove(9)
except Exception as e:
    print(type(e).__name__)
```

Correct Output:
```text
ValueError
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

50.
```python
a = [1, 2, 3]
print(a[slice(0, 3, 2)])
```

Correct Output:
```text
[1, 3]
```
Reason: Python executes each list operation in order; the printed result reflects the final state (or computed value) after those operations.

### MCQ Theory Answer Key (50)

1. List comprehension primarily creates:
Answer: **A**
Reason: `new list` is correct for this list concept based on Python behavior and the worksheet notes.

2. Generator expression syntax:
Answer: **A**
Reason: `(x for x in data)` is correct for this list concept based on Python behavior and the worksheet notes.

3. Comprehension with `if` performs:
Answer: **A**
Reason: `filtering` is correct for this list concept based on Python behavior and the worksheet notes.

4. Comprehension expression part performs:
Answer: **A**
Reason: `mapping/transformation` is correct for this list concept based on Python behavior and the worksheet notes.

5. Nested comprehension flatten order typically:
Answer: **A**
Reason: `for row in m for x in row` is correct for this list concept based on Python behavior and the worksheet notes.

6. `map` in Python 3 returns:
Answer: **A**
Reason: `iterator` is correct for this list concept based on Python behavior and the worksheet notes.

7. `filter` in Python 3 returns:
Answer: **A**
Reason: `iterator` is correct for this list concept based on Python behavior and the worksheet notes.

8. `list(map(...))` is used to:
Answer: **A**
Reason: `materialize iterator` is correct for this list concept based on Python behavior and the worksheet notes.

9. `any()` returns True if:
Answer: **A**
Reason: `at least one truthy item` is correct for this list concept based on Python behavior and the worksheet notes.

10. `all()` returns True if:
Answer: **A**
Reason: `all items truthy` is correct for this list concept based on Python behavior and the worksheet notes.

11. `enumerate(lst)` yields:
Answer: **A**
Reason: `index-value pairs` is correct for this list concept based on Python behavior and the worksheet notes.

12. `enumerate(lst, start=1)` changes:
Answer: **A**
Reason: `first index value` is correct for this list concept based on Python behavior and the worksheet notes.

13. `zip(a,b)` stops at:
Answer: **A**
Reason: `shortest input` is correct for this list concept based on Python behavior and the worksheet notes.

14. `zip_longest` from itertools allows:
Answer: **A**
Reason: `padding unequal lengths` is correct for this list concept based on Python behavior and the worksheet notes.

15. `*` unpack in list literal `[ *a, *b ]` means:
Answer: **A**
Reason: `merge iterables into new list` is correct for this list concept based on Python behavior and the worksheet notes.

16. Star unpack assignment `first,*mid,last` gives:
Answer: **A**
Reason: `middle as list` is correct for this list concept based on Python behavior and the worksheet notes.

17. `sorted(iterable)` accepts:
Answer: **A**
Reason: `any iterable` is correct for this list concept based on Python behavior and the worksheet notes.

18. `key=` in sort should return:
Answer: **A**
Reason: `comparison key per item` is correct for this list concept based on Python behavior and the worksheet notes.

19. `reverse=True` with sort means:
Answer: **A**
Reason: `descending by key` is correct for this list concept based on Python behavior and the worksheet notes.

20. Sort stability means:
Answer: **A**
Reason: `equal keys keep relative order` is correct for this list concept based on Python behavior and the worksheet notes.

21. `lambda x: x[1]` in sorting tuples means:
Answer: **A**
Reason: `sort by second item` is correct for this list concept based on Python behavior and the worksheet notes.

22. `str.lower` as sort key enables:
Answer: **A**
Reason: `case-insensitive ordering` is correct for this list concept based on Python behavior and the worksheet notes.

23. `a.copy()` on nested list is:
Answer: **A**
Reason: `shallow copy` is correct for this list concept based on Python behavior and the worksheet notes.

24. `copy.deepcopy(a)` ensures:
Answer: **A**
Reason: `independent nested objects` is correct for this list concept based on Python behavior and the worksheet notes.

25. `is` checks:
Answer: **A**
Reason: `object identity` is correct for this list concept based on Python behavior and the worksheet notes.

26. `==` for lists checks:
Answer: **A**
Reason: `element-wise equality` is correct for this list concept based on Python behavior and the worksheet notes.

27. `a += [x]` for list typically:
Answer: **A**
Reason: `mutates existing list` is correct for this list concept based on Python behavior and the worksheet notes.

28. `a = a + [x]` typically:
Answer: **A**
Reason: `creates new list object` is correct for this list concept based on Python behavior and the worksheet notes.

29. `del a[:]` effect:
Answer: **A**
Reason: `clear contents in-place` is correct for this list concept based on Python behavior and the worksheet notes.

30. `slice(1,5,2)` can be applied as:
Answer: **A**
Reason: `a[slice(1,5,2)]` is correct for this list concept based on Python behavior and the worksheet notes.

31. `list(dict.fromkeys(lst))` is useful for:
Answer: **A**
Reason: `order-preserving dedupe` is correct for this list concept based on Python behavior and the worksheet notes.

32. `list(set(lst))` may change:
Answer: **A**
Reason: `element order` is correct for this list concept based on Python behavior and the worksheet notes.

33. Membership-heavy workflow usually better with:
Answer: **A**
Reason: `set for lookups` is correct for this list concept based on Python behavior and the worksheet notes.

34. `reversed(lst)` memory profile is:
Answer: **A**
Reason: `lazy iterator` is correct for this list concept based on Python behavior and the worksheet notes.

35. `.reverse()` return value is:
Answer: **A**
Reason: `None` is correct for this list concept based on Python behavior and the worksheet notes.

36. Complexity of `insert(0, x)` in list:
Answer: **A**
Reason: `O(n)` is correct for this list concept based on Python behavior and the worksheet notes.

37. Complexity of `append(x)` in list:
Answer: **A**
Reason: `amortized O(1)` is correct for this list concept based on Python behavior and the worksheet notes.

38. Complexity of `pop()` from end:
Answer: **A**
Reason: `O(1)` is correct for this list concept based on Python behavior and the worksheet notes.

39. Complexity of `pop(0)` typically:
Answer: **A**
Reason: `O(n)` is correct for this list concept based on Python behavior and the worksheet notes.

40. Complexity of `x in list`:
Answer: **A**
Reason: `O(n)` is correct for this list concept based on Python behavior and the worksheet notes.

41. `join` on list requires elements of type:
Answer: **A**
Reason: `str` is correct for this list concept based on Python behavior and the worksheet notes.

42. `print(*lst)` does:
Answer: **A**
Reason: `argument unpacking` is correct for this list concept based on Python behavior and the worksheet notes.

43. `sum(x*x for x in nums)` uses:
Answer: **A**
Reason: `generator expression` is correct for this list concept based on Python behavior and the worksheet notes.

44. `next((x for x in lst if cond), default)` is commonly used for:
Answer: **A**
Reason: `first match with fallback` is correct for this list concept based on Python behavior and the worksheet notes.

45. `zip(*matrix)` pattern is used for:
Answer: **A**
Reason: `transpose-like operation` is correct for this list concept based on Python behavior and the worksheet notes.

46. `[[0]*m]*n` bug cause:
Answer: **A**
Reason: `shared inner references` is correct for this list concept based on Python behavior and the worksheet notes.

47. For readable simple transformations, prefer:
Answer: **A**
Reason: `comprehensions` is correct for this list concept based on Python behavior and the worksheet notes.

48. When list methods return None, reason is often:
Answer: **A**
Reason: `in-place mutation design` is correct for this list concept based on Python behavior and the worksheet notes.

49. Best interview practice for list problems:
Answer: **A**
Reason: `handle edge cases: empty, one-item, duplicates, nested refs` is correct for this list concept based on Python behavior and the worksheet notes.

50. For multi-key custom sorting readability, best pattern is:
Answer: **B**
Reason: `sorted(data, key=lambda x: (key1, key2))` is correct for this list concept based on Python behavior and the worksheet notes.

## Interview Theory Answers (Top 25)

1. Difference between list and tuple in Python?
Answer: Lists are mutable and use square brackets, while tuples are immutable and use parentheses. Lists are preferred when updates are needed.

2. Why are lists mutable and what practical impact does that have?
Answer: Mutability means in-place updates affect the same object reference. If two variables alias one list, a change through one appears in the other.

3. Explain append vs extend with example.
Answer: append adds one object at the end; extend iterates another iterable and adds each element individually.

4. When should you use remove vs pop vs del?
Answer: Use remove for first matching value, pop for index-based removal with returned element, and del for statement-based deletion of index/slice/name.

5. Why does list.sort() return None?
Answer: sort mutates in-place for performance and API clarity, so it returns None to avoid confusion with creating a new list.

6. Difference between sorted(lst) and lst.sort().
Answer: sorted returns a new sorted list; list.sort mutates the existing list in-place.

7. How does slicing work with start:end:step?
Answer: start is inclusive, end is exclusive, and step controls stride/direction. Negative step means reverse-direction slicing.

8. Why slicing out-of-range does not throw IndexError?
Answer: Slicing is bounds-tolerant; Python clips slice boundaries safely instead of raising IndexError.

9. Explain negative indexing with examples.
Answer: Negative indices count from the end: -1 last, -2 second last, etc.

10. What is aliasing in Python lists?
Answer: Aliasing means two references point to the same list object (`b = a`). Mutating one mutates the shared object.

11. Difference between shallow copy and deep copy.
Answer: Shallow copy copies outer container only; nested mutable children remain shared. Deep copy recursively clones nested objects.

12. Why does [[0]*m]*n cause bugs in nested lists?
Answer: `[[0]*m]*n` repeats references to the same inner row, so editing one row cell updates all rows at that column.

13. How to safely create a matrix/list of lists?
Answer: Use comprehension: `[[0 for _ in range(m)] for _ in range(n)]` so each row is an independent list.

14. Complexities of append, pop, insert, remove, in-membership.
Answer: append amortized O(1), pop() O(1), insert/remove/pop(i)/membership O(n), index access O(1), sort O(n log n).

15. Why is membership check in list O(n)?
Answer: List membership is linear because it scans elements sequentially until match/end.

16. How does key-based sorting work?
Answer: The key function maps each item to a comparable key used for ordering, e.g., `sorted(data, key=len)`.

17. What does sort stability mean and why is it useful?
Answer: Stable sort preserves relative order of equal-key elements, enabling reliable multi-pass and tie-break workflows.

18. How do you perform multi-key sorting in Python?
Answer: Use tuple key: `sorted(data, key=lambda x: (x.k1, x.k2))`, optionally with sign transforms or reverse flags.

19. When to use list comprehension vs map/filter?
Answer: Use comprehensions for readable simple transformations/filters; use map/filter when reusing callable pipelines or iterator workflows.

20. How does enumerate improve readability?
Answer: enumerate provides index+value cleanly and avoids manual counters/off-by-one errors.

21. How does zip work with unequal length iterables?
Answer: zip pairs iterables until shortest ends; use itertools.zip_longest when you must retain longest with fill values.

22. How to remove duplicates while preserving order?
Answer: Use `list(dict.fromkeys(lst))` for order-preserving dedupe in modern Python.

23. Common exceptions in list operations and when they happen.
Answer: Common ones: IndexError (bad index/pop empty), ValueError (remove/index value not found), TypeError (non-iterable to list or mixed invalid ops).

24. How to avoid mutability bugs in function arguments?
Answer: Never use mutable defaults (`def f(x=[])`). Use `None` then create list inside function.

25. Best interview-safe checklist for list problems before final submission?
Answer: Check edge cases (empty/1 item/duplicates/nested refs), confirm complexity, avoid aliasing bugs, and validate outputs with small tests.
