# Java Methods - Beginner to Interview Level

Java calls functions **methods** because they are declared inside a class, interface, record, or enum.

A method gives a name to reusable behavior.

## 1) Method Parts

```java
static int add(int left, int right) {
    return left + right;
}

System.out.println(add(20, 22));
// Output: 42
```

- `static`: method belongs to the class
- `int`: return type
- `add`: method name
- `left`, `right`: parameters
- `return`: sends the result to the caller

## 2) Parameters and Arguments

A parameter is the variable in the method declaration. An argument is the value supplied by a caller.

```java
static String greet(String name) { // name is a parameter
    return "Hello " + name;
}
System.out.println(greet("Asha")); // "Asha" is an argument
// Output: Hello Asha
```

Validate arguments at the beginning when invalid data should stop the operation.

## 3) `void` Methods

`void` means the method does not return a value.

```java
static void printStatus() {
    System.out.println("ready");
}
printStatus();
// Output: ready
```

## 4) Instance vs Static Method

An instance method works with one object's state. A static method has no current object.

```java
final class Counter {
    private int value;
    void increment() { value++; }
    int value() { return value; }
}
Counter counter = new Counter();
counter.increment();
System.out.println(counter.value());
// Output: 1
```

## 5) Java Is Pass-by-Value

Java always copies the argument value into the parameter.

```java
static void change(int number, List<String> names) {
    number = 99;
    names.add("Ravi");
    names = new ArrayList<>();
}
int number = 10;
List<String> names = new ArrayList<>(List.of("Asha"));
change(number, names);
System.out.println(number);
System.out.println(names);
// Output:
// 10
// [Asha, Ravi]
```

The number copy changed only inside the method. The copied list reference still identified the caller's list, so mutation was visible. Reassigning the parameter did not replace the caller's variable.

## 6) Method Overloading

Overloading means several methods share a name but have different parameter lists.

```java
static int area(int side) { return side * side; }
static int area(int width, int height) { return width * height; }
System.out.println(area(4));
System.out.println(area(4, 5));
// Output:
// 16
// 20
```

Return type alone cannot distinguish overloads.

## 7) Overload Selection

The compiler chooses the most specific applicable overload. A useful beginner order is:

1. exact fixed-parameter match
2. primitive widening, such as `int` to `long`
3. boxing/unboxing, such as `int` to `Integer`
4. varargs

```java
static String choose(long value) { return "long"; }
static String choose(Integer value) { return "Integer"; }
System.out.println(choose(10));
// Output: long
// Primitive widening is preferred here over boxing.
```

Passing `null` to unrelated reference overloads can be ambiguous and fail compilation.

## 8) Varargs

Varargs let callers provide zero or more values. Inside the method they are an array.

```java
static int sum(int... values) {
    return Arrays.stream(values).sum();
}
System.out.println(sum(1, 2, 3));
// Output: 6
```

The varargs parameter must be last.

## 9) Recursion

A recursive method calls itself. It needs a base case that stops the calls.

```java
static int factorial(int value) {
    if (value < 0) throw new IllegalArgumentException("value must be non-negative");
    if (value <= 1) return 1;
    return value * factorial(value - 1);
}
System.out.println(factorial(5));
// Output: 120
```

Deep recursion can overflow the thread stack. Prefer a loop when depth may be large.

## 10) Argument Evaluation Order

Java evaluates method arguments from left to right.

```java
static void print(int first, int second) {
    System.out.println(first + ", " + second);
}
int value = 1;
print(value++, ++value);
// Output: 1, 3
```

Avoid writing production calls with several mutations; the code is legal but hard to read.

## 11) Method Design Rules

- one clear responsibility
- intention-revealing name
- few parameters
- explicit validation
- no surprising hidden mutation
- small enough to understand without scrolling through unrelated work
- return a result instead of mutating an output holder when possible

## Interview Checklist

Know overriding vs overloading, static vs instance methods, pass-by-value, widening vs boxing vs varargs, recursion, left-to-right argument evaluation, and why returning from `finally` is unsafe.
