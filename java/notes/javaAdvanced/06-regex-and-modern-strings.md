# 06 - Regular Expressions and Modern Strings

## 1) Compile Reused Patterns

```java
Pattern orderId = Pattern.compile("ORD-[0-9]{4}");
System.out.println(orderId.matcher("ORD-2048").matches());
System.out.println(orderId.matcher("xORD-2048").matches());
// Output:
// true
// false
```

`matches()` checks the whole input. `find()` searches for a matching region.

## 2) Capturing Groups

```java
Matcher matcher = Pattern.compile("([A-Z]+)-(\\d+)").matcher("INV-42");
if (matcher.matches()) {
    System.out.println(matcher.group(1));
    System.out.println(matcher.group(2));
}
// Output:
// INV
// 42
```

## 3) Safe Replacement

```java
String secret = "token=abc123";
System.out.println(secret.replaceAll("token=[^&\\s]+", "token=***"));
// Output: token=***
```

Use `Pattern.quote` for literal user-provided search text and `Matcher.quoteReplacement` for literal replacement text.

## 4) Text Blocks

```java
String json = """
        {"status":"ok"}
        """;
System.out.println(json.strip());
// Output: {"status":"ok"}
```

Text blocks improve readability but do not validate JSON or prevent injection.

## 5) Formatting

```java
String message = "Order %d costs %.2f".formatted(7, 19.5);
System.out.println(message);
// Output: Order 7 costs 19.50
```

Use `NumberFormat` for locale-sensitive numbers and `DateTimeFormatter` for dates.

## 6) Regex Safety

- Set input size limits before expensive matching.
- Avoid nested ambiguous quantifiers such as `(a+)+`.
- Prefer simple string methods for literal prefix, suffix, and equality checks.
- Treat regex validation as syntax validation, not authorization.
