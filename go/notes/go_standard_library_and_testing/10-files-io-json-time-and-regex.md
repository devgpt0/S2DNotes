# 10 - Files, I/O, JSON, Time, and Regular Expressions

## `io.Reader` and `io.Writer`

Go I/O composes around small interfaces:

```go
type Reader interface {
	Read([]byte) (int, error)
}

type Writer interface {
	Write([]byte) (int, error)
}
```

## Copy a Stream

```go
source := strings.NewReader("Go course")
var destination strings.Builder
written, err := io.Copy(&destination, source)
if err != nil {
	log.Fatal(err)
}
fmt.Println(written, destination.String())
// Output: 9 Go course
```

Stream data instead of loading everything when inputs can be large.

## Read a Small File

```go
data, err := os.ReadFile("course.txt")
if err != nil {
	return fmt.Errorf("read course file: %w", err)
}
fmt.Println(string(data))
```

`ReadFile` is appropriate only when size is bounded and acceptable in memory.

## Safe Paths

Never join untrusted input and assume it remains under a root:

```go
func SafePath(root, name string) (string, error) {
	if filepath.IsAbs(name) {
		return "", errors.New("absolute path is not allowed")
	}
	clean := filepath.Clean(name)
	if clean == "." || clean == ".." || strings.HasPrefix(clean, ".."+string(filepath.Separator)) {
		return "", errors.New("path escapes root")
	}
	return filepath.Join(root, clean), nil
}
```

Symlinks and race conditions require stronger OS-specific containment when attackers can control filesystem contents.

## Buffered I/O

```go
scanner := bufio.NewScanner(reader)
for scanner.Scan() {
	fmt.Println(scanner.Text())
}
if err := scanner.Err(); err != nil {
	return err
}
```

Scanner has a token-size limit. Increase it intentionally or use `bufio.Reader` for larger records.

## JSON Encode

```go
type Course struct {
	ID    string `json:"id"`
	Title string `json:"title"`
}

data, err := json.Marshal(Course{ID: "go", Title: "Go"})
if err != nil {
	log.Fatal(err)
}
fmt.Println(string(data))
// Output: {"id":"go","title":"Go"}
```

Only exported fields are encoded.

## Strict JSON Decode

```go
func DecodeCourse(reader io.Reader) (Course, error) {
	decoder := json.NewDecoder(io.LimitReader(reader, 1<<20))
	decoder.DisallowUnknownFields()

	var course Course
	if err := decoder.Decode(&course); err != nil {
		return Course{}, fmt.Errorf("decode course: %w", err)
	}
	if err := ValidateCourse(course); err != nil {
		return Course{}, err
	}
	if decoder.More() {
		return Course{}, errors.New("unexpected additional JSON value")
	}
	return course, nil
}
```

Limit bodies, reject unknown fields when contract requires it, validate semantics, and ensure only one JSON value. A robust implementation may perform a second decode expecting `io.EOF`.

## Time

```go
start := time.Date(2026, time.July, 19, 0, 0, 0, 0, time.UTC)
fmt.Println(start.AddDate(0, 0, 7).Format(time.DateOnly))
// Output: 2026-07-26
```

- use `time.Time` with explicit location
- use `time.Duration` for elapsed limits
- compare instants with `Before`, `After`, `Equal`
- inject a clock when deterministic tests need current time

## Timers and Tickers

```go
timer := time.NewTimer(100 * time.Millisecond)
defer timer.Stop()
select {
case <-timer.C:
	fmt.Println("timer fired")
}
```

Stop tickers and define cancellation. Prefer context deadlines for request-scoped operations.

## Regular Expressions

Go uses RE2-style regular expressions with linear-time guarantees for supported syntax.

```go
var courseIDPattern = regexp.MustCompile(`^[a-z][a-z0-9-]{1,31}$`)
fmt.Println(courseIDPattern.MatchString("go-basics"))
// Output: true
```

Use `MustCompile` only for trusted constant patterns. Use `Compile` for external patterns and bound input/work.

## Serialization Boundaries

JSON loses Go-specific types and may need explicit representations:

- time: RFC 3339 string or documented format
- duration: string or numeric unit with contract
- bytes: base64 under JSON rules
- large integers: client compatibility policy
- nullable vs absent: pointers/custom types when distinction matters

## Expert Rules

- stream unbounded data
- limit request/file sizes
- close resources and handle important close errors
- validate paths beyond string joining
- strictly decode known schemas
- separate syntax decoding from semantic validation
- use explicit time zones/formats
- compile trusted regex once
