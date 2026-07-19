# 15 - Macros, Unsafe Rust, FFI, and Sound Abstractions

Most Rust programs need little or no `unsafe` code. Learn safe Rust first. Use macros to remove true repetition, and use `unsafe` only at a small boundary whose rules you can prove.

## Declarative Macros

A `macro_rules!` macro matches Rust syntax and produces Rust syntax before compilation.

```rust
macro_rules! announce {
    ($label:expr, $value:expr) => {
        println!("{}: {}", $label, $value);
    };
}

fn main() {
    announce!("courses", 3);
}
```

Output:

```text
courses: 3
```

The arguments are syntax fragments. `$label:expr` means "match one expression." The extra braces create a block so the expansion behaves like one expression.

Use a normal function when a function can solve the problem. A function is easier to read, test, debug, and type-check. A macro is useful when it must accept varying syntax, generate items, or work with a varying number of arguments.

## Repetition in a Macro

```rust
macro_rules! string_set {
    ($($value:expr),* $(,)?) => {{
        let mut set = std::collections::HashSet::new();
        $(set.insert(String::from($value));)*
        set
    }};
}

fn main() {
    let tags = string_set!["rust", "systems", "safe"];
    println!("{}", tags.contains("safe"));
    println!("{}", tags.len());
}
```

Output:

```text
true
3
```

- `$()*` repeats zero or more times.
- `$(,)?` accepts an optional trailing comma.
- The double braces make the expansion an expression that returns `set`.

Do not evaluate a macro argument more than once unless the macro documents that behavior. An argument can contain a function call with side effects.

## Procedural Macros

Procedural macros are Rust functions that receive and return token streams. They live in a crate whose library type is `proc-macro`.

The three forms are:

- derive: `#[derive(Serialize)]`
- attribute: `#[route("/courses")]`
- function-like: `sql!("SELECT id FROM course")`

They are powerful build-time programs. Keep dependencies small, audit them, and produce compiler errors that point to the user's code. Prefer a maintained macro library over writing a parser casually.

## What `unsafe` Changes

An `unsafe` block does not disable the borrow checker. It permits five additional operations:

1. dereference a raw pointer;
2. call an unsafe function or method;
3. read or modify a mutable static variable;
4. implement an unsafe trait;
5. access a union field.

You are responsible for preserving every Rust safety rule around those operations.

## Raw Pointer Example

```rust
fn main() {
    let score = 95_i32;
    let pointer = &score as *const i32;

    // SAFETY: `pointer` came from a live, aligned `i32` reference. `score`
    // remains in scope, and no mutation occurs while the pointer is read.
    let observed = unsafe { *pointer };

    println!("score = {observed}");
}
```

Output:

```text
score = 95
```

This example teaches the boundary; it is not a reason to replace `&i32` with `*const i32`. Use a safe reference whenever possible.

## Build a Safe Abstraction

The standard library exposes `slice::from_raw_parts` because low-level integrations sometimes provide a pointer and length.

```rust
use std::slice;

/// Views `len` initialized bytes beginning at `pointer`.
///
/// # Safety
/// `pointer` must be non-null and properly aligned, and the memory range must
/// be valid for reads of `len` bytes for the returned lifetime. The range must
/// not be mutated while the returned slice is used. `len` must not exceed
/// `isize::MAX` bytes.
unsafe fn bytes_from_raw<'a>(pointer: *const u8, len: usize) -> &'a [u8] {
    // SAFETY: The caller must satisfy the function's documented contract.
    unsafe { slice::from_raw_parts(pointer, len) }
}

fn main() {
    let source = [10_u8, 20, 30];

    // SAFETY: the pointer and length come from the same live array.
    let view = unsafe { bytes_from_raw(source.as_ptr(), source.len()) };

    println!("{view:?}");
}
```

Output:

```text
[10, 20, 30]
```

An `unsafe fn` must document what the caller must prove. Since Edition 2024, unsafe operations inside an unsafe function still belong in an explicit `unsafe` block. This makes the exact risky operation visible.

## Soundness Review Checklist

For every unsafe block, answer:

- Is the pointer non-null when required?
- Is it correctly aligned?
- Does it point to initialized memory of the correct type?
- Is the allocation alive for the complete access?
- Are aliasing rules preserved?
- Is the computed length within the allocation?
- Can integer arithmetic overflow?
- Can another thread mutate the memory concurrently?
- Can a panic leave an invariant broken?

If the proof is unclear, the code is not ready.

## Interior Mutability Is Usually Safer

Do not reach for `static mut`. Prefer:

- `Atomic*` for a simple shared number or flag;
- `Mutex<T>` or `RwLock<T>` for shared structured state;
- `OnceLock<T>` or `LazyLock<T>` for one-time initialization;
- ordinary ownership when global state is unnecessary.

These types state and enforce their synchronization rules.

## C-Compatible Layout

Rust's default representation is not a C ABI contract. Use `#[repr(C)]` for shared structs.

```rust
#[repr(C)]
pub struct CourseStats {
    pub total: u64,
    pub active: u64,
}
```

Use fixed-width integers at the boundary. Do not expose `String`, `Vec<T>`, trait objects, Rust references, or Rust enums directly to C unless an explicitly documented ABI representation makes them safe.

## Calling a C Function

```rust
use std::ffi::{c_char, CStr};

unsafe extern "C" {
    fn strlen(value: *const c_char) -> usize;
}

fn c_string_length(value: &CStr) -> usize {
    // SAFETY: `CStr` guarantees a valid non-null, NUL-terminated pointer for
    // the duration of this call. C's `strlen` only reads through that NUL.
    unsafe { strlen(value.as_ptr()) }
}

fn main() {
    let value = c"Rust";
    println!("length = {}", c_string_length(value));
}
```

Output:

```text
length = 4
```

The `c"..."` literal creates a checked `&CStr`. Use `CString::new` for runtime Rust strings; it returns an error if an interior NUL byte exists.

## Exporting a Function to C

```rust
#[unsafe(no_mangle)]
pub extern "C" fn add_scores(left: i32, right: i32) -> i32 {
    left.saturating_add(right)
}
```

`extern "C"` chooses the C calling convention. `no_mangle` exports the requested symbol name and is an unsafe attribute in Edition 2024 because symbol collisions can violate safety.

Do not let a Rust panic unwind through a foreign ABI boundary. Catch it at the outer boundary when the function can panic, translate it to an explicit status code, and keep the caught data entirely on the Rust side. Better still, design the exported operation so expected failures are returned and its implementation does not panic.

## Ownership Across FFI

Every allocation needs one clear owner and one matching release function.

```text
C calls course_name_create -> Rust allocates -> C receives opaque pointer
C calls course_name_read   -> Rust borrows   -> C does not free or retain view
C calls course_name_free   -> Rust deallocates exactly once
```

Document:

- who owns each pointer;
- whether null is allowed;
- how lengths are represented;
- how errors are returned;
- which thread may call the function;
- whether callbacks may be retained;
- which function releases memory.

Never free memory with an allocator different from the one that created it.

## Unions

Reading a union field is unsafe because Rust cannot know which field is active. Prefer an enum inside Rust. Use a union only for a required foreign layout, and carry a reliable tag that determines the active field.

## Final Rules

- prefer functions over macros when both work;
- keep macro syntax small and errors readable;
- keep unsafe blocks tiny and local;
- document safety requirements and invariants;
- wrap unsafe mechanics in a safe API only when the API can enforce them;
- use `repr(C)` and ABI-safe types at FFI boundaries;
- define ownership and error behavior explicitly;
- never allow unwinding or borrowed data to escape beyond its valid boundary;
- test unsafe code with Miri, sanitizers, fuzzing, and platform integration where applicable.

