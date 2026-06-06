# Python Set Worksheet

Source: python/notes/collection_framework/set.md

## Level 1

### Tricky Predict the Output (50)

1.
```python
s = {1, 2, 2, 3, 3}
print(s)
print(len(s))
```

Answer: _____________

2.
```python
a = {}
b = set()
print(type(a).__name__, type(b).__name__)
```

Answer: _____________

3.
```python
s = {10, 20, 30}
print(20 in s, 99 in s)
```

Answer: _____________

4.
```python
s = {1, 2, 3}
s.add(2)
print(s)
```

Answer: _____________

5.
```python
s = {1, 2}
s.update([3, 4], (5,))
print(s)
```

Answer: _____________

6.
```python
s = {1, 2, 3}
s.remove(2)
print(s)
```

Answer: _____________

7.
```python
s = {1, 2, 3}
try:
    s.remove(100)
except Exception as e:
    print(type(e).__name__)
```

Answer: _____________

8.
```python
s = {1, 2, 3}
s.discard(100)
print(s)
```

Answer: _____________

9.
```python
s = {10, 20, 30}
x = s.pop()
print(x in {10, 20, 30})
print(len(s))
```

Answer: _____________

10.
```python
s = {1, 2, 3}
s.clear()
print(s, len(s))
```

Answer: _____________

11.
```python
a = {1, 2}
b = {2, 3}
print(a | b)
```

Answer: _____________

12.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)
```

Answer: _____________

13.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a - b)
```

Answer: _____________

14.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a ^ b)
```

Answer: _____________

15.
```python
a = {1, 2}
b = {1, 2, 3}
print(a.issubset(b))
```

Answer: _____________

16.
```python
a = {1, 2, 3}
b = {1, 2}
print(a.issuperset(b))
```

Answer: _____________

17.
```python
a = {1, 2}
b = {3, 4}
print(a.isdisjoint(b))
```

Answer: _____________

18.
```python
s = {x * x for x in range(5)}
print(s)
```

Answer: _____________

19.
```python
nums = [1, 2, 2, 3, 3]
s = set(nums)
print(s)
```

Answer: _____________

20.
```python
nums = [5, 4, 4, 3, 5, 2]
print(sorted(set(nums)))
```

Answer: _____________

21.
```python
s = {"apple", "banana", "apple"}
print(s)
```

Answer: _____________

22.
```python
s = {1, 2.5, "hi", (1, 2)}
print(len(s))
```

Answer: _____________

23.
```python
try:
    s = {[1, 2], [3, 4]}
except Exception as e:
    print(type(e).__name__)
```

Answer: _____________

24.
```python
fs = frozenset([1, 2, 2, 3])
print(fs)
print(type(fs).__name__)
```

Answer: _____________

25.
```python
fs = frozenset([1, 2, 3])
try:
    fs.add(4)
except Exception as e:
    print(type(e).__name__)
```

Answer: _____________

26.
```python
s1 = {1, 2, 3}
s2 = s1.copy()
print(s1 == s2, s1 is s2)
```

Answer: _____________

27.
```python
s1 = {1, 2}
s2 = s1
s2.add(3)
print(s1, s2)
```

Answer: _____________

28.
```python
a = {1, 2}
b = {2, 3}
a |= b
print(a)
```

Answer: _____________

29.
```python
a = {1, 2, 3}
b = {2, 3, 4}
a &= b
print(a)
```

Answer: _____________

30.
```python
a = {1, 2, 3}
b = {2, 3}
a -= b
print(a)
```

Answer: _____________

31.
```python
a = {1, 2, 3}
b = {3, 4}
a ^= b
print(a)
```

Answer: _____________

32.
```python
s = {1}
s.update([2, 3], (4, 5), {6})
print(s)
```

Answer: _____________

33.
```python
s = {10, 20, 30}
s.remove(20)
s.add(40)
print(s)
```

Answer: _____________

34.
```python
s = {True, 1, 2}
print(s)
print(len(s))
```

Answer: _____________

35.
```python
s = {1, 1.0, 2.0, 2}
print(s)
print(len(s))
```

Answer: _____________

36.
```python
s = {None, None, 0}
print(s)
print(len(s))
```

Answer: _____________

37.
```python
s = set()
print(bool(s))
s.add(1)
print(bool(s))
```

Answer: _____________

38.
```python
s = {0, 1, 2}
print(any(s), all(s))
```

Answer: _____________

39.
```python
s = {10, 20, 30}
total = 0
for x in s:
    total += x
print(total)
```

Answer: _____________

40.
```python
s = {7, 2, 9, 5}
print(min(s), max(s))
```

Answer: _____________

41.
```python
word = "banana"
print(set(word))
```

Answer: _____________

42.
```python
word = "banana"
duplicates = set()
for ch in word:
    if word.count(ch) > 1:
        duplicates.add(ch)
print(duplicates)
```

Answer: _____________

43.
```python
a = [1, 2, 3, 4]
b = [3, 4, 5]
print(set(a) & set(b))
```

Answer: _____________

44.
```python
a = [1, 2, 3, 4]
b = [3, 4, 5]
print(set(a) - set(b))
```

Answer: _____________

45.
```python
a = [1, 2, 3, 4]
b = [3, 4, 5]
print(set(a) ^ set(b))
```

Answer: _____________

46.
```python
s = {x for x in range(10) if x % 2 == 0}
print(s)
```

Answer: _____________

47.
```python
s = set(range(1, 6))
print(s)
print(len(s))
```

Answer: _____________

48.
```python
s = {1, 2, 3}
s.add(4)
s.discard(2)
s.discard(100)
print(s, len(s))
```

Answer: _____________

49.
```python
s = {1, 2, 3, 4}
s.intersection_update({2, 4, 6})
print(s)
```

Answer: _____________

50.
```python
s = {1, 2, 3, 4}
s.difference_update({2, 3})
print(s)
```

Answer: _____________

### MCQ Theory (50)

1. Sets in Python are:
```text
A) Ordered and immutable
B) Unordered and unique-value collection
C) Key-value pairs only
D) Indexed sequence
```

2. Correct way to create an empty set:
```text
A) {}
B) []
C) set()
D) ()
```

3. `{}` creates:
```text
A) set
B) dict
C) tuple
D) list
```

4. Duplicate elements in a set are:
```text
A) stored twice
B) automatically removed
C) converted to None
D) rejected with error
```

5. Set indexing like `s[0]` is:
```text
A) valid
B) valid only for int sets
C) invalid (TypeError)
D) valid after sorting
```

6. Method to add one element:
```text
A) append
B) add
C) insert
D) push
```

7. Method to add multiple elements from iterable(s):
```text
A) extend
B) update
C) append
D) merge
```

8. `remove(x)` when x is missing:
```text
A) does nothing
B) returns False
C) raises KeyError
D) raises IndexError
```

9. `discard(x)` when x is missing:
```text
A) raises KeyError
B) does nothing
C) raises ValueError
D) adds x
```

10. `pop()` on set removes:
```text
A) first element
B) last element
C) random/arbitrary element
D) minimum element
```

11. `clear()` does:
```text
A) delete variable
B) empty set in-place
C) convert to list
D) sort set
```

12. Union operator is:
```text
A) &
B) |
C) ^
D) -
```

13. Intersection operator is:
```text
A) &
B) |
C) ^
D) /
```

14. Difference operator is:
```text
A) *
B) /
C) -
D) %
```

15. Symmetric difference operator is:
```text
A) ~
B) ^
C) &
D) +
```

16. `issubset` checks:
```text
A) all elements of A are in B
B) all elements of B are in A
C) both sets equal size only
D) sets are sorted
```

17. `issuperset` checks:
```text
A) A has fewer elements than B
B) A contains all elements of B
C) A and B disjoint
D) A and B are lists
```

18. `isdisjoint` means:
```text
A) no common elements
B) one set empty only
C) sets equal
D) same length
```

19. Set comprehension uses:
```text
A) [ ]
B) ( )
C) {expr for ...}
D) < >
```

20. Elements inside a set must be:
```text
A) mutable
B) hashable
C) sorted
D) numeric only
```

21. Which is hashable?
```text
A) list
B) dict
C) tuple (with hashable items)
D) set
```

22. Which is unhashable?
```text
A) int
B) str
C) tuple
D) list
```

23. `frozenset` is:
```text
A) mutable set
B) immutable set
C) ordered set
D) list-like set
```

24. `frozenset` supports `.add()`:
```text
A) yes
B) no
C) yes if empty
D) yes after cast
```

25. Membership in set is average:
```text
A) O(1)
B) O(n)
C) O(log n)
D) O(n log n)
```

26. Typical time for `add` is average:
```text
A) O(1)
B) O(n)
C) O(log n)
D) O(n^2)
```

27. Best collection for heavy lookup checks:
```text
A) list
B) tuple
C) set
D) string
```

28. `list(set(nums))` can:
```text
A) preserve order always
B) lose original order
C) keep duplicates
D) fail always
```

29. Order-preserving dedupe often uses:
```text
A) set only
B) dict.fromkeys
C) frozenset only
D) tuple conversion
```

30. In-place union operator is:
```text
A) +=
B) |=
C) &=
D) ^=
```

31. In-place intersection operator is:
```text
A) &=
B) |=
C) -=
D) +=
```

32. In-place difference operator is:
```text
A) ^=
B) -=
C) *=
D) /=
```

33. In-place symmetric difference operator is:
```text
A) |=
B) &=
C) ^=
D) -=
```

34. `copy()` on set gives:
```text
A) same reference
B) shallow copy (new set object)
C) deep copy of nested mutable
D) tuple
```

35. `b = a` means:
```text
A) new independent copy
B) alias/same object
C) deep copy
D) sorted copy
```

36. `True` and `1` in set:
```text
A) always two separate items
B) considered equal keys
C) both invalid
D) raise TypeError
```

37. `1` and `1.0` in set:
```text
A) always separate
B) considered equal keys
C) invalid together
D) syntax error
```

38. `set("banana")` returns:
```text
A) set of words
B) set of unique characters
C) list of chars
D) dict
```

39. `update("ab")` adds:
```text
A) string "ab" as one item
B) characters 'a' and 'b'
C) nothing
D) raises KeyError
```

40. Empty set truthiness is:
```text
A) True
B) False
C) None
D) Error
```

41. Non-empty set truthiness is:
```text
A) False
B) True
C) None
D) depends on element type only
```

42. `any({0, 0})` is:
```text
A) True
B) False
C) Error
D) None
```

43. `all({1, 2, 3})` is:
```text
A) False
B) True
C) Error
D) None
```

44. Set can contain another set directly:
```text
A) yes
B) no (unhashable)
C) yes if same size
D) yes if sorted
```

45. Set can contain frozenset:
```text
A) no
B) yes
C) only empty frozenset
D) only numeric frozenset
```

46. Best way to avoid KeyError while deleting maybe-missing item:
```text
A) remove
B) discard
C) pop
D) clear
```

47. `len(set(range(5)))` is:
```text
A) 4
B) 5
C) 6
D) depends on Python version
```

48. Which statement is correct?
```text
A) Sets keep insertion order guarantee forever
B) Sets are indexed collections
C) Sets are hash table based
D) Sets allow duplicate keys
```

49. In interview problems, sets are commonly used for:
```text
A) fast duplicate detection
B) preserving exact order always
C) matrix multiplication
D) GUI rendering
```

50. Average complexity of `intersection` is near:
```text
A) O(min(len(a), len(b)))
B) O(1)
C) O(n^2)
D) O(log n)
```

## Level 2

### Tricky Predict the Output (50)

1.
```python
a = {1, 2}
b = {1, 2, 3}
print(a <= b, a < b)
```

Answer: _____________

2.
```python
a = {1, 2, 3}
b = {1, 2, 3}
print(a <= b, a < b)
```

Answer: _____________

3.
```python
a = {1, 2, 3}
b = {1, 2}
print(a >= b, a > b)
```

Answer: _____________

4.
```python
a = {1, 2}
b = {3, 4}
print(a < b, a > b)
```

Answer: _____________

5.
```python
a = {1, 2, 3}
b = {2, 3, 4}
c = {3, 4, 5}
print(a | b & c)
```

Answer: _____________

6.
```python
a = {1, 2, 3}
b = {2, 3, 4}
c = {3, 4, 5}
print((a | b) & c)
```

Answer: _____________

7.
```python
a = {1, 2, 3, 4}
b = {2, 4}
c = {4, 5}
print((a - b) ^ c)
```

Answer: _____________

8.
```python
print(set().union({1, 2}, {2, 3}, {3, 4}))
```

Answer: _____________

9.
```python
print(set.intersection({1, 2, 3}, {2, 3, 4}, {3, 4, 5}))
```

Answer: _____________

10.
```python
s = {1, 2, 3, 4}
result = s.difference_update({2, 4})
print(result)
print(s)
```

Answer: _____________

11.
```python
s = {1, 2, 3, 4}
result = s.intersection_update({2, 4, 6})
print(result)
print(s)
```

Answer: _____________

12.
```python
s = {1, 2, 3}
result = s.symmetric_difference_update({3, 4, 5})
print(result)
print(s)
```

Answer: _____________

13.
```python
s = {x for x in range(10) if x % 3 == 0}
print(s)
```

Answer: _____________

14.
```python
s = {x if x % 2 == 0 else -x for x in range(6)}
print(s)
```

Answer: _____________

15.
```python
s = set(x * x for x in [1, 2, 2, 3])
print(s)
```

Answer: _____________

16.
```python
s = set(map(str, [1, 2, 2, 3]))
print(s)
```

Answer: _____________

17.
```python
s = set("Mississippi")
print(s)
print(len(s))
```

Answer: _____________

18.
```python
s = {1}
s.update("ab")
print(s)
```

Answer: _____________

19.
```python
d = {"a": 1, "b": 2, "a": 3}
print(set(d))
print(set(d.values()))
```

Answer: _____________

20.
```python
nums = [5, 1, 3, 3, 2, 2, 4]
print(sorted(set(nums), reverse=True))
```

Answer: _____________

21.
```python
s = {-10, 5, -3, 2}
print(max(s, key=abs))
```

Answer: _____________

22.
```python
s = {10, 20, 30}
print(min(s), max(s), sum(s))
```

Answer: _____________

23.
```python
print(len(set(range(0, 20, 3))))
```

Answer: _____________

24.
```python
a = frozenset({1, 2})
b = frozenset({2, 3})
s = {a, b}
print(len(s))
```

Answer: _____________

25.
```python
try:
    s = {{1, 2}, {3, 4}}
except Exception as e:
    print(type(e).__name__)
```

Answer: _____________

26.
```python
s = {1, 2, 3, 4}
removed = []
while s:
    removed.append(s.pop())
print(len(removed), len(s))
```

Answer: _____________

27.
```python
large = set(range(1000))
print(999 in large, 1001 in large)
```

Answer: _____________

28.
```python
words = ["Apple", "apple", "BANANA", "banana"]
normalized = {w.lower() for w in words}
print(normalized)
```

Answer: _____________

29.
```python
a = set("abcde")
b = set("cdefg")
print(a & b)
```

Answer: _____________

30.
```python
a = set("abcde")
b = set("cdefg")
print(a - b)
```

Answer: _____________

31.
```python
a = set("abcde")
b = set("cdefg")
print(a ^ b)
```

Answer: _____________

32.
```python
a = {1, 2, 3}
b = {3, 4}
print(a.isdisjoint(b))
```

Answer: _____________

33.
```python
a = {1, 2}
b = {1, 2, 3}
print(b.issubset(a))
```

Answer: _____________

34.
```python
s1 = {1, 2, 3}
s2 = s1.copy()
s1.add(4)
print(s1)
print(s2)
```

Answer: _____________

35.
```python
s1 = {1, 2}
s2 = s1
s1.update({3, 4})
print(s1)
print(s2)
```

Answer: _____________

36.
```python
s = set()
s |= {1, 2}
s |= {2, 3}
print(s)
```

Answer: _____________

37.
```python
s = {1, 2, 3}
s.clear()
s.add(99)
print(s)
```

Answer: _____________

38.
```python
matrix = [[1, 2], [2, 3], [3, 4]]
flat_unique = {x for row in matrix for x in row}
print(flat_unique)
```

Answer: _____________

39.
```python
words = ["set", "python", "hash", "table"]
lengths = {len(w) for w in words}
print(lengths)
```

Answer: _____________

40.
```python
nums = {2, 3, 4, 5, 6, 7, 8}
primes = {x for x in nums if all(x % d for d in range(2, x))}
print(primes)
```

Answer: _____________

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

Answer: _____________

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

Answer: _____________

43.
```python
t = (1, 2, 2, 3)
print(set(t))
```

Answer: _____________

44.
```python
s = {True, False, 1, 0, 2}
print(s)
print(len(s))
```

Answer: _____________

45.
```python
s = {frozenset([1, 2]), frozenset([2, 1]), frozenset([3])}
print(len(s))
```

Answer: _____________

46.
```python
sets = [{1, 2}, {2, 3}, {3, 4}]
print(set().union(*sets))
```

Answer: _____________

47.
```python
sets = [{1, 2, 3}, {2, 3, 4}, {0, 2, 3}]
print(set.intersection(*sets))
```

Answer: _____________

48.
```python
s = {1, 2, 3, 4}
print(s.difference({2, 3}))
print(s)
```

Answer: _____________

49.
```python
s = {1, 2, 3, 4}
print(s.symmetric_difference({3, 4, 5}))
print(s)
```

Answer: _____________

50.
```python
s = {1, 2, 3}
print(s.update([4]))
print(s)
```

Answer: _____________

### MCQ Theory (50)

1. Proper subset operator is:
```text
A) <=
B) <
C) >=
D) ==
```

2. Proper superset operator is:
```text
A) >
B) >=
C) <
D) <=
```

3. `a <= b` means:
```text
A) a is subset of b (or equal)
B) a is proper subset only
C) a size <= b size only
D) compare by sorted order
```

4. `a < b` means:
```text
A) subset or equal
B) proper subset only
C) lexicographic comparison
D) invalid for sets
```

5. Operator precedence between `&` and `|`:
```text
A) | has higher precedence
B) & has higher precedence
C) same precedence
D) depends on set size
```

6. `difference_update` returns:
```text
A) updated set
B) new set
C) None
D) bool
```

7. `intersection_update` returns:
```text
A) None
B) updated set object
C) tuple
D) int
```

8. `symmetric_difference_update` behavior:
```text
A) mutates set in-place
B) returns sorted set
C) preserves insertion index
D) deep copies set
```

9. `set.intersection(a, b, c)`:
```text
A) works for multiple sets
B) works for two only
C) returns list
D) raises TypeError always
```

10. `set().union(*iterables)`:
```text
A) merges all into one set
B) returns list
C) mutates first iterable
D) fails for 3+ sets
```

11. `update("abc")` on set adds:
```text
A) one string item
B) characters a, b, c
C) nothing
D) KeyError
```

12. Best way to make case-insensitive unique word set:
```text
A) {w.lower() for w in words}
B) set(words).lower()
C) words.lower()
D) list(words)
```

13. Set comprehension with nested loops can:
```text
A) flatten and dedupe
B) preserve duplicates
C) preserve matrix shape
D) avoid hashing
```

14. `set(map(str, nums))` does:
```text
A) converts values to strings and dedupes
B) keeps ints and order
C) returns tuple
D) returns dict
```

15. `set("Mississippi")` length equals number of:
```text
A) total characters
B) unique characters
C) vowels only
D) consonants only
```

16. Which can be an element of a set?
```text
A) set
B) list
C) frozenset
D) dict
```

17. Set of sets is usually invalid because:
```text
A) sets are mutable and unhashable
B) sets are too big
C) sets are ordered
D) Python forbids nesting
```

18. `frozenset([1,2]) == frozenset([2,1])`:
```text
A) False
B) True
C) TypeError
D) depends on Python version
```

19. `copy()` for a plain set of ints is enough because:
```text
A) ints are immutable values
B) copy makes deep clone automatically
C) sets cannot alias
D) ints are hash tables
```

20. `b = a` then mutating `a` affects `b` because:
```text
A) both names reference same object
B) Python auto copies
C) set is immutable
D) b is frozen view
```

21. `discard` is preferred over `remove` when:
```text
A) key may be absent
B) key always present
C) performance critical only
D) set is empty only
```

22. `pop()` from set is not ideal for deterministic order because:
```text
A) removes arbitrary element
B) always removes max
C) always removes min
D) raises every time
```

23. To print deterministic view of set contents, use:
```text
A) sorted(s)
B) s[0]
C) order(s)
D) index(s)
```

24. Which creates a new set without mutating original?
```text
A) s.union(t)
B) s.update(t)
C) s.intersection_update(t)
D) s.clear()
```

25. Which mutates original set?
```text
A) s.difference(t)
B) s.symmetric_difference(t)
C) s |= t
D) s.copy()
```

26. `difference` versus `difference_update`:
```text
A) both mutate
B) first returns new, second mutates
C) both return None
D) first mutates, second returns new
```

27. `s ^ t` gives:
```text
A) common elements
B) elements in either set but not both
C) only elements of s
D) only elements of t
```

28. Complexity of union is typically:
```text
A) O(1)
B) O(len(a)+len(b))
C) O(log n)
D) O(n^2)
```

29. Complexity of `x in s` average:
```text
A) O(1)
B) O(n)
C) O(n log n)
D) O(log n)
```

30. Worst-case set operations can degrade due to:
```text
A) hash collisions
B) alphabetical order
C) float rounding
D) recursion depth
```

31. In-place operations are useful when:
```text
A) you want to reuse same set object
B) you need immutable result
C) you need tuple output
D) you avoid hashing
```

32. `set.intersection(*sets)` requires:
```text
A) at least one set argument
B) exactly two sets
C) exactly three sets
D) list only
```

33. Empty set literal does not exist because:
```text
A) {} already used by dict
B) set is deprecated
C) parser limitation only
D) set must be typed
```

34. `bool(set())` and `bool({1})` are:
```text
A) True, False
B) False, True
C) True, True
D) False, False
```

35. Which statement about order is safest?
```text
A) set iteration order is a sorted order
B) set iteration order should not be relied on
C) set order always equals insertion order
D) set order is reverse insertion order
```

36. Which is a valid dedupe + sorted result?
```text
A) list(set(nums))
B) sorted(set(nums))
C) nums.sort(set)
D) set.sort(nums)
```

37. For large duplicate detection in one pass, common approach:
```text
A) nested loops only
B) keep `seen` set
C) convert to tuple each step
D) use recursion only
```

38. In interview coding, set is often paired with:
```text
A) membership checks
B) positional indexing
C) binary tree rotations
D) string formatting only
```

39. `issubset` and `<=` relationship:
```text
A) same semantic check
B) always opposite
C) unrelated
D) one checks order
```

40. `isdisjoint` is equivalent to checking:
```text
A) len(a & b) == 0
B) a == b
C) a <= b
D) len(a) == len(b)
```

41. `set(d)` for dictionary `d` gives:
```text
A) keys
B) values
C) items tuples
D) error
```

42. To get unique dictionary values:
```text
A) set(d.values())
B) set(d.keys())
C) set(d.items())
D) d.unique()
```

43. Best type to put inside a set when representing an immutable group:
```text
A) list
B) dict
C) frozenset
D) set
```

44. Equality of sets checks:
```text
A) same order
B) same unique elements regardless of order
C) same memory address
D) same hash seed
```

45. `set(range(0, 10, 2))` contains:
```text
A) odd numbers only
B) even numbers under 10
C) all numbers 0..10
D) empty set
```

46. If deterministic display is needed in logs:
```text
A) print(set_obj)
B) print(sorted(set_obj))
C) print(hash(set_obj))
D) print(reversed(set_obj))
```

47. `any(s)` on a set of numbers checks:
```text
A) all non-zero
B) at least one truthy element
C) set length > 5
D) sorted order
```

48. `all(s)` on a set of numbers checks:
```text
A) at least one truthy element
B) every element truthy
C) every element unique
D) all integers only
```

49. Main reason sets cannot contain mutable lists:
```text
A) memory heavy
B) lists are unhashable
C) lists are too long
D) syntax limitation
```

50. Best mental model of set internals:
```text
A) linked list of duplicates
B) hash table of unique hashable keys
C) balanced tree only
D) stack with random access
```

## Interview Theory (Top 25)

1. What is a set in Python, and how is it different from a list or tuple?
2. Why does Python require set elements to be hashable?
3. Why does `{}` create a dictionary and not a set?
4. Explain `add` vs `update` with examples.
5. Explain `remove` vs `discard` vs `pop`.
6. Why can `pop()` from set feel random?
7. Difference between union, intersection, difference, and symmetric difference.
8. Difference between operator forms (`|`, `&`, `-`, `^`) and method forms.
9. What is the difference between `difference()` and `difference_update()`?
10. What is subset, proper subset, superset, and proper superset?
11. How does `isdisjoint` help in real interview problems?
12. Why is membership in sets usually O(1)?
13. What can make set performance degrade in worst case?
14. Why are sets great for duplicate detection?
15. How would you remove duplicates from a list, and what order caveat exists?
16. How do you preserve order while removing duplicates?
17. Explain aliasing and copying with sets (`b = a` vs `a.copy()`).
18. What is `frozenset` and when should you use it?
19. Why can `frozenset` be used inside a set but `set` cannot?
20. How do `True`, `1`, and `1.0` behave inside sets and why?
21. When should you prefer set comprehension over loops?
22. How do you perform fast intersection of two large lists?
23. How would you find first duplicate efficiently in an array?
24. Common exceptions with sets and when they happen.
25. Interview-safe checklist for set problems before final submission.
