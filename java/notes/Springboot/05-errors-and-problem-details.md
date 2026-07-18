# 05 - Errors and Problem Details

## What, Why, and How

**What:** Error handling converts known failures into consistent HTTP Problem Details while unexpected failures reach the application error boundary.

**Why:** Clients need stable actionable responses, while stack traces, SQL, secrets, and internal class names must stay private.

**How:** Throw specific exceptions where the failure is understood, map them once in `@RestControllerAdvice`, and log unexpected failures once with safe correlation context.

## 1) Domain Error

```java
final class ProductNotFoundException extends RuntimeException {
    ProductNotFoundException(long id) {
        super("product not found: " + id);
    }
}

System.out.println(new ProductNotFoundException(10).getMessage());
// Output: product not found: 10
```

## 2) Central Exception Handler

Spring supports RFC Problem Details through `ProblemDetail`.

```java
@RestControllerAdvice
final class ApiExceptionHandler {
    @ExceptionHandler(ProductNotFoundException.class)
    ResponseEntity<ProblemDetail> handleNotFound(ProductNotFoundException exception) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.NOT_FOUND, exception.getMessage());
        problem.setTitle("Product not found");
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(problem);
        // HTTP 404 application/problem+json with title and detail.
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    ResponseEntity<ProblemDetail> handleConflict(DataIntegrityViolationException exception) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.CONFLICT, "request conflicts with existing data");
        return ResponseEntity.status(HttpStatus.CONFLICT).body(problem);
        // HTTP 409 without exposing database details.
    }
}
```

Do not include stack traces, SQL, internal class names, or secrets in client responses.

## 3) Validation Errors

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
ResponseEntity<ProblemDetail> handleValidation(MethodArgumentNotValidException exception) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, "request validation failed");
    List<String> fields = exception.getBindingResult().getFieldErrors().stream()
            .map(FieldError::getField)
            .distinct()
            .sorted()
            .toList();
    problem.setProperty("invalidFields", fields);
    return ResponseEntity.badRequest().body(problem);
    // HTTP 400 with invalidFields, for example [name, price].
}
```

Avoid echoing rejected sensitive values.

## 4) Error Rules

- map known domain failures deliberately
- let unexpected failures reach the framework’s error boundary
- log an unexpected failure once with a correlation identifier
- keep client messages stable and actionable
- never return `200` with an error body
