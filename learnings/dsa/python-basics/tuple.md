# Python Tuples: 30 MCQs

## Questions

1. Which expression creates an empty tuple?
   - A. `{}`
   - B. `[]`
   - C. `()`
   - D. `set()`

2. Which expression creates a one-item tuple containing `5`?
   - A. `(5)` 
   - B. `(5,)`
   - C. `[5]`
   - D. `{5}`

3. What is the type of `(5)`?
   - A. `tuple`
   - B. `int`
   - C. `list`
   - D. `set`

4. Which statement is true about tuples?
   - A. They are mutable and unordered.
   - B. They are immutable and preserve order.
   - C. They allow only unique items.
   - D. They can store only integers.

5. What does `values[0]` return for `values = ('a', 'b', 'c')`?
   - A. `'a'`
   - B. `'b'`
   - C. `'c'`
   - D. Error

6. What does `values[-1]` return for `values = ('a', 'b', 'c')`?
   - A. `'a'`
   - B. `'b'`
   - C. `'c'`
   - D. Error

7. What is the result of `(1, 2) + (3, 4)`?
   - A. `(1, 2, 3, 4)`
   - B. `[1, 2, 3, 4]`
   - C. `(4, 6)`
   - D. Error

8. What is the result of `(1, 2) * 2`?
   - A. `(2, 4)`
   - B. `(1, 2, 1, 2)`
   - C. `[1, 2, 1, 2]`
   - D. Error

9. What is the result of `('p', 'q', 'r', 's')[1:3]`?
   - A. `('p', 'q')`
   - B. `('q', 'r')`
   - C. `('q', 'r', 's')`
   - D. `('r', 's')`

10. What happens when `values[0] = 'x'` is attempted for a tuple?
    - A. The first item is replaced.
    - B. It raises `TypeError`.
    - C. It raises `KeyError`.
    - D. It adds a new item.

11. Which method returns the number of occurrences of a value in a tuple?
    - A. `find()`
    - B. `count()`
    - C. `index()`
    - D. `total()`

12. What does `(1, 2, 2, 3).count(2)` return?
    - A. `1`
    - B. `2`
    - C. `3`
    - D. `True`

13. What does `('a', 'b', 'c').index('b')` return?
    - A. `'b'`
    - B. `1`
    - C. `2`
    - D. `True`

14. What happens when `('a', 'b').index('z')` is evaluated?
    - A. It returns `None`.
    - B. It returns `-1`.
    - C. It raises `ValueError`.
    - D. It raises `KeyError`.

15. Which assignment correctly unpacks `point = (10, 20)`?
    - A. `x = y = point`
    - B. `x, y = point`
    - C. `x + y = point`
    - D. `x, y = (10)`

16. What is the value of `first` after `first, *middle, last = (1, 2, 3, 4)`?
    - A. `1`
    - B. `[1]`
    - C. `(1,)`
    - D. `4`

17. What is the value of `middle` after `first, *middle, last = (1, 2, 3, 4)`?
    - A. `(2, 3)`
    - B. `[2, 3]`
    - C. `2`
    - D. `[1, 4]`

18. What is the result of `tuple([1, 2, 3])`?
    - A. `[1, 2, 3]`
    - B. `(1, 2, 3)`
    - C. `{1, 2, 3}`
    - D. Error

19. Which expression checks whether `3` belongs to `values`?
    - A. `values.has(3)`
    - B. `values[3]`
    - C. `3 in values`
    - D. `values.contains(3)`

20. When can a tuple be used as a dictionary key?
    - A. Never.
    - B. Only when it contains strings.
    - C. When all of its items are hashable.
    - D. Only when it contains one item.

21. Why can `(1, [2, 3])` not be used as a dictionary key?
    - A. Tuples cannot be keys.
    - B. The contained list is unhashable.
    - C. The tuple has two items.
    - D. The tuple mixes data types.

22. What does `len((4, 5, 6))` return?
    - A. `2`
    - B. `3`
    - C. `6`
    - D. Error

23. What is the result of `min((4, 1, 7))`?
    - A. `1`
    - B. `4`
    - C. `7`
    - D. `(1, 4, 7)`

24. What is the value of `a` after `a, b = b, a` when initially `a = 1` and `b = 2`?
    - A. `1`
    - B. `2`
    - C. `(1, 2)`
    - D. Error

25. What is the result of `('a',) == ('a')`?
    - A. `True`
    - B. `False`
    - C. `None`
    - D. Error

26. What is the type of `1, 2, 3`?
    - A. `list`
    - B. `tuple`
    - C. `set`
    - D. `int`

27. What is the result of `tuple('cat')`?
    - A. `('cat',)`
    - B. `('c', 'a', 't')`
    - C. `['c', 'a', 't']`
    - D. Error

28. Which is a valid way to concatenate tuples `first` and `second`?
    - A. `first.append(second)`
    - B. `first.extend(second)`
    - C. `first + second`
    - D. `first.add(second)`

29. Can a tuple contain a mutable object such as a list?
    - A. No, tuples can contain only immutable objects.
    - B. Yes, but the tuple's item reference cannot be reassigned.
    - C. No, Python raises `TypeError` on creation.
    - D. Yes, and the tuple itself becomes mutable.

30. Which use case is most appropriate for a tuple?
    - A. A collection that must frequently gain and lose items.
    - B. A fixed record such as an `(x, y)` coordinate.
    - C. A collection requiring unique items only.
    - D. A key-value mapping.

## Answers and Reasons

1. **C — `()`**. Parentheses with no items create an empty tuple.
2. **B — `(5,)`**. The trailing comma, not the parentheses, makes this a one-item tuple.
3. **B — `int`**. `(5)` is simply the integer `5` enclosed in grouping parentheses.
4. **B — They are immutable and preserve order**. Tuple positions remain ordered, but items cannot be reassigned.
5. **A — `'a'`**. Index `0` accesses the first tuple item.
6. **C — `'c'`**. Index `-1` accesses the final tuple item.
7. **A — `(1, 2, 3, 4)`**. `+` concatenates tuples into a new tuple.
8. **B — `(1, 2, 1, 2)`**. Tuple multiplication repeats the tuple's sequence.
9. **B — `('q', 'r')`**. Slicing includes index `1` and stops before index `3`.
10. **B — It raises `TypeError`**. Tuples do not permit item assignment because they are immutable.
11. **B — `count()`**. `count()` returns how many times a value appears.
12. **B — `2`**. The value `2` occurs twice in the tuple.
13. **B — `1`**. The first occurrence of `'b'` is at zero-based index `1`.
14. **C — It raises `ValueError`**. `index()` raises `ValueError` when no matching item exists.
15. **B — `x, y = point`**. The two tuple values are unpacked into the two variables.
16. **A — `1`**. The first target receives the first value from the tuple.
17. **B — `[2, 3]`**. A starred unpacking target collects the middle values in a list.
18. **B — `(1, 2, 3)`**. `tuple()` converts the list into a tuple.
19. **C — `3 in values`**. The `in` operator checks membership in a tuple.
20. **C — When all of its items are hashable**. A tuple's hashability depends on every item it contains.
21. **B — The contained list is unhashable**. A tuple containing an unhashable list is itself unhashable.
22. **B — `3`**. `len()` returns the number of tuple items.
23. **A — `1`**. `min()` returns the smallest comparable tuple item.
24. **B — `2`**. Simultaneous assignment evaluates the right side first, then swaps the values.
25. **B — `False`**. `('a',)` is a tuple, while `('a')` is the string `'a'`.
26. **B — `tuple`**. Comma-separated values form a tuple even without parentheses.
27. **B — `('c', 'a', 't')`**. `tuple()` iterates over the string's characters.
28. **C — `first + second`**. Tuples are immutable, so concatenation creates a new tuple.
29. **B — Yes, but the item reference cannot be reassigned**. The list can be mutated, but the tuple cannot replace its reference to that list.
30. **B — A fixed record such as an `(x, y)` coordinate**. Tuples suit ordered collections whose structure should not change.
