
# Python Functions — Level 1 (Interview-Focused, Tricky Syntax)

## Q1
```python
def fun(x=[]):
    x.append(1)
    print(x)

fun()
fun()
```


**What is the output? Why does it behave this way?**

---

## Q2

```python
def fun(a, b=10, c=20):
    print(a, b, c)

fun(5, c=30)
```

**Output? Explain keyword vs positional argument binding.**

---

## Q3

```python
def fun(a, b):
    return a + b

print(fun(b=2, a=3))
```

**Output? Does order of keyword arguments matter?**

---

## Q4

```python
def fun(a, b, c):
    print(a, b, c)

args = (1, 2)
fun(*args, 3)
```

**Output? Explain unpacking behavior.**

---

## Q5

```python
def fun(a, b=[]):
    b.append(a)
    return b

print(fun(1))
print(fun(2))
```

**Output? Why is this a common pitfall?**

---

## Q6

```python
def fun(x):
    x = x + [4]
    print(x)

lst = [1, 2, 3]
fun(lst)
print(lst)
```

**Output? Explain mutation vs reassignment.**

---

## Q7

```python
def fun(x):
    x.append(4)
    print(x)

lst = [1, 2, 3]
fun(lst)
print(lst)
```

**Output? Why different from previous question?**

---

## Q8

```python
def fun(a, b):
    print(a, b)

fun(1, *(2,))
```

**Output? Explain argument unpacking precedence.**

---

## Q9

```python
def fun(a, b=2, c=3):
    print(a, b, c)

fun(1, **{'b': 10})
```

**Output? How does `**kwargs` override defaults?**

---

## Q10

```python
def fun(a, b):
    print(a, b)

fun(*(1, 2, 3))
```

**What happens? Compile or runtime error? Why?**

---

## Q11

```python
def fun(a, b=2, c=3):
    print(a, b, c)

fun(1, *(4,), c=5)
```

**Output? Explain precedence of unpacking vs keyword args.**

---

## Q12

```python
def fun(a, b, /, c, d):
    print(a, b, c, d)

fun(1, 2, c=3, d=4)
```

**Output? What does `/` mean here?**

---

## Q13

```python
def fun(a, b, *, c, d):
    print(a, b, c, d)

fun(1, 2, c=3, d=4)
```

**Output? What does `*` enforce in parameters?**

---

## Q14

```python
def fun(a, b=10):
    print(a, b)

fun(1, b=20)
fun(a=1, 20)
```

**Which call works? Which fails? Why?**

---

## Q15

```python
def fun(a, b=10):
    print(a, b)

fun(1, **{'a': 2})
```

**Output or error? Explain argument conflict resolution.**

````md id="pyfnl2_15"
# Python Functions — Level 2 (Advanced, Interview-Focused)

## Q1
```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])
```
````

**Output? Explain late binding in closures.**

---

## Q2

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)

print([f() for f in funcs])
```

**Output? Why is this different from previous question?**

---

## Q3

```python
def fun(x, lst=[]):
    lst.append(x)
    return lst

print(fun(1))
print(fun(2))
print(fun(3, []))
```

**Output? Explain default argument persistence and override.**

---

## Q4

```python
def outer():
    x = 10
    def inner():
        x += 1
        return x
    return inner

f = outer()
print(f())
```

**Output or error? Explain scope resolution (LEGB).**

---

## Q5

```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1
        return x
    return inner

f = outer()
print(f())
print(f())
```

**Output? How does `nonlocal` change behavior?**

---

## Q6

```python
def fun(a, b, c):
    print(a, b, c)

args = {'a': 1, 'b': 2}
fun(**args, c=3)
```

**Output? Explain `**kwargs` merging behavior.**

---

## Q7

```python
def fun(*args, **kwargs):
    print(args, kwargs)

fun(1, 2, a=3, b=4)
```

**Output? Explain how Python binds args and kwargs.**

---

## Q8

```python
def fun(a, b=2, c=3):
    print(a, b, c)

fun(*[1], **{'c': 10})
```

**Output? Explain combined unpacking.**

---

## Q9

```python
def fun(x):
    def inner(y):
        return x + y
    return inner

f1 = fun(10)
f2 = fun(20)

print(f1(5), f2(5))
```

**Output? Explain closure capturing.**

---

## Q10

```python
def fun(x):
    print(x)

print(fun(fun(10)))
```

**Output? Explain return value of functions.**

---

## Q11

```python
def fun(x):
    return x * x

print(list(map(fun, [1, 2, 3])))
```

**Output? What is happening internally with `map`?**

---

## Q12

```python
def fun():
    try:
        return 1
    finally:
        return 2

print(fun())
```

**Output? Why does finally override return?**

---

## Q13

```python
def fun(x, y=[]):
    y = y + [x]
    return y

print(fun(1))
print(fun(2))
```

**Output? Why is this different from `.append()` case?**

---

## Q14

```python
def fun(a, b):
    print(a, b)

fun(*(1,), **{'b': 2})
```

**Output? Explain argument merging order.**

---

## Q15

```python
def fun(a, b, *, c):
    print(a, b, c)

fun(1, 2, *(3,), c=4)
```

**Output or error? Explain positional vs keyword-only conflict.**

````md id="pyfnl3_15"
# Python Functions — Level 3 (Expert, Internals + Edge Cases)

## Q1
```python
def outer():
    x = 10
    def inner():
        return x
    x = 20
    return inner

f = outer()
print(f())
````

**Output? Explain closure binding timing (late vs early binding).**

---

## Q2

```python
def outer():
    x = []
    def inner():
        x.append(1)
        return x
    return inner

f1 = outer()
f2 = outer()

print(f1(), f1(), f2())
```

**Output? Explain closure state isolation.**

---

## Q3

```python
def fun(a, b):
    return a + b

print(fun(*[1, 2], **{'a': 3}))
```

**Output or error? Explain argument collision resolution.**

---

## Q4

```python
def fun(x):
    return lambda y: lambda z: x + y + z

print(fun(1)(2)(3))
```

**Output? Explain nested closures and scope chaining.**

---

## Q5

```python
def fun():
    x = 10
    def inner():
        global x
        x = 20
    inner()
    print(x)

fun()
```

**Output? Explain global vs local scope interaction.**

---

## Q6

```python
def fun():
    x = 10
    def inner():
        nonlocal x
        x = 20
    inner()
    print(x)

fun()
```

**Output? Compare with previous question.**

---

## Q7

```python
def decorator(f):
    def wrapper():
        return f() + 1
    return wrapper

@decorator
def fun():
    return 10

print(fun())
```

**Output? Explain decorator transformation.**

---

## Q8

```python
def decorator(f):
    def wrapper(*args, **kwargs):
        print("Before")
        return f(*args, **kwargs)
    return wrapper

@decorator
def fun(x):
    print(x)

fun(5)
```

**Output? Explain function wrapping and argument forwarding.**

---

## Q9

```python
def fun():
    return [lambda: i for i in range(3)]

funcs = fun()
print([f() for f in funcs])
```

**Output? Why is this different from normal loop lambda case?**

---

## Q10

```python
def fun(x):
    def inner(y):
        return x + y
    return inner

f = fun(10)
del fun

print(f(5))
```

**Output? Explain function object + closure persistence.**

---

## Q11

```python
def fun(x, y):
    return x + y

print(fun.__code__.co_varnames)
print(fun.__code__.co_argcount)
```

**Output? What do these attributes represent?**

---

## Q12

```python
def fun():
    return 1

print(callable(fun), callable(10))
```

**Output? What makes an object callable?**

---

## Q13

```python
def fun(x):
    return x * 2

def wrapper(f):
    return lambda x: f(f(x))

g = wrapper(fun)
print(g(3))
```

**Output? Explain higher-order function composition.**

---

## Q14

```python
def fun(x):
    return x + 1

print((lambda f: f(5))(fun))
```

**Output? Explain passing functions as first-class objects.**

---

## Q15

```python
def fun(x):
    return x + 1

print((lambda f, x: f(x))(fun, 10))
```

**Output? Explain function invocation inside lambda.**


