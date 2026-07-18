# 28 - Common Spring Boot Code Snippets and Solved Interview Questions

## 1) Create a Validated POST Endpoint

```java
record CreateUserRequest(@NotBlank String name, @Email String email) {}
record UserResponse(long id, String name, String email) {}

@PostMapping("/api/users")
ResponseEntity<UserResponse> create(@Valid @RequestBody CreateUserRequest request) {
    UserResponse response = service.create(request);
    return ResponseEntity.created(URI.create("/api/users/" + response.id())).body(response);
    // HTTP output: 201 Created, Location header, and user JSON.
}
```

Interview point: controller translates HTTP; service owns business logic.

## 2) Global Validation/Error Response

```java
@RestControllerAdvice
final class ApiErrors {
    @ExceptionHandler(UserNotFoundException.class)
    ProblemDetail notFound(UserNotFoundException error) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, error.getMessage());
        problem.setTitle("User not found");
        return problem;
        // HTTP output: 404 application/problem+json.
    }
}
```

Do not return internal stack traces or database details.

## 3) Type-Safe Validated Configuration

```java
@ConfigurationProperties("notification")
@Validated
record NotificationProperties(
        @NotBlank String baseUrl,
        @DurationMin(seconds = 1) Duration timeout) {
    // Startup output: application fails immediately when required configuration is invalid.
}
```

## 4) Repository Pagination and Projection

```java
interface UserSummary {
    Long getId();
    String getName();
}

interface UserRepository extends JpaRepository<User, Long> {
    Page<UserSummary> findByActiveTrue(Pageable pageable);
    // Result: bounded active-user page loading only projected fields.
}
```

Allow-list sort fields and cap page size.

## 5) Transactional Service

```java
@Service
final class TransferService {
    private final AccountRepository accounts;

    TransferService(AccountRepository accounts) { this.accounts = accounts; }

    @Transactional
    void transfer(long fromId, long toId, BigDecimal amount) {
        if (amount == null || amount.signum() <= 0) throw new IllegalArgumentException("invalid amount");
        Account from = accounts.findById(fromId).orElseThrow();
        Account to = accounts.findById(toId).orElseThrow();
        from.debit(amount);
        to.credit(amount);
        // Result: both dirty-checked updates commit together or roll back together.
    }
}
```

## 6) Optimistic Locking

```java
@Version
private long version;
// Result: stale concurrent update affects no row and JPA raises an optimistic-lock failure.
```

Map the conflict to an actionable 409 when appropriate.

## 7) Security Filter Chain

```java
@Bean
SecurityFilterChain security(HttpSecurity http) throws Exception {
    return http
            .authorizeHttpRequests(auth -> auth
                    .requestMatchers("/actuator/health").permitAll()
                    .requestMatchers(HttpMethod.GET, "/api/users/**").hasAuthority("user:read")
                    .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    // HTTP result: health is public; user reads require user:read; other requests require authentication.
}
```

## 8) External HTTP Client

```java
@Component
final class ProfileClient {
    private final RestClient client;
    ProfileClient(RestClient.Builder builder, ProfileProperties properties) {
        client = builder.baseUrl(properties.baseUrl()).build();
    }
    ProfileResponse find(long id) {
        return client.get().uri("/profiles/{id}", id).retrieve().body(ProfileResponse.class);
        // Result: successful JSON maps to ProfileResponse; HTTP errors raise a client exception.
    }
}
```

Configure deadlines at the HTTP request/client factory and validate response fields.

## 9) Cache a Read and Evict on Update

```java
@Cacheable(cacheNames = "users", key = "#id")
UserResponse find(long id) {
    return load(id);
    // Result: repeated id can reuse cached response according to cache policy.
}

@CacheEvict(cacheNames = "users", key = "#result.id")
UserResponse update(UpdateUserRequest request) {
    return updateUser(request);
    // Result: successfully updated user's cached entry is evicted.
}
```

Define size, expiry, invalidation, and failure behavior.

## 10) MVC Slice Test

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired MockMvc mvc;
    @MockitoBean UserService service;

    @Test
    void returnsUser() throws Exception {
        given(service.find(1)).willReturn(new UserResponse(1, "Asha", "asha@example.com"));
        mvc.perform(get("/api/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Asha"));
        // Test output: HTTP 200 JSON with name Asha.
    }
}
```

Include deliberate security configuration rather than accidentally bypassing it.

## 11) Scheduled Job with Explicit Zone

```java
@Scheduled(cron = "0 0 2 * * *", zone = "UTC")
void cleanup() {
    System.out.println("cleanup started");
    // Output daily at 02:00 UTC: cleanup started
}
```

Multiple application instances will each run it unless distributed coordination exists.

## 12) Publish After Commit

```java
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
void on(OrderCreated event) {
    System.out.println("committed order=" + event.orderId());
    // Output only after successful transaction commit: committed order=<id>
}
```

This remains in-process and non-durable; use an outbox for reliable external publication.

## Most-Asked Spring Boot Questions

1. Spring vs Boot? Framework/container vs opinionated auto-configuration/starters/runtime/operations.
2. IOC vs DI? Container control of creation/lifecycle vs supplying required collaborators.
3. Bean scopes? Singleton, prototype, request, session, and custom scopes.
4. `@Component` vs `@Bean`? Scanned component class vs explicit configuration method.
5. `@Controller` vs `@RestController`? View-oriented controller vs controller plus response-body semantics.
6. `@RequestParam` vs `@PathVariable`? Query/form parameter vs URI path segment.
7. `@Valid` vs `@Validated`? Jakarta cascaded validation vs Spring validation support including groups/method use.
8. `@ConfigurationProperties` vs `@Value`? Typed grouped validated config vs isolated expression/value injection.
9. Auto-configuration? Conditional beans based on classpath/properties/existing beans.
10. Why constructor injection? Required immutable explicit dependencies and easy unit testing.
11. Bean lifecycle? Definition, instantiate, inject, post-process/proxy, init, use, destroy.
12. `@Transactional` self-invocation? Bypasses proxy, so advice does not run.
13. Propagation REQUIRED vs REQUIRES_NEW? Join/create current vs suspend and create independent transaction.
14. Default rollback? Runtime exceptions/errors; checked exceptions need explicit policy.
15. JPA dirty checking? Managed changes become SQL at flush.
16. N+1? One parent query plus query per relationship; solve with use-case fetch design.
17. Lazy vs eager? Loading timing intent; neither guarantees query count.
18. Optimistic vs pessimistic lock? Version conflict vs database lock.
19. 401 vs 403? Unauthenticated/invalid identity vs authenticated but forbidden.
20. CSRF vs CORS? Forged browser state-changing request vs cross-origin read permission policy.
21. Filter vs interceptor vs AOP? Servlet request, MVC handler, Spring bean method boundary.
22. `@WebMvcTest` vs `@SpringBootTest`? Focused MVC slice vs full context.
23. Actuator? Secured health/metrics/operational endpoints.
24. MVC vs WebFlux? Blocking servlet model vs non-blocking reactive pipeline.
25. RestClient vs WebClient? Imperative synchronous client vs reactive non-blocking client.
26. How make Kafka consumer safe? Idempotency, bounded retry, DLT, schema/version, offset after durable effect.
27. Outbox? Atomic business row + publish intent, later broker delivery.
28. How secure secrets? External secret manager, least privilege, rotation, never logs/source.
29. How deploy safely? Immutable artifact, compatible migrations, health/readiness, graceful shutdown, canary/rollback.
30. Spring AI safety? Validate output, authorize tools, isolate tenants/memory/RAG, limits, evaluation, observability.
