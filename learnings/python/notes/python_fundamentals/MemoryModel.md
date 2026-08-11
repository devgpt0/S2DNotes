# PYTHON - MEMORY MODEL

Python programs work with objects and references. Exact memory layout is an implementation detail.

## 1. Names Reference Objects

A namespace maps names to objects.

```python
number = 10
alias = number

print(number == alias)
print(number is alias)
```

Output:

```text
True
True
```

Both names currently reference the same integer object.

## 2. Object State, Type, and Identity

Every object has:

- a type that defines behavior;
- a value or state;
- an identity that distinguishes it from other objects.

```python
first = [1, 2]
second = [1, 2]

print(type(first).__name__)
print(first == second)
print(first is second)
```

Output:

```text
list
True
False
```

The lists have equal state but different identities.

## 3. `id()`

`id(object)` returns an identity value unique during that object's lifetime.

```python
items = [1, 2]
alias = items
copy = [1, 2]

print(id(items) == id(alias))
print(id(items) == id(copy))
```

Output:

```text
True
False
```

Do not treat `id()` as a permanent memory address or persistent identifier.

## 4. Aliasing

Aliasing occurs when multiple references point to one mutable object.

```python
original = [1, 2]
alias = original
alias.append(3)

print(original)
print(alias)
```

Output:

```text
[1, 2, 3]
[1, 2, 3]
```

Mutation through either name is visible through both.

## 5. Rebinding Does Not Change the Old Object

Rebinding moves one name to another object.

```python
original = [1, 2]
alias = original
alias = [9]

print(original)
print(alias)
```

Output:

```text
[1, 2]
[9]
```

## 6. Mutable Objects

Mutation changes object state while preserving identity.

```python
items = [1, 2]
identity_before = id(items)
items[0] = 9

print(items)
print(id(items) == identity_before)
```

Output:

```text
[9, 2]
True
```

## 7. Immutable Objects

An operation on an immutable object returns another object instead of changing the original.

```python
text = "Py"
identity_before = id(text)
text = text + "thon"

print(text)
print(id(text) == identity_before)
```

Output:

```text
Python
False
```

## 8. Object Lifetime

An object remains reachable while at least one live reference can reach it.

```python
items = [1, 2]
alias = items
del items

print(alias)
```

Output:

```text
[1, 2]
```

Deleting one name does not delete an object still referenced elsewhere.

## 9. Garbage Collection

Unreachable objects can be reclaimed. CPython combines reference counting with a cyclic garbage collector.

```python
import gc
import weakref


class Node:
    pass


gc.disable()
node = Node()
node.link = node
reference = weakref.ref(node)
del node

print(reference() is None)
gc.collect()
print(reference() is None)
gc.enable()
```

Output:

```text
False
True
```

The self-reference forms a cycle. Explicit collection reclaims it after external references are removed.

Garbage-collection timing is not a reliable resource-management strategy. Use `with` for files, locks, and connections.

## 10. Assignment Versus Copying

Assignment creates another reference. Copying creates another outer object.

```python
import copy

original = [1, 2]
alias = original
duplicate = copy.copy(original)

print(alias is original)
print(duplicate is original)
print(duplicate == original)
```

Output:

```text
True
False
True
```

## 11. Shallow Copy

A shallow copy creates a new outer container but reuses references to nested objects.

```python
import copy

original = [[1, 2], [3, 4]]
duplicate = copy.copy(original)
duplicate[0].append(9)

print(original)
print(duplicate)
print(original is duplicate)
print(original[0] is duplicate[0])
```

Output:

```text
[[1, 2, 9], [3, 4]]
[[1, 2, 9], [3, 4]]
False
True
```

List slicing, `list.copy()`, and `copy.copy()` make shallow copies.

## 12. Deep Copy

A deep copy recursively copies nested mutable objects while preserving the graph structure.

```python
import copy

original = [[1, 2], [3, 4]]
duplicate = copy.deepcopy(original)
duplicate[0].append(9)

print(original)
print(duplicate)
print(original[0] is duplicate[0])
```

Output:

```text
[[1, 2], [3, 4]]
[[1, 2, 9], [3, 4]]
False
```

Deep copying can be expensive and may be unsuitable for objects that represent external resources.

## 13. Shared Nested Objects

Sequence multiplication repeats references; it does not independently copy nested objects.

```python
rows = [[0] * 2] * 3
rows[0][0] = 1

print(rows)
print(rows[0] is rows[1])
```

Output:

```text
[[1, 0], [1, 0], [1, 0]]
True
```

Create independent rows with a comprehension:

```python
rows = [[0] * 2 for _ in range(3)]
rows[0][0] = 1

print(rows)
print(rows[0] is rows[1])
```

Output:

```text
[[1, 0], [0, 0], [0, 0]]
False
```

## 14. Function Calls Share Objects

Arguments create local parameter bindings to the same objects.

```python
def update(items):
    print(items is original)
    items.append(3)


original = [1, 2]
update(original)
print(original)
```

Output:

```text
True
[1, 2, 3]
```

This is often called call-by-sharing.

## 15. Interning Is an Optimization

Python implementations may reuse some immutable objects. Never use identity to compare normal values.

```python
first = "python"
second = "".join(["py", "thon"])

print(first == second)
print(first is second)
```

Output:

```text
True
False
```

The construction forces separate string objects in this example. Correct code still depends only on `==`.

## 16. Memory Size Is Implementation-Dependent

Object overhead, caching, allocation, and garbage collection vary by Python implementation and version.

```python
import platform

implementation = platform.python_implementation()
print(type(implementation).__name__)
print(bool(implementation))
```

Output:

```text
str
True
```

Do not build application logic around a particular object size or collection time.

## 17. Final Mental Model

Think of memory as an object graph:

- objects are nodes;
- references are edges;
- assignment creates or changes an edge;
- mutation changes a node's state;
- shallow copy creates a new outer node with shared inner edges;
- deep copy recreates reachable nodes;
- unreachable nodes become eligible for collection.

For a memory question, ask:

1. Which objects exist?
2. Which names or containers reference them?
3. Which references are shared?
4. Is the operation mutation, rebinding, shallow copy, or deep copy?
5. Is the object still reachable?
