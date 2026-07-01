# 13 - Design Choice Cheatsheet

## 1) Fast Decision Matrix

| Requirement | Recommended Structure |
|---|---|
| indexed access + append heavy | `ArrayList` |
| uniqueness check heavy | `HashSet` |
| key lookup heavy | `HashMap` |
| predictable insertion order map | `LinkedHashMap` |
| sorted keys | `TreeMap` |
| enum keys | `EnumMap` |
| thread-safe concurrent key-value updates | `ConcurrentHashMap` |
| immutable API response | `List.copyOf`, `Set.copyOf`, `Map.copyOf` |

## 2) Mutation Contract Matrix

| Factory/Wrapper | Add/Remove | Reflects source changes |
|---|---|---|
| `new ArrayList<>(src)` | yes | no |
| `Arrays.asList(...)` | no (size fixed) | backed by array |
| `Collections.unmodifiableList(src)` | no | yes |
| `List.copyOf(src)` | no | no |

## 3) Rule of Thumb

- start simple (`ArrayList`, `HashMap`, `HashSet`)
- optimize only after operation profile is clear
- expose immutable snapshots in public APIs

## 4) Summary

The right data structure is a design decision, not a coding detail.
