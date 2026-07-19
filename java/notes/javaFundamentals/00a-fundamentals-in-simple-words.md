# Java Fundamentals in Simple Words

Read this before the detailed fundamentals chapters.

## The Big Picture

A Java program is a list of instructions written inside classes. Data is kept in variables. Methods group reusable instructions. Conditions choose what happens. Loops repeat work.

That sentence describes most beginner Java programs.

## 1. A Value and a Variable

A **value** is data such as `10`, `true`, or `"Asha"`.

A **variable** is a name used to hold one value:

```java
int age = 20;
String name = "Asha";
System.out.println(name + " is " + age);
// Output: Asha is 20
```

Read `int age = 20;` as: create an integer variable named `age` and give it the value `20`.

## 2. A Type Is a Rule

A type tells Java which values and operations are allowed.

```java
int count = 3;
boolean finished = false;
String course = "Java";
```

- `int`: whole number
- `boolean`: `true` or `false`
- `String`: text

Java rejects the wrong type before the program runs:

```java
// int count = "three"; // compile-time error
```

## 3. An Expression Produces a Value

```java
int total = 10 + 5;
boolean adult = age >= 18;
```

- `10 + 5` produces `15`
- `age >= 18` produces `true` or `false`

An expression is a value-producing piece of code.

## 4. A Condition Makes a Choice

```java
int score = 75;

if (score >= 70) {
    System.out.println("Passed");
} else {
    System.out.println("Try again");
}
// Output: Passed
```

Java checks the condition. Exactly one branch runs.

## 5. A Loop Repeats Work

```java
for (int lesson = 1; lesson <= 3; lesson++) {
    System.out.println("Lesson " + lesson);
}
// Output:
// Lesson 1
// Lesson 2
// Lesson 3
```

The loop starts at `1`, continues while the lesson is at most `3`, and adds `1` after each run.

## 6. A Method Names Reusable Work

```java
static int doubleNumber(int number) {
    return number * 2;
}

System.out.println(doubleNumber(5));
// Output: 10
```

- `int number`: input
- `int` before the method name: result type
- `return`: sends the answer back
- `doubleNumber(5)`: method call

## 7. A Class Describes a Kind of Object

```java
final class Course {
    private final String title;

    Course(String title) {
        this.title = title;
    }

    String title() {
        return title;
    }
}

Course course = new Course("Java");
System.out.println(course.title());
// Output: Java
```

- `class Course`: defines a new type
- `new Course("Java")`: creates an object
- `title`: state stored by the object
- `title()`: behavior that reads the state

## 8. Java Passes Values to Methods

Java is always pass-by-value. The method receives a copy of the value.

For an object variable, the copied value is a reference to the same object. That is why a method can mutate the shared object but cannot replace the caller's variable.

Do not worry if this feels difficult now. Read the dedicated pass-by-value chapter after variables, methods, arrays, and objects.

## 9. Errors Have Different Times

- **compile-time error:** Java rejects invalid code before running it
- **runtime exception:** compiled code starts, then an invalid operation fails
- **logic bug:** code runs but produces the wrong answer

```java
int divisor = 0;
// System.out.println(10 / divisor); // ArithmeticException at runtime
```

## Beginner to Expert Path

1. **Beginner:** write values, variables, conditions, loops, and methods.
2. **Developing programmer:** understand arrays, strings, objects, scope, and errors.
3. **Working developer:** choose clear names, validate inputs, test behavior, and keep methods focused.
4. **Expert:** understand memory, initialization, numeric limits, API contracts, performance, and tradeoffs.

Expert knowledge sits on top of simple behavior. Never skip the runnable examples to memorize internals.

## Ready for the Detailed Notes?

Predict this output:

```java
int total = 0;
for (int number = 1; number <= 3; number++) {
    total += number;
}
System.out.println(total);
// Output: 6
```

`total` becomes `1`, then `3`, then `6`.
