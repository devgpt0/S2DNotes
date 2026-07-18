# 06 - Strings, String Pool, and Builders

## Immutability

`String` is immutable. Operations return a new string; the original value does not change.

```java
String value = "java";
value.toUpperCase();
System.out.println(value);
System.out.println(value.toUpperCase());
// Output:
// java
// JAVA
```

## String Pool and `intern`

```java
String literalA = "java";
String literalB = "java";
String heap = new String("java");
System.out.println(literalA == literalB);
System.out.println(literalA == heap);
System.out.println(literalA == heap.intern());
// Output:
// true
// false
// true
```

Use `equals` for content. `==` compares references.

## Compile-Time Concatenation

```java
String first = "ja" + "va";
String part = "ja";
String second = part + "va";
System.out.println(first == "java");
System.out.println(second == "java");
// Output:
// true
// false
```

The compiler folds constant expressions. Runtime concatenation creates a result dynamically.

## `StringBuilder` and `StringBuffer`

```java
StringBuilder builder = new StringBuilder();
for (int i = 1; i <= 3; i++) builder.append(i);
System.out.println(builder);
// Output: 123
```

- `StringBuilder`: mutable, not synchronized, preferred for local construction.
- `StringBuffer`: synchronized legacy alternative; synchronization rarely makes a multi-step workflow correct.
- Modern `+` is readable for a small fixed expression; use a builder for repeated mutation in a loop.

## Frequently Asked Methods

```java
String text = " Java Interview ";
System.out.println(text.strip());
System.out.println(text.substring(1, 5));
System.out.println("a,b,,c".split(",", -1).length);
// Output:
// Java Interview
// Java
// 4
```

`strip` is Unicode-aware; `trim` removes characters with code points up to U+0020. `split` accepts a regular expression.
