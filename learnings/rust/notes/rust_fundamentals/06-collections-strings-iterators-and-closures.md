# 06 - Collections, Strings, Iterators, and Closures

## Vec

```rust
let mut values = vec![10, 20];
values.push(30);
println!("{values:?}");
// Output: [10, 20, 30]
```

`Vec<T>` owns a growable contiguous buffer.

## Safe Access

```rust
let values = vec![10, 20];
println!("{:?}", values.get(5));
// Output: None
```

Indexing out of bounds panics; `get` returns Option.

## Borrow Invalidation

```rust
let mut values = vec![1, 2, 3];
let first = &values[0];
println!("{first}");
values.push(4);
```

The reference is not used after push. Rust prevents holding a reference across a possible reallocation when it would be used later.

## HashMap

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();
scores.insert(String::from("Asha"), 90);
println!("{:?}", scores.get("Asha"));
// Output: Some(90)
```

Map iteration order is not stable. Sort keys for deterministic output.

## Entry API

```rust
let mut counts = HashMap::new();
for word in ["rust", "go", "rust"] {
    *counts.entry(word).or_insert(0) += 1;
}
println!("{}", counts["rust"]);
// Output: 2
```

## HashSet, VecDeque, BinaryHeap

- `HashSet<T>`: unique membership
- `VecDeque<T>`: efficient ends/queue
- `BinaryHeap<T>`: priority queue
- `BTreeMap/Set`: sorted keys/range queries

Choose by required operations and order.

## String vs str

- `String`: owned growable UTF-8 bytes
- `str`: borrowed UTF-8 string slice, normally used as `&str`

```rust
fn label(value: &str) -> String {
    format!("Course: {value}")
}

let title = String::from("Rust");
println!("{}", label(&title));
// Output: Course: Rust
```

## Unicode Iteration

```rust
let text = "Rust語";
println!("{} {}", text.len(), text.chars().count());
// Output: 7 5
```

Bytes differ from Unicode scalar values; grapheme clusters may differ again.

## Iterator Laziness

```rust
let values = [1, 2, 3, 4];
let doubled: Vec<_> = values
    .iter()
    .filter(|value| **value % 2 == 0)
    .map(|value| value * 2)
    .collect();
println!("{doubled:?}");
// Output: [4, 8]
```

Adapters build lazy processing. `collect`, `sum`, `for_each`, or a loop consumes it.

## `iter`, `iter_mut`, `into_iter`

- `iter`: shared references
- `iter_mut`: mutable references
- `into_iter`: consumes collection into owned items (for owned collections)

Choose based on ownership after traversal.

## Closures

```rust
let factor = 3;
let multiply = |value| value * factor;
println!("{}", multiply(7));
// Output: 21
```

Closures infer capture by shared borrow, mutable borrow, or move.

## Closure Traits

- `Fn`: callable by shared reference
- `FnMut`: may mutate captured state
- `FnOnce`: may consume captured values; callable at least once

Every closure implements the least restrictive compatible traits.

```rust
fn apply_twice(mut operation: impl FnMut(i32) -> i32, value: i32) -> i32 {
    operation(operation(value))
}
```

## Move Closure

```rust
let title = String::from("Rust");
let print = move || println!("{title}");
print();
// Output: Rust
```

`move` moves captured bindings into the closure, commonly needed for threads/async tasks. Copy types are copied.

## Iterator vs Loop

Use iterators for clear transformations and loops for complex branching/state. Rust iterators are typically optimized without allocating intermediate collections.

## Expert Rules

- choose collection by operation/order
- avoid indexing when iteration/get is clearer
- understand iterator ownership mode
- do not clone merely to satisfy closures
- use `&str` inputs broadly
- define Unicode behavior explicitly
- sort hash keys for deterministic output
- reserve capacity only when size is known/material
