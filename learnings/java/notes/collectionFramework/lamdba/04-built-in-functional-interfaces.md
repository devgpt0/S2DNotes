# 04 - Built-In Functional Interfaces

Java keeps the most common lambda shapes in `java.util.function`. Learn them by the question they answer.

## 1. `Predicate<T>`: Does This Value Pass?

```java
Predicate<String> notBlank = text -> !text.isBlank();
System.out.println(notBlank.test("Java"));
System.out.println(notBlank.test(""));
// Output:
// true
// false
```

- input: one `T`
- result: `boolean`
- run it with: `test`

Common use: filtering and validation rules.

## 2. `Function<T, R>`: Turn This into That

```java
Function<String, Integer> length = text -> text.length();
System.out.println(length.apply("lambda"));
// Output: 6
```

- input: one `T`
- result: one `R`
- run it with: `apply`

Here, `T` is `String` and `R` is `Integer`.

## 3. `Consumer<T>`: Use This Value, Return Nothing

```java
Consumer<String> print = text -> System.out.println(text);
print.accept("Hello");
// Output: Hello
```

- input: one `T`
- result: none (`void`)
- run it with: `accept`

Common use: sending a value to an output or callback. Keep side effects deliberate.

## 4. `Supplier<T>`: Give Me a Value

```java
Supplier<String> courseName = () -> "Java";
System.out.println(courseName.get());
// Output: Java
```

- input: none
- result: one `T`
- run it with: `get`

Common use: lazy creation or a factory.

## One Table to Remember

| Interface | Input | Result | Method | Think |
|---|---|---|---|---|
| `Predicate<T>` | `T` | `boolean` | `test` | “Does it pass?” |
| `Function<T, R>` | `T` | `R` | `apply` | “Convert it.” |
| `Consumer<T>` | `T` | `void` | `accept` | “Use it.” |
| `Supplier<T>` | none | `T` | `get` | “Create/get it.” |

## Operators: Same Input and Result Type

`UnaryOperator<T>` is a `Function<T, T>`:

```java
UnaryOperator<Integer> square = number -> number * number;
System.out.println(square.apply(5));
// Output: 25
```

`BinaryOperator<T>` combines two values of the same type into that type:

```java
BinaryOperator<Integer> add = (left, right) -> left + right;
System.out.println(add.apply(4, 6));
// Output: 10
```

Use these names when “same type in and out” helps the reader.

## `Bi` Interfaces: Two Inputs

```java
BiPredicate<String, Integer> hasMinimumLength =
        (text, minimum) -> text.length() >= minimum;
BiFunction<Integer, Integer, String> scoreLabel =
        (score, total) -> score + "/" + total;
BiConsumer<String, Integer> printScore =
        (name, score) -> System.out.println(name + ": " + score);

System.out.println(hasMinimumLength.test("Java", 4));
System.out.println(scoreLabel.apply(8, 10));
printScore.accept("Asha", 90);
// Output:
// true
// 8/10
// Asha: 90
```

The `Bi` prefix means two inputs. It does not mean two results.

## Primitive Specializations

Generic interfaces use wrapper types such as `Integer`. Numeric hot paths sometimes use primitive specializations:

```java
IntUnaryOperator addTen = number -> number + 10;
System.out.println(addTen.applyAsInt(5));
// Output: 15
```

Common names:

- `IntPredicate`: `int` -> `boolean`
- `IntFunction<R>`: `int` -> `R`
- `ToIntFunction<T>`: `T` -> `int`
- `IntUnaryOperator`: `int` -> `int`

Choose them first when the API clearly models primitive numeric work. Claim a performance benefit only after measurement.

## How to Choose

Ask in order:

1. How many inputs?
2. Is there a result?
3. Is the result always `boolean`?
4. Are input and result the same type?
5. Is a primitive specialization clearer?

Example: “Take one `Course` and return its title.” That is `Function<Course, String>`.

## Complete Example

```java
import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;

public class BuiltInFunctionsDemo {
    public static void main(String[] args) {
        Predicate<String> longName = name -> name.length() >= 4;
        Function<String, String> upper = String::toUpperCase;

        List<String> result = List.of("Go", "Java", "SQL")
                .stream()
                .filter(longName)
                .map(upper)
                .toList();

        System.out.println(result);
    }
}
// Output: [JAVA]
```

## Expert Understanding

- interface method names differ, so learn `test`, `apply`, `accept`, and `get`
- `andThen`, `compose`, `and`, `or`, and `negate` can combine compatible behavior
- checked-exception rules come from the interface method
- a domain-specific interface is better when it adds a real named promise, not merely a new type alias

## Quick Memory Card

- test -> `Predicate`
- transform -> `Function`
- consume -> `Consumer`
- supply -> `Supplier`
- same type in/out -> operator
- two inputs -> an interface whose name starts with `Bi`, such as `BiFunction`
