# 07 - Immutable Map Core

## 1) Internal Idea

Immutable maps cannot be structurally modified after creation.

Common factories:

- `Map.of(...)`
- `Map.ofEntries(...)`
- `Map.copyOf(...)`

## 2) Basic Usage

```java
import java.util.Map;

public class ImmutableMapCoreDemo {
    public static void main(String[] args) {
        Map<String, Integer> m = Map.of("A", 1, "B", 2);
        System.out.println(m);

        // m.put("C", 3); // throws UnsupportedOperationException
    }
}
```

## 3) Rules

- no `null` keys
- no `null` values
- duplicate keys are rejected

## 4) When To Use

- constants/configuration maps
- defensive API return values
- safe sharing across threads
