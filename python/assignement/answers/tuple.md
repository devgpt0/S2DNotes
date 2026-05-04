# Python Tuple Worksheet Answers

Source Worksheet: `python/assignement/worksheets/collection_framwork/tuple.md`

## Level 1 Answers

### Tricky Predict the Output Solutions (50)

1. Answer:
```text
10 50
```
Reason: Index `0` is first element; `-1` is last element.

2. Answer:
```text
(20, 30, 40)
```
Reason: Slice end is exclusive, so indices `1..3` are returned.

3. Answer:
```text
(10, 20, 30)
```
Reason: `t[:3]` takes from start to index `2`.

4. Answer:
```text
(30, 40, 50)
```
Reason: `t[2:]` takes from index `2` to end.

5. Answer:
```text
(50, 40, 30, 20, 10)
```
Reason: Step `-1` reverses the tuple.

6. Answer:
```text
(10, 30, 50)
```
Reason: Step `2` picks every second item starting at index `0`.

7. Answer:
```text
(20, 40)
```
Reason: Start at index `1`, then step by `2`.

8. Answer:
```text
(30, 40, 50)
```
Reason: `-3:` means last 3 elements.

9. Answer:
```text
(40, 50)
```
Reason: Out-of-range slice end is safely clipped.

10. Answer:
```text
a c
```
Reason: `-4` is first element and `-2` is third element.

11. Answer:
```text
(6, 4)
```
Reason: Reverse slice from index `5` down to `>1` stepping `-2`.

12. Answer:
```text
(5, 3, 1)
```
Reason: Start at second-last element and move backward by `2`.

13. Answer:
```text
(1, 2, 3, 4, 5)
```
Reason: Full slice returns the full tuple value.

14. Answer:
```text
(5, 3, 1)
```
Reason: Full reverse with step `-2`.

15. Answer:
```text
()
```
Reason: Start and end are same (`1:1`), so empty slice.

16. Answer:
```text
<class 'tuple'> (1, 2, 3)
```
Reason: Comma-separated values create a tuple (packing).

17. Answer:
```text
int tuple
```
Reason: `(5)` is `int`; `(5,)` is a one-element tuple.

18. Answer:
```text
15
```
Reason: Unpacked values `4+5+6`.

19. Answer:
```text
1 [2, 3, 4] 5
```
Reason: Starred target collects middle values into a list.

20. Answer:
```text
[1, 2, 3] 4
```
Reason: `*head` captures all except final element.

21. Answer:
```text
20 10
```
Reason: Tuple packing/unpacking swaps values.

22. Answer:
```text
10 20
```
Reason: Function returns a tuple-like multiple return value.

23. Answer:
```text
1
(2, 3)
{'x': 4}
```
Reason: First arg binds `a`; extras go to `args` tuple and `kwargs` dict.

24. Answer:
```text
6
```
Reason: `*(1,2,3)` unpacks into `a,b,c`.

25. Answer:
```text
(1, 2, 3, 4)
```
Reason: `+` concatenates tuples into a new tuple.

26. Answer:
```text
(1, 2, 1, 2, 1, 2)
```
Reason: `*3` repeats tuple contents.

27. Answer:
```text
True True
```
Reason: `'2'` exists; `9` does not exist.

28. Answer:
```text
3 3
```
Reason: `2` appears 3 times; `3` first appears at index `3`.

29. Answer:
```text
4 1 9 16
```
Reason: Basic built-ins on numeric tuple.

30. Answer:
```text
Alice Charlie
```
Reason: Lexicographic min/max on strings.

31. Answer:
```text
([99, 2], [3, 4])
```
Reason: Tuple is immutable, but nested list elements are mutable.

32. Answer:
```text
3 7 
```
Reason: Prints sums `1+2` and `3+4` with trailing space.

33. Answer:
```text
Y 7
```
Reason: First pattern `(0, y)` matches.

34. Answer:
```text
X 3
```
Reason: Second pattern `(x, 0)` matches.

35. Answer:
```text
G 2 5
```
Reason: Falls to general `(x, y)` case.

36. Answer:
```text
(1, [2, 3, 9])
(1, [2, 3, 9])
(1, [2, 3])
```
Reason: Assignment and shallow copy share nested list; deep copy does not.

37. Answer:
```text
True
```
Reason: `copy.copy` may return same object for immutable tuples.

38. Answer:
```text
True
```
Reason: Full slicing on immutable tuple may preserve identity.

39. Answer:
```text
pt
```
Reason: Tuple key lookup succeeds.

40. Answer:
```text
True
```
Reason: `hash((1,2,3))` returns an integer, not `None`.

41. Answer:
```text
(1, 2, 3)
```
Reason: `tuple(list_obj)` converts iterable to tuple.

42. Answer:
```text
('a', 'b', 'c')
```
Reason: Strings are iterable by character.

43. Answer:
```text
[1, 2, 3] list
```
Reason: `sorted()` always returns a new list.

44. Answer:
```text
(3, 2, 1)
```
Reason: `reversed()` iterator converted back to tuple.

45. Answer:
```text
(1, 3)
```
Reason: `slice(0,4,2)` selects indices `0` and `2`.

46. Answer:
```text
1 2 3
```
Reason: Nested unpacking splits inner tuple.

47. Answer:
```text
255 0 0
```
Reason: Tuple unpacking into `r, g, b`.

48. Answer:
```text
(1, 2, 3) (1, 2)
```
Reason: `a + (3,)` creates a new tuple; `b` still references old one.

49. Answer:
```text
0 1 | 1 2 | 2 3 | 
```
Reason: `enumerate` yields index-value pairs.

50. Answer:
```text
tuple list
```
Reason: `a` is tuple, `b` is list.

### MCQ Theory Answer Key (50)

1. Answer: **A**
Reason: Tuple is ordered and immutable.

2. Answer: **A**
Reason: `()` is empty tuple literal.

3. Answer: **A**
Reason: Single-element tuple needs trailing comma.

4. Answer: **A**
Reason: `tuple("Ada")` iterates characters.

5. Answer: **A**
Reason: `-1` refers to last element.

6. Answer: **A**
Reason: Slice upper bound is exclusive.

7. Answer: **A**
Reason: Slicing clips bounds safely.

8. Answer: **A**
Reason: Bad direct index raises `IndexError`.

9. Answer: **A**
Reason: Tuple does not allow item assignment.

10. Answer: **A**
Reason: No mutation methods like append/remove exist.

11. Answer: **A**
Reason: Tuple methods are `count` and `index`.

12. Answer: **A**
Reason: Missing value in `index` raises `ValueError`.

13. Answer: **A**
Reason: Concatenation returns a new tuple.

14. Answer: **A**
Reason: Multiplication repeats sequence.

15. Answer: **A**
Reason: Unpacking count mismatch raises `ValueError`.

16. Answer: **A**
Reason: Starred target receives a list.

17. Answer: **A**
Reason: `*args` is a tuple.

18. Answer: **A**
Reason: `**kwargs` is a dict.

19. Answer: **A**
Reason: `*t` unpacks positional arguments.

20. Answer: **A**
Reason: Tuple key requires all elements hashable.

21. Answer: **A**
Reason: List inside tuple is unhashable.

22. Answer: **A**
Reason: Tuple slicing may return same object.

23. Answer: **A**
Reason: Nested mutable members can mutate.

24. Answer: **A**
Reason: `deepcopy` recursively copies nested objects.

25. Answer: **A**
Reason: `sorted` returns list.

26. Answer: **A**
Reason: `reversed` returns iterator.

27. Answer: **A**
Reason: Tuples are typically more memory-efficient.

28. Answer: **A**
Reason: Tuples are ideal for fixed records.

29. Answer: **A**
Reason: `tuple()` converts iterables.

30. Answer: **A**
Reason: String iterates into chars.

31. Answer: **A**
Reason: Swap uses packing/unpacking.

32. Answer: **A**
Reason: Each element must unpack into two values.

33. Answer: **A**
Reason: `(0, y)` fixes first value as zero.

34. Answer: **A**
Reason: Negative step reverses direction.

35. Answer: **A**
Reason: Outer tuple length is 4.

36. Answer: **A**
Reason: String comparison is lexicographic.

37. Answer: **A**
Reason: Commas create tuple literals.

38. Answer: **A**
Reason: Immutable tuple copy can reuse object.

39. Answer: **A**
Reason: Numeric sum of tuple values.

40. Answer: **A**
Reason: `append` does not exist for tuple.

41. Answer: **A**
Reason: Tuple is a sequence type.

42. Answer: **A**
Reason: Unpacking mismatch is `ValueError`.

43. Answer: **A**
Reason: One starred target is valid.

44. Answer: **A**
Reason: `+=` on tuple rebinds to new object.

45. Answer: **A**
Reason: Tuple keys suit coordinate pairs.

46. Answer: **A**
Reason: "tuple methods are many" is false.

47. Answer: **A**
Reason: `print(*t)` uses argument unpacking.

48. Answer: **A**
Reason: Tuple may hold mixed data types.

49. Answer: **A**
Reason: Immutability is container-level.

50. Answer: **A**
Reason: Lists are better for frequent updates.

## Level 2 Answers

### Tricky Questions Solutions (50)

1. Answer:
```python
t = 10, 20, 30
```
Reason: Commas perform tuple packing.

2. Answer:
```python
empty = ()
print(type(empty))
```
Reason: Empty tuple literal is `()`.

3. Answer:
```python
one = (42,)
```
Reason: Trailing comma is required.

4. Answer:
```python
t = tuple([1, 2, 3])
```
Reason: `tuple()` converts iterables.

5. Answer:
```python
t = tuple("python")
```
Reason: String is iterable by character.

6. Answer:
```python
a, b, c = (10, 20, 30)
```
Reason: Standard unpacking by position.

7. Answer:
```python
first, *middle, last = (1, 2, 3, 4, 5)
```
Reason: Star target captures remaining values.

8. Answer:
```python
x, y = y, x
```
Reason: Pack right, unpack left.

9. Answer:
```python
def point():
    return 3, 7
```
Reason: Multiple return values are tuple-packed.

10. Answer:
```python
t = (1, 2, 3)
f(*t)
```
Reason: `*` expands tuple into positional args.

11. Answer:
```python
def show(*args):
    print(args)
```
Reason: `*args` is tuple capture.

12. Answer:
```python
def show(**kwargs):
    print(kwargs)
```
Reason: `**kwargs` captures keyword args dict.

13. Answer:
```python
part = t[1:4]
```
Reason: End index excluded.

14. Answer:
```python
rev = t[::-1]
```
Reason: Negative step reverses.

15. Answer:
```python
ev = t[::2]
```
Reason: Step selects alternate elements.

16. Answer:
```python
u = (1, 2) + (3, 4)
```
Reason: `+` concatenates tuples.

17. Answer:
```python
u = (1, 2) * 5
```
Reason: `*` repeats sequence.

18. Answer:
```python
print("a" in t)
```
Reason: Membership test works for tuples.

19. Answer:
```python
print(t.count(2))
```
Reason: `count` returns frequency.

20. Answer:
```python
print(t.index("x"))
```
Reason: `index` returns first occurrence position.

21. Answer:
```python
print(len(t), min(t), max(t), sum(t))
```
Reason: Built-ins operate on numeric tuples.

22. Answer:
```python
t = (1, 2, 3)
t[0] = 9
```
Reason: Raises `TypeError`, proving immutability.

23. Answer:
```python
t = ([1, 2],)
t[0].append(3)
print(t)
```
Reason: Inner list is mutable.

24. Answer:
```python
d = {(2, 3): "P"}
```
Reason: Hashable tuple keys are valid.

25. Answer:
```python
try:
    hash(([1, 2], 3))
    print(True)
except TypeError:
    print(False)
```
Reason: List inside tuple makes it unhashable.

26. Answer:
```python
pairs = [(1, 'a'), (2, 'b')]
for x, y in pairs:
    print(x, y)
```
Reason: Loop unpacking splits each pair.

27. Answer:
```python
match point:
    case (0, y):
        print("Y-axis", y)
```
Reason: Pattern matches first element fixed to `0`.

28. Answer:
```python
match point:
    case (x, 0):
        print("X-axis", x)
```
Reason: Pattern matches second element fixed to `0`.

29. Answer:
```python
match point:
    case (0, y):
        print("Y-axis", y)
    case (x, 0):
        print("X-axis", x)
    case (x, y):
        print("General", x, y)
```
Reason: Covers special and default tuple-shape cases.

30. Answer:
```python
t1 = (1, [2, 3])
t2 = t1
t1[1].append(9)
print(t2)
```
Reason: Assignment aliases same nested object.

31. Answer:
```python
import copy
t1 = (1, [2, 3])
t2 = copy.copy(t1)
t1[1].append(9)
print(t2)
```
Reason: Shallow copy shares nested mutable values.

32. Answer:
```python
import copy
t1 = (1, [2, 3])
t2 = copy.deepcopy(t1)
t1[1].append(9)
print(t2)
```
Reason: Deep copy creates independent nested objects.

33. Answer:
```python
import copy
t = (1, 2, 3)
print(copy.copy(t) is t)
```
Reason: Immutable tuple may be reused.

34. Answer:
```python
t = (1, 2, 3)
print(t[:] is t)
```
Reason: Full tuple slice may preserve identity.

35. Answer:
```python
import sys
t = (1, 2, 3, 4)
l = [1, 2, 3, 4]
print(sys.getsizeof(t), sys.getsizeof(l))
```
Reason: Demonstrates container memory difference.

36. Answer:
```python
import timeit
print(timeit.timeit('for x in t: pass', setup='t=(1,2,3,4,5)', number=1_000_000))
print(timeit.timeit('for x in l: pass', setup='l=[1,2,3,4,5]', number=1_000_000))
```
Reason: Measures iteration overhead quickly.

37. Answer:
```python
point = (x, y)  # e.g., dict key for coordinates
```
Reason: Tuple fits fixed, hashable record usage.

38. Answer:
```python
queue = [1, 2, 3]
queue.append(4)
```
Reason: List is better for frequent mutations.

39. Answer:
```python
t = (1, (2, 3))
a, (b, c) = t
```
Reason: Nested unpacking follows structure.

40. Answer:
```python
for i, v in enumerate(t):
    print(i, v)
```
Reason: `enumerate` yields index and value.

41. Answer:
```python
rev = tuple(reversed(t))
```
Reason: Convert reversed iterator back to tuple.

42. Answer:
```python
s = sorted(t)
```
Reason: `sorted` returns a list with sorted values.

43. Answer:
```python
try:
    a, b = (1, 2, 3)
except ValueError as e:
    print(type(e).__name__)
```
Reason: Unpacking mismatch raises `ValueError`.

44. Answer:
```python
rgb = (255, 0, 0)
r, g, b = rgb
```
Reason: Fixed 3-value record unpacking.

45. Answer:
```python
if t:
    print(t[0], t[-1])
```
Reason: Avoids error on empty tuple.

46. Answer:
```python
part = t[slice(0, 5, 2)]
```
Reason: `slice` object works in subscription.

47. Answer:
```python
def f():
    return 10, 20
x, y = f()
```
Reason: Return packs, assignment unpacks.

48. Answer:
```python
def g(a, b, c=0):
    print(a, b, c)

t = (1, 2)
d = {"c": 3}
g(*t, **d)
```
Reason: `*` expands positional; `**` expands keyword args.

49. Answer:
```python
t = (1, "python", 3.14, True)
```
Reason: Tuples can hold mixed types.

50. Answer:
```python
# packing: many -> one tuple, unpacking: one tuple -> many vars
```
Reason: This is the core tuple mental model.

### MCQ Theory Answer Key (50)

1. **A** - Tuple is an ordered immutable sequence.
2. **A** - Commas can form tuple literals.
3. **A** - One-element tuple requires trailing comma.
4. **A** - Tuples support indexing and slicing.
5. **A** - Counts must match unless using starred target.
6. **A** - Only one starred assignment target is allowed.
7. **A** - Starred unpack target is a list.
8. **A** - Multiple return values are tuple-packed.
9. **A** - Swap uses packing/unpacking semantics.
10. **A** - `*args` stores extra positional args as tuple.
11. **A** - `**kwargs` stores extra keyword args as dict.
12. **A** - `*t` expands positional args at call site.
13. **A** - `**d` expands keyword args at call site.
14. **A** - Tuple exposes `count` and `index`.
15. **A** - Membership scan is linear on sequence.
16. **A** - Hashability depends on all elements hashable.
17. **A** - List member makes tuple unhashable.
18. **A** - Immutability fixes container structure.
19. **A** - Nested mutable members can still mutate.
20. **A** - Shallow copy may return same immutable tuple.
21. **A** - Deep copy clones nested mutable objects.
22. **A** - Tuple slice may be identity optimization.
23. **A** - `sorted` returns new list.
24. **A** - `reversed` gives iterator.
25. **A** - Pattern fixes first value as `0`.
26. **A** - Structural pattern matching starts Python 3.10.
27. **A** - Tuple suits fixed read-only records.
28. **A** - List is better for frequent modification.
29. **A** - `range(4)` converted to `(0,1,2,3)`.
30. **A** - Tuple often has lower overhead than list.
31. **A** - Loop unpacking needs two-value items.
32. **A** - Tuples can contain mixed types.
33. **A** - `append` is invalid for tuple.
34. **A** - `+=` rebinds to new tuple object.
35. **A** - Outer tuple length is 3.
36. **A** - Coordinate tuple is a natural hashable key.
37. **A** - Unpacking mismatch raises `ValueError`.
38. **A** - Tuple literals are comma-driven.
39. **A** - `print(*t)` is argument unpacking.
40. **A** - Coordinates/RGB are tuple-friendly fixed records.
41. **A** - Common tuple built-ins: len/min/max/sum.
42. **A** - String tuple comparison is lexicographic.
43. **A** - Shallow copy shares nested mutables.
44. **A** - Tuple protects structure, not deep mutability.
45. **A** - Tuple iteration can be slightly faster in practice.
46. **A** - Rebinding `a` does not change `b` alias.
47. **A** - `t[slice(...)]` is correct slice-object usage.
48. **A** - Packing many->one, unpacking one->many.
49. **A** - Tuple is ideal for fixed API multi-value returns.
50. **A** - Tuple can contain mutable objects though immutable itself.

## Interview Theory Answers (Top 25)

1. Tuple vs list?
Answer: Tuple is immutable sequence; list is mutable sequence.
Reasoning: Choose tuple for fixed records, list for changing collections.

2. Why comma for one-element tuple?
Answer: `(x,)`.
Reasoning: Comma defines tuple literal; parentheses alone do not.

3. Packing/unpacking?
Answer: `t = 1,2` and `a,b = t`.
Reasoning: Same mechanism in opposite directions.

4. Why unpacking ValueError?
Answer: Variable/value count mismatch.
Reasoning: Python needs compatible arity unless using `*`.

5. What is extended unpacking?
Answer: `a,*mid,b = seq`.
Reasoning: One target absorbs remaining values as list.

6. Negative indexing/slicing?
Answer: `-1` last element; slices support negative steps.
Reasoning: Sequence indices count from end for negatives.

7. Why out-of-range slicing no IndexError?
Answer: Slices are bounds-tolerant.
Reasoning: Python clips slice limits safely.

8. Two tuple methods?
Answer: `count`, `index`.
Reasoning: Tuple has minimal API due to immutability.

9. Useful built-ins on numeric tuples?
Answer: `len`, `min`, `max`, `sum`.
Reasoning: Common aggregate operations for sequences.

10. Concatenation/repetition behavior?
Answer: `+` and `*` create new tuples.
Reasoning: Immutable container cannot change in place.

11. Why inner objects may still change?
Answer: Tuple immutability is shallow.
Reasoning: Referenced mutable objects can mutate.

12. What determines tuple hashability?
Answer: All elements must be hashable.
Reasoning: Hash must be stable.

13. Why `(1,2)` key works but `([1,2],3)` fails?
Answer: List is unhashable.
Reasoning: Any unhashable member makes whole tuple unhashable.

14. `*args` relation to tuples?
Answer: Packs extra positional args into tuple.
Reasoning: It is function-side tuple packing.

15. `*t` relation in calls?
Answer: Unpacks tuple into positional args.
Reasoning: Call-site unpacking counterpart of packing.

16. How swap uses tuples?
Answer: `a,b = b,a`.
Reasoning: RHS packed then unpacked into LHS.

17. Loop unpacking meaning?
Answer: `for x,y in pairs:`.
Reasoning: Each element is unpacked by position.

18. Tuple pattern matching?
Answer: `case (0,y)` etc.
Reasoning: Matches tuple shape and constants/variables.

19. Assignment vs shallow vs deep copy?
Answer: Assignment aliases; shallow shares nested mutables; deep clones nested graph.
Reasoning: Copy depth controls reference sharing.

20. Why `copy.copy()` may return same tuple?
Answer: Immutable optimization.
Reasoning: Reusing object is safe.

21. Why `t[:] is t` can be `True`?
Answer: Tuple full-slice may return original object.
Reasoning: Optimization for immutable types.

22. Tuple vs list performance practical view?
Answer: Tuples usually lighter and can iterate slightly faster.
Reasoning: Fixed-size immutable layout has less overhead.

23. When choose tuple?
Answer: Fixed-size read-mostly records, hashable keys.
Reasoning: Clear immutability intent and key safety.

24. Common tuple pitfalls?
Answer: Missing comma in single-item tuple, unpack mismatch, assuming deep immutability.
Reasoning: These cause most beginner/interview bugs.

25. Final mental model?
Answer: Packing many->one tuple, unpacking one->many vars.
Reasoning: Explains returns, swapping, loops, and `*args` mechanics.
