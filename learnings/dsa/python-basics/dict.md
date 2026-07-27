# Python Dictionaries: 30 MCQs

## Questions

1. Which expression creates an empty dictionary?
   - A. `set()`
   - B. `[]`
   - C. `{}`
   - D. `()`

2. Which statement is true about dictionary keys?
   - A. They may be duplicated.
   - B. They must be hashable.
   - C. They must be strings.
   - D. They are accessed by numeric index.

3. What is the value of `scores['sam']` for `scores = {'sam': 90, 'lee': 80}`?
   - A. `'sam'`
   - B. `80`
   - C. `90`
   - D. `KeyError`

4. What happens when `scores['alex']` is evaluated and `'alex'` is not a key?
   - A. It returns `None`.
   - B. It returns `False`.
   - C. It raises `KeyError`.
   - D. It creates the key with `None`.

5. What does `scores.get('alex')` return when `'alex'` is absent?
   - A. `KeyError`
   - B. `None`
   - C. `False`
   - D. An empty string

6. What does `scores.get('alex', 0)` return when `'alex'` is absent?
   - A. `None`
   - B. `KeyError`
   - C. `0`
   - D. `'alex'`

7. What is `data` after `data = {'a': 1}; data['b'] = 2`?
   - A. `{'a': 1}`
   - B. `{'b': 2}`
   - C. `{'a': 1, 'b': 2}`
   - D. Error

8. What is `data` after `data = {'a': 1}; data['a'] = 9`?
   - A. `{'a': 1, 'a': 9}`
   - B. `{'a': 9}`
   - C. `{'a': [1, 9]}`
   - D. Error

9. Which expression tests whether `'name'` is a dictionary key in `person`?
   - A. `'name' in person`
   - B. `'name' in person.values()`
   - C. `person.has('name')`
   - D. `person['name'] is not None`

10. What does `list({'a': 1, 'b': 2})` contain?
    - A. The dictionary values.
    - B. The dictionary keys.
    - C. Key-value tuples.
    - D. A nested dictionary.

11. What does `data.keys()` return?
    - A. A dynamic view of the dictionary's keys.
    - B. A list of values.
    - C. A tuple of key-value pairs.
    - D. A set of keys.

12. What does `data.values()` return?
    - A. A copy of the dictionary.
    - B. A dynamic view of the dictionary's values.
    - C. A set of values.
    - D. Key-value pairs.

13. Which loop accesses both key and value?
    - A. `for key, value in data:`
    - B. `for key, value in data.items():`
    - C. `for key, value in data.keys():`
    - D. `for key, value in data.values():`

14. What does `data.pop('a')` do when `'a'` exists?
    - A. Returns the value for `'a'` and removes that key-value pair.
    - B. Returns `'a'` but keeps the pair.
    - C. Removes an arbitrary pair.
    - D. Clears the dictionary.

15. What happens when `data.pop('missing')` is called without a default and the key is absent?
    - A. It returns `None`.
    - B. It raises `KeyError`.
    - C. It returns `False`.
    - D. It does nothing.

16. What does `data.popitem()` do for a non-empty dictionary?
    - A. Removes and returns the first inserted key-value pair.
    - B. Removes and returns the last inserted key-value pair.
    - C. Returns an arbitrary key only.
    - D. Clears the dictionary.

17. What does `data.update({'b': 2})` do?
    - A. Adds or replaces the value for key `'b'`.
    - B. Returns a new dictionary without changing `data`.
    - C. Removes key `'b'`.
    - D. Sorts the dictionary.

18. What is the result of `{'a': 1} | {'a': 2, 'b': 3}` in Python 3.9+?
    - A. `{'a': 1, 'b': 3}`
    - B. `{'a': 2, 'b': 3}`
    - C. `{'a': [1, 2], 'b': 3}`
    - D. Error

19. Which type cannot be used as a dictionary key?
    - A. `str`
    - B. `int`
    - C. `tuple` of hashable items
    - D. `list`

20. What is the result of `{key: value * 2 for key, value in {'a': 1, 'b': 2}.items()}`?
    - A. `{'a': 1, 'b': 2}`
    - B. `{'a': 2, 'b': 4}`
    - C. `{1: 'aa', 2: 'bb'}`
    - D. Error

21. What does `dict.fromkeys(['a', 'b'], 0)` produce?
    - A. `{'a': 0, 'b': 0}`
    - B. `{'a': 'b', 0: 0}`
    - C. `['a', 'b', 0]`
    - D. `set()`

22. What is the result of `len({'a': 1, 'b': 2})`?
    - A. `1`
    - B. `2`
    - C. `4`
    - D. Error

23. Which expression removes the key-value pair for `'name'` without returning its value?
    - A. `data.remove('name')`
    - B. `del data['name']`
    - C. `data.clear('name')`
    - D. `data.discard('name')`

24. What does `data.clear()` do?
    - A. Deletes the variable `data`.
    - B. Removes all key-value pairs from the existing dictionary.
    - C. Removes only duplicate values.
    - D. Returns a new empty dictionary.

25. In modern Python, what order does a dictionary preserve when keys are iterated?
    - A. Sorted key order.
    - B. Hash order only.
    - C. Insertion order.
    - D. Reverse insertion order.

26. What does `data.setdefault('count', 0)` do when `'count'` is absent?
    - A. Raises `KeyError`.
    - B. Returns `None` without changing `data`.
    - C. Inserts `'count': 0` and returns `0`.
    - D. Removes `'count'`.

27. What does `data.setdefault('count', 0)` return when `data['count']` is already `5`?
    - A. `0`
    - B. `5`
    - C. `None`
    - D. `KeyError`

28. What is the result of `dict([('x', 1), ('y', 2)])`?
    - A. `{'x': 1, 'y': 2}`
    - B. `[('x', 1), ('y', 2)]`
    - C. `{'x', 'y'}`
    - D. Error

29. Which statement correctly creates a shallow copy of `data`?
    - A. `copy = data`
    - B. `copy = data.copy()`
    - C. `copy = data.clear()`
    - D. `copy = data.items()`

30. What does `for key in data:` iterate over by default?
    - A. Values
    - B. Key-value pairs
    - C. Keys
    - D. Indices

## Answers and Reasons

1. **C — `{}`**. Empty braces are the literal for an empty dictionary.
2. **B — They must be hashable**. Dictionary keys need a stable hash value and equality behavior.
3. **C — `90`**. The key `'sam'` maps to the value `90`.
4. **C — It raises `KeyError`**. Bracket lookup requires the requested key to exist.
5. **B — `None`**. `get()` returns `None` by default for an absent key.
6. **C — `0`**. The second `get()` argument is returned when the key is missing.
7. **C — `{'a': 1, 'b': 2}`**. Assignment adds a new key-value pair when the key is absent.
8. **B — `{'a': 9}`**. Assigning an existing key replaces its associated value.
9. **A — `'name' in person`**. Membership on a dictionary checks its keys.
10. **B — The dictionary keys**. Iterating over a dictionary, including via `list()`, yields keys.
11. **A — A dynamic view of keys**. `keys()` returns a view that reflects later dictionary changes.
12. **B — A dynamic view of values**. `values()` returns a view rather than a standalone list or set.
13. **B — `for key, value in data.items():`**. `items()` provides key-value pairs for unpacking.
14. **A — Returns the value and removes the pair**. `pop(key)` removes a specific key-value pair.
15. **B — It raises `KeyError`**. Without a default, `pop()` requires the key to exist.
16. **B — Removes and returns the last inserted pair**. `popitem()` is last-in, first-out in modern Python.
17. **A — Adds or replaces key `'b'`**. `update()` merges supplied key-value pairs into the dictionary.
18. **B — `{'a': 2, 'b': 3}`**. With `|`, right-hand values replace values for matching keys.
19. **D — `list`**. Lists are mutable and unhashable, so they cannot be dictionary keys.
20. **B — `{'a': 2, 'b': 4}`**. The comprehension doubles each value while preserving each key.
21. **A — `{'a': 0, 'b': 0}`**. `fromkeys()` assigns the provided value to every supplied key.
22. **B — `2`**. `len()` counts dictionary key-value pairs.
23. **B — `del data['name']`**. `del` removes the pair for the named key without returning its value.
24. **B — Removes all key-value pairs**. `clear()` empties the same dictionary object.
25. **C — Insertion order**. Modern Python dictionaries retain the order in which keys were inserted.
26. **C — Inserts `'count': 0` and returns `0`**. `setdefault()` uses its default only for a missing key.
27. **B — `5`**. `setdefault()` returns an existing value and does not replace it.
28. **A — `{'x': 1, 'y': 2}`**. `dict()` accepts an iterable of two-item key-value pairs.
29. **B — `copy = data.copy()`**. `copy()` produces a shallow dictionary copy; assignment only shares the original object.
30. **C — Keys**. A plain dictionary iteration yields keys by default.
