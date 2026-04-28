# JAVA - FUNCTIONS

## 1. Core Mental Model

Functions in Java are tested mostly through 4 things:
- Method overloading resolution
- Argument evaluation order
- Pass-by-value behavior
- Return behavior with try/finally

If you can simulate these correctly, most interview questions become mechanical.

## 2. Overloading Resolution Priority

Java chooses the most specific applicable method using this practical order:
1. Exact match (same type, fixed arity)
2. Primitive widening (for example int -> long)
3. Boxing/unboxing (int <-> Integer)
4. Varargs

Important practical rules:
- Fixed arity beats varargs.
- Widening is generally preferred over boxing.
- Non-generic overloads are usually preferred over generic ones when both match.
- If two candidates are equally specific, compilation fails with ambiguity.

## 3. Null and Specificity

When calling with null:
- Java can choose any reference-typed overload.
- The most specific type wins (for example String over Object).
- If two unrelated reference types are equally specific, it is ambiguous.

Example ambiguity pattern:
- fun(String s)
- fun(Integer i)
- fun(null)  // compile-time error

## 4. Varargs Rules

Varargs are fallback candidates.
- If fixed-parameter overload matches, it is chosen first.
- Among varargs overloads, the more specific element type wins.
- A call with no args only matches methods that can accept zero arguments.

## 5. Argument Evaluation and Increment Operators

Method arguments are evaluated left to right.
- a++ returns old value, then increments.
- ++a increments first, then returns new value.

This explains mixed-output questions using post/pre increment in function calls.

## 6. Pass-by-Value (Always)

Java is always pass-by-value.

Primitive argument:
- A copy of value is passed.
- Reassigning parameter does not change caller variable.

Object/array argument:
- A copy of reference is passed.
- Mutating object state is visible to caller.
- Reassigning parameter reference is not visible to caller.

## 7. try/finally and return

finally always executes after try/catch and before control leaves method.

Critical cases:
- try returns value, finally has no return -> original return value is kept.
- try returns value, finally also returns -> finally return overrides earlier return.

Avoid return in finally in production code because it hides earlier outcomes/exceptions.

## 8. Common Ambiguity Patterns

You should quickly detect compile-time ambiguity in these cases:
- Symmetric overloads such as (int, long) and (long, int) with (10, 10).
- Cross boxing patterns such as (int, Integer) and (Integer, int) with (10, 10).
- Multiple equally specific reference overloads with null.

## 9. Generic vs Non-Generic Overloads

When both are applicable:
- A concrete non-generic method is generally more specific.
- Generic method is used when no better non-generic overload exists.

For null, a specific reference overload (for example String) can beat generic <T>.

## 10. Interview Solve Template

For any function question:
1. List all candidate overloads.
2. Remove non-applicable ones.
3. Apply priority: exact -> widening -> boxing -> varargs.
4. Check specificity and ambiguity.
5. If call includes state changes, evaluate arguments left to right.
6. If try/finally exists, resolve return override rules last.

## 11. Worksheet Concept Coverage Checklist

Use this checklist to revise:
- Primitive vs wrapper overload
- Widening vs boxing vs varargs priority
- Fixed arity vs varargs
- Most specific method with null
- Generic overload interactions
- Ambiguity compile errors
- a++ / ++a evaluation order
- Pass-by-value with primitives
- Pass-by-value with arrays/objects and mutation
- try/finally return behavior
