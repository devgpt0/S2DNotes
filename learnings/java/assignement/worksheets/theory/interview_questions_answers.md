THEORY ANSWERS
🔷 LEVEL 1
🔹 Data Types & Variables

Variables store values or references?
→ References to objects

Mutable vs Immutable
→ Mutable: can change in-place
→ Immutable: cannot change, new object created

Examples
→ Mutable: list, dict, set
→ Immutable: int, str, tuple

Can variables change type? Why?
→ Yes; variables are untyped references, objects have types

list vs tuple vs set
→ list: ordered, mutable
→ tuple: ordered, immutable
→ set: unordered, unique elements

🔹 Memory Model

Where are objects stored?
→ Heap

What does a variable hold?
→ Reference (pointer) to object

a = [1, 2] memory behavior
→ list object created in heap → a points to it

Reference counting
→ each object tracks number of references; when 0 → eligible for deletion

🔹 Execution Model

Assignment
→ binds name to object (no copy unless explicitly done)

=, ==, is
→ =: binding
→ ==: value equality
→ is: identity (same object)

Passing variable to function
→ reference is passed (object not copied)

Pass-by-value or reference?
→ pass-by-object-reference (reference passed by value)

🔷 LEVEL 2
🔹 Execution Model

b = a
→ copies reference → both point to same object

Mutation vs Rebinding
→ mutation: modify same object
→ rebinding: new object, reference changes

Why list modification affects caller?
→ same object shared

Why reassignment doesn’t affect caller?
→ only local reference changes

a = a + [1] vs a.append(1)
→ +: new object
→ append: in-place mutation

🔹 Memory Model

Aliasing
→ multiple names pointing to same object

Shallow vs Deep copy
→ shallow: outer copy, inner shared
→ deep: full recursive copy

Nested list slicing
→ new outer list, inner lists shared

Memory cleanup
→ reference counting + garbage collector

Garbage collection
→ cleans cyclic references not handled by ref counting

🔹 Data Types Behavior

Tuple with mutable elements
→ tuple immutable, but elements can be mutable

Modify list inside tuple
→ allowed (list mutates, tuple unchanged)

copy.copy() vs copy.deepcopy()
→ shallow vs recursive copy

Mutable default arguments issue
→ evaluated once → shared across calls

Hashability
→ object must be immutable to be hashable (used as dict key/set element)

🔷 LEVEL 3
🔹 Internals & Optimization

Object interning
→ reuse of objects (small ints, some strings)

Small integers shared
→ optimization for performance (-5 to 256 typically)

String sharing
→ literals may be interned and reused

Use of is for comparison
→ only for identity, not value

🔹 Execution Nuances

Late binding in closures
→ variables looked up at call time, not definition

Lambda loop issue
→ all lambdas reference same final variable value

Function definition vs execution
→ definition creates function object; execution runs body

Default arguments evaluation
→ evaluated once at function definition time

🔹 Memory & Performance

Unnecessary object creation
→ repeated rebinding (a = a + ...)

Why a = a + [x] slower
→ creates new list each time (O(n))

Shallow vs deep copy cost
→ shallow: O(n)
→ deep: O(total nested elements)

Memory for large objects
→ managed via heap + reference counting + GC

🔹 Identity & Correctness

Identity vs equality
→ identity: same object (is)
→ equality: same value (==)

When to use is
→ for None or identity checks

Problems with shared references
→ unintended side effects due to mutation

🔹 Edge Cases

Lambda loop behavior

funcs = []
for i in range(3):
    funcs.append(lambda: i)

→ all return last value (late binding)

Multiple references to mutable object
→ mutation affects all references

Nested object modification
→ shallow copies share inner objects → changes propagate