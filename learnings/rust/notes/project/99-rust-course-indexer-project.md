# 99 - Complete Project: Concurrent Rust Course Indexer

This project combines the course into one small production-style command-line application. It reads JSON course files, validates every field, loads files with bounded worker threads, rejects duplicate IDs, and prints a deterministic index.

## What You Will Learn

- organize a binary and library crate;
- deserialize external data without silently coercing it;
- preserve domain invariants with private fields;
- read files with explicit count and size limits;
- use a bounded number of worker threads;
- send worker results through a channel;
- make output deterministic with `BTreeMap`;
- preserve error sources and fail the complete operation;
- test the public API as an external consumer.

## Request-to-Output Flow

```mermaid
flowchart LR
    A[Directory argument] --> B[Discover JSON files]
    B --> C[Enforce file count limit]
    C --> D[Fixed worker threads]
    D --> E[Bounded file read]
    E --> F[Strict JSON decode]
    F --> G[Domain validation]
    G --> H[Duplicate ID check]
    H --> I[Sorted output]
```

Any error stops the operation. The program does not print a partial index as though it were complete.

## Folder Structure

```text
rust-course-indexer/
|-- Cargo.toml
|-- src/
|   |-- lib.rs
|   |-- course.rs
|   |-- loader.rs
|   |-- index.rs
|   `-- main.rs
`-- tests/
    `-- indexer.rs
```

## 1. `Cargo.toml`

```toml
[package]
name = "rust-course-indexer"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[dev-dependencies]
tempfile = "3"

[lints.rust]
unsafe_code = "forbid"
```

Concepts learned:

- Edition 2024 language behavior;
- a declared minimum supported Rust version;
- minimal runtime dependencies;
- project-level unsafe-code policy;
- a test-only temporary-directory dependency.

Applications should commit the generated `Cargo.lock` so CI and deployments resolve the tested dependency versions.

## 2. `src/lib.rs`

```rust
mod course;
mod index;
mod loader;

pub use course::{Course, CourseError};
pub use index::{CourseIndex, IndexError};
pub use loader::{LoadError, load_courses};
```

Concepts learned:

- implementation modules remain private;
- deliberate re-exports form one small public API;
- external code does not depend on the internal file layout.

## 3. `src/course.rs`

```rust
use std::{collections::HashSet, error::Error, fmt};

use serde::Deserialize;

const MAX_ID_BYTES: usize = 40;
const MAX_TITLE_CHARACTERS: usize = 120;
const MAX_TAGS: usize = 20;
const MAX_TAG_BYTES: usize = 30;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Course {
    id: String,
    title: String,
    tags: Box<[String]>,
}

impl Course {
    pub fn new(id: String, title: String, tags: Vec<String>) -> Result<Self, CourseError> {
        validate_id(&id)?;
        validate_title(&title)?;
        validate_tags(&tags)?;

        Ok(Self {
            id,
            title,
            tags: tags.into_boxed_slice(),
        })
    }

    #[must_use]
    pub fn id(&self) -> &str {
        &self.id
    }

    #[must_use]
    pub fn title(&self) -> &str {
        &self.title
    }

    #[must_use]
    pub fn tags(&self) -> &[String] {
        &self.tags
    }
}

#[derive(Debug, Eq, PartialEq)]
pub enum CourseError {
    EmptyId,
    IdTooLong,
    InvalidIdCharacter(char),
    EmptyTitle,
    TitleTooLong,
    TooManyTags,
    EmptyTag { index: usize },
    TagTooLong { index: usize },
    DuplicateTag(String),
}

impl fmt::Display for CourseError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyId => formatter.write_str("course ID must not be empty"),
            Self::IdTooLong => write!(formatter, "course ID exceeds {MAX_ID_BYTES} bytes"),
            Self::InvalidIdCharacter(character) => {
                write!(
                    formatter,
                    "course ID contains invalid character {character:?}"
                )
            }
            Self::EmptyTitle => formatter.write_str("course title must not be empty"),
            Self::TitleTooLong => {
                write!(
                    formatter,
                    "course title exceeds {MAX_TITLE_CHARACTERS} characters"
                )
            }
            Self::TooManyTags => write!(formatter, "course exceeds {MAX_TAGS} tags"),
            Self::EmptyTag { index } => write!(formatter, "tag at index {index} is empty"),
            Self::TagTooLong { index } => {
                write!(
                    formatter,
                    "tag at index {index} exceeds {MAX_TAG_BYTES} bytes"
                )
            }
            Self::DuplicateTag(tag) => write!(formatter, "duplicate tag {tag:?}"),
        }
    }
}

impl Error for CourseError {}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub(crate) struct CourseDocument {
    id: String,
    title: String,
    tags: Vec<String>,
}

impl TryFrom<CourseDocument> for Course {
    type Error = CourseError;

    fn try_from(document: CourseDocument) -> Result<Self, Self::Error> {
        Self::new(document.id, document.title, document.tags)
    }
}

fn validate_id(id: &str) -> Result<(), CourseError> {
    if id.is_empty() {
        return Err(CourseError::EmptyId);
    }
    if id.len() > MAX_ID_BYTES {
        return Err(CourseError::IdTooLong);
    }
    if let Some(character) = id.chars().find(|character| {
        !character.is_ascii_lowercase() && !character.is_ascii_digit() && *character != '-'
    }) {
        return Err(CourseError::InvalidIdCharacter(character));
    }

    Ok(())
}

fn validate_title(title: &str) -> Result<(), CourseError> {
    if title.is_empty() {
        return Err(CourseError::EmptyTitle);
    }
    if title.chars().count() > MAX_TITLE_CHARACTERS {
        return Err(CourseError::TitleTooLong);
    }

    Ok(())
}

fn validate_tags(tags: &[String]) -> Result<(), CourseError> {
    if tags.len() > MAX_TAGS {
        return Err(CourseError::TooManyTags);
    }

    let mut observed = HashSet::with_capacity(tags.len());
    for (index, tag) in tags.iter().enumerate() {
        if tag.is_empty() {
            return Err(CourseError::EmptyTag { index });
        }
        if tag.len() > MAX_TAG_BYTES {
            return Err(CourseError::TagTooLong { index });
        }
        if !observed.insert(tag.as_str()) {
            return Err(CourseError::DuplicateTag(tag.clone()));
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{Course, CourseError};

    #[test]
    fn rejects_uppercase_id_without_normalizing_it() {
        let result = Course::new(String::from("Rust"), String::from("Rust"), Vec::new());

        assert_eq!(result, Err(CourseError::InvalidIdCharacter('R')));
    }

    #[test]
    fn rejects_duplicate_tag() {
        let result = Course::new(
            String::from("rust"),
            String::from("Rust"),
            vec![String::from("systems"), String::from("systems")],
        );

        assert_eq!(
            result,
            Err(CourseError::DuplicateTag(String::from("systems")))
        );
    }
}
```

Concepts learned:

- private fields prevent callers from bypassing validation;
- early returns make each failed invariant explicit;
- validation rejects invalid data instead of trimming or converting it;
- `deny_unknown_fields` catches misspelled JSON properties;
- `TryFrom` separates transport decoding from domain construction;
- borrowed getters avoid unnecessary clones;
- focused unit tests exercise private validation behavior.

## 4. `src/loader.rs`

```rust
use std::{
    error::Error,
    fmt, fs,
    io::{self, Read},
    path::{Path, PathBuf},
    sync::{
        Arc,
        atomic::{AtomicUsize, Ordering},
        mpsc,
    },
    thread,
};

use crate::course::{Course, CourseDocument, CourseError};

const MAX_FILES: usize = 10_000;
const MAX_FILE_BYTES: u64 = 1_048_576;

#[derive(Debug)]
pub enum LoadError {
    NotDirectory(PathBuf),
    ReadDirectory {
        path: PathBuf,
        source: io::Error,
    },
    ReadEntry {
        path: PathBuf,
        source: io::Error,
    },
    TooManyFiles {
        found: usize,
    },
    ReadMetadata {
        path: PathBuf,
        source: io::Error,
    },
    FileTooLarge {
        path: PathBuf,
        bytes: u64,
    },
    ReadFile {
        path: PathBuf,
        source: io::Error,
    },
    DecodeJson {
        path: PathBuf,
        source: serde_json::Error,
    },
    InvalidCourse {
        path: PathBuf,
        source: CourseError,
    },
}

impl fmt::Display for LoadError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::NotDirectory(path) => write!(formatter, "{} is not a directory", path.display()),
            Self::ReadDirectory { path, .. } => {
                write!(formatter, "failed to read directory {}", path.display())
            }
            Self::ReadEntry { path, .. } => {
                write!(formatter, "failed to read an entry in {}", path.display())
            }
            Self::TooManyFiles { found } => {
                write!(formatter, "found {found} JSON files; limit is {MAX_FILES}")
            }
            Self::ReadMetadata { path, .. } => {
                write!(formatter, "failed to read metadata for {}", path.display())
            }
            Self::FileTooLarge { path, bytes } => write!(
                formatter,
                "{} is {bytes} bytes; limit is {MAX_FILE_BYTES}",
                path.display()
            ),
            Self::ReadFile { path, .. } => write!(formatter, "failed to read {}", path.display()),
            Self::DecodeJson { path, .. } => {
                write!(formatter, "failed to decode JSON from {}", path.display())
            }
            Self::InvalidCourse { path, .. } => {
                write!(formatter, "invalid course in {}", path.display())
            }
        }
    }
}

impl Error for LoadError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::ReadDirectory { source, .. }
            | Self::ReadEntry { source, .. }
            | Self::ReadMetadata { source, .. }
            | Self::ReadFile { source, .. } => Some(source),
            Self::DecodeJson { source, .. } => Some(source),
            Self::InvalidCourse { source, .. } => Some(source),
            Self::NotDirectory(_) | Self::TooManyFiles { .. } | Self::FileTooLarge { .. } => None,
        }
    }
}

pub fn load_courses(directory: &Path) -> Result<Vec<Course>, LoadError> {
    let paths = Arc::new(discover_files(directory)?);
    if paths.is_empty() {
        return Ok(Vec::new());
    }

    let worker_count = thread::available_parallelism()
        .map_or(1, usize::from)
        .min(paths.len());
    let next_index = Arc::new(AtomicUsize::new(0));
    let (sender, receiver) = mpsc::channel();

    thread::scope(|scope| {
        for _ in 0..worker_count {
            let paths = Arc::clone(&paths);
            let next_index = Arc::clone(&next_index);
            let sender = sender.clone();

            scope.spawn(move || {
                loop {
                    let index = next_index.fetch_add(1, Ordering::Relaxed);
                    let Some(path) = paths.get(index) else {
                        break;
                    };

                    if sender.send((index, load_file(path))).is_err() {
                        break;
                    }
                }
            });
        }

        drop(sender);
    });

    let mut results: Vec<_> = receiver.into_iter().collect();
    results.sort_unstable_by_key(|(index, _)| *index);
    results.into_iter().map(|(_, result)| result).collect()
}

fn discover_files(directory: &Path) -> Result<Vec<PathBuf>, LoadError> {
    if !directory.is_dir() {
        return Err(LoadError::NotDirectory(directory.to_path_buf()));
    }

    let entries = fs::read_dir(directory).map_err(|source| LoadError::ReadDirectory {
        path: directory.to_path_buf(),
        source,
    })?;
    let mut paths = Vec::new();

    for entry in entries {
        let entry = entry.map_err(|source| LoadError::ReadEntry {
            path: directory.to_path_buf(),
            source,
        })?;
        let file_type = entry
            .file_type()
            .map_err(|source| LoadError::ReadMetadata {
                path: entry.path(),
                source,
            })?;
        let path = entry.path();

        if file_type.is_file()
            && path
                .extension()
                .is_some_and(|extension| extension == "json")
        {
            paths.push(path);
            if paths.len() > MAX_FILES {
                return Err(LoadError::TooManyFiles { found: paths.len() });
            }
        }
    }

    paths.sort_unstable();
    Ok(paths)
}

fn load_file(path: &Path) -> Result<Course, LoadError> {
    let file = fs::File::open(path).map_err(|source| LoadError::ReadFile {
        path: path.to_path_buf(),
        source,
    })?;
    let metadata = file.metadata().map_err(|source| LoadError::ReadMetadata {
        path: path.to_path_buf(),
        source,
    })?;
    if metadata.len() > MAX_FILE_BYTES {
        return Err(LoadError::FileTooLarge {
            path: path.to_path_buf(),
            bytes: metadata.len(),
        });
    }

    let mut json = String::new();
    file.take(MAX_FILE_BYTES + 1)
        .read_to_string(&mut json)
        .map_err(|source| LoadError::ReadFile {
            path: path.to_path_buf(),
            source,
        })?;
    if json.len() as u64 > MAX_FILE_BYTES {
        return Err(LoadError::FileTooLarge {
            path: path.to_path_buf(),
            bytes: json.len() as u64,
        });
    }

    let document: CourseDocument =
        serde_json::from_str(&json).map_err(|source| LoadError::DecodeJson {
            path: path.to_path_buf(),
            source,
        })?;

    Course::try_from(document).map_err(|source| LoadError::InvalidCourse {
        path: path.to_path_buf(),
        source,
    })
}
```

Concepts learned:

- file discovery is separated from file decoding;
- only regular `.json` files in the selected directory are read;
- file count and byte limits prevent unbounded resource use;
- reading is capped even if a file grows after its metadata check;
- a fixed number of workers pull indices atomically;
- a channel transfers ownership of results back to the caller;
- sorting by discovery index makes the reported first error deterministic;
- errors retain their path and original source.

`Ordering::Relaxed` is sufficient for the counter because it only gives each worker a unique index. The channel supplies the synchronization needed to transfer each completed result.

## 5. `src/index.rs`

```rust
use std::{collections::BTreeMap, error::Error, fmt};

use crate::Course;

#[derive(Debug, Default)]
pub struct CourseIndex {
    courses: BTreeMap<String, Course>,
}

impl CourseIndex {
    pub fn from_courses(courses: Vec<Course>) -> Result<Self, IndexError> {
        let mut index = Self::default();

        for course in courses {
            let id = course.id().to_owned();
            if index.courses.insert(id.clone(), course).is_some() {
                return Err(IndexError::DuplicateId(id));
            }
        }

        Ok(index)
    }

    #[must_use]
    pub fn len(&self) -> usize {
        self.courses.len()
    }

    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.courses.is_empty()
    }

    pub fn iter(&self) -> impl Iterator<Item = &Course> {
        self.courses.values()
    }
}

#[derive(Debug, Eq, PartialEq)]
pub enum IndexError {
    DuplicateId(String),
}

impl fmt::Display for IndexError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DuplicateId(id) => write!(formatter, "duplicate course ID {id:?}"),
        }
    }
}

impl Error for IndexError {}
```

Concepts learned:

- `BTreeMap` keeps output sorted by course ID;
- consuming the input vector avoids cloning complete courses;
- duplicate IDs fail the index operation;
- `impl Iterator` exposes traversal without exposing the internal map.

## 6. `src/main.rs`

```rust
use std::{env, error::Error, io, path::PathBuf, process::ExitCode};

use rust_course_indexer::{CourseIndex, load_courses};

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            report_error(error.as_ref());
            ExitCode::FAILURE
        }
    }
}

fn run() -> Result<(), Box<dyn Error>> {
    let directory = parse_directory_argument()?;
    let courses = load_courses(&directory)?;
    let index = CourseIndex::from_courses(courses)?;

    for course in index.iter() {
        println!(
            "{}\t{}\t{}",
            course.id(),
            course.title(),
            course.tags().join(",")
        );
    }
    println!("total\t{}", index.len());

    Ok(())
}

fn parse_directory_argument() -> Result<PathBuf, io::Error> {
    let mut arguments = env::args_os();
    let executable = arguments.next().unwrap_or_default();
    let directory = arguments.next().ok_or_else(|| {
        io::Error::new(
            io::ErrorKind::InvalidInput,
            format!(
                "usage: {} <course-directory>",
                PathBuf::from(executable).display()
            ),
        )
    })?;

    if arguments.next().is_some() {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "expected exactly one course-directory argument",
        ));
    }

    Ok(PathBuf::from(directory))
}

fn report_error(error: &(dyn Error + 'static)) {
    eprintln!("error: {error}");

    let mut source = error.source();
    while let Some(cause) = source {
        eprintln!("caused by: {cause}");
        source = cause.source();
    }
}
```

Concepts learned:

- `main` converts success or failure into a process exit code;
- `args_os` accepts platform paths without forcing Unicode conversion;
- exactly one argument is required;
- errors are printed once at the application boundary;
- the source chain retains detailed diagnostics;
- normal results go to stdout and diagnostics go to stderr.

## 7. `tests/indexer.rs`

```rust
use std::fs;

use rust_course_indexer::{CourseIndex, LoadError, load_courses};

#[test]
fn loads_and_indexes_courses_in_id_order() {
    let directory = tempfile::tempdir().expect("temporary directory");
    fs::write(
        directory.path().join("rust.json"),
        r#"{"id":"rust","title":"Rust","tags":["systems","safe"]}"#,
    )
    .expect("write Rust fixture");
    fs::write(
        directory.path().join("go.json"),
        r#"{"id":"go","title":"Go","tags":["services"]}"#,
    )
    .expect("write Go fixture");

    let courses = load_courses(directory.path()).expect("valid courses");
    let index = CourseIndex::from_courses(courses).expect("unique IDs");
    let ids: Vec<_> = index.iter().map(|course| course.id()).collect();

    assert_eq!(ids, ["go", "rust"]);
}

#[test]
fn rejects_unknown_json_field() {
    let directory = tempfile::tempdir().expect("temporary directory");
    fs::write(
        directory.path().join("course.json"),
        r#"{"id":"rust","title":"Rust","tags":[],"titel":"misspelled"}"#,
    )
    .expect("write invalid fixture");

    let error = load_courses(directory.path()).expect_err("unknown field must fail");

    assert!(matches!(error, LoadError::DecodeJson { .. }));
}
```

Concepts learned:

- integration tests use only public exports;
- temporary directories isolate filesystem tests;
- deterministic ordering is asserted;
- strict decoding prevents ignored spelling mistakes.

## Example Input

Create `courses/go.json`:

```json
{"id":"go","title":"Go Concurrency","tags":["go","channels"]}
```

Create `courses/rust.json`:

```json
{"id":"rust","title":"Rust Ownership","tags":["rust","memory-safety"]}
```

Run:

```powershell
cargo run --release -- courses
```

Output:

```text
go      Go Concurrency  go,channels
rust    Rust Ownership  rust,memory-safety
total   2
```

The display above aligns tabs for readability; exact spacing depends on the terminal's tab width.

## Verify the Project

```powershell
cargo fmt --check
cargo check --all-targets
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
cargo doc --no-deps
```

## Failure Exercises

Try one change at a time and predict the error before running:

1. Add an unknown JSON property.
2. Change an ID to `Rust`.
3. Repeat a tag.
4. Put the same ID in two files.
5. Pass a file instead of a directory.
6. Create a JSON file larger than 1 MiB.
7. Remove the command-line argument.

Then trace the failure through discovery, decoding, domain validation, indexing, and the final error-source report.

## Production Extension Decisions

Add a feature only when the requirement exists:

- recursive discovery needs a root-containment and symlink policy;
- cancellation needs an explicit signal shared with workers;
- very large indexes need a streaming or database design;
- long-running service mode needs structured tracing and shutdown handling;
- remote input needs timeouts, authentication, authorization, and body limits;
- user-visible error formats need stable error codes separate from internal causes.

The current project stays deliberately small while demonstrating complete boundaries and failure behavior.
