# 05 - Serialization and Safe Data Exchange

## 1) Serialization Means Encoding State

Serialization converts data to a transport or storage format. Deserialization reconstructs data.

Java native serialization is tightly coupled to classes and unsafe for untrusted input. Prefer explicit formats such as JSON, protocol buffers, or a database schema at system boundaries.

## 2) Simple Explicit Text Encoding

```java
record Product(long id, String name) {
    String toCsv() {
        if (name.contains(",")) {
            throw new IllegalArgumentException("name must not contain comma");
        }
        return id + "," + name;
    }
}

System.out.println(new Product(10, "Book").toCsv());
// Output: 10,Book
```

This is intentionally small. Real CSV requires a proven library because quoting rules are more complex.

## 3) Native Serialization Mechanics

```java
record Point(int x, int y) implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
}

Point point = new Point(2, 3);
System.out.println(point);
// Output: Point[x=2, y=3]
// Do not deserialize native Java objects from untrusted bytes.
```

`transient` fields are omitted. `serialVersionUID` identifies a serialization version, but it does not solve schema evolution.

## 4) Strict Boundary Validation

```java
static Product parseProduct(String text) {
    String[] parts = text.split(",", -1);
    if (parts.length != 2 || parts[1].isBlank()) {
        throw new IllegalArgumentException("expected: numeric-id,nonblank-name");
    }
    return new Product(Long.parseLong(parts[0]), parts[1]);
}

System.out.println(parseProduct("10,Book"));
// Output: Product[id=10, name=Book]
```

Validation verifies input; it should not silently coerce malformed data.

## 5) Production Checklist

- Define an explicit schema and versioning strategy.
- Limit message size and nesting depth.
- Reject unknown or invalid fields when strict compatibility is required.
- Never enable polymorphic deserialization for arbitrary classes.
- Authenticate and authorize before acting on decoded data.
- Never log entire sensitive payloads.
