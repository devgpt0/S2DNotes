# PYTHON WEEK 1 TEST - ANSWER KEY

Format: Qn -> Output | Reason

## Q1
Output: 15 10
Reason: `b` binds to integer value 10; later rebinding `a` does not affect `b`.

## Q2
Output: [1, 2, 3]
Reason: `x` and `y` reference the same list object.

## Q3
Output: [4, 5]` then `[9, 9]
Reason: `q` is rebound to a new list; `p` still points to old list.

## Q4
Output: 7
Reason: Both names reference same dict; mutation via `b` is visible via `a`.

## Q5
Output: [100, 2, 3]` then `[1, 2, 3]
Reason: Slice `a[:]` makes a new outer list for this 1D case.

## Q6
Output: [[1, 9], [2]]
Reason: `copy()` is shallow; nested list objects are shared.

## Q7
Output: devops dev
Reason: Strings are immutable; concatenation creates a new string for `s1`.

## Q8
Output: None
Reason: `b` remains bound to `None` after `a` is rebound.

## Q9
Output: [0, 42]
Reason: All names alias the same list object.

## Q10
Output: 30
Reason: `r` references second inner list; mutation reflects in `a`.

## Q11
Output: 4
Reason: Integer argument is immutable; reassignment inside function is local.

## Q12
Output: [6]
Reason: List is mutable; in-place mutation is visible to caller.

## Q13
Output: [5]
Reason: Parameter rebinding to new list does not affect caller binding.

## Q14
Output: 25
Reason: Function returns square of 5.

## Q15
Output: 13
Reason: Default `y=10`; so `3+10`.

## Q16
Output: 8
Reason: Explicit argument overrides default.

## Q17
Output: 1 2 3
Reason: Keyword arguments bind by name, independent of order.

## Q18
Output: 3 6
Reason: `args` has 3 elements; second element is 6.

## Q19
Output: ['a', 'z']
Reason: `kwargs` keys sorted alphabetically.

## Q20
Output: [1]` then `[1, 1]
Reason: Mutable default list persists across calls.

## Q21
Output: [1]` then `[1]
Reason: Each call passes a fresh list literal `[]`.

## Q22
Output: F` then `1`
Reason: `finally` runs before return value is delivered.

## Q23
Output: 9
Reason: `finally` return overrides `try` return.

## Q24
Output: 10
Reason: Inner function closes over `x` from enclosing scope.

## Q25
Output: S1` then `MAIN`
Reason: Top-level statements execute in order.

## Q26
Output: 5
Reason: Function reads global `x` (no local assignment).

## Q27
Output: 9` then `5`
Reason: Local `x` inside function shadows global `x`.

## Q28
Output: 3
Reason: `global x` updates module-level `x` from 1 to 3.

## Q29
Output: `UnboundLocalError`
Reason: Assignment to `y` makes it local; read happens before local assignment.

## Q30
Output: 2` then `done`
Reason: Function returns 2, then next print executes.

## Q31
Output: 3
Reason: `z` exists globally before function call.

## Q32
Output: function
Reason: Lambda object type name is `function`.

## Q33
Output: int
Reason: Literal 10 is `int`.

## Q34
Output: float
Reason: Literal 2.5 is `float`.

## Q35
Output: bool
Reason: `True` is boolean.

## Q36
Output: str
Reason: `'7'` is string.

## Q37
Output: 20
Reason: `int('12')` converts to integer 12; plus 8 gives 20.

## Q38
Output: 7.0
Reason: `float('3.5') * 2` gives float result.

## Q39
Output: False True
Reason: Empty list is falsy; non-empty list is truthy.

## Q40
Output: True` then `False
Reason: Lists compare by value with `==`; `is` checks identity.

## Q41
Output: True
Reason: `a` is exactly `None`.

## Q42
Output: 2
Reason: Tuple indexing is zero-based.

## Q43
Output: {1, 2, 3} (order may vary)
Reason: Set removes duplicates and is unordered.

## Q44
Output: 0
Reason: `dict.get` returns default when key is missing.

## Q45
Output: [[1], [2]]` then `[[1], ['x']]
Reason: Shallow copy new outer list; replacing `b[1]` doesn?t change `a[1]`.

## Q46
Output: [[1, 9], [2]]` then `[[1, 9], [2]]
Reason: Nested list object is shared in shallow copy.

## Q47
Output: N
Reason: Condition is false, so else branch runs.

## Q48
Output: B
Reason: `x > 5` matches `elif` branch.

## Q49
Output: 0 1 2
Reason: `range(3)` yields 0,1,2.

## Q50
Output: 1 2 3
Reason: `while` loop prints until `i` becomes 4.

## Q51
Output: 1 2 4
Reason: Skips 3 via `continue`; breaks at 5.

## Q52
Output: 0 0 | 0 1 | 1 0 | 1 1 |
Reason: Nested loops iterate all index pairs.

## Q53
Output: F
Reason: `and` short-circuits because first condition is false.

## Q54
Output: `ZeroDivisionError`
Reason: `or` evaluates right side when left is false; division by zero occurs.

## Q55
Output: done
Reason: `for-else`: else executes because loop ends without `break`.

## Q56
Output: (no output)
Reason: Loop hits `break` at `i==1`, so `else` does not run.

## Q57
Output: big
Reason: Ternary condition `x > 3` is true.

## Q58
Output: YES
Reason: `and` has higher preceden                                                                         ce: `a or (b and False)` -> `True`.

## Q59 
Output: 1 3
Reason: `i==2` continues, so print skipped; breaks after printing 3.

## Q60
Output: O E O
Reason: Odd/even labeling for 1,2,3.
