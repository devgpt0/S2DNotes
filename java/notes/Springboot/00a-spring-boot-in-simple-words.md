# Spring Boot in Simple Words

Read this before the detailed Spring Boot chapters.

## What Problem Does Spring Boot Solve?

A web application needs an HTTP server, request routing, JSON conversion, object wiring, configuration, validation, security, database access, tests, and health information.

Spring provides these building blocks. Spring Boot chooses useful defaults and starts the application with less setup.

## Your First Application

```java
@SpringBootApplication
public class CourseApplication {
    public static void main(String[] args) {
        SpringApplication.run(CourseApplication.class, args);
    }
}
```

- `@SpringBootApplication`: this is the main configuration class
- `SpringApplication.run`: create the Spring container and start the application
- **container:** the part of Spring that creates and connects application objects

## Your First HTTP Endpoint

```java
@RestController
final class CourseController {
    @GetMapping("/courses/hello")
    String hello() {
        return "Hello, Java learner";
    }
}
```

```powershell
curl http://localhost:8080/courses/hello
# Output: Hello, Java learner
```

- `@RestController`: this class handles HTTP requests and writes response bodies
- `@GetMapping`: connect an HTTP GET path to a method
- returned string: response body

For web code, the HTTP response is the visible result. `System.out.println` is useful in small language demos, but production server events belong in structured logs.

## Dependency Injection

A controller should translate HTTP. Business rules belong in a service.

```java
@Service
final class CourseService {
    String greeting() {
        return "Hello, Java learner";
    }
}

@RestController
final class CourseController {
    private final CourseService courseService;

    CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    @GetMapping("/courses/hello")
    String hello() {
        return courseService.greeting();
    }
}
```

Spring creates `CourseService`, then passes it into the controller constructor. That is **dependency injection**.

Constructor injection makes required dependencies visible and supports ordinary unit tests.

## A Bean

A **bean** is an object managed by the Spring container.

Spring can discover a bean through `@Service`, `@Repository`, `@Controller`, or a `@Bean` method.

Do not make every object a bean. Plain data values can remain ordinary Java objects.

## Request Flow

```text
HTTP request
  -> security and filters
  -> controller
  -> service
  -> repository or external service
  -> response
```

- controller: HTTP translation
- service: use case and business rules
- repository: persistence boundary

This is a guide, not a rule that every tiny endpoint needs three empty layers.

## Validate External Input

```java
record CreateCourseRequest(
        @NotBlank String title,
        @Positive int durationHours) {
}

@PostMapping("/courses")
ResponseEntity<CourseResponse> create(
        @Valid @RequestBody CreateCourseRequest request) {
    return ResponseEntity.status(HttpStatus.CREATED)
            .body(courseService.create(request));
}
```

- `@RequestBody`: read JSON into the request object
- `@Valid`: run declared validation rules
- invalid input stops before the use case runs
- `201 Created`: tells the client a resource was created

Validation should reject the wrong type or missing value. Do not silently coerce invalid input.

## Database Work and Transactions

A transaction groups database changes so they commit together or roll back together.

```java
@Transactional
public CourseResponse create(CreateCourseCommand command) {
    Course saved = courseRepository.save(Course.create(command));
    return CourseResponse.from(saved);
}
```

Place the transaction around the complete application operation, usually in the service. Understand proxy boundaries before relying on annotations.

## Errors

Return stable, safe error responses. Do not send stack traces, database details, tokens, or internal class names to clients.

Use an exception handler to translate known application failures into problem details. Let unexpected failures reach central handling and operational logs.

## Security

- authenticate who the caller is
- authorize what that caller may do
- treat every request as untrusted
- keep secrets outside source code and frontend bundles
- use CSRF protection for cookie-based browser sessions
- configure CORS for known origins, methods, and headers

Authentication does not replace authorization.

## Testing Levels

- unit test: one class and its rules
- MVC slice test: HTTP mapping, validation, and response behavior
- repository test: database mapping and queries
- integration test: important parts working together with real infrastructure

Test visible behavior and failure cases, not framework implementation details.

## Observability

Production understanding needs structured logs, metrics, traces, and health checks. Never log passwords, tokens, secrets, or unnecessary personal data.

## Beginner to Expert Path

1. **Beginner:** start one app and understand controller, service, and bean.
2. **Developer:** build validated REST endpoints with tests and persistence.
3. **Senior:** design transactions, security, messaging, and failure behavior.
4. **Expert:** understand proxies, lifecycle, reactive vs blocking choices, distributed consistency, performance, and operations.

## Before Moving On

Be able to explain what Spring creates, why the controller receives the service, where input is validated, what result the client sees, and what happens when work fails.
