# PYTHON - OPERATORS

Operators combine, compare, or update values.

## 1. Arithmetic Operators

| Operator | Meaning |
| --- | --- |
| `+` | addition |
| `-` | subtraction |
| `*` | multiplication |
| `/` | true division |
| `//` | floor division |
| `%` | remainder |
| `**` | exponentiation |

```python
print(10 + 3)
print(10 - 3)
print(10 * 3)
print(10 / 4)
print(10 // 4)
print(10 % 4)
print(2**3)
```

Output:

```text
13
7
30
2.5
2
2
8
```

## 2. True Division and Floor Division

`/` returns a float. `//` rounds down toward negative infinity.

```python
print(7 / 2)
print(7 // 2)
print(-7 // 2)
```

Output:

```text
3.5
3
-4
```

`-7 // 2` is `-4`, not `-3`, because floor division rounds down.

## 3. Modulo

`a % b` returns the remainder consistent with floor division.

```python
print(10 % 3)
print(-10 % 3)
print(10 == (10 // 3) * 3 + (10 % 3))
```

Output:

```text
1
2
True
```

The identity `a == (a // b) * b + (a % b)` holds for non-zero `b`.

## 4. Exponentiation

`**` raises the left operand to a power.

```python
print(3**2)
print(9**0.5)
print(-3**2)
print((-3) ** 2)
```

Output:

```text
9
3.0
-9
9
```

Exponentiation binds before unary minus, so parentheses matter.

## 5. Unary Operators

Unary operators act on one value.

```python
number = 5

print(+number)
print(-number)
print(not number)
```

Output:

```text
5
-5
False
```

`not` always returns a Boolean.

## 6. Operator Overloading by Type

An operator's behavior depends on operand types.

```python
print(2 + 3)
print("Py" + "thon")
print([1, 2] + [3])
print("ha" * 3)
```

Output:

```text
5
Python
[1, 2, 3]
hahaha
```

The same symbol can call different type-specific behavior.

## 7. Operator Precedence

Common precedence from high to low:

1. parentheses;
2. exponentiation;
3. unary `+`, `-`, `~`;
4. `*`, `/`, `//`, `%`;
5. `+`, `-`;
6. shifts;
7. bitwise `&`, `^`, `|`;
8. comparisons, identity, membership;
9. `not`, `and`, `or`.

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(True or False and False)
```

Output:

```text
14
20
True
```

Use parentheses when grouping is not immediately clear.

## 8. Comparison Operators

Comparisons return `True` or `False`.

```python
print(5 == 5)
print(5 != 3)
print(5 > 3)
print(5 >= 5)
print(3 < 5)
print(3 <= 2)
```

Output:

```text
True
True
True
True
True
False
```

## 9. Chained Comparisons

Python evaluates a comparison chain as connected conditions.

```python
age = 25

print(18 <= age < 60)
print(18 <= age and age < 60)
```

Output:

```text
True
True
```

The middle expression is evaluated once in a comparison chain.

## 10. Equality Versus Identity

`==` compares values. `is` compares object identity.

```python
first = [1, 2]
alias = first
copy = [1, 2]

print(first == copy)
print(first is copy)
print(first is alias)
```

Output:

```text
True
False
True
```

Use `is` for singleton checks such as `value is None`, not normal value comparison.

## 11. Logical Operators

`not` negates truthiness. `and` and `or` short-circuit and return an operand.

```python
print(not "")
print("" and "second")
print("" or "fallback")
print("first" and "second")
```

Output:

```text
True

fallback
second
```
The universal rule

This is what I recommend memorizing:

and
```
A and B and C and D

Find the first FALSY value.

If none exists → return the last value.
```

or
```
A or B or C or D

Find the first TRUTHY value.

If none exists → return the last value.  

The blank output is the empty string returned by `"" and "second"`.
```


## 12. Membership Operators

`in` and `not in` test membership.

```python
numbers = [10, 20, 30]
profile = {"name": "Ana", "role": "Developer"}

print(20 in numbers)
print(40 not in numbers)
print("name" in profile)
print("Ana" in profile)
```

Output:

```text
True
True
True
False
```

Dictionary membership tests keys, not values.

## 13. Assignment Operators

`=` binds a name. Augmented assignment updates using an operator.

```python
total = 10
total += 5
total *= 2

print(total)
```

Output:

```text
30
```

Common forms are `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, and `**=`.

## 14. Augmented Assignment: Mutable Versus Immutable

`+=` may mutate a mutable object but creates a new immutable object.

```python
number = 10
number_before = id(number)
number += 1

items = [1, 2]
items_before = id(items)
items += [3]

print(id(number) == number_before)
print(id(items) == items_before)
print(items)
```

Output:

```text
False
True
[1, 2, 3]
```

Integers are immutable. Lists implement in-place addition.

## 15. Assignment Expression: `:=`

The walrus operator assigns a value inside an expression.

```python
values = [2, 4, 6]

if (count := len(values)) > 2:
    print(count)
```

Output:

```text
3
```

Use it only when assignment makes the expression clearer.

## 16. Bitwise AND: `&`

Bitwise operators work on integer bits.

```python
print(bin(5))
print(bin(3))
print(5 & 3)
```

Output:

```text
0b101
0b11
1
```

Only the lowest bit is `1` in both numbers.

## 17. Bitwise OR and XOR

`|` sets a bit present in either operand. `^` sets a bit present in exactly one operand.

```python
print(5 | 3)
print(5 ^ 3)
```

Output:

```text
7
6
```

## 18. Bitwise NOT

For integers, `~number` equals `-(number + 1)`.

```python
print(~5)
print(-(5 + 1))
```

Output:

```text
-6
-6
```

## 19. Bit Shifts

`<<` shifts bits left. `>>` shifts bits right.

```python
print(5 << 1)
print(5 >> 1)
print(bin(5 << 1))
```

Output:

```text
10
2
0b1010
```

For non-negative integers, shifting left by one multiplies by two and shifting right divides by two using floor division.

## 20. Set Operators

Sets reuse bitwise symbols for set operations.

```python
left = {1, 2, 3}
right = {3, 4}

print(sorted(left | right))
print(sorted(left & right))
print(sorted(left - right))
print(sorted(left ^ right))
```

Output:

```text
[1, 2, 3, 4]
[3]
[1, 2]
[1, 2, 4]
```

| Operator | Set meaning |
| --- | --- |
| `|` | union |
| `&` | intersection |
| `-` | difference |
| `^` | symmetric difference |

## 21. Common Errors

### Mixing Unsupported Types

```python
try:
    print("age: " + 25)
except TypeError as error:
    print(type(error).__name__)

print("age: " + str(25))
```

Output:

```text
TypeError
age: 25
```

Python does not silently convert an integer to a string for `+`.

### Division by Zero

```python
try:
    print(10 / 0)
except ZeroDivisionError as error:
    print(type(error).__name__)
```

Output:

```text
ZeroDivisionError
```

## 22. Final Compression

| Category | Operators |
| --- | --- |
| Arithmetic | `+ - * / // % **` |
| Comparison | `== != < <= > >=` |
| Logical | `not and or` |
| Identity | `is`, `is not` |
| Membership | `in`, `not in` |
| Bitwise | `& | ^ ~ << >>` |
| Assignment | `= += -= *= /= //= %= **= :=` |

Remember:

- operator behavior depends on operand types;
- `/` and `//` are different;
- `==` checks value, while `is` checks identity;
- `and` and `or` return operands;
- parentheses make complex expressions safer to read.
