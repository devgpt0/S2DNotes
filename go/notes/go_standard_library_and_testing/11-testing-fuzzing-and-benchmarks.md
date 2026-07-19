# 11 - Testing, Table Tests, Fuzzing, Examples, and Benchmarks

## Basic Test

```go
func TestSum(t *testing.T) {
	got := Sum([]int{1, 2, 3})
	if got != 6 {
		t.Fatalf("Sum() = %d, want 6", got)
	}
}
```

Run:

```powershell
go test ./...
```

## Table-Driven Test

```go
func TestParseLevel(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    int
		wantErr bool
	}{
		{name: "valid", input: "3", want: 3},
		{name: "not a number", input: "x", wantErr: true},
		{name: "out of range", input: "8", wantErr: true},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got, err := ParseLevel(test.input)
			if (err != nil) != test.wantErr {
				t.Fatalf("error = %v, wantErr %t", err, test.wantErr)
			}
			if !test.wantErr && got != test.want {
				t.Fatalf("value = %d, want %d", got, test.want)
			}
		})
	}
}
```

Each subtest has its own descriptive case.

## Test Helpers

```go
func requireNoError(t *testing.T, err error) {
	t.Helper()
	if err != nil {
		t.Fatal(err)
	}
}
```

Keep helpers focused; do not build a private assertion framework.

## Error Assertions

```go
if !errors.Is(err, ErrCourseNotFound) {
	t.Fatalf("error = %v, want ErrCourseNotFound", err)
}
```

Do not compare wrapped error strings.

## Fakes

```go
type memoryRepository struct {
	courses map[string]Course
}

func (repository *memoryRepository) Save(_ context.Context, course Course) error {
	repository.courses[course.ID] = course
	return nil
}
```

Small stateful fakes often test behavior better than interaction-heavy mocks.

## HTTP Tests

```go
request := httptest.NewRequest(http.MethodGet, "/courses/go", nil)
recorder := httptest.NewRecorder()
handler.ServeHTTP(recorder, request)

if recorder.Code != http.StatusOK {
	t.Fatalf("status = %d, want %d", recorder.Code, http.StatusOK)
}
```

Test status, headers, body schema, errors, limits, and cancellation where relevant.

## Example Tests

```go
func ExampleSum() {
	fmt.Println(Sum([]int{1, 2, 3}))
	// Output: 6
}
```

Examples become documentation and executable output checks.

## Fuzzing

```go
func FuzzParseLevel(f *testing.F) {
	f.Add("3")
	f.Add("invalid")
	f.Fuzz(func(t *testing.T, input string) {
		level, err := ParseLevel(input)
		if err == nil && (level < 1 || level > 5) {
			t.Fatalf("accepted out-of-range level %d", level)
		}
	})
}
```

Run:

```powershell
go test -fuzz=FuzzParseLevel ./...
```

Fuzz invariants and parsers. Seed meaningful edge cases and preserve discovered failures.

## Benchmarks

```go
func BenchmarkSum(b *testing.B) {
	values := []int{1, 2, 3, 4, 5}
	for b.Loop() {
		_ = Sum(values)
	}
}
```

Use the benchmark loop API supported by the current toolchain. Record Go version, CPU, input, allocations, and environment.

```powershell
go test -bench=. -benchmem ./...
```

## Race Detector

```powershell
go test -race ./...
```

It detects races exercised by the run, not every theoretical race. Use realistic concurrent tests.

## Test Isolation

- use `t.TempDir()` for files
- use `t.Setenv()` for environment
- inject time/random/IDs when deterministic behavior matters
- avoid shared mutable package globals
- use `t.Cleanup()` for teardown
- parallelize only independent tests

## Golden Files

Golden output can help stable complex formatting. Review updates explicitly; do not add an automatic “update all” mode to normal CI.

## Production Test Pyramid

- unit: domain rules
- package integration: repository/adapter
- HTTP: transport contract
- end-to-end: critical flow with real dependencies
- fuzz: parser/invariant robustness
- benchmark/profile: measured hot path

## Final Rules

- descriptive failure messages
- behavior over implementation
- explicit error cases
- deterministic dependencies
- race tests for concurrency
- benchmarks only for decisions
- no network-dependent unit tests
