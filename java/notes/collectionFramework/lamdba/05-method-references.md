# 05 - Method References

Method reference is a short form of lambda when lambda only calls one method.

## 1) Types

1. Static method: `ClassName::staticMethod`
2. Instance method of particular object: `instance::method`
3. Instance method of arbitrary object of type: `ClassName::instanceMethod`
4. Constructor reference: `ClassName::new`

## 2) Examples

```java
Function<String, Integer> p1 = Integer::parseInt;
Consumer<String> p2 = System.out::println;
Function<String, String> p3 = String::toUpperCase;
Supplier<ArrayList<String>> p4 = ArrayList::new;
```

## 3) Equivalent Lambda Comparison

```java
Function<String, Integer> a = s -> Integer.parseInt(s);
Function<String, Integer> b = Integer::parseInt;
```

## 4) When To Use

- use method reference when it improves readability
- use normal lambda when logic needs extra steps

