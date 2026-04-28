# PYTHON - FUNCTIONS

## 1. Core Mental Model

Python function questions are mostly about:
- Argument binding rules
- Default argument evaluation timing
- Mutability and aliasing
- Scope and closures (LEGB)
- Return behavior with try/finally

If you simulate these in order, most tricky outputs become predictable.

## 2. Argument Binding Order

Python binds call arguments in this practical sequence:
1. Positional arguments
2. Unpacked positional (*iterable)
3. Keyword arguments
4. Unpacked keyword (**mapping)
5. Remaining defaults

Conflict rules:
- Same parameter assigned twice -> TypeError.
- Too many positional args -> TypeError.
- Missing required args -> TypeError.

Keyword argument order in call does not matter for matching by name.

## 3. Positional-Only and Keyword-Only Parameters

Syntax markers:
- / : parameters before this are positional-only.
- * : parameters after this are keyword-only (unless captured by *args).

Examples of what these markers enforce are common interview traps.

## 4. Default Arguments: Evaluated Once

Default values are created at function definition time, not each call.

Mutable defaults (list, dict, set) persist across calls:
- Using append on a default list reuses same list.
- This causes state leakage between calls.

Safe pattern:
- Use None default, then create new object inside function.

## 5. Mutation vs Reassignment

Inside function:
- Mutation changes the same object (visible outside if shared).
- Reassignment binds local name to a new object (caller object unchanged).

Example distinction:
- x.append(4) mutates shared list.
- x = x + [4] creates new list and rebinds local x.

## 6. *args and **kwargs Unpacking

Unpacking expands data into call-site arguments.

Important rules:
- * provides positional arguments.
- ** provides keyword arguments.
- Multiple unpackings are merged left to right, but duplicate keys/targets raise error.

## 7. Closures and Late Binding

Closures capture variables by reference (name lookup at call time).

Classic trap:
- Lambdas created in loop all use final loop variable value.

Common fix:
- Bind current value as default parameter, e.g. lambda i=i: i

## 8. LEGB, nonlocal, global

Lookup order: Local -> Enclosing -> Global -> Builtins.

- Assigning to a name in function creates local binding unless declared otherwise.
- nonlocal updates variable from nearest enclosing function scope.
- global updates module-level variable.

## 9. Functions as First-Class Objects

In Python, functions can be:
- Passed as arguments
- Returned from other functions
- Stored in variables/collections
- Wrapped by decorators

Decorator mental model:
- @decorator replaces original function object with wrapper returned by decorator.

## 10. try/finally Return Behavior

finally always executes before function exits.

Critical rule:
- If finally has return, it overrides return from try/except.

This mirrors a common interview edge case and can hide errors.

## 11. Introspection and Callability

Useful internals often asked:
- f.__code__.co_varnames -> local variable names (including params)
- f.__code__.co_argcount -> positional parameter count
- callable(obj) -> whether object can be invoked with ()

## 12. Interview Solve Template

For any function snippet:
1. Bind arguments exactly (including *, **, /, and * markers).
2. Check for binding conflicts first.
3. Determine whether operations mutate or rebind.
4. Apply LEGB for each variable read/write.
5. For closures, decide if value is late-bound or fixed via default.
6. Apply try/finally return override last.

## 13. Worksheet Concept Coverage Checklist

- Mutable default argument pitfalls
- Positional vs keyword binding
- *args / **kwargs unpacking and conflicts
- Positional-only (/) and keyword-only (*) rules
- Mutation vs reassignment for lists
- Closure late binding and lambda fixes
- LEGB with nonlocal/global
- Functions as first-class objects
- Decorator wrapping behavior
- try/finally return override
- map/callable/code object basics
