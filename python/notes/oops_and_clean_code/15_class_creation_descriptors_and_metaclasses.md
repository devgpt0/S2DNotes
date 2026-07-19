# Class Creation, Descriptors, and Metaclasses

Metaclasses are advanced class-construction hooks. Most application problems should use a normal function, decorator, base class, or `__init_subclass__` first.

## 1. Classes Are Objects

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

By default, `type` is the class that creates class objects. An instance has a class; a class also has a class, called its metaclass.

## 2. Class Body Execution

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

The class body executes immediately when Python reaches the class statement, commonly during module import.

## 3. Class Creation Flow

Simplified flow:

```text
resolve bases and metaclass
    -> metaclass.__prepare__ creates class namespace
    -> execute class body in that namespace
    -> metaclass.__new__ creates class object
    -> metaclass.__init__ initializes class object
    -> descriptor.__set_name__ hooks complete
    -> parent.__init_subclass__ hooks run
    -> decorators receive and may replace the class
```

Exact hook ordering has details, but this model explains where each customization belongs.

## 4. Dynamic Class Creation with `type`

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
print(course.title())
```

Output:

```text
Course
Python Internals
```

This is roughly what a class statement ultimately asks a metaclass to do. A class statement is clearer for ordinary code.

## 5. Descriptors Power Attribute Behavior

A descriptor is an object defining one or more of `__get__`, `__set__`, or `__delete__`.

```python
from typing import Self, overload


class PositiveInteger:
    def __init__(self) -> None:
        self._storage_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self._storage_name = f"_{name}"

    @overload
    def __get__(self, instance: None, owner: type[object]) -> Self: ...

    @overload
    def __get__(self, instance: object, owner: type[object]) -> int: ...

    def __get__(self, instance: object | None, owner: type[object]) -> Self | int:
        if instance is None:
            return self
        value = getattr(instance, self._storage_name)
        if not isinstance(value, int):
            raise RuntimeError("descriptor storage contains a non-integer")
        return value

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("value must be an int")
        if value <= 0:
            raise ValueError("value must be positive")
        setattr(instance, self._storage_name, value)


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

Functions, `property`, class methods, static methods, and many ORM fields use descriptor behavior.

The overloaded `__get__` signatures distinguish class access (the descriptor itself) from instance access (an integer).

## 6. Attribute Lookup Priority

Simplified instance lookup:

1. data descriptor on the class (`__set__` or `__delete__` exists);
2. instance dictionary;
3. non-data descriptor or ordinary class attribute;
4. base classes according to MRO;
5. `__getattr__` fallback.

This is why a `property` can control assignment even when an instance has a dictionary.

## 7. `__set_name__`

`__set_name__` tells a descriptor which class attribute owns it. This avoids manually repeating the field name.

```python
class NamedField:
    def __set_name__(self, owner: type[object], name: str) -> None:
        print(f"{owner.__name__}.{name}")


class Course:
    title = NamedField()
```

Output:

```text
Course.title
```

## 8. Prefer `__init_subclass__` for Subclass Registration

```python
class Parser:
    _registry: dict[str, type["Parser"]] = {}
    format_name: str

    def __init_subclass__(cls, *, format_name: str, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not format_name:
            raise ValueError("format_name must not be empty")
        if format_name in cls._registry:
            raise ValueError(f"duplicate format_name: {format_name}")

        cls.format_name = format_name
        cls._registry[format_name] = cls


class JsonParser(Parser, format_name="json"):
    pass


print(Parser._registry["json"].__name__)
```

Output:

```text
JsonParser
```

This is simpler than a custom metaclass when only subclasses of one base class need a hook.

Registration occurs at import/class-definition time. Define duplicate behavior explicitly and avoid hidden network or database work.

## 9. Class Decorator

```python
registry: dict[str, type[object]] = {}


def registered[T](cls: type[T]) -> type[T]:
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

The decorator preserves the decorated class type while registering the completed class. Registration still happens at import time, so duplicate and import-order behavior need an explicit policy.

Class decorators are appropriate when the final class alone needs transformation and subclasses do not automatically inherit a construction policy.

## 10. First Metaclass

```python
class AnnouncingMeta(type):
    def __new__(
        metaclass,
        name: str,
        bases: tuple[type[object], ...],
        namespace: dict[str, object],
        **kwargs: object,
    ) -> "AnnouncingMeta":
        print(f"creating {name}")
        return super().__new__(metaclass, name, bases, namespace, **kwargs)


class Course(metaclass=AnnouncingMeta):
    pass


print(Course.__name__)
```

Output:

```text
creating Course
Course
```

The metaclass runs when the class is created, not when instances are created.

## 11. Validate a Class Contract

```python
class HandlerMeta(type):
    def __new__(
        metaclass,
        name: str,
        bases: tuple[type[object], ...],
        namespace: dict[str, object],
        **kwargs: object,
    ) -> "HandlerMeta":
        created = super().__new__(metaclass, name, bases, namespace, **kwargs)

        if bases:
            handle = namespace.get("handle")
            if not callable(handle):
                raise TypeError(f"{name} must define handle")

        return created


class BaseHandler(metaclass=HandlerMeta):
    pass


class CourseHandler(BaseHandler):
    def handle(self, course_id: str) -> str:
        return course_id


print(CourseHandler().handle("python"))
```

Output:

```text
python
```

For most application interfaces, an abstract base class or `Protocol` provides a clearer contract. Metaclass validation is justified when a framework must enforce class-definition rules immediately.

## 12. `__prepare__`

A metaclass can choose the mapping used for the class body namespace.

```python
from collections.abc import MutableMapping


class PreparedMeta(type):
    @classmethod
    def __prepare__(
        metaclass,
        name: str,
        bases: tuple[type[object], ...],
        **kwargs: object,
    ) -> MutableMapping[str, object]:
        print(f"prepare {name}")
        return {}


class Course(metaclass=PreparedMeta):
    pass
```

Output:

```text
prepare Course
```

Modern dictionaries preserve insertion order, so a custom ordered namespace is rarely needed. A specialized namespace can detect duplicate definitions or collect declarations, but it increases framework magic.

## 13. Metaclass Conflicts

If a class inherits from bases with incompatible metaclasses, Python cannot choose one automatically and raises a metaclass-conflict `TypeError`.

The selected metaclass must be a subclass of the metaclasses of all bases. Avoid combining metaclass-heavy frameworks casually. Composition or adapter boundaries are often simpler.

## 14. Abstract Base Classes Already Use a Metaclass

`abc.ABC` uses `ABCMeta`. Usually you should use the `ABC` API rather than writing another metaclass.

```python
from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def find(self, course_id: str) -> str | None:
        raise NotImplementedError
```

The existing mechanism prevents instantiation until abstract methods are implemented.

## 15. Generic Classes and Frameworks

Typing, dataclasses, enums, ORMs, validation frameworks, and web frameworks can use class-creation hooks. Prefer their public documented API instead of depending on undocumented metaclass internals.

## 16. Common Misuses

- singleton metaclass for ordinary dependency lifetime;
- global registry hidden behind import side effects;
- automatic field transformation that surprises type checkers;
- network or database calls during class creation;
- metaclass used where a function or decorator works;
- incompatible metaclasses from multiple frameworks;
- changing class semantics without documentation or tests.

## 17. Decision Guide

Use:

- normal function: transform data or build an object explicitly;
- descriptor/property: control one attribute's access;
- class decorator: transform one completed class;
- `__init_subclass__`: validate/register subclasses of one base;
- abstract base class/protocol: express an interface;
- metaclass: control the creation of a family of classes when simpler hooks cannot enforce the requirement.

## 18. Testing Class-Creation Hooks

Test:

- valid class creation;
- missing or invalid declaration rejection;
- duplicate registration;
- inheritance behavior;
- class decorator/metaclass ordering if relied upon;
- import order and repeated import;
- static type-checker behavior;
- metaclass compatibility with other required bases.

## Final Rules

- understand descriptors before metaclasses;
- remember class bodies execute at definition/import time;
- prefer `Protocol`, ABC, decorator, or `__init_subclass__` first;
- keep class-creation hooks deterministic and free of external I/O;
- fail immediately on an invalid class contract;
- document registry, inheritance, and ownership behavior;
- use a metaclass only for a demonstrated class-family construction requirement.
