# 08 - Errors, Panic, Recovery, Validation, and Cleanup

## Errors Are Values

```go
func ParseLevel(value string) (int, error) {
	level, err := strconv.Atoi(value)
	if err != nil {
		return 0, fmt.Errorf("parse level %q: %w", value, err)
	}
	if level < 1 || level > 5 {
		return 0, fmt.Errorf("level must be between 1 and 5")
	}
	return level, nil
}
```

Add context and wrap with `%w` when callers need to inspect the cause.

## Check Immediately

```go
level, err := ParseLevel("3")
if err != nil {
	log.Fatal(err)
}
fmt.Println(level)
// Output: 3
```

Do not continue with a zero/fake value after invalid input.

## Sentinel Errors

```go
var ErrCourseNotFound = errors.New("course not found")

if errors.Is(err, ErrCourseNotFound) {
	// translate to a 404 or domain result
}
```

Export a sentinel only when identity is part of the API. Its message should not be the only machine-readable contract.

## Typed Errors

```go
type ValidationError struct {
	Field string
	Rule  string
}

func (err *ValidationError) Error() string {
	return fmt.Sprintf("%s: %s", err.Field, err.Rule)
}

var validationError *ValidationError
if errors.As(err, &validationError) {
	fmt.Println(validationError.Field)
}
```

Use typed errors when callers need structured information.

## Error Joining

```go
err := errors.Join(firstErr, secondErr)
```

Joining preserves several causes for `errors.Is`/`As`. Use it for independent cleanup/validation failures, not to avoid choosing the primary operational outcome.

## Validation

Validation verifies; it should not silently coerce.

```go
func ValidateCourse(course Course) error {
	var problems []error
	if course.ID == "" {
		problems = append(problems, &ValidationError{Field: "id", Rule: "required"})
	}
	if course.Title == "" {
		problems = append(problems, &ValidationError{Field: "title", Rule: "required"})
	}
	return errors.Join(problems...)
}
```

Fail fast or return all independent field errors according to the API contract.

## Panic

Panic stops normal control flow and unwinds the goroutine stack while running deferred calls.

Use panic for unrecoverable programmer invariants or runtime failures, not ordinary bad requests, missing files, or expected network errors.

```go
func mustPositive(value int) int {
	if value <= 0 {
		panic("value must be positive")
	}
	return value
}
```

## Recover

`recover` works only inside a deferred function in the same goroutine during panic unwinding.

```go
func safeHandler(next http.Handler) http.Handler {
	return http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		defer func() {
			if recovered := recover(); recovered != nil {
				http.Error(writer, "internal server error", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(writer, request)
	})
}
```

Recovery boundaries should log safe operational context and stack evidence, then fail the request/task. Do not recover and continue with possibly corrupted state.

## Cleanup Errors

For read-only resources, deferred close is often enough. For writers, close/flush can report data loss:

```go
func WriteFile(path string, data []byte) (err error) {
	file, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("create file: %w", err)
	}
	defer func() {
		err = errors.Join(err, file.Close())
	}()

	if _, err := file.Write(data); err != nil {
		return fmt.Errorf("write file: %w", err)
	}
	return nil
}
```

## Error Boundaries

```text
low-level package -> wrap context -> service classifies -> transport translates -> logs/metrics record safe category
```

Do not expose database errors, stack traces, file paths, secrets, or internal types to clients.

## Production Rules

- expected failures return errors
- add operation context once
- preserve causes with `%w`
- inspect with `errors.Is`/`As`
- validate external input before work
- never ignore errors without a documented reason
- recover only at process/task/request boundaries
- handle close/flush errors when durability matters
- keep client messages stable and safe
