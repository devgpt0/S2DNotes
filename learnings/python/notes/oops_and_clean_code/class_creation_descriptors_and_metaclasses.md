# Class Creation, Descriptors, and Metaclasses
## 1. Core truth

Python lets you customize how classes are built and how attributes behave.
This is powerful, but it is also advanced, so the simple tools should come first.

```python
class Course:
    category = "programming"

print(type(Course).__name__)
print(Course.category)
```

Output:

```text
type
programming
```

`Course` is itself an object, and its class is `type`.

## 2. Class creation foundations

### Classes are objects

```python
class Course:
    category = "programming"

print(type(Course).__name__)
print(Course.category)
```

Output:

```text
type
programming
```

Practical takeaway: a class can be inspected and manipulated like any other object.

### The class body executes immediately

```python
print("before")

class Course:
    print("inside class body")
    title = "Python"

print(Course.title)
```

Output:

```text
before
inside class body
Python
```

Practical takeaway: class bodies run at definition time, which is usually import time.

### A descriptor controls attribute access

```python
class PositiveInteger:
    def __set_name__(self, owner, name) -> None:
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("value must be an int")
        if value <= 0:
            raise ValueError("value must be positive")
        setattr(instance, self.storage_name, value)

class Course:
    duration_hours = PositiveInteger()

    def __init__(self, duration_hours: int) -> None:
        self.duration_hours = duration_hours

course = Course(12)
print(course.duration_hours)
```

Output:

```text
12
```

Practical takeaway: descriptors are a clean way to centralize attribute rules.

## 3. Class creation hooks

### `__set_name__`

Lets a descriptor learn the attribute name it was assigned to.

### `__init_subclass__`

Runs when a subclass is defined and is usually simpler than a metaclass for registration or validation.

### Class decorators

Receive the finished class and can register or modify it.

### `__prepare__`

Chooses the namespace used while the class body runs.

### Metaclasses

Control class construction itself.

```python
def title(self: object) -> str:
    return "Python Internals"

Course = type(
    "Course",
    (),
    {
        "category": "programming",
        "title": title,
    },
)

course = Course()
print(type(course).__name__)
print(getattr(course, "title")())
```

Output:

```text
Course
Python Internals
```

## 4. Practical class customization

### Example 1: Dynamic class creation

```python
def title(self: object) -> str:
    return "Python Internals"

Course = type(
    "Course",
    (),
    {
        "category": "programming",
        "title": title,
    },
)

course = Course()
print(type(course).__name__)
print(getattr(course, "title")())
```

Output:

```text
Course
Python Internals
```

### Example 2: `__init_subclass__` for registration

```python
class Parser:
    _registry: dict[str, type["Parser"]] = {}

    def __init_subclass__(cls, *, format_name: str, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if not format_name:
            raise ValueError("format_name must not be empty")
        cls._registry[format_name] = cls

class JsonParser(Parser, format_name="json"):
    pass

print(Parser._registry["json"].__name__)
```

Output:

```text
JsonParser
```

### Example 3: Class decorator registration

```python
registry: dict[str, type[object]] = {}

def registered(cls):
    registry[cls.__name__] = cls
    return cls

@registered
class Course:
    pass

print(registry["Course"].__name__)
```

Output:

```text
Course
```

- Descriptors power `property`, ORMs, validation fields, and computed attributes.
- `__init_subclass__` is good for subclass registration and simple class rules.
- Class decorators are good for registration or small class-level transformations.
- Metaclasses are used by frameworks that need to control class construction deeply.

## 5. Metaprogramming mistakes

### Mistake 1: Reaching for a metaclass first

Use a normal function, descriptor, decorator, or `__init_subclass__` first.

### Mistake 2: Doing side effects during class creation

Avoid network calls, database work, or other unpredictable work when the class is being defined.

### Mistake 3: Using metaclasses when ABCs already solve the problem

If you just need an abstract interface, `ABC` is clearer.

### Mistake 4: Making descriptor behavior surprising

Attribute hooks should be predictable and documented.

## 6. Customization decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Simple transformation | function | easiest to understand | no transformation is needed |
| Attribute control | descriptor | centralizes field rules | the attribute is plain data |
| Subclass registration | `__init_subclass__` | simpler than metaclass | non-subclass classes need the rule |
| Final class decoration | class decorator | clean and local | subclasses must inherit the rule automatically |
| Interface enforcement | ABC | explicit and familiar | structural typing is enough |
| Deep class-family control | metaclass | powerful but rare | a simpler hook works |

Selection rule:

- Prefer the simplest hook that solves the problem.
- Use a metaclass only when simpler tools cannot enforce the requirement.

## 7. Safety and maintainability

- Keep class-creation hooks deterministic.
- Avoid hidden I/O in class bodies, decorators, or metaclasses.
- Document any registry or automatic behavior clearly.
- Be careful with metaclass conflicts when mixing frameworks.

Best practices:

- Learn descriptors before metaclasses.
- Prefer `__init_subclass__` and decorators first.
- Keep advanced hooks narrow and intentional.

## 8. Metaclass behavior

### `__prepare__`

This hook can customize the namespace used while the class body executes.

```python
class PreparedMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        print(f"prepare {name}")
        return {}

class Course(metaclass=PreparedMeta):
    pass
```

Output:

```text
prepare Course
```

### ABCs already use a metaclass

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def find(self, course_id: str) -> str | None:
        raise NotImplementedError

print("defined")
```

Output:

```text
defined
```

## 9. Mental model

| Hook | Best use |
| --- | --- |
| Descriptor | control one attribute |
| `__init_subclass__` | register or validate subclasses |
| Class decorator | transform one finished class |
| `__prepare__` | customize class namespace |
| Metaclass | rare deep class-construction control |

## 10. Descriptor lookup precedence

A data descriptor defines `__set__` or `__delete__` and takes precedence over an
instance dictionary entry. A non-data descriptor defines only `__get__`; an
instance attribute can shadow it.

```python
class NonDataDescriptor:
    def __get__(self, instance: object, owner: type) -> str:
        return "descriptor"


class Example:
    value = NonDataDescriptor()


example = Example()
print(example.value)
example.__dict__["value"] = "instance"
print(example.value)
```

Output:

```text
descriptor
instance
```

Functions are non-data descriptors, which is how attribute access creates bound
methods. `property` is a data descriptor, so normal instance assignment cannot
silently bypass its setter policy.
