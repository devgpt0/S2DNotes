# PYTHON - CONSTANTS, TYPE CONVERSION, AND BUILT-INS

Python has no enforced constant keyword. Type conversion is explicit, and tools such as `type`, `id`, `ord`, and `hex` are built-in functions, not methods.

## 1. Constants by Convention

Use `UPPER_SNAKE_CASE` for a value that should not be reassigned.

```python
MAX_RETRIES = 3
SECONDS_PER_MINUTE = 60

print(MAX_RETRIES)
print(SECONDS_PER_MINUTE)
```

Output:

```text
3
60
```

Python allows reassignment; the naming convention communicates intent.

## 2. `Final` Type Hint

`Final` tells static type checkers that a name should not be reassigned.

```python
from typing import Final

API_VERSION: Final[str] = "v1"

print(API_VERSION)
```

Output:

```text
v1
```

`Final` is not runtime enforcement. A static checker reports reassignment.

## 3. `type()`

`type(value)` returns the value's exact class.

```python
print(type(10))
print(type(3.5))
print(type("Python"))
print(type([1, 2]))
```

Output:

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'list'>
```

Use `type(value) is SomeType` only when an exact type is required.

## 4. `isinstance()`

`isinstance()` accepts a type and its subclasses.

```python
print(isinstance(True, bool))
print(isinstance(True, int))
print(type(True) is int)
```

Output:

```text
True
True
False
```

`bool` is a subclass of `int`. Prefer `isinstance()` for normal runtime type checks.

## 5. Explicit Type Conversion

Conversion creates a value of another type when the conversion is valid.

```python
count = int("42")
price = float("19.5")
label = str(100)

print(count, type(count).__name__)
print(price, type(price).__name__)
print(label, type(label).__name__)
```

Output:

```text
42 int
19.5 float
100 str
```

Python does not automatically convert arbitrary strings into numbers.

## 6. String to Integer

`int()` accepts integer text. Invalid text raises `ValueError`.

```python
print(int("25"))
print(int("-7"))

try:
    print(int("2.5"))
except ValueError as error:
    print(type(error).__name__)
```

Output:

```text
25
-7
ValueError
```

Convert decimal text through `float()` only when accepting that format is intentional.

## 7. Integer Bases

The second argument to `int()` specifies the source base.

```python
print(int("1010", 2))
print(int("17", 8))
print(int("ff", 16))
```

Output:

```text
10
15
255
```

Valid bases are `2` through `36`, or `0` for a recognized prefix such as `0x`.

## 8. Float to Integer

`int(float_value)` truncates toward zero. It does not round.

```python
print(int(3.9))
print(int(-3.9))
print(round(3.9))
```

Output:

```text
3
-3
4
```

Use `round()` when rounding is the intended rule.

## 9. Integer to Float

`float()` creates a floating-point value.

```python
value = float(7)

print(value)
print(type(value).__name__)
```

Output:

```text
7.0
float
```

## 10. Conversion to String

`str()` creates a human-readable string representation.

```python
age = 25
message = "Age: " + str(age)

print(message)
print(type(message).__name__)
```

Output:

```text
Age: 25
str
```

## 11. Conversion to Boolean

`bool()` uses truthiness. It does not parse words such as `"False"`.

```python
print(bool(0))
print(bool(1))
print(bool(""))
print(bool("False"))
```

Output:

```text
False
True
False
True
```

Any non-empty string is truthy. Parse expected text explicitly:

```python
raw_value = "false"
is_enabled = raw_value.lower() == "true"

print(is_enabled)
```

Output:

```text
False
```

## 12. List, Tuple, and Set Conversion

Collection constructors consume an iterable.

```python
text = "aba"

print(list(text))
print(tuple(text))
print(sorted(set(text)))
```

Output:

```text
['a', 'b', 'a']
('a', 'b', 'a')
['a', 'b']
```

A set removes duplicates and does not guarantee display order, so the example sorts it.

## 13. Dictionary Conversion

`dict()` can convert an iterable of key-value pairs.

```python
pairs = [("name", "Ana"), ("role", "Developer")]
profile = dict(pairs)

print(profile)
```

Output:

```text
{'name': 'Ana', 'role': 'Developer'}
```

Each input item must contain exactly two values.

## 14. Bytes and Text Conversion

Encoding converts text to bytes. Decoding converts bytes to text.

```python
text = "Python"
data = text.encode("utf-8")
restored = data.decode("utf-8")

print(data)
print(restored)
```

Output:

```text
b'Python'
Python
```

Use the same compatible encoding at both boundaries.

## 15. Implicit Numeric Conversion

Mixed integer and float arithmetic promotes the integer to a float.

```python
result = 2 + 3.5

print(result)
print(type(result).__name__)
```

Output:

```text
5.5
float
```

This numeric promotion does not mean Python freely converts unrelated types.

## 16. `id()`

`id(object)` returns an identity value unique during that object's lifetime.

Do not treat it as a permanent address or store it as application data.

```python
first = [1, 2]
alias = first
copy = [1, 2]

print(id(first) == id(alias))
print(id(first) == id(copy))
```

Output:

```text
True
False
```

Aliases have the same identity. Equal but separate lists do not.

## 17. `ord()`

`ord(character)` returns the Unicode code point of one character.

```python
print(ord("A"))
print(ord("a"))
print(ord("0"))
```

Output:

```text
65
97
48
```

The argument must contain exactly one Unicode character.

```python
try:
    print(ord("AB"))
except TypeError as error:
    print(type(error).__name__)
```

Output:

```text
TypeError
```

## 18. `chr()`

`chr(code_point)` is the reverse of `ord()`.

```python
print(chr(65))
print(chr(97))
print(chr(ord("Z")))
```

Output:

```text
A
a
Z
```

## 19. `hex()`

`hex(integer)` returns a lowercase hexadecimal string with a `0x` prefix.

```python
print(hex(255))
print(hex(16))
print(int("0xff", 0))
```

Output:

```text
0xff
0x10
255
```

Use formatting when the prefix or letter case must be controlled.

```python
number = 255

print(f"{number:x}")
print(f"{number:X}")
print(f"{number:#x}")
```

Output:

```text
ff
FF
0xff
```

## 20. `bin()` and `oct()`

`bin()` and `oct()` return base-prefixed strings.

```python
print(bin(10))
print(oct(10))
print(hex(10))
```

Output:

```text
0b1010
0o12
0xa
```

## 21. Lossy Conversions

Some conversions discard information.

```python
original = 3.75
converted = int(original)

print(original)
print(converted)
print(float(converted))
```

Output:

```text
3.75
3
3.0
```

The fractional part cannot be recovered after conversion to `int`.

## 22. Strict Conversion Rule

Validate expected input before converting when accepting another type would hide bad data.

```python
def double(value):
    if type(value) is not int:
        raise TypeError("value must be an int")
    return value * 2


print(double(4))

try:
    print(double("4"))
except TypeError as error:
    print(error)
```

Output:

```text
8
value must be an int
```

Validation checks data. Conversion changes data. Do not combine them accidentally.

## 23. Final Compression

| Tool | Result |
| --- | --- |
| `type(value)` | exact class |
| `isinstance(value, Type)` | type or subclass check |
| `int(value)` | integer conversion |
| `float(value)` | float conversion |
| `str(value)` | string conversion |
| `bool(value)` | truthiness conversion |
| `list`, `tuple`, `set`, `dict` | collection conversion |
| `id(value)` | runtime object identity |
| `ord(character)` | character to code point |
| `chr(number)` | code point to character |
| `bin`, `oct`, `hex` | integer to base-prefixed string |

Remember:

- constants are a naming convention; `Final` helps static checking;
- conversion should be explicit and intentional;
- `int()` truncates floats;
- `bool("False")` is `True` because the string is non-empty;
- `id()` describes identity, not value;
- `ord`, `id`, and `hex` are built-in functions, not object methods.
