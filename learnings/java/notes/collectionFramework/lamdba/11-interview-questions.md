# 11 - Interview Questions (Lambda)

## 1) What is a lambda in Java

Anonymous function used to provide implementation of functional interface.

## 2) Difference: Lambda vs Anonymous Class

- lambda is concise
- lambda does not create separate `this` context
- anonymous class can define extra state/methods

## 3) What is functional interface

Interface with one abstract method; can include default/static methods.

## 4) Why effectively final

Captured local variables are immutable snapshots for safety and lifecycle reasons.

## 5) Method reference vs lambda

Method reference is shorthand; use it when it is clearer.

## 6) Can lambda throw checked exception

Not directly unless target method declares it; usually wrap or handle.

## 7) Lambda and Stream side effects

Avoid side effects, especially in parallel streams.

## 8) Common coding prompts

1. Sort objects by field using lambda
2. Group list by key using `Collectors.groupingBy`
3. Count frequencies using `Map.merge`
4. Filter/map/reduce data pipeline
5. Build mini strategy pattern using functional interface

