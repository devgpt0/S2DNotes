# Theory Interview Questions

## LEVEL 1 (Fundamentals — expected instant answers)

### Data Types & Variables
1. What is the difference between primitive and reference types in Java?
2. Where are primitive variables stored vs objects stored?
3. What exactly does a variable store for a reference type?
4. Can a primitive be null? Why or why not?
5. What is the default value of primitive types?
6. What is the default value of reference types?

### Memory Model Basics
1. What is the difference between stack memory and heap memory?
2. What is stored in the stack frame of a method?
3. What happens in memory when you write: `String s = "hello";`
4. How is an array stored in memory?

### Execution Model Basics
1. How does Java execute a simple assignment statement?
2. What happens internally when a method is called?
3. What does “Java is pass-by-value” mean?
4. What is copied during assignment for a primitive?
5. What is copied during assignment for an object?

## LEVEL 2 (Intermediate — real interview filter)

### Execution Model (Core Focus)
1. Explain step-by-step what happens during: `Box b = a;`
2. What is the difference between mutation and reassignment in terms of memory?
3. In a method call, what exactly is passed: object, reference, or value?
4. Why does modifying an object inside a method affect the caller, but reassigning it does not?
5. What happens in memory when: `x = new Box();`

### Memory Model (Deep Understanding)
1. How many objects are created in this scenario?
   `Box a = new Box();`
   `Box b = a;`
2. What is aliasing in Java? Why is it dangerous?
3. What is the difference between copying a reference and copying an object?
4. How do you reason about shared state in memory?
5. What is the lifecycle of an object after no references point to it?

### Data Types & Behavior
1. Why are arrays considered reference types?
2. What happens when you assign one array to another variable?
3. What is the difference between `==` and `.equals()`?
4. Why is `.equals()` needed for objects?
5. What happens when you compare two objects using `==`?

## LEVEL 3 (Advanced — strong candidate differentiator)

### JVM Behavior & Optimization
1. What is Integer caching in Java? Why does it exist?
2. What is the range of Integer cache and why that range?
3. What is the String pool and how does it work?
4. What is the difference between `"abc"` and `new String("abc")`?
5. What does `String.intern()` do internally?

### Execution Nuances
1. What is the difference between compile-time evaluation and runtime evaluation?
2. Why does `"a" + "b"` behave differently from `new String("a") + "b"`?
3. Why are wrapper classes (like Integer) immutable?
4. What happens internally when autoboxing occurs?

### Memory & Performance Thinking
1. What causes excessive object creation in Java?
2. How does object allocation affect performance?
3. What is GC (Garbage Collection) and when does it run?
4. What is object reachability?

### Identity & Correctness
1. Why should you not rely on `==` for object comparison?
2. When is it safe to use `==`?

### Edge-case Reasoning
1. Why does modifying a loop variable not affect the original array/object?
2. How does immutability affect memory behavior?
3. What happens if multiple references point to the same object and one modifies it?
