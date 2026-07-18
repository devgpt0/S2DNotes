# 08 - Object Contracts and Value Objects

## 1) `equals` and `hashCode`

Equal objects must have equal hash codes. Equality should be reflexive, symmetric, transitive, consistent, and false for `null`.

```java
record CustomerId(long value) {
    CustomerId {
        if (value <= 0) {
            throw new IllegalArgumentException("value must be positive");
        }
    }
}

CustomerId first = new CustomerId(10);
CustomerId second = new CustomerId(10);
System.out.println(first.equals(second));
System.out.println(first.hashCode() == second.hashCode());
// Output:
// true
// true
```

Records are excellent value objects when their components represent equality.

## 2) Stable Hash Keys

Do not mutate fields participating in equality while an object is inside a `HashSet` or used as a `HashMap` key.

```java
Set<CustomerId> ids = new HashSet<>();
ids.add(new CustomerId(10));
System.out.println(ids.contains(new CustomerId(10)));
// Output: true
```

## 3) `toString`

`toString` should help diagnostics but must never reveal passwords, tokens, keys, or personal data.

```java
record ApiResult(int status, String message) {}

System.out.println(new ApiResult(200, "ok"));
// Output: ApiResult[status=200, message=ok]
```

## 4) Entity vs Value Object

- An entity is defined by identity over time, such as an order ID.
- A value object is defined by its values, such as money or an address.
- Value objects should normally be immutable and validate themselves.

## 5) Copying

Avoid `Cloneable`; it has awkward semantics and often produces shallow copies. Prefer an explicit copy constructor, factory, or immutable object.
