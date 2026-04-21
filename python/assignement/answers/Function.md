````md id="pyfnl1_15"
# Python Functions — Level 1 (Interview-Focused, Tricky Syntax)

## Q1
```python
def fun(x=[]):
    x.append(1)
    print(x)

fun()
fun()
```
````

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
