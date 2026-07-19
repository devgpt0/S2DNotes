# 07 - Generics, Traits, Associated Types, and Lifetimes

## Generics Preserve Relationships

```rust
fn first<T>(values: &[T]) -> Option<&T> {
    values.first()
}

println!("{:?}", first(&[10, 20]));
println!("{:?}", first(&["Rust", "Go"]));
// Output:
// Some(10)
// Some("Rust")
```

`T` is one consistent type for a call.

## Trait

```rust
trait Label {
    fn label(&self) -> String;
}

impl Label for Course {
    fn label(&self) -> String {
        format!("{}: {}", self.id, self.title)
    }
}
```

Traits define shared behavior and can include default methods, associated types, and constants.

## Trait Bounds

```rust
fn print_label(value: &impl Label) {
    println!("{}", value.label());
}
```

Equivalent generic form:

```rust
fn print_label<T: Label>(value: &T) {
    println!("{}", value.label());
}
```

Use `where` for complex bounds:

```rust
fn compare_and_print<T>(left: &T, right: &T)
where
    T: Label + PartialEq,
{
    println!("{} {}", left == right, left.label());
}
```

## Static Dispatch

Generic trait bounds are monomorphized into concrete implementations, enabling inlining at possible code-size cost.

## Trait Objects

```rust
fn print_dynamic(value: &dyn Label) {
    println!("{}", value.label());
}
```

Trait objects use dynamic dispatch and can store different concrete implementors behind pointers such as `Box<dyn Label>`.

Use generics when concrete type relationships matter; trait objects for runtime heterogeneity and stable abstraction boundaries.

## Object Safety / Dyn Compatibility

Not every trait can become `dyn Trait`. Methods involving `Self`, generic methods, or return types can make dynamic dispatch impossible unless constrained. Read current dyn-compatibility rules when designing plugin APIs.

## Associated Types

```rust
trait Repository {
    type Error;
    fn find(&self, id: &str) -> Result<Course, Self::Error>;
}
```

Associated types let an implementation choose one related type. Generic trait parameters allow several implementations for different parameter choices.

## Associated Constants

```rust
trait Limited {
    const MAX_LENGTH: usize;
}
```

## `From`, `Into`, `TryFrom`, and `TryInto`

```rust
struct CourseId(String);

impl TryFrom<String> for CourseId {
    type Error = String;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        if value.trim().is_empty() {
            return Err(String::from("course id is required"));
        }
        Ok(Self(value))
    }
}
```

Implement `From`/`TryFrom`; callers receive `Into`/`TryInto` automatically.

## Lifetimes in Plain Language

Lifetimes describe relationships between references so none outlive borrowed data. They do not extend runtime lifetime.

```rust
fn longer<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() >= right.len() { left } else { right }
}
```

The result is valid no longer than the shorter relevant input lifetime.

## Lifetime Elision

Common signatures infer lifetimes:

```rust
fn length(text: &str) -> usize {
    text.len()
}
```

Annotations are needed when relationships are ambiguous, not on every reference.

## Struct Holding a Reference

```rust
struct CourseView<'a> {
    title: &'a str,
}

let title = String::from("Rust");
let view = CourseView { title: &title };
println!("{}", view.title);
// Output: Rust
```

The view cannot outlive the title.

## `'static`

`'static` means a reference can live for the entire program or an owned value meets a bound without borrowing shorter data. It does not mean the value is immortal or should be leaked.

String literals are `&'static str`.

## Higher-Ranked Trait Bounds

Library APIs sometimes require a callback valid for any lifetime:

```rust
fn use_parser<F>(parser: F)
where
    F: for<'a> Fn(&'a str) -> &'a str,
{
    println!("{}", parser("Rust"));
}
```

Learn this only after ordinary borrow relationships.

## Blanket Implementations and Coherence

The orphan rule allows implementing a trait when either the trait or type is local. This preserves global coherence.

Newtypes let you implement external traits for external data under a local type.

## Expert Rules

- generics preserve compile-time relationships
- traits define capabilities
- associated types express one implementation choice
- `dyn Trait` enables runtime heterogeneity
- lifetimes describe reference validity relationships
- prefer owned data when borrowed structs create unnecessary complexity
- do not add `'static` or clones merely to silence errors
- keep public bounds minimal
