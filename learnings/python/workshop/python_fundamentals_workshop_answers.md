# Python Fundamentals Workshop: Correct Answers with Reasoning

Reference questions: `python/workshop/python_fundamentals_workshop_mcq.md`

## Q1-Q30 (Code-Based)

1. **Q1 -> B**  
Reason: `b = a` creates an alias to the same list, and `append` mutates that shared list.

2. **Q2 -> C**  
Reason: `b = b + [3]` creates a new list and rebinds `b`; `a` still points to original `[1, 2]`.

3. **Q3 -> C**  
Reason: `int` is immutable, so `y += 1` rebinds `y` to a new object; `x` remains `10`.

4. **Q4 -> B**  
Reason: Function parameter references the same list object; `append` mutates original list.

5. **Q5 -> B**  
Reason: `lst = [999]` is local rebinding inside function; caller’s `a` is unchanged.

6. **Q6 -> B**  
Reason: `a is b` is `True` (same object), `a == c` is `True` (same content), `a is c` is `False`.

7. **Q7 -> B**  
Reason: `x[:]` makes shallow copy of outer list; inner list objects are shared.

8. **Q8 -> B**  
Reason: `deepcopy` duplicates nested lists, so modifying `y` does not affect `x`.

9. **Q9 -> B**  
Reason: Mutable default argument is evaluated once and reused, accumulating values.

10. **Q10 -> B**  
Reason: Lambdas capture `i` by reference (late binding); after loop, `i` is `2`.

11. **Q11 -> B**  
Reason: `and` short-circuits on first falsy operand (`a != 0` is `False`), no division occurs.

12. **Q12 -> B**  
Reason: Precedence is `not > and > or`; expression becomes `False or (True and True)`.

13. **Q13 -> B**  
Reason: Loop finds odd `5`, prints `"odd"`, then `break` prevents loop `else`.

14. **Q14 -> A**  
Reason: `continue` does not cancel loop `else`; loop ends normally, so `"done"` prints.

15. **Q15 -> C**  
Reason: `i` reaches `4` and `break` executes; final printed value is `4`.

16. **Q16 -> B**  
Reason: `pass` is a no-op placeholder; only `"end"` is printed.

17. **Q17 -> B**  
Reason: Inner loop breaks at `j == 1`, so only `j == 0` prints for each outer iteration.

18. **Q18 -> B**  
Reason: First time `i + j > 2` is at `(1, 2)`; flags trigger break out of both loops.

19. **Q19 -> A**  
Reason: For each element, `finally` runs: outputs are `10 F`, then `E F`, then `5 F`.

20. **Q20 -> B**  
Reason: `finally` runs even on `break`, incrementing `count` from `1` to `2`.

21. **Q21 -> B**  
Reason: First case guard `x == y` fails (`2 != 3`), second tuple case matches and prints `5`.

22. **Q22 -> C**  
Reason: `any([0,1,2])` is `True` (at least one truthy), `all([0,1,2])` is `False` (contains `0`).

23. **Q23 -> B**  
Reason: Walrus assigns `n = 3`; condition is true, so `3` prints.

24. **Q24 -> A**  
Reason: Removing while iterating shifts elements; `2` and `4` are removed, leaving `[1, 3]`.

25. **Q25 -> B**  
Reason: For lists, `+=` mutates in place; `a` and `b` still reference same list.

26. **Q26 -> B**  
Reason: Tuples are immutable; `x += (3,)` creates new tuple and rebinds `x`.

27. **Q27 -> B**  
Reason: `True or ...` short-circuits; `side()` is never called.

28. **Q28 -> B**  
Reason: `finally` return overrides `try` return in Python.

29. **Q29 -> C**  
Reason: `"stop"` matches no explicit case, so wildcard `case _` runs.

30. **Q30 -> B**  
Reason: Loop exits by `break` at `i == 2`, so loop `else` is skipped.

## Q31-Q50 (Conceptual)

31. **Q31 -> B**  
Reason: A Python variable is a name bound to an object reference, not a raw value slot.

32. **Q32 -> C**  
Reason: Assignment binds both names to same object unless explicit copy is used.

33. **Q33 -> A**  
Reason: `list`, `dict`, and `set` are mutable built-ins.

34. **Q34 -> B**  
Reason: Python uses call-by-sharing: function parameters receive references to objects.

35. **Q35 -> C**  
Reason: `is` checks identity (same object), `==` checks value/content equality.

36. **Q36 -> B**  
Reason: List slicing creates new outer list but nested references remain shared.

37. **Q37 -> C**  
Reason: `deepcopy` recursively duplicates nested mutable objects.

38. **Q38 -> C**  
Reason: Interning/caching is implementation optimization; never rely on it for logic.

39. **Q39 -> B**  
Reason: Mutable default arguments are evaluated once at function definition time.

40. **Q40 -> B**  
Reason: Closure-captured names are looked up when function executes (late binding).

41. **Q41 -> B**  
Reason: `set` is hash-based and best for average O(1) membership checks.

42. **Q42 -> A**  
Reason: `dict` is designed for key-to-value mapping and fast key lookup.

43. **Q43 -> B**  
Reason: `tuple` is immutable and suitable for fixed records.

44. **Q44 -> B**  
Reason: `append` avoids repeated list recreation done by `arr = arr + [i]`.

45. **Q45 -> B**  
Reason: Shallow copy scales with container size; deep copy scales with total nested structure.

46. **Q46 -> C**  
Reason: Boolean precedence order is `not`, then `and`, then `or`.

47. **Q47 -> A**  
Reason: `break` exits loop, `continue` skips current iteration, `pass` does nothing.

48. **Q48 -> A**  
Reason: Loop `else` executes only if loop completes without `break`.

49. **Q49 -> C**  
Reason: `finally` runs on all exit paths before leaving the `try` statement.

50. **Q50 -> C**  
Reason: `match/case` checks cases top-to-bottom and executes first matching case.
