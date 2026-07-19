# 13 - Files, Serde, Networking, Time, and Databases

## Read a Small File

```rust
let text = std::fs::read_to_string("course.txt")?;
println!("{text}");
```

Use only when file size is bounded. Stream large inputs with `BufReader`.

## Buffered Lines

```rust
use std::io::{BufRead, BufReader};

let file = std::fs::File::open("courses.txt")?;
for line in BufReader::new(file).lines() {
    println!("{}", line?);
}
```

Define maximum record sizes when inputs are untrusted; `lines` can allocate for large lines.

## Paths

Use `Path`/`PathBuf`, not string concatenation.

```rust
use std::path::{Component, Path, PathBuf};

fn safe_relative(root: &Path, input: &Path) -> Result<PathBuf, String> {
    if input.is_absolute() || input.components().any(|part| matches!(part, Component::ParentDir)) {
        return Err(String::from("path must stay below root"));
    }
    Ok(root.join(input))
}
```

Symlinks and races need stronger OS/filesystem containment for hostile environments.

## Serde

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct CourseDto {
    id: String,
    title: String,
}

let course: CourseDto = serde_json::from_str(r#"{"id":"rust","title":"Rust"}"#)?;
println!("{}", course.title);
// Output: Rust
```

DTO deserialization verifies syntax/shape, then domain construction validates semantic rules.

## Borrowed Deserialization

Serde can borrow string slices from input for performance, but lifetimes tie values to the input buffer. Use owned DTOs unless profiling shows borrowing is valuable and API lifetimes stay clear.

## Time

`std::time::Instant` measures monotonic elapsed time:

```rust
let start = std::time::Instant::now();
do_work();
println!("{:?}", start.elapsed());
```

`SystemTime` represents wall-clock points but can move. Calendar/time-zone work typically uses a reviewed ecosystem crate; define UTC/storage/display policy.

## TCP

```rust
use std::io::{Read, Write};
use std::net::TcpStream;

let mut stream = TcpStream::connect_timeout(&address, timeout)?;
stream.set_read_timeout(Some(timeout))?;
stream.set_write_timeout(Some(timeout))?;
stream.write_all(request_bytes)?;
```

Network protocols require framing, size limits, timeouts, partial I/O handling, TLS, validation, and shutdown.

## HTTP Clients

Use a maintained HTTP client crate. Reuse clients/connection pools, propagate deadlines, validate status/body size/schema, and do not retry unsafe requests automatically.

```rust
let response = client
    .get(url)
    .timeout(timeout)
    .send()
    .await?
    .error_for_status()?;
```

Prevent SSRF by allowlisting destinations/schemes/ports and resolving network policy at the trusted service boundary.

## HTTP Servers

Frameworks such as Axum provide routing/extractors around Tokio/HTTP libraries. Keep domain rules framework-independent and configure body limits, timeouts, concurrency limits, graceful shutdown, safe errors, tracing, and TLS/proxy trust.

## Database Principles

- pooled connections with limits
- parameterized queries
- context/deadline/cancellation where driver supports it
- short transactions
- no external calls inside transaction
- explicit migrations
- least-privilege credentials
- validate dynamic sort/identifier choices

Example with a common async SQL style:

```rust
let course = sqlx::query_as!(
    CourseRow,
    "SELECT id, title FROM courses WHERE id = $1",
    id,
)
.fetch_optional(&pool)
.await?;
```

Exact macros/driver features depend on database and crate version. Pin and test the selected stack.

## Transactions

```rust
let mut transaction = pool.begin().await?;
// execute related statements through &mut transaction
transaction.commit().await?;
```

Dropping often rolls back, but explicitly handle commit errors and transaction semantics.

## Secrets

Load protected credentials through deployment secret mechanisms. Do not print config Debug output containing secrets, commit `.env`, or embed service credentials in client binaries.

## Final Rules

- stream/limit large input
- safe path policy
- deny unknown fields when contract is strict
- DTO then domain validation
- network timeouts and body limits
- reusable clients/pools
- parameterized queries
- explicit time-zone representation
- least privilege and safe logs
