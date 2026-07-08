# Python Collections Workshop: Correct Answers with Reasoning

Reference questions: `python/workshop/python_collections_workshop_mcq.md`

## Q1-Q30 (Code-Based)

1. **Q1 -> B**  
Reason: `b = a` aliases same list object, so `append` changes list seen by both names.

2. **Q2 -> B**  
Reason: Slicing `a[:]` makes a new outer list; editing `b` does not change `a`.

3. **Q3 -> B**  
Reason: `append` adds one element as-is, so nested list becomes a single item.

4. **Q4 -> B**  
Reason: `extend` iterates argument and adds its elements individually.

5. **Q5 -> A**  
Reason: Slice `[start:stop:step]` with `1:5:2` picks indices `1` and `3`.

6. **Q6 -> B**  
Reason: `list.sort()` sorts in place and returns `None`.

7. **Q7 -> B**  
Reason: `[::-1]` creates reversed copy of list.

8. **Q8 -> B**  
Reason: Tuples are immutable; `+` creates a new tuple for `u` and leaves `t` unchanged.

9. **Q9 -> B**  
Reason: `(5)` is just `int`; `(5,)` is singleton tuple because of trailing comma.

10. **Q10 -> A**  
Reason: Star unpacking collects middle values into a list.

11. **Q11 -> B**  
Reason: Duplicate key in dict literal keeps last occurrence value.

12. **Q12 -> A**  
Reason: `get` returns fallback for missing key and does not mutate dictionary.

13. **Q13 -> B**  
Reason: Existing key `a` remains `1`; missing key `b` inserted with default `200`.

14. **Q14 -> A**  
Reason: `update` overwrites `q` and adds `r`; `pop('p')` returns removed value `1`.

15. **Q15 -> B**  
Reason: Dict keys preserve insertion order in modern Python.

16. **Q16 -> A**  
Reason: Dict comprehension keeps only even `k`, mapping to squares.

17. **Q17 -> B**  
Reason: Sets remove duplicates; sorted output shows unique ascending values.

18. **Q18 -> A**  
Reason: Union = all elements, intersection = common elements, difference = in `a` not in `b`.

19. **Q19 -> B**  
Reason: `update` on set adds each iterable element.

20. **Q20 -> B**  
Reason: `set(a)` removes duplicates; `sorted` returns ordered list.

21. **Q21 -> B**  
Reason: Tuple is immutable, but contained list is mutable and can be modified.

22. **Q22 -> B**  
Reason: Assigning tuple item raises `TypeError`, caught by `except`.

23. **Q23 -> B**  
Reason: `keys()` view is dynamic and reflects later dict modifications.

24. **Q24 -> B**  
Reason: `list(x)` is shallow copy; inner list aliases remain shared.

25. **Q25 -> B**  
Reason: `discard` ignores missing item; `remove` raises `KeyError` for missing item.

26. **Q26 -> B**  
Reason: `fromkeys` reuses same list object for each key when mutable default is passed.

27. **Q27 -> B**  
Reason: Multiplying nested list repeats references to same inner list object.

28. **Q28 -> A**  
Reason: Dict comprehension builds key-value mapping from tuple pairs.

29. **Q29 -> B**  
Reason: `zip` truncates to shortest iterable, so only `x` and `y` are used.

30. **Q30 -> B**  
Reason: Sorting by `len` gives ascending length; equal-length words keep stable relative order.

## Q31-Q50 (Conceptual)

31. **Q31 -> B**  
Reason: Lists are ordered and mutable sequences.

32. **Q32 -> B**  
Reason: Tuples are good for fixed records because immutability signals no in-place changes.

33. **Q33 -> C**  
Reason: Tuples are hashable if all contained items are hashable.

34. **Q34 -> B**  
Reason: Python dict maintains insertion order as language guarantee (3.7+).

35. **Q35 -> B**  
Reason: Repeated key gets overwritten by last assignment in literal construction.

36. **Q36 -> C**  
Reason: Set stores unique elements and has no indexing contract.

37. **Q37 -> C**  
Reason: Set membership is hash-based and average O(1).

38. **Q38 -> B**  
Reason: Slice-copy gives shallow copy of list.

39. **Q39 -> B**  
Reason: Same mutable object is shared across all keys created by `fromkeys`.

40. **Q40 -> C**  
Reason: `setdefault` returns existing value or inserts default when key absent.

41. **Q41 -> C**  
Reason: Tuple structure is immutable, but mutable members inside may still change.

42. **Q42 -> B**  
Reason: `append` adds one item; `extend` adds many items from iterable.

43. **Q43 -> C**  
Reason: `popitem()` behaves LIFO in modern Python dictionaries.

44. **Q44 -> C**  
Reason: Set algebra operators (`&`, `|`, `-`, `^`) are valid for sets.

45. **Q45 -> B**  
Reason: Converting through set removes duplicates but does not guarantee original order.

46. **Q46 -> B**  
Reason: Dict views are live, reflecting updates to underlying dict.

47. **Q47 -> B**  
Reason: `get` safely returns default instead of raising `KeyError`.

48. **Q48 -> B**  
Reason: Multiplication duplicates references, not deep copies, for nested mutables.

49. **Q49 -> A**  
Reason: Dict is Python’s native key-value mapping type.

50. **Q50 -> C**  
Reason: Set provides uniqueness, fast membership checks, and set operations.
