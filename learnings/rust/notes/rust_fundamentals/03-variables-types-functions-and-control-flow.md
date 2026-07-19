# 03 - Variables, Types, Functions, and Control Flow

## Immutable by Default

```rust
let course = "Rust";
println!("{course}");
// Output: Rust
```

Use `mut` for mutation:

```rust
let mut lessons = 0;
lessons += 1;
println!("{lessons}");
// Output: 1
```

## Shadowing

```rust
let spaces = "   ";
let spaces = spaces.len();
println!("{spaces}");
// Output: 3
```

Shadowing creates a new binding and may change type. Mutation keeps one binding/type.

## Scalar Types

- signed: `i8` through `i128`, `isize`
- unsigned: `u8` through `u128`, `usize`
- floating: `f32`, `f64`
- boolean: `bool`
- Unicode scalar: `char`

```rust
let count: u32 = 42;
let ratio: f64 = 0.5;
let letter: char = '語';
println!("{count} {ratio} {letter}");
// Output: 42 0.5 語
```

## Numeric Safety

Debug builds check integer overflow and panic. Release overflow behavior depends on operation/profile rules. Use checked/saturating/wrapping/overflowing methods when behavior matters.

```rust
let value = u8::MAX;
println!("{:?}", value.checked_add(1));
// Output: None
```

## Compound Types

Tuple:

```rust
let course: (&str, u32) = ("Rust", 12);
println!("{} {}", course.0, course.1);
// Output: Rust 12
```

Array:

```rust
let values = [10, 20, 30];
println!("{} {}", values[0], values.len());
// Output: 10 3
```

Arrays have fixed length as part of their type.

## Statements and Expressions

```rust
let value = {
    let base = 10;
    base + 5
};
println!("{value}");
// Output: 15
```

The block's final expression has no semicolon.

## Functions

```rust
fn add(left: i32, right: i32) -> i32 {
    left + right
}
println!("{}", add(2, 3));
// Output: 5
```

Parameter and return types are explicit in function signatures.

## `if` Is an Expression

```rust
let score = 80;
let result = if score >= 70 { "passed" } else { "retry" };
println!("{result}");
// Output: passed
```

Both branches must produce compatible types.

## Loops

```rust
for value in 1..=3 {
    println!("{value}");
}
// Output: 1 2 3 on separate lines.
```

```rust
let mut count = 0;
while count < 2 {
    count += 1;
}
println!("{count}");
// Output: 2
```

`loop` can return a value:

```rust
let mut count = 0;
let result = loop {
    count += 1;
    if count == 3 {
        break count * 10;
    }
};
println!("{result}");
// Output: 30
```

## Match

```rust
let level = 2;
let label = match level {
    1 => "beginner",
    2 => "intermediate",
    3 => "advanced",
    _ => "unknown",
};
println!("{label}");
// Output: intermediate
```

Match is exhaustive.

## Conversions

```rust
let count: u16 = 300;
let small = u8::try_from(count);
println!("{small:?}");
// Output: Err(TryFromIntError(())) or equivalent debug representation.
```

Use `TryFrom` for potentially failing numeric conversions. `as` can truncate; use it only with proven bounds/intent.

## Type Aliases and Newtypes

Alias does not create a new type:

```rust
type CourseId = String;
```

Newtype creates a distinction:

```rust
struct CourseId(String);
struct UserId(String);
```

Use newtypes for domain safety, validation, trait control, and units.

## Never Type and Unit

- `()`: unit, no meaningful result
- `!`: never returns, such as `panic!` or infinite loop

## Expert Rules

- immutable by default
- checked conversions at boundaries
- explicit overflow semantics
- newtypes for meaningful distinctions
- expressions for concise clear flow
- exhaustive matches for finite states
- avoid clever shadowing that hides meaning
