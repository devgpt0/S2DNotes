# 09 - Errors, Panic, Validation, and Resource Cleanup

## Recoverable Errors

Use `Result<T, E>`:

```rust
#[derive(Debug)]
enum ParseLevelError {
    NotNumber,
    OutOfRange,
}

fn parse_level(text: &str) -> Result<u8, ParseLevelError> {
    let value = text.parse::<u8>().map_err(|_| ParseLevelError::NotNumber)?;
    if !(1..=5).contains(&value) {
        return Err(ParseLevelError::OutOfRange);
    }
    Ok(value)
}
```

## Display and Error

Library error types should implement meaningful `Display` and `std::error::Error`, preserve sources, and remain matchable when callers need categories.

```rust
impl std::fmt::Display for ParseLevelError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::NotNumber => write!(formatter, "level must be a number"),
            Self::OutOfRange => write!(formatter, "level must be 1 through 5"),
        }
    }
}

impl std::error::Error for ParseLevelError {}
```

## `?` Operator

```rust
fn load_level(path: &std::path::Path) -> Result<u8, Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string(path)?;
    Ok(parse_level(text.trim())?)
}
```

Applications can use flexible report errors at the outer boundary; libraries should expose structured types when callers need decisions.

## Error Context

Add operation context once:

```rust
let text = std::fs::read_to_string(path)
    .map_err(|error| format!("read {}: {error}", path.display()))?;
```

For production applications, maintained error-context crates can preserve sources and backtraces. Do not flatten everything into strings inside reusable libraries.

## Panic

Panic is for violated programmer invariants or unrecoverable states, not ordinary invalid input or missing files.

Avoid `unwrap`/`expect` on external data. `expect` is reasonable when the code proves an invariant and the message explains it.

## Panic Boundaries

Panics unwind by default where supported, running destructors. Projects may configure abort. Catching unwind is for FFI/task/plugin isolation boundaries and only works with unwind-safe values.

Do not catch a panic and continue using possibly inconsistent state.

## Validation

```rust
#[derive(Debug)]
struct Course {
    id: String,
    title: String,
}

impl Course {
    fn new(id: String, title: String) -> Result<Self, ValidationError> {
        if id.trim().is_empty() {
            return Err(ValidationError::Required("id"));
        }
        if title.trim().is_empty() {
            return Err(ValidationError::Required("title"));
        }
        Ok(Self { id, title })
    }
}
```

Validation checks values. Put normalization/transformation in explicit separate operations when business rules require them.

## Drop and RAII

Resources clean up when owners leave scope:

```rust
{
    let file = std::fs::File::open("course.txt")?;
    // use file
} // file is closed here
```

This is RAII: resource acquisition is initialization.

## Fallible Cleanup

`Drop::drop` cannot return an error. Operations requiring flush/commit confirmation must call explicit fallible methods before drop:

```rust
writer.flush()?;
```

Do not rely on destructor-only cleanup for transactional success.

## Main Return

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    run()?;
    Ok(())
}
```

For stable user-facing CLI errors and exit codes, translate errors explicitly rather than relying only on debug output.

## Expert Rules

- structured errors for caller decisions
- context without losing source
- panic for bugs/invariants
- no unwrap on external values
- validation before side effects
- explicit fallible commit/flush
- safe stable client/user messages
- logs contain operational detail without secrets
