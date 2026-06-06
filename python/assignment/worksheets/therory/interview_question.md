# PYTHON — THEORY INTERVIEW QUESTIONS

## LEVEL 1 (Fundamentals — must be instant)

### Data Types & Variables
1. Are variables in Python storing values or references?
2. What is the difference between mutable and immutable types?
3. Give examples of mutable vs immutable types.
4. Can variables change type in Python? Why?
5. What is the difference between list, tuple, and set?

### Memory Model Basics
1. Where are Python objects stored?
2. What does a variable actually hold in Python?
3. What happens in memory when you write: `a = [1, 2]`
4. What is reference counting in Python?

### Execution Model Basics
1. How does assignment work in Python?
2. What is the difference between `=`, `==`, and `is`?
3. What happens when you pass a variable to a function?
4. Does Python use pass-by-value or pass-by-reference?

## LEVEL 2 (Intermediate — real interview filter)

### Execution Model
1. What happens internally when you write: `b = a`
2. What is the difference between mutation and rebinding?
3. Why does modifying a list inside a function affect the caller?
4. Why does reassigning a variable inside a function not affect the caller?
5. What happens when you use `a = a + [1]` vs `a.append(1)`?

### Memory Model
1. What is aliasing in Python?
2. What is the difference between shallow copy and deep copy?
3. What happens when you copy a nested list using slicing?
4. How does Python handle memory cleanup?
5. What is garbage collection in Python?

### Data Types Behavior
1. Why are tuples immutable but can contain mutable elements?
2. What happens if you modify a list inside a tuple?
3. What is the difference between `copy.copy()` and `copy.deepcopy()`?
4. Why is using mutable default arguments dangerous?
5. What is hashability and why does it matter?

## LEVEL 3 (Advanced — strong candidate differentiator)

### Python Internals & Optimization
1. What is object interning in Python?
2. Why do small integers sometimes share the same memory?
3. Why do some strings share the same object?
4. Should you rely on `is` for value comparison? Why or why not?

### Execution Nuances
1. What is late binding in closures?
2. Why do lambda functions inside loops behave unexpectedly?
3. What happens during function definition vs function execution?
4. When are default arguments evaluated?

### Memory & Performance
1. What causes unnecessary object creation in Python?
2. Why is `a = a + [x]` slower than `a.append(x)`?
3. What is the cost of shallow copy vs deep copy?
4. How does Python manage memory for large objects?

### Identity & Correctness
1. What is the difference between identity and equality?
2. When should you use `is` instead of `==`?
3. What problems arise from shared references?

### Edge-case Reasoning
1. Why does this happen:
   ```python
   funcs = []
   for i in range(3):
       funcs.append(lambda: i)
   ```
2. What happens when multiple variables reference the same mutable object?
3. Why can modifying nested objects affect copies?
