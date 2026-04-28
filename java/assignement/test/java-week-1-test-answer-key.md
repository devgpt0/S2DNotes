# JAVA WEEK 1 TEST - ANSWER KEY

Format: Qn -> Output | Reason

## Q1
Output: 15 10
Reason: `b` copies primitive value of `a`; later `a` changes do not affect `b`.

## Q2
Output: 5
Reason: `p1` and `p2` reference the same object; updating through `p2` updates shared state.

## Q3
Output: 7 20
Reason: `p1` is rebound to a new object; `p2` still points to old object.

## Q4
Output: 99
Reason: `a` and `b` point to same array.

## Q5
Output: 6 5
Reason: `clone()` creates a separate array; changes are independent.

## Q6
Output: devops dev
Reason: Strings are immutable; concatenation rebinds `s1` to a new String.

## Q7
Output: A
Reason: `n2` still references the object even after `n1 = null`.

## Q8
Output: 8
Reason: `y` is block-local; only `x` is printed.

## Q9
Output: 30
Reason: `r` references `m[1]`; mutation through `r` changes matrix row.

## Q10
Output: 10 10
Reason: All references point to same `B` object.

## Q11
Output: 4
Reason: Java passes primitives by value.

## Q12
Output: 6
Reason: Object reference is passed by value, but object state is mutated.

## Q13
Output: 5
Reason: Parameter `b` is rebound locally; caller reference unchanged.

## Q14
Output: 25
Reason: Method returns square of 5.

## Q15
Output: int
Reason: Exact overload `show(int)` is preferred.

## Q16
Output: Integer
Reason: For `null`, most specific applicable reference overload is `Integer`.

## Q17
Output: two
Reason: Fixed-arity overload is preferred over varargs.

## Q18
Output: long
Reason: `int` literal widens to `long` for this overload set.

## Q19
Output: F` then `1`
Reason: `finally` executes before method returns the `try` value.

## Q20
Output: 9
Reason: Return in `finally` overrides return in `try`.

## Q21
Output: 6` then `0`
Reason: Varargs sums values; empty varargs gives 0.

## Q22
Output: 2` then `2` then `3`
Reason: `++p` increments before use; `p++` uses then increments.

## Q23
Output: int
Reason: Non-generic exact match beats generic overload.

## Q24
Output: 40
Reason: Object field is changed before local rebinding of parameter.

## Q25
Output: S1` then `M`
Reason: Static block runs when class initializes, before `main`.

## Q26
Output: INIT` then `BLOCK` then `5`
Reason: Static field init executes first, then static block, then `main`.

## Q27
Output: P` then `C` then `MAIN`
Reason: Superclass static init runs before subclass static init.

## Q28
Output: ctor` then `ctor`
Reason: Constructor runs for each `new A()`.

## Q29
Output: 0
Reason: Uninitialized static `int` default is 0.

## Q30
Output: 0
Reason: Uninitialized instance `int` default is 0.

## Q31
Output: `start` then `NegativeArraySizeException`
Reason: Program prints `start`; negative array size throws runtime exception before `end`.

## Q32
Output: 6
Reason: Static initializers execute in source order: 1 -> 3 -> 6.

## Q33
Output: 9
Reason: `byte` widens to `int`.

## Q34
Output: 7
Reason: Cast from `double` to `int` truncates fractional part.

## Q35
Output: 66
Reason: `'B'` converts to Unicode code point 66.

## Q36
Output: 20
Reason: `Integer` unboxes to `int`; sum is 10 + 10.

## Q37
Output: `NullPointerException`
Reason: `a + 1` needs unboxing; unboxing `null` throws NPE.

## Q38
Output: true
Reason: Compile-time constant concatenation uses same pooled literal.

## Q39
Output: true
Reason: `Integer` cache includes -128..127.

## Q40
Output: false
Reason: 128 is outside cache range; distinct wrapper objects.

## Q41
Output: true
Reason: `.equals()` compares value, not reference identity.

## Q42
Output: true
Reason: `intern()` returns pooled reference matching literal.

## Q43
Output: 1 9
Reason: After `clone`, `q` points to new array; `p` remains unchanged.

## Q44
Output: [1, 20, 3]
Reason: `Arrays.asList` supports `set` on fixed-size list.

## Q45
Output: `UnsupportedOperationException`
Reason: `Arrays.asList` result is fixed-size; `add` is not allowed.

## Q46
Output: 2 4
Reason: Enhanced-for variable is a copy for primitive elements.

## Q47
Output: N
Reason: Condition `n > 0` is false.

## Q48
Output: B` then `C`
Reason: Missing `break` causes fall-through from case 2 to default.

## Q49
Output: 0 1 2
Reason: Loop prints values for `i = 0..2`.

## Q50
Output: 1 2 3
Reason: `while` prints and increments until condition fails.

## Q51
Output: 5
Reason: `do-while` executes body once before checking condition.

## Q52
Output: 1 3
Reason: Even numbers skipped by `continue`; loop breaks at 5.

## Q53
Output: F
Reason: `&&` short-circuits; division by zero is never evaluated.

## Q54
Output: `ArithmeticException` (/ by zero)
Reason: Single `&` evaluates both sides, so `10/x` runs with `x=0`.

## Q55
Output: 11 12 13 21
Reason: Labeled `break outer` exits both loops at `a=2,b=2`.

## Q56
Output: 0:3 1:2 2:1
Reason: Both loop variables update each iteration until condition fails.

## Q57
Output: 1 3
Reason: `i==2` continues; `i==4` breaks before print.

## Q58
Output: one
Reason: Switch expression matches case `1`.

## Q59
Output: 6
Reason: Nested ternary chooses `b` because `a>b` false and `b>c` true.

## Q60
Output: Offday
Reason: Switch arrow case `6,7` matches day 6.
