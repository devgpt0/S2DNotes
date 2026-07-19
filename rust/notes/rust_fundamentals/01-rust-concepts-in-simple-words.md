# 01 - Rust Concepts in Simple Words

## The One-Sentence Idea

Rust lets you write fast native programs while the compiler checks who owns each value, who may borrow it, and whether shared data is safe across threads.

## First Program

```rust
fn main() {
    println!("Hello, Rust");
}
// Output: Hello, Rust
```

- `fn`: define a function
- `main`: executable entry point
- `println!`: macro that prints a line
- `!`: indicates a macro call

## Variables

```rust
fn main() {
    let course = "Rust";
    let lessons = 12;
    println!("{course} has {lessons} lessons");
}
// Output: Rust has 12 lessons
```

Variables are immutable by default.

```rust
let mut completed = 0;
completed += 1;
println!("{completed}");
// Output: 1
```

Use `mut` only when changing the binding is part of the design.

## Types

```rust
let count: i32 = 3;
let ratio: f64 = 0.5;
let published: bool = true;
let symbol: char = 'R';
println!("{count} {ratio} {published} {symbol}");
// Output: 3 0.5 true R
```

Rust does not silently convert unrelated types.

## Functions and Expressions

```rust
fn double(number: i32) -> i32 {
    number * 2
}

fn main() {
    println!("{}", double(5));
}
// Output: 10
```

The final expression without a semicolon becomes the return value. Adding a semicolon changes it into a statement returning `()`.

## Ownership

Every value has an owner. When the owner leaves scope, Rust drops the value.

```rust
let first = String::from("Rust");
let second = first;
println!("{second}");
// Output: Rust
// first cannot be used here because ownership moved.
```

Rust prevents two variables from both believing they own the same heap allocation.

## Borrowing

Borrow a value without taking ownership:

```rust
fn length(text: &str) -> usize {
    text.len()
}

let course = String::from("Rust");
println!("{} {}", course, length(&course));
// Output: Rust 4
```

`&course` creates a shared reference.

## Structs

```rust
struct Course {
    id: String,
    title: String,
}

let course = Course {
    id: String::from("rust"),
    title: String::from("Rust Foundations"),
};
println!("{}: {}", course.id, course.title);
// Output: rust: Rust Foundations
```

## Enums and Match

```rust
enum Status {
    Draft,
    Published,
}

let status = Status::Published;
let label = match status {
    Status::Draft => "Draft",
    Status::Published => "Published",
};
println!("{label}");
// Output: Published
```

The compiler requires every possible enum case to be handled.

## Option

Rust represents possible absence with `Option<T>`:

```rust
let title: Option<&str> = Some("Rust");
println!("{}", title.unwrap_or("Missing"));
// Output: Rust
```

There is no ordinary null reference.

## Result

Expected failure uses `Result<T, E>`:

```rust
fn divide(left: i32, right: i32) -> Result<i32, String> {
    if right == 0 {
        return Err(String::from("right cannot be zero"));
    }
    Ok(left / right)
}

match divide(10, 2) {
    Ok(value) => println!("{value}"),
    Err(error) => eprintln!("{error}"),
}
// Output: 5
```

## Collections

```rust
let mut courses = vec![String::from("Go")];
courses.push(String::from("Rust"));
println!("{courses:?}");
// Output: ["Go", "Rust"]
```

## Safe Concurrency

```rust
let handle = std::thread::spawn(|| 21 * 2);
println!("{}", handle.join().expect("worker panicked"));
// Output: 42
```

Ownership and `Send`/`Sync` rules prevent many data races at compile time.

## Beginner to Expert Path

1. values, functions, control flow
2. ownership, borrowing, slices
3. structs, enums, Result, collections
4. traits, generics, lifetimes, smart pointers
5. threads, async, unsafe boundaries, performance, deployment

## Ready to Continue?

```rust
let values = [1, 2, 3];
let total: i32 = values.iter().sum();
println!("{total}");
// Output: 6
```
