# 14 - HTTP Services, Databases, Security, and Graceful Shutdown

## HTTP Handler

```go
func healthHandler(writer http.ResponseWriter, request *http.Request) {
	if request.Method != http.MethodGet {
		http.Error(writer, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(http.StatusOK)
	_, _ = io.WriteString(writer, `{"status":"ok"}`)
}
```

For important writes, handle returned write errors where the server architecture can observe them.

## Server Timeouts

```go
server := &http.Server{
	Addr:              ":8080",
	Handler:           handler,
	ReadHeaderTimeout: 5 * time.Second,
	ReadTimeout:       10 * time.Second,
	WriteTimeout:      15 * time.Second,
	IdleTimeout:       60 * time.Second,
}
```

Choose timeouts from workload and proxy behavior. Never rely on zero defaults blindly for an internet-facing service.

## Request Body Limit and Strict Decode

```go
func createCourse(writer http.ResponseWriter, request *http.Request) {
	request.Body = http.MaxBytesReader(writer, request.Body, 1<<20)
	defer request.Body.Close()

	course, err := DecodeCourse(request.Body)
	if err != nil {
		http.Error(writer, "invalid request", http.StatusBadRequest)
		return
	}
	_ = course
}
```

Reject invalid input before business work. Do not expose decoder internals to clients.

## Context Propagation

Pass `request.Context()` through service, database, and external HTTP calls. Stop work when the client/server deadline is cancelled.

## HTTP Client

```go
client := &http.Client{Timeout: 10 * time.Second}
request, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
if err != nil {
	return err
}
response, err := client.Do(request)
```

Reuse clients/transports. Always close response bodies and drain/reuse connections according to response handling.

## Database

`sql.DB` is a concurrency-safe connection pool, not one connection.

```go
database, err := sql.Open("driver-name", dataSourceName)
if err != nil {
	return err
}
database.SetMaxOpenConns(20)
database.SetMaxIdleConns(10)
database.SetConnMaxLifetime(time.Hour)
```

Driver import/configuration is deployment-specific. Ping with context during startup when readiness requires connectivity.

## Parameterized Queries

```go
row := database.QueryRowContext(ctx,
	"SELECT id, title FROM courses WHERE id = ?",
	id,
)
```

Placeholder syntax differs by driver. Never concatenate untrusted values into SQL. Allowlist dynamic identifiers such as sort columns.

## Transactions

```go
transaction, err := database.BeginTx(ctx, nil)
if err != nil {
	return err
}
defer transaction.Rollback()

// Execute all related statements with transaction.

if err := transaction.Commit(); err != nil {
	return fmt.Errorf("commit transaction: %w", err)
}
```

Rollback after commit is harmless according to database/sql behavior. Keep transactions short and avoid external network calls inside them.

## Authentication and Authorization

- TLS at the edge/service boundary
- server validates session/token
- every operation authorizes resource/action
- least privilege database/service credentials
- secrets from protected configuration, never source
- rate/capacity limits at appropriate layers

Authentication answers who. Authorization answers what they may do.

## Security Headers

Set headers appropriate to the application and deployment: content type, anti-sniffing, transport security at HTTPS boundary, CSP for browser content, and safe cache policies. Do not copy a header set without understanding proxy/asset behavior.

## Logging

Use structured logs with request/trace IDs and safe categories. Never log tokens, passwords, full private payloads, or unnecessary personal data.

## Graceful Shutdown

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()

go func() {
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Printf("server failed: %v", err)
		stop()
	}
}()

<-ctx.Done()

shutdownCtx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()
if err := server.Shutdown(shutdownCtx); err != nil {
	return fmt.Errorf("shutdown server: %w", err)
}
```

Stop accepting, allow in-flight work within a deadline, stop background workers, flush telemetry, close dependencies, and exit non-zero on startup/runtime failure as appropriate.

## Health

- liveness: process should be restarted?
- readiness: should receive traffic?
- startup: initialization still progressing?

Do not make liveness depend on every downstream dependency; a database outage should not necessarily cause a restart loop.

## Final Rules

- bounded bodies and timeouts
- context everywhere request-scoped
- parameterized queries
- short transactions
- server-side authorization
- safe errors/logs
- pooled dependency limits
- graceful shutdown with deadline
- meaningful health semantics
