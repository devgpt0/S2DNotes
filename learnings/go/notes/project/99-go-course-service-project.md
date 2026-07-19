# 99 - Complete Go Project: Concurrent Course Service

## Project Overview

Build a production-shaped HTTP service using only the Go standard library. It validates JSON strictly, keeps domain rules outside HTTP, protects an in-memory repository with a mutex, propagates context, returns safe errors, tests behavior, and shuts down gracefully.

## What You Learn

- module and `internal` layout
- domain validation and error identity
- consumer-owned repository interface
- concurrency-safe in-memory storage
- strict bounded HTTP JSON handling
- dependency construction
- table/integration tests
- timeouts and signal-based shutdown

## Folder Structure

```text
go-course-service/
|-- go.mod
|-- cmd/api/main.go
`-- internal/course/
    |-- course.go
    |-- handler.go
    |-- handler_test.go
    |-- memory_repository.go
    |-- service.go
    `-- service_test.go
```

## File: `go.mod`

```go
module example.com/go-course-service

go 1.24
```

Use the current stable Go version supported by your environment; update the directive through a reviewed toolchain upgrade.

Concepts learned: one module, no unnecessary dependencies, reproducible language intent.

## File: `internal/course/course.go`

```go
package course

import (
	"errors"
	"fmt"
	"strings"
)

var ErrNotFound = errors.New("course not found")

type ValidationError struct {
	Field string
	Rule  string
}

func (err *ValidationError) Error() string {
	return fmt.Sprintf("%s: %s", err.Field, err.Rule)
}

type Course struct {
	ID    string `json:"id"`
	Title string `json:"title"`
}

func New(id, title string) (Course, error) {
	if id == "" {
		return Course{}, &ValidationError{Field: "id", Rule: "required"}
	}
	if title == "" {
		return Course{}, &ValidationError{Field: "title", Rule: "required"}
	}
	if len(id) > 64 {
		return Course{}, &ValidationError{Field: "id", Rule: "maximum length is 64 bytes"}
	}
	if len(title) > 200 {
		return Course{}, &ValidationError{Field: "title", Rule: "maximum length is 200 bytes"}
	}
	if strings.TrimSpace(id) != id {
		return Course{}, &ValidationError{Field: "id", Rule: "leading or trailing whitespace is not allowed"}
	}
	if strings.TrimSpace(title) != title {
		return Course{}, &ValidationError{Field: "title", Rule: "leading or trailing whitespace is not allowed"}
	}
	for _, character := range id {
		valid := character >= 'a' && character <= 'z' ||
			character >= '0' && character <= '9' ||
			character == '-'
		if !valid {
			return Course{}, &ValidationError{Field: "id", Rule: "use lowercase ASCII letters, digits, or hyphens"}
		}
	}
	return Course{ID: id, Title: title}, nil
}
```

Concepts learned: stable domain errors, validated construction, exported response fields, no transport coupling, and strict validation that rejects rather than rewrites input.

## File: `internal/course/service.go`

```go
package course

import "context"

type Repository interface {
	Create(context.Context, Course) error
	FindByID(context.Context, string) (Course, error)
}

type Service struct {
	repository Repository
}

func NewService(repository Repository) *Service {
	if repository == nil {
		panic("course repository is required")
	}
	return &Service{repository: repository}
}

func (service *Service) Create(ctx context.Context, id, title string) (Course, error) {
	course, err := New(id, title)
	if err != nil {
		return Course{}, err
	}
	if err := service.repository.Create(ctx, course); err != nil {
		return Course{}, err
	}
	return course, nil
}

func (service *Service) FindByID(ctx context.Context, id string) (Course, error) {
	if err := ctx.Err(); err != nil {
		return Course{}, err
	}
	return service.repository.FindByID(ctx, id)
}
```

Concepts learned: small consumer-owned interface, explicit dependency, context-first methods, validation before persistence.

## File: `internal/course/memory_repository.go`

```go
package course

import (
	"context"
	"errors"
	"sync"
)

var ErrDuplicateID = errors.New("course id already exists")

type MemoryRepository struct {
	mu      sync.RWMutex
	courses map[string]Course
}

func NewMemoryRepository() *MemoryRepository {
	return &MemoryRepository{courses: make(map[string]Course)}
}

func (repository *MemoryRepository) Create(ctx context.Context, value Course) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	repository.mu.Lock()
	defer repository.mu.Unlock()
	if _, exists := repository.courses[value.ID]; exists {
		return ErrDuplicateID
	}
	repository.courses[value.ID] = value
	return nil
}

func (repository *MemoryRepository) FindByID(ctx context.Context, id string) (Course, error) {
	if err := ctx.Err(); err != nil {
		return Course{}, err
	}
	repository.mu.RLock()
	defer repository.mu.RUnlock()
	value, exists := repository.courses[id]
	if !exists {
		return Course{}, ErrNotFound
	}
	return value, nil
}
```

Concepts learned: one mutex protects the map invariant, readers use read lock, context is checked, duplicate/not-found results stay explicit.

## File: `internal/course/handler.go`

```go
package course

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log/slog"
	"net/http"
)

const maxRequestBody = 1 << 20

type Handler struct {
	service *Service
	logger  *slog.Logger
}

func NewHandler(service *Service, logger *slog.Logger) *Handler {
	if service == nil {
		panic("course service is required")
	}
	if logger == nil {
		panic("logger is required")
	}
	return &Handler{service: service, logger: logger}
}

type createRequest struct {
	ID    string `json:"id"`
	Title string `json:"title"`
}

func (handler *Handler) Register(mux *http.ServeMux) {
	mux.HandleFunc("POST /courses", handler.Create)
	mux.HandleFunc("GET /courses/{id}", handler.Get)
}

func (handler *Handler) Create(writer http.ResponseWriter, request *http.Request) {
	request.Body = http.MaxBytesReader(writer, request.Body, maxRequestBody)
	defer request.Body.Close()

	decoder := json.NewDecoder(request.Body)
	decoder.DisallowUnknownFields()
	var input createRequest
	if err := decoder.Decode(&input); err != nil {
		if responseErr := writeError(writer, http.StatusBadRequest, "invalid JSON request"); responseErr != nil {
			handler.logger.WarnContext(request.Context(), "response write failed", "error", responseErr)
		}
		return
	}
	if err := ensureJSONEnd(decoder); err != nil {
		if responseErr := writeError(writer, http.StatusBadRequest, "request must contain one JSON object"); responseErr != nil {
			handler.logger.WarnContext(request.Context(), "response write failed", "error", responseErr)
		}
		return
	}

	created, err := handler.service.Create(request.Context(), input.ID, input.Title)
	if err != nil {
		if responseErr := writeDomainError(writer, err); responseErr != nil {
			handler.logger.WarnContext(request.Context(), "response write failed", "error", responseErr)
		}
		return
	}
	if err := writeJSON(writer, http.StatusCreated, created); err != nil {
		handler.logger.WarnContext(request.Context(), "response write failed", "error", err)
	}
}

func (handler *Handler) Get(writer http.ResponseWriter, request *http.Request) {
	value, err := handler.service.FindByID(request.Context(), request.PathValue("id"))
	if err != nil {
		if responseErr := writeDomainError(writer, err); responseErr != nil {
			handler.logger.WarnContext(request.Context(), "response write failed", "error", responseErr)
		}
		return
	}
	if err := writeJSON(writer, http.StatusOK, value); err != nil {
		handler.logger.WarnContext(request.Context(), "response write failed", "error", err)
	}
}

func ensureJSONEnd(decoder *json.Decoder) error {
	var extra any
	if err := decoder.Decode(&extra); !errors.Is(err, io.EOF) {
		if err == nil {
			return errors.New("additional JSON value")
		}
		return err
	}
	return nil
}

func writeDomainError(writer http.ResponseWriter, err error) error {
	status := http.StatusInternalServerError
	message := "internal server error"
	var validation *ValidationError
	switch {
	case errors.As(err, &validation):
		status, message = http.StatusBadRequest, "invalid course"
	case errors.Is(err, ErrNotFound):
		status, message = http.StatusNotFound, "course not found"
	case errors.Is(err, ErrDuplicateID):
		status, message = http.StatusConflict, "course id already exists"
	}
	return writeError(writer, status, message)
}

func writeError(writer http.ResponseWriter, status int, message string) error {
	return writeJSON(writer, status, map[string]string{"error": message})
}

func writeJSON(writer http.ResponseWriter, status int, value any) error {
	payload, err := json.Marshal(value)
	if err != nil {
		return fmt.Errorf("encode JSON response: %w", err)
	}
	payload = append(payload, '\n')
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(status)
	if _, err := writer.Write(payload); err != nil {
		return fmt.Errorf("write JSON response: %w", err)
	}
	return nil
}
```

Concepts learned: method-aware routes, body limit, strict decoder, one-value check, safe error translation, response error propagation, and contextual operational logging.

The response is encoded before headers are written. A client disconnect can still make `Write` fail after the status has been committed; that failure is logged without attempting a second response.

## File: `cmd/api/main.go`

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"example.com/go-course-service/internal/course"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	if err := run(logger); err != nil {
		logger.Error("server stopped", "error", err)
		os.Exit(1)
	}
}

func run(logger *slog.Logger) error {
	repository := course.NewMemoryRepository()
	service := course.NewService(repository)
	handler := course.NewHandler(service, logger)
	mux := http.NewServeMux()
	handler.Register(mux)

	server := &http.Server{
		Addr:              ":8080",
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	serverErrors := make(chan error, 1)
	go func() {
		logger.Info("server starting", "address", server.Addr)
		serverErrors <- server.ListenAndServe()
	}()

	select {
	case <-ctx.Done():
		logger.Info("shutdown requested")
	case err := <-serverErrors:
		if !errors.Is(err, http.ErrServerClosed) {
			return fmt.Errorf("serve HTTP: %w", err)
		}
		return nil
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer cancel()
	if err := server.Shutdown(shutdownCtx); err != nil {
		if closeErr := server.Close(); closeErr != nil {
			return errors.Join(
				fmt.Errorf("graceful shutdown: %w", err),
				fmt.Errorf("force close: %w", closeErr),
			)
		}
		return fmt.Errorf("graceful shutdown: %w", err)
	}

	if err := <-serverErrors; !errors.Is(err, http.ErrServerClosed) {
		return fmt.Errorf("serve HTTP during shutdown: %w", err)
	}
	return nil
}
```

Concepts learned: explicit wiring, structured logs, bounded server timeouts, owned error channel, signal cancellation, graceful/forced close, and a non-zero exit for runtime failure.

## File: `internal/course/service_test.go`

```go
package course

import (
	"context"
	"errors"
	"testing"
)

func TestServiceCreateAndFind(t *testing.T) {
	service := NewService(NewMemoryRepository())
	created, err := service.Create(context.Background(), "go", "Go Foundations")
	if err != nil {
		t.Fatal(err)
	}
	found, err := service.FindByID(context.Background(), created.ID)
	if err != nil {
		t.Fatal(err)
	}
	if found != created {
		t.Fatalf("found = %#v, want %#v", found, created)
	}
}

func TestServiceRejectsInvalidCourse(t *testing.T) {
	service := NewService(NewMemoryRepository())
	tests := []struct {
		name  string
		id    string
		title string
	}{
		{name: "empty title", id: "go", title: ""},
		{name: "uppercase id", id: "Go", title: "Go"},
		{name: "padded title", id: "go", title: " Go "},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			_, err := service.Create(context.Background(), test.id, test.title)
			var validation *ValidationError
			if !errors.As(err, &validation) {
				t.Fatalf("error = %v, want ValidationError", err)
			}
		})
	}
}
```

Concepts learned: real service/repository integration, table-driven validation tests, error type assertion, strict rejection without normalization, and no mocking framework.

## File: `internal/course/handler_test.go`

```go
package course

import (
	"io"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestCreateAndGetCourse(t *testing.T) {
	logger := slog.New(slog.NewTextHandler(io.Discard, nil))
	handler := NewHandler(NewService(NewMemoryRepository()), logger)
	mux := http.NewServeMux()
	handler.Register(mux)

	createRequest := httptest.NewRequest(
		http.MethodPost,
		"/courses",
		strings.NewReader(`{"id":"go","title":"Go Foundations"}`),
	)
	createRecorder := httptest.NewRecorder()
	mux.ServeHTTP(createRecorder, createRequest)
	if createRecorder.Code != http.StatusCreated {
		t.Fatalf("create status = %d, want %d", createRecorder.Code, http.StatusCreated)
	}

	getRequest := httptest.NewRequest(http.MethodGet, "/courses/go", nil)
	getRecorder := httptest.NewRecorder()
	mux.ServeHTTP(getRecorder, getRequest)
	if getRecorder.Code != http.StatusOK {
		t.Fatalf("get status = %d, want %d", getRecorder.Code, http.StatusOK)
	}
	if !strings.Contains(getRecorder.Body.String(), `"title":"Go Foundations"`) {
		t.Fatalf("unexpected body: %s", getRecorder.Body.String())
	}
}
```

Concepts learned: complete HTTP flow, real router path values, status/body verification.

## Run and Verify

```powershell
gofmt -w .
go test ./...
go test -race ./...
go vet ./...
go run ./cmd/api
```

```powershell
curl.exe -X POST http://localhost:8080/courses -H "Content-Type: application/json" -d '{"id":"go","title":"Go Foundations"}'
curl.exe http://localhost:8080/courses/go
# Response: {"id":"go","title":"Go Foundations"}
```

## Completion Definition

Formatting, tests, race detector, and vet pass; invalid/unknown/duplicate input returns safe status; concurrent repository access is protected; request work accepts context; server timeouts and graceful shutdown are verified.
