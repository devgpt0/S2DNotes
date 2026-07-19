# 98 - Rust Expert Tips and Production Snippets

These patterns are small on purpose. Use them when they make a contract clearer; do not collect abstractions that the program does not need.

## 1. Model a Valid Value Once

```rust
use std::{fmt, str::FromStr};

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct CourseId(String);

#[derive(Debug, Eq, PartialEq)]
pub enum CourseIdError {
    Empty,
    TooLong,
    InvalidCharacter(char),
}

impl FromStr for CourseId {
    type Err = CourseIdError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        if value.is_empty() {
            return Err(CourseIdError::Empty);
        }
        if value.len() > 40 {
            return Err(CourseIdError::TooLong);
        }
        if let Some(character) = value
            .chars()
            .find(|character| !character.is_ascii_lowercase() && *character != '-')
        {
            return Err(CourseIdError::InvalidCharacter(character));
        }

        Ok(Self(value.to_owned()))
    }
}

impl fmt::Display for CourseId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

fn main() {
    let id: CourseId = "rust-ownership".parse().expect("valid literal");
    println!("{id}");
    println!("{:?}", "Rust".parse::<CourseId>());
}
```

Output:

```text
rust-ownership
Err(InvalidCharacter('R'))
```

The constructor does not trim, lowercase, or silently fix input. Validation verifies the caller's value. Once created, `CourseId` is known to be valid.

## 2. Borrow at Read-Only Boundaries

```rust
fn has_tag(tags: &[String], expected: &str) -> bool {
    tags.iter().any(|tag| tag == expected)
}

fn main() {
    let tags = vec![String::from("rust"), String::from("safe")];
    println!("{}", has_tag(&tags, "safe"));
    println!("{}", tags.len()); // The caller still owns the vector.
}
```

Output:

```text
true
2
```

Accept `&str` instead of `&String`, and `&[T]` instead of `&Vec<T>`, unless the concrete container is part of the contract.

## 3. Make States Impossible to Confuse

```rust
#[derive(Debug)]
struct DraftCourse {
    title: String,
}

#[derive(Debug)]
struct PublishedCourse {
    title: String,
    published_at_epoch_seconds: u64,
}

impl DraftCourse {
    fn publish(self, published_at_epoch_seconds: u64) -> PublishedCourse {
        PublishedCourse {
            title: self.title,
            published_at_epoch_seconds,
        }
    }
}

fn main() {
    let draft = DraftCourse {
        title: String::from("Rust Lifetimes"),
    };
    let published = draft.publish(1_800_000_000);
    println!("{} @ {}", published.title, published.published_at_epoch_seconds);
}
```

Output:

```text
Rust Lifetimes @ 1800000000
```

Consuming `self` prevents the same draft value from being published twice accidentally.

## 4. Return an Iterator When Streaming Is Natural

```rust
fn passing_scores(scores: &[u8]) -> impl Iterator<Item = u8> + '_ {
    scores.iter().copied().filter(|score| *score >= 60)
}

fn main() {
    let scores = [45, 60, 82, 30];
    for score in passing_scores(&scores) {
        println!("pass: {score}");
    }
}
```

Output:

```text
pass: 60
pass: 82
```

No result vector is allocated. Return a collection when the caller requires ownership, repeated traversal, indexing, or a stable snapshot.

## 5. Preserve the Source Error

```rust
use std::{error::Error, fmt, fs, io, path::Path};

#[derive(Debug)]
struct LoadError {
    path: String,
    source: io::Error,
}

impl fmt::Display for LoadError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "failed to read {}", self.path)
    }
}

impl Error for LoadError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

fn load(path: &Path) -> Result<String, LoadError> {
    fs::read_to_string(path).map_err(|source| LoadError {
        path: path.display().to_string(),
        source,
    })
}
```

The display message says what failed. `source()` preserves the lower-level cause for diagnostics. Domain libraries should not log and return the same error.

## 6. Use a Bounded Async Pipeline

```rust
use std::sync::Arc;
use tokio::sync::{mpsc, Semaphore};

async fn process(course_id: String) {
    println!("processed {course_id}");
}

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel::<String>(32);
    let permits = Arc::new(Semaphore::new(4));

    let worker_permits = Arc::clone(&permits);
    let worker = tokio::spawn(async move {
        let mut tasks = tokio::task::JoinSet::new();

        while let Some(course_id) = receiver.recv().await {
            let permit = Arc::clone(&worker_permits)
                .acquire_owned()
                .await
                .expect("semaphore remains open");
            tasks.spawn(async move {
                process(course_id).await;
                drop(permit);
            });
        }

        while let Some(result) = tasks.join_next().await {
            result.expect("worker task must not panic");
        }
    });

    sender.send(String::from("rust-async")).await.expect("worker alive");
    drop(sender); // Closing every sender ends the receive loop.
    worker.await.expect("worker must not panic");
}
```

Output:

```text
processed rust-async
```

The channel bounds queued work; the semaphore bounds active work; dropping the sender provides a clean completion signal.

## 7. Put a Deadline Around External Work

```rust
use std::time::Duration;
use tokio::time::{sleep, timeout};

async fn dependency_call() -> &'static str {
    sleep(Duration::from_millis(20)).await;
    "ready"
}

#[tokio::main]
async fn main() {
    match timeout(Duration::from_millis(50), dependency_call()).await {
        Ok(value) => println!("{value}"),
        Err(_) => println!("dependency timed out"),
    }
}
```

Output:

```text
ready
```

A timeout stops waiting; whether it stops the underlying operation depends on cancellation behavior. Know whether dropping that future is cancellation-safe.

## 8. Keep Lock Scope Small

```rust
use std::sync::Mutex;

fn next_id(counter: &Mutex<u64>) -> u64 {
    let mut value = counter.lock().expect("counter mutex poisoned");
    *value += 1;
    *value
} // Guard is dropped here.

fn main() {
    let counter = Mutex::new(0);
    println!("{}", next_id(&counter));
    println!("{}", next_id(&counter));
}
```

Output:

```text
1
2
```

Do not perform slow I/O or `.await` while holding a synchronous mutex guard. Copy or move the minimum data out, release the guard, then perform slow work.

## 9. Prefer Deterministic Output

```rust
use std::collections::BTreeMap;

fn main() {
    let courses = BTreeMap::from([
        ("rust", "Rust"),
        ("go", "Go"),
        ("python", "Python"),
    ]);

    for (id, title) in courses {
        println!("{id}: {title}");
    }
}
```

Output:

```text
go: Go
python: Python
rust: Rust
```

Use deterministic order for snapshots, command output, signatures, and reproducible tests. Use `HashMap` when ordering is irrelevant and hashing better matches the workload.

## 10. Make Exhaustive Decisions Explicit

```rust
enum Access {
    Reader,
    Editor,
    Owner,
}

fn can_delete(access: Access) -> bool {
    match access {
        Access::Reader | Access::Editor => false,
        Access::Owner => true,
    }
}
```

When a new variant is added, the compiler points to every exhaustive match that needs a product decision.

## Expert Review Questions

- Who owns this value, connection, task, and allocation?
- Which invalid states are impossible to construct?
- Which inputs are externally controlled, and where are they bounded?
- Can a queue, retry loop, task set, or label cardinality grow forever?
- What happens on partial failure, panic, cancellation, or shutdown?
- Is the output deterministic where users or tests depend on it?
- Does the error preserve actionable context without leaking secrets?
- Is every clone, allocation, lock, and unsafe block necessary and measured?
- Can a simpler synchronous or single-threaded design meet the requirement?

