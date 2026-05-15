# Python Set Worksheet Answers
Source Worksheet: `python/assignement/worksheets/collection_framwork/set.md`

## Level 1 Answers

### Tricky Predict the Output Solutions (50)

Note: For printed sets, element order can vary. Equivalent set content is considered correct.

1.
```python
s = {1, 2, 2, 3, 3}
print(s)
print(len(s))
```

Correct Output:
```text
{1, 2, 3}
3
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

2.
```python
a = {}
b = set()
print(type(a).__name__, type(b).__name__)
```

Correct Output:
```text
dict set
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

3.
```python
s = {10, 20, 30}
print(20 in s, 99 in s)
```

Correct Output:
```text
True False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

4.
```python
s = {1, 2, 3}
s.add(2)
print(s)
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

5.
```python
s = {1, 2}
s.update([3, 4], (5,))
print(s)
```

Correct Output:
```text
{1, 2, 3, 4, 5}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

6.
```python
s = {1, 2, 3}
s.remove(2)
print(s)
```

Correct Output:
```text
{1, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

7.
```python
s = {1, 2, 3}
try:
    s.remove(100)
except Exception as e:
    print(type(e).__name__)
```

Correct Output:
```text
KeyError
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

8.
```python
s = {1, 2, 3}
s.discard(100)
print(s)
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

9.
```python
s = {10, 20, 30}
x = s.pop()
print(x in {10, 20, 30})
print(len(s))
```

Correct Output:
```text
True
2
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

10.
```python
s = {1, 2, 3}
s.clear()
print(s, len(s))
```

Correct Output:
```text
set() 0
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

11.
```python
a = {1, 2}
b = {2, 3}
print(a | b)
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

12.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)
```

Correct Output:
```text
{2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

13.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a - b)
```

Correct Output:
```text
{1}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

14.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a ^ b)
```

Correct Output:
```text
{1, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

15.
```python
a = {1, 2}
b = {1, 2, 3}
print(a.issubset(b))
```

Correct Output:
```text
True
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

16.
```python
a = {1, 2, 3}
b = {1, 2}
print(a.issuperset(b))
```

Correct Output:
```text
True
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

17.
```python
a = {1, 2}
b = {3, 4}
print(a.isdisjoint(b))
```

Correct Output:
```text
True
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

18.
```python
s = {x * x for x in range(5)}
print(s)
```

Correct Output:
```text
{0, 1, 4, 9, 16}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

19.
```python
nums = [1, 2, 2, 3, 3]
s = set(nums)
print(s)
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

20.
```python
nums = [5, 4, 4, 3, 5, 2]
print(sorted(set(nums)))
```

Correct Output:
```text
[2, 3, 4, 5]
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

21.
```python
s = {"apple", "banana", "apple"}
print(s)
```

Correct Output:
```text
{'apple', 'banana'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

22.
```python
s = {1, 2.5, "hi", (1, 2)}
print(len(s))
```

Correct Output:
```text
4
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

23.
```python
try:
    s = {[1, 2], [3, 4]}
except Exception as e:
    print(type(e).__name__)
```

Correct Output:
```text
TypeError
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

24.
```python
fs = frozenset([1, 2, 2, 3])
print(fs)
print(type(fs).__name__)
```

Correct Output:
```text
frozenset({1, 2, 3})
frozenset
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

25.
```python
fs = frozenset([1, 2, 3])
try:
    fs.add(4)
except Exception as e:
    print(type(e).__name__)
```

Correct Output:
```text
AttributeError
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

26.
```python
s1 = {1, 2, 3}
s2 = s1.copy()
print(s1 == s2, s1 is s2)
```

Correct Output:
```text
True False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

27.
```python
s1 = {1, 2}
s2 = s1
s2.add(3)
print(s1, s2)
```

Correct Output:
```text
{1, 2, 3} {1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

28.
```python
a = {1, 2}
b = {2, 3}
a |= b
print(a)
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

29.
```python
a = {1, 2, 3}
b = {2, 3, 4}
a &= b
print(a)
```

Correct Output:
```text
{2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

30.
```python
a = {1, 2, 3}
b = {2, 3}
a -= b
print(a)
```

Correct Output:
```text
{1}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

31.
```python
a = {1, 2, 3}
b = {3, 4}
a ^= b
print(a)
```

Correct Output:
```text
{1, 2, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

32.
```python
s = {1}
s.update([2, 3], (4, 5), {6})
print(s)
```

Correct Output:
```text
{1, 2, 3, 4, 5, 6}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

33.
```python
s = {10, 20, 30}
s.remove(20)
s.add(40)
print(s)
```

Correct Output:
```text
{40, 10, 30}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

34.
```python
s = {True, 1, 2}
print(s)
print(len(s))
```

Correct Output:
```text
{True, 2}
2
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

35.
```python
s = {1, 1.0, 2.0, 2}
print(s)
print(len(s))
```

Correct Output:
```text
{1, 2.0}
2
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

36.
```python
s = {None, None, 0}
print(s)
print(len(s))
```

Correct Output:
```text
{None, 0}
2
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

37.
```python
s = set()
print(bool(s))
s.add(1)
print(bool(s))
```

Correct Output:
```text
False
True
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

38.
```python
s = {0, 1, 2}
print(any(s), all(s))
```

Correct Output:
```text
True False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

39.
```python
s = {10, 20, 30}
total = 0
for x in s:
    total += x
print(total)
```

Correct Output:
```text
60
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

40.
```python
s = {7, 2, 9, 5}
print(min(s), max(s))
```

Correct Output:
```text
2 9
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

41.
```python
word = "banana"
print(set(word))
```

Correct Output:
```text
{'a', 'n', 'b'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

42.
```python
word = "banana"
duplicates = set()
for ch in word:
    if word.count(ch) > 1:
        duplicates.add(ch)
print(duplicates)
```

Correct Output:
```text
{'a', 'n'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

43.
```python
a = [1, 2, 3, 4]
b = [3, 4, 5]
print(set(a) & set(b))
```

Correct Output:
```text
{3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

44.
```python
a = [1, 2, 3, 4]
b = [3, 4, 5]
print(set(a) - set(b))
```

Correct Output:
```text
{1, 2}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

45.
```python
a = [1, 2, 3, 4]
b = [3, 4, 5]
print(set(a) ^ set(b))
```

Correct Output:
```text
{1, 2, 5}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

46.
```python
s = {x for x in range(10) if x % 2 == 0}
print(s)
```

Correct Output:
```text
{0, 2, 4, 6, 8}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

47.
```python
s = set(range(1, 6))
print(s)
print(len(s))
```

Correct Output:
```text
{1, 2, 3, 4, 5}
5
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

48.
```python
s = {1, 2, 3}
s.add(4)
s.discard(2)
s.discard(100)
print(s, len(s))
```

Correct Output:
```text
{1, 3, 4} 3
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

49.
```python
s = {1, 2, 3, 4}
s.intersection_update({2, 4, 6})
print(s)
```

Correct Output:
```text
{2, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

50.
```python
s = {1, 2, 3, 4}
s.difference_update({2, 3})
print(s)
```

Correct Output:
```text
{1, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

### MCQ Theory Answer Key (50)

1. Answer: **B**

2. Answer: **C**

3. Answer: **B**

4. Answer: **B**

5. Answer: **C**

6. Answer: **B**

7. Answer: **B**

8. Answer: **C**

9. Answer: **B**

10. Answer: **C**

11. Answer: **B**

12. Answer: **B**

13. Answer: **A**

14. Answer: **C**

15. Answer: **B**

16. Answer: **A**

17. Answer: **B**

18. Answer: **A**

19. Answer: **C**

20. Answer: **B**

21. Answer: **C**

22. Answer: **D**

23. Answer: **B**

24. Answer: **B**

25. Answer: **A**

26. Answer: **A**

27. Answer: **C**

28. Answer: **B**

29. Answer: **B**

30. Answer: **B**

31. Answer: **A**

32. Answer: **B**

33. Answer: **C**

34. Answer: **B**

35. Answer: **B**

36. Answer: **B**

37. Answer: **B**

38. Answer: **B**

39. Answer: **B**

40. Answer: **B**

41. Answer: **B**

42. Answer: **B**

43. Answer: **B**

44. Answer: **B**

45. Answer: **B**

46. Answer: **B**

47. Answer: **B**

48. Answer: **C**

49. Answer: **A**

50. Answer: **A**

## Level 2 Answers

### Tricky Predict the Output Solutions (50)

Note: For printed sets, element order can vary. Equivalent set content is considered correct.

1.
```python
a = {1, 2}
b = {1, 2, 3}
print(a <= b, a < b)
```

Correct Output:
```text
True True
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

2.
```python
a = {1, 2, 3}
b = {1, 2, 3}
print(a <= b, a < b)
```

Correct Output:
```text
True False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

3.
```python
a = {1, 2, 3}
b = {1, 2}
print(a >= b, a > b)
```

Correct Output:
```text
True True
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

4.
```python
a = {1, 2}
b = {3, 4}
print(a < b, a > b)
```

Correct Output:
```text
False False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

5.
```python
a = {1, 2, 3}
b = {2, 3, 4}
c = {3, 4, 5}
print(a | b & c)
```

Correct Output:
```text
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

6.
```python
a = {1, 2, 3}
b = {2, 3, 4}
c = {3, 4, 5}
print((a | b) & c)
```

Correct Output:
```text
{3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

7.
```python
a = {1, 2, 3, 4}
b = {2, 4}
c = {4, 5}
print((a - b) ^ c)
```

Correct Output:
```text
{1, 3, 4, 5}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

8.
```python
print(set().union({1, 2}, {2, 3}, {3, 4}))
```

Correct Output:
```text
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

9.
```python
print(set.intersection({1, 2, 3}, {2, 3, 4}, {3, 4, 5}))
```

Correct Output:
```text
{3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

10.
```python
s = {1, 2, 3, 4}
result = s.difference_update({2, 4})
print(result)
print(s)
```

Correct Output:
```text
None
{1, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

11.
```python
s = {1, 2, 3, 4}
result = s.intersection_update({2, 4, 6})
print(result)
print(s)
```

Correct Output:
```text
None
{2, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

12.
```python
s = {1, 2, 3}
result = s.symmetric_difference_update({3, 4, 5})
print(result)
print(s)
```

Correct Output:
```text
None
{1, 2, 4, 5}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

13.
```python
s = {x for x in range(10) if x % 3 == 0}
print(s)
```

Correct Output:
```text
{0, 9, 3, 6}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

14.
```python
s = {x if x % 2 == 0 else -x for x in range(6)}
print(s)
```

Correct Output:
```text
{0, 2, 4, -5, -3, -1}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

15.
```python
s = set(x * x for x in [1, 2, 2, 3])
print(s)
```

Correct Output:
```text
{1, 4, 9}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

16.
```python
s = set(map(str, [1, 2, 2, 3]))
print(s)
```

Correct Output:
```text
{'3', '2', '1'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

17.
```python
s = set("Mississippi")
print(s)
print(len(s))
```

Correct Output:
```text
{'p', 's', 'M', 'i'}
4
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

18.
```python
s = {1}
s.update("ab")
print(s)
```

Correct Output:
```text
{1, 'a', 'b'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

19.
```python
d = {"a": 1, "b": 2, "a": 3}
print(set(d))
print(set(d.values()))
```

Correct Output:
```text
{'a', 'b'}
{2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

20.
```python
nums = [5, 1, 3, 3, 2, 2, 4]
print(sorted(set(nums), reverse=True))
```

Correct Output:
```text
[5, 4, 3, 2, 1]
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

21.
```python
s = {-10, 5, -3, 2}
print(max(s, key=abs))
```

Correct Output:
```text
-10
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

22.
```python
s = {10, 20, 30}
print(min(s), max(s), sum(s))
```

Correct Output:
```text
10 30 60
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

23.
```python
print(len(set(range(0, 20, 3))))
```

Correct Output:
```text
7
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

24.
```python
a = frozenset({1, 2})
b = frozenset({2, 3})
s = {a, b}
print(len(s))
```

Correct Output:
```text
2
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

25.
```python
try:
    s = {{1, 2}, {3, 4}}
except Exception as e:
    print(type(e).__name__)
```

Correct Output:
```text
TypeError
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

26.
```python
s = {1, 2, 3, 4}
removed = []
while s:
    removed.append(s.pop())
print(len(removed), len(s))
```

Correct Output:
```text
4 0
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

27.
```python
large = set(range(1000))
print(999 in large, 1001 in large)
```

Correct Output:
```text
True False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

28.
```python
words = ["Apple", "apple", "BANANA", "banana"]
normalized = {w.lower() for w in words}
print(normalized)
```

Correct Output:
```text
{'apple', 'banana'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

29.
```python
a = set("abcde")
b = set("cdefg")
print(a & b)
```

Correct Output:
```text
{'d', 'e', 'c'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

30.
```python
a = set("abcde")
b = set("cdefg")
print(a - b)
```

Correct Output:
```text
{'a', 'b'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

31.
```python
a = set("abcde")
b = set("cdefg")
print(a ^ b)
```

Correct Output:
```text
{'b', 'f', 'a', 'g'}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

32.
```python
a = {1, 2, 3}
b = {3, 4}
print(a.isdisjoint(b))
```

Correct Output:
```text
False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

33.
```python
a = {1, 2}
b = {1, 2, 3}
print(b.issubset(a))
```

Correct Output:
```text
False
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

34.
```python
s1 = {1, 2, 3}
s2 = s1.copy()
s1.add(4)
print(s1)
print(s2)
```

Correct Output:
```text
{1, 2, 3, 4}
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

35.
```python
s1 = {1, 2}
s2 = s1
s1.update({3, 4})
print(s1)
print(s2)
```

Correct Output:
```text
{1, 2, 3, 4}
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

36.
```python
s = set()
s |= {1, 2}
s |= {2, 3}
print(s)
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

37.
```python
s = {1, 2, 3}
s.clear()
s.add(99)
print(s)
```

Correct Output:
```text
{99}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

38.
```python
matrix = [[1, 2], [2, 3], [3, 4]]
flat_unique = {x for row in matrix for x in row}
print(flat_unique)
```

Correct Output:
```text
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

39.
```python
words = ["set", "python", "hash", "table"]
lengths = {len(w) for w in words}
print(lengths)
```

Correct Output:
```text
{3, 4, 5, 6}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

40.
```python
nums = {2, 3, 4, 5, 6, 7, 8}
primes = {x for x in nums if all(x % d for d in range(2, x))}
print(primes)
```

Correct Output:
```text
{2, 3, 5, 7}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

41.
```python
nums = [1, 2, 2, 3, 4, 4, 4]
seen = set()
dups = set()
for x in nums:
    if x in seen:
        dups.add(x)
    seen.add(x)
print(dups)
```

Correct Output:
```text
{2, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

42.
```python
nums = [5, 1, 3, 2, 3, 4, 2]
seen = set()
first_dup = None
for x in nums:
    if x in seen:
        first_dup = x
        break
    seen.add(x)
print(first_dup)
```

Correct Output:
```text
3
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

43.
```python
t = (1, 2, 2, 3)
print(set(t))
```

Correct Output:
```text
{1, 2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

44.
```python
s = {True, False, 1, 0, 2}
print(s)
print(len(s))
```

Correct Output:
```text
{False, True, 2}
3
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

45.
```python
s = {frozenset([1, 2]), frozenset([2, 1]), frozenset([3])}
print(len(s))
```

Correct Output:
```text
2
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

46.
```python
sets = [{1, 2}, {2, 3}, {3, 4}]
print(set().union(*sets))
```

Correct Output:
```text
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

47.
```python
sets = [{1, 2, 3}, {2, 3, 4}, {0, 2, 3}]
print(set.intersection(*sets))
```

Correct Output:
```text
{2, 3}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

48.
```python
s = {1, 2, 3, 4}
print(s.difference({2, 3}))
print(s)
```

Correct Output:
```text
{1, 4}
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

49.
```python
s = {1, 2, 3, 4}
print(s.symmetric_difference({3, 4, 5}))
print(s)
```

Correct Output:
```text
{1, 2, 5}
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

50.
```python
s = {1, 2, 3}
print(s.update([4]))
print(s)
```

Correct Output:
```text
None
{1, 2, 3, 4}
```
Reason: Python executes statements in order; this is the resulting output for the snippet.

### MCQ Theory Answer Key (50)

1. Answer: **B**

2. Answer: **A**

3. Answer: **A**

4. Answer: **B**

5. Answer: **B**

6. Answer: **C**

7. Answer: **A**

8. Answer: **A**

9. Answer: **A**

10. Answer: **A**

11. Answer: **B**

12. Answer: **A**

13. Answer: **A**

14. Answer: **A**

15. Answer: **B**

16. Answer: **C**

17. Answer: **A**

18. Answer: **B**

19. Answer: **A**

20. Answer: **A**

21. Answer: **A**

22. Answer: **A**

23. Answer: **A**

24. Answer: **A**

25. Answer: **C**

26. Answer: **B**

27. Answer: **B**

28. Answer: **B**

29. Answer: **A**

30. Answer: **A**

31. Answer: **A**

32. Answer: **A**

33. Answer: **A**

34. Answer: **B**

35. Answer: **B**

36. Answer: **B**

37. Answer: **B**

38. Answer: **A**

39. Answer: **A**

40. Answer: **A**

41. Answer: **A**

42. Answer: **A**

43. Answer: **C**

44. Answer: **B**

45. Answer: **B**

46. Answer: **B**

47. Answer: **B**

48. Answer: **B**

49. Answer: **B**

50. Answer: **B**

## Interview Theory Answers (Top 25)

1. A set is an unordered collection of unique hashable elements. Lists are ordered and allow duplicates; tuples are ordered and immutable.

2. Because sets use hashing internally; hashable values have stable hash/equality behavior needed for fast lookup.

3. Because `{}` is reserved for dictionaries in Python syntax. Use `set()` for an empty set.

4. `add(x)` inserts one element, while `update(iterable)` adds each element from one or more iterables.

5. `remove(x)` raises `KeyError` if missing, `discard(x)` does nothing if missing, and `pop()` removes an arbitrary element.

6. Sets are unordered, so `pop()` removes an arbitrary element, not by index/position.

7. Union combines all unique elements, intersection keeps common ones, difference keeps left-only items, symmetric difference keeps non-common items from both.

8. Operators (`|`, `&`, `-`, `^`) and methods (`union`, `intersection`, etc.) are equivalent in result; methods are often clearer with many operands.

9. `difference()` returns a new set; `difference_update()` mutates the original set in place and returns `None`.

10. Subset: all elements of A in B (`A <= B`), proper subset (`A < B`), superset (`A >= B`), proper superset (`A > B`).

11. It quickly checks whether two groups overlap at all, useful in scheduling/conflict or category-separation problems.

12. Average-case hash-table lookup is O(1) for membership checks.

13. Heavy hash collisions can degrade performance toward linear behavior in worst cases.

14. They give O(1) average membership, so duplicate detection in one pass is efficient.

15. Use `list(set(nums))` for quick dedupe, but order may change.

16. Use `list(dict.fromkeys(nums))` in modern Python to preserve first-seen order.

17. `b = a` creates aliasing (same object), while `a.copy()` creates a new set object.

18. `frozenset` is an immutable set; use it when a set must be hashable (e.g., inside another set or as dict key).

19. `set` is mutable and unhashable; `frozenset` is immutable and hashable.

20. They compare equal (`True == 1 == 1.0`), so only one representative is stored in a set.

21. Prefer set comprehensions for readable filter/transform logic that directly produces unique values.

22. Convert both lists to sets and intersect: `set(a) & set(b)`.

23. Use a `seen` set; first element already in `seen` is the first duplicate in O(n) time.

24. Common ones: `TypeError` for unhashable elements, `KeyError` from `remove` on missing value, `AttributeError` when mutating `frozenset`.

25. Check edge cases (empty, one item, duplicates), confirm mutation vs new-set behavior, and handle unordered output expectations.
