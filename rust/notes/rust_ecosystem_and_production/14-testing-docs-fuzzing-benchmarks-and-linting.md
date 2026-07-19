# 14 - Testing, Documentation, Fuzzing, Benchmarks, and Linting

## Unit Test

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_valid_level() {
        assert_eq!(parse_level("3"), Ok(3));
    }
}
```

Run:

```powershell
cargo test
```

## Result-Returning Test

```rust
#[test]
fn creates_course() -> Result<(), Box<dyn std::error::Error>> {
    let course = Course::new("rust", "Rust")?;
    assert_eq!(course.title(), "Rust");
    Ok(())
}
```

## Panic Test

Use `#[should_panic(expected = "...")]` only when panic is the contract. Prefer Result for expected failures.

## Integration Tests

Files under `tests/` compile as external consumers and test the public API:

```text
tests/course_api.rs
```

## Test Fixtures

- `tempfile`-style maintained crate for temporary files/directories
- in-memory fakes for small repository contracts
- real database/container integration for query/migration behavior
- deterministic clock/random/ID injection

Avoid global environment mutation in parallel tests without synchronization.

## Documentation Tests

```rust
/// Adds two numbers.
///
/// ```
/// assert_eq!(course_math::add(2, 3), 5);
/// ```
pub fn add(left: i32, right: i32) -> i32 {
    left + right
}
```

`cargo test --doc` compiles examples.

## Property Testing

Property tests generate structured inputs and shrink failures:

```rust
proptest! {
    #[test]
    fn reversing_twice_returns_original(values in proptest::collection::vec(any::<i32>(), 0..100)) {
        let mut reversed = values.clone();
        reversed.reverse();
        reversed.reverse();
        prop_assert_eq!(reversed, values);
    }
}
```

Use a maintained property-testing crate as a dev dependency.

## Fuzzing

`cargo-fuzz` integrates libFuzzer on supported toolchains/platforms:

```rust
fuzz_target!(|data: &[u8]| {
    if let Ok(text) = std::str::from_utf8(data) {
        let _ = parse_course(text);
    }
});
```

Fuzz parsers, unsafe boundaries, codecs, and invariants. Keep discovered corpus cases.

## Benchmarks

Use a maintained benchmark harness such as Criterion for statistical measurements on stable Rust.

```rust
fn benchmark_parse(criterion: &mut Criterion) {
    criterion.bench_function("parse course", |bencher| {
        bencher.iter(|| parse_course(black_box(INPUT)))
    });
}
```

Record Rust version, target, CPU, input, allocation behavior, and profile settings.

## Formatting

```powershell
cargo fmt --check
```

Do not hand-format against rustfmt.

## Clippy

```powershell
cargo clippy --all-targets --all-features -- -D warnings
```

Review lints; do not add broad allows. A narrow documented allow is acceptable only when the code intentionally violates a lint and no clearer design exists.

## Miri and Sanitizers

Miri can detect classes of undefined behavior in unsafe/interior-mutability code. Sanitizers help memory/thread issues on supported nightly/platform configurations. Use them for unsafe/FFI-heavy projects.

## Coverage

Coverage shows executed code, not correctness. Include meaningful failure and concurrency paths rather than optimizing a percentage.

## CI Matrix

- minimum supported Rust version when declared
- stable current toolchain
- required targets/features
- fmt/check/clippy/test/doc
- audit/deny policy
- unsafe/fuzz/sanitizer jobs as risk demands

## Final Rules

- test public behavior and invariants
- integration tests as consumers
- documentation examples compile
- property/fuzz tests for broad inputs
- benchmarks for decisions
- no warnings hidden globally
- failure artifacts reproducible
