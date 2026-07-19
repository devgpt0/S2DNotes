# 10 - Smart Pointers, Drop, Interior Mutability, and Cycles

## Box

`Box<T>` owns one value on the heap:

```rust
let value = Box::new(42);
println!("{value}");
// Output: 42
```

Use for recursive types, large move-cost values when justified, or trait objects. Do not box every struct.

## Recursive Type

```rust
enum List {
    Node(i32, Box<List>),
    End,
}
```

Box gives the recursive field a known pointer size.

## Deref

Smart pointers can implement `Deref` to behave like references. Deref coercion enables `&String` to become `&str` in function calls.

Use custom Deref only for pointer-like types; it can hide method resolution.

## Drop

```rust
struct Tracer(&'static str);

impl Drop for Tracer {
    fn drop(&mut self) {
        println!("dropping {}", self.0);
    }
}

let _value = Tracer("course");
// Output at scope end: dropping course
```

Fields drop in documented order. Use `std::mem::drop(value)` for early drop; do not call `Drop::drop` directly.

## Rc

`Rc<T>` provides single-threaded shared ownership:

```rust
use std::rc::Rc;

let value = Rc::new(String::from("Rust"));
let second = Rc::clone(&value);
println!("{} {}", Rc::strong_count(&value), second);
// Output: 2 Rust
```

Cloning Rc increments a count; it does not deep clone `T`.

## Arc

`Arc<T>` provides atomic shared ownership across threads when `T` satisfies required thread-safety traits. Arc alone does not make mutable data safe.

## Cell

`Cell<T>` permits replacing/copying values through shared references in single-threaded contexts.

## RefCell

`RefCell<T>` enforces borrowing rules at runtime:

```rust
use std::cell::RefCell;

let value = RefCell::new(vec![1, 2]);
value.borrow_mut().push(3);
println!("{:?}", value.borrow());
// Output: [1, 2, 3]
```

Violating borrow rules panics. Keep borrow guards short and never hold them across callbacks that may borrow again.

## Rc<RefCell<T>>

This enables shared mutable ownership in single-threaded structures but moves errors to runtime and can create cycles. Prefer simpler ownership where possible.

## Mutex and RwLock

Thread-safe interior mutability uses synchronization:

```rust
let value = std::sync::Mutex::new(0);
*value.lock().expect("mutex poisoned") += 1;
println!("{}", *value.lock().expect("mutex poisoned"));
// Output: 1
```

Poisoning indicates a panic while holding a lock. Decide whether state can be safely recovered; do not blindly unwrap in resilient services.

## Cow

`Cow<'a, T>` can hold borrowed or owned data and clone only when mutation is needed:

```rust
use std::borrow::Cow;

fn normalize(value: &str) -> Cow<'_, str> {
    if value.contains(' ') {
        Cow::Owned(value.replace(' ', "-"))
    } else {
        Cow::Borrowed(value)
    }
}
```

Measure before introducing Cow; it increases type complexity.

## Pin

`Pin<P>` prevents moving a value through that pointer when its invariants require a stable address. It is fundamental to some futures/self-referential patterns.

Most application code uses pinned APIs without implementing pin-sensitive types. Unsafe pin projections require expert invariant review.

## Cycles

Rc/Arc strong reference cycles leak because counts never reach zero.

Use `Weak<T>` for non-owning back-references:

```mermaid
flowchart LR
    Parent -->|Rc strong| Child
    Child -.->|Weak non-owning| Parent
```

Upgrade Weak returns Option because owner may be gone.

## Expert Rules

- Box for ownership/layout, not habit
- Rc single-thread shared ownership
- Arc cross-thread shared ownership
- RefCell runtime borrow checking
- Mutex/RwLock synchronized mutation
- Weak breaks ownership cycles
- keep guards short
- explicit fallible finalization before Drop
- unsafe pin code requires written invariants
