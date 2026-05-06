# 13 - Debugging and Testing Maps

## 1) Common Debugging Checks

1. Is key object mutable after insertion?
2. Are `equals/hashCode` both correctly overridden?
3. Is map type correct for ordering requirement?
4. Are null assumptions valid for chosen map implementation?

## 2) Helpful Print Strategies

```java
map.forEach((k, v) -> System.out.println(k + " -> " + v));
```

For deterministic debug output:

```java
new TreeMap<>(map).forEach((k, v) -> System.out.println(k + " -> " + v));
```

## 3) Unit Test Patterns

Test key behaviors:

- insertion and overwrite
- missing key default behavior
- merge/compute idempotence where expected
- iteration order (if using ordered map type)

## 4) Edge Case Checklist

- empty map
- null key/value where allowed/disallowed
- duplicate key insert
- large volume inserts (resize behavior)
- concurrent writes where applicable
