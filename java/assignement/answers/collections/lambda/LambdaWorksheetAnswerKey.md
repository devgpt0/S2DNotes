# Answer Key - LambdaWorksheet

## Tricky Predict the Output

1. `Hi`
2. `16`
3. `false`
4. `JAVA`
5. `Hi!`
6. `13`
7. `16`
8. `[a, ccc]`
9. `[BB, CCC]`
10. `2`
11. `42`
12. `15`
13. Compile-time error (captured variable is not effectively final)
14. `ConcurrentModificationException`
15. `15`

## MCQ Answers

1. B  
2. A  
3. B  
4. B  
5. C  
6. C  
7. B  
8. B  
9. B  
10. B  
11. B  
12. A  
13. B  
14. B  
15. B

## Interview Key Points

1. Reduced boilerplate for behavior passing vs anonymous classes.
2. Functional interface = one abstract method target for lambda.
3. Method reference is shorthand when lambda just calls existing method.
4. Locals captured by value snapshot; must be effectively final.
5. `Function` transform, `Consumer` side-effect, `Supplier` source, `Predicate` test.
6. `andThen`: current then next; `compose`: next then current.
7. Avoid side effects in stream intermediate ops.
8. Wrap checked exceptions or handle inside lambda carefully.
9. Primitive specializations reduce boxing overhead.
10. Real-world: validation rules, sorting/grouping, map aggregation (`merge`, `compute`).

