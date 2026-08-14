# Python Functions Worksheet Answers

## Level 1

1.
```text
[1]
[1, 1]
```
The default list is created once and is reused by both calls.

2.
```text
5 10 30
```
`a` is positional; `c=30` replaces its default.

3.
```text
5
```
Keyword names, not their written order, bind the arguments.

4.
```text
1 2 3
```
`*args` supplies the first two positional arguments.

5.
```text
[1]
[1, 2]
```
The mutable default list persists across calls.

6.
```text
[1, 2, 3, 4]
[1, 2, 3]
```
`x = x + [4]` rebinds local `x`; it does not mutate `lst`.

7.
```text
[1, 2, 3, 4]
[1, 2, 3, 4]
```
`append` mutates the shared list object.

8.
```text
1 2
```
The starred tuple provides the second positional argument.

9.
```text
1 10 3
```
The unpacked dictionary supplies `b`, replacing only that default.

10. A runtime error is raised before `print` runs.
```text
TypeError: fun() takes 2 positional arguments but 3 were given
```

11.
```text
1 4 5
```
The positional value fills `a`, the unpacked value fills `b`, and `c` is a keyword.

12.
```text
1 2 3 4
```
Parameters before `/` are positional-only.

13.
```text
1 2 3 4
```
Parameters after `*` are keyword-only.

14. The first call prints `1 20`. The second call is invalid syntax because a positional argument follows a keyword argument.
```text
SyntaxError: positional argument follows keyword argument
```

15. A value is supplied for `a` both positionally and through `**`.
```text
TypeError: fun() got multiple values for argument 'a'
```

## Level 2

1.
```text
[2, 2, 2]
```
Each lambda reads the final loop value when called.

2.
```text
[0, 1, 2]
```
`i=i` stores the current value as each lambda's default.

3.
```text
[1]
[1, 2]
[3]
```
The explicit empty list is a new argument for the third call.

4.
```text
UnboundLocalError: cannot access local variable 'x' where it is not associated with a value
```
Assignment makes `x` local to `inner`; it cannot read that local first.

5.
```text
11
12
```
`nonlocal x` updates the value in `outer`'s scope.

6.
```text
1 2 3
```
The dictionary is unpacked into named arguments and `c=3` supplies the remaining parameter.

7.
```text
(1, 2) {'a': 3, 'b': 4}
```
Extra positional arguments form `args`; named arguments form `kwargs`.

8.
```text
1 2 10
```
The list supplies `a`; the dictionary supplies `c`.

9.
```text
15 25
```
Each returned function closes over its own `x`.

10.
```text
10
None
```
`fun(10)` prints `10` and returns `None`; that return value is then printed.

11.
```text
[1, 4, 9]
```
`map` calls `fun` for each input value.

12.
```text
2
```
The `return` in `finally` overrides the one in `try`.

13.
```text
[1]
[2]
```
`y = y + [x]` creates and rebinds a new list instead of mutating the default.

14.
```text
1 2
```
The starred tuple supplies `a`; the dictionary supplies `b`.

15. The starred tuple adds a third positional argument, but `c` is keyword-only.
```text
TypeError: fun() takes 2 positional arguments but 3 positional arguments (and 1 keyword-only argument) were given
```

## Level 3

1.
```text
20
```
The closure reads the final value stored in its enclosing scope.

2.
```text
[1] [1, 1] [1]
```
`f1` and `f2` have separate enclosed lists.

3. `a` receives a value from both the starred list and the dictionary.
```text
TypeError: fun() got multiple values for argument 'a'
```

4.
```text
6
```
The nested lambdas retain `x` and then `y` until `z` is supplied.

5.
```text
10
```
`global x` creates or updates a module-level name, not `fun`'s local `x`.

6.
```text
20
```
`nonlocal x` changes the enclosing function's `x`.

7.
```text
11
```
The decorator replaces `fun` with `wrapper`, which adds one to its result.

8.
```text
Before
5
```
The wrapper forwards the argument to the original function.

9.
```text
[2, 2, 2]
```
The list-comprehension variable is also late-bound by the lambdas.

10.
```text
15
```
The returned closure retains `x` even after the outer function name is deleted.

11.
```text
('x', 'y')
2
```
`co_varnames` lists local names; `co_argcount` is the positional-argument count.

12.
```text
True False
```
Functions implement call behavior; integers do not.

13.
```text
12
```
The returned lambda applies `fun` twice: `3 -> 6 -> 12`.

14.
```text
6
```
Functions can be passed to, and called by, other functions.

15.
```text
11
```
The lambda receives `fun` and `10`, then calls `fun(10)`.
