# 98 - Go Expert Tips and Production Snippets

## Design Principles

- synchronous before concurrent
- concrete types until an interface is needed
- small consumer-owned interfaces
- explicit errors and dependencies
- zero values that work when practical
- bounded work, queues, retries, and memory
- standard library before dependencies
- measurement before optimization

## Context-Aware Send

```go
func Send[T any](ctx context.Context, output chan<- T, value T) error {
	select {
	case output <- value:
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}
```

Prevents a producer from leaking forever after consumers stop.

## Bounded Parallel Map

```go
func ParallelMap[T, R any](
	ctx context.Context,
	values []T,
	limit int,
	operation func(context.Context, T) (R, error),
) ([]R, error) {
	if limit <= 0 {
		return nil, errors.New("limit must be positive")
	}
	results := make([]R, len(values))
	group, groupCtx := errgroup.WithContext(ctx)
	group.SetLimit(limit)
	for index, value := range values {
		index, value := index, value
		group.Go(func() error {
			result, err := operation(groupCtx, value)
			if err != nil {
				return err
			}
			results[index] = result
			return nil
		})
	}
	if err := group.Wait(); err != nil {
		return nil, err
	}
	return results, nil
}
```

This uses `golang.org/x/sync/errgroup`, preserves order, bounds concurrency, and cancels related work after failure.

## Retry Policy

```go
func Retry(ctx context.Context, attempts int, operation func(context.Context) error) error {
	if attempts <= 0 {
		return errors.New("attempts must be positive")
	}
	var err error
	for attempt := 1; attempt <= attempts; attempt++ {
		if err = operation(ctx); err == nil {
			return nil
		}
		if attempt == attempts {
			break
		}
		delay := time.Duration(attempt) * 100 * time.Millisecond
		timer := time.NewTimer(delay)
		select {
		case <-timer.C:
		case <-ctx.Done():
			if !timer.Stop() {
				<-timer.C
			}
			return ctx.Err()
		}
	}
	return fmt.Errorf("operation failed after %d attempts: %w", attempts, err)
}
```

Use only for classified transient failures and idempotent/safely deduplicated operations. Add jitter in distributed production systems.

## Atomic Immutable Snapshot

```go
type ConfigStore struct {
	value atomic.Pointer[Config]
}

func (store *ConfigStore) Load() *Config {
	return store.value.Load()
}

func (store *ConfigStore) Replace(config *Config) error {
	if config == nil {
		return errors.New("config is required")
	}
	copyOfConfig := *config
	store.value.Store(&copyOfConfig)
	return nil
}
```

Readers receive an immutable snapshot. Never mutate a published config.

## HTTP Error Translation

```go
func WriteError(writer http.ResponseWriter, err error) {
	status := http.StatusInternalServerError
	message := "internal server error"

	switch {
	case errors.Is(err, ErrCourseNotFound):
		status, message = http.StatusNotFound, "course not found"
	default:
		var validation *ValidationError
		if errors.As(err, &validation) {
			status, message = http.StatusBadRequest, "invalid request"
		}
	}

	http.Error(writer, message, status)
}
```

Clients get stable safe messages; internal logs retain wrapped detail separately.

## Defensive Slice Copy

```go
func CloneCourses(values []Course) []Course {
	return append([]Course(nil), values...)
}
```

This is shallow. Clone nested mutable fields if the ownership contract requires it.

## Expert Review

- can a goroutine block after its owner returns?
- who closes each channel?
- are all queues and pools bounded?
- does every network/database call have context/deadline?
- are errors classified without string matching?
- are interfaces owned by consumers?
- can internal slices/maps escape and mutate state?
- is telemetry safe and bounded-cardinality?
- does profile evidence support optimization?
- does shutdown drain every worker/resource?

## Avoid Cleverness

Do not add reflection, unsafe, code generation, custom pools, generic frameworks, or lock-free algorithms until a measured/architectural need is clear. Straightforward Go is a production feature.
