# 09 - Testing

## What, Why, and How

**What:** Tests verify behavior through plain Java units, Spring slices, infrastructure integration, and full journeys.

**Why:** Starting the whole application for every test is slow, while mocking everything misses configuration, SQL, security, and serialization failures.

**How:** Use the smallest test that proves behavior, keep time/data deterministic, use Testcontainers for infrastructure semantics, and test failure/authorization/rollback paths.

## 1) Test Pyramid

- unit tests for domain and service logic
- slice tests for MVC and persistence boundaries
- a smaller number of full integration tests
- end-to-end tests for critical journeys

## 2) Unit Test Without Spring

```java
@Test
void calculatesTotalWithTax() {
    TaxPolicy tax = subtotal -> new BigDecimal("18.00");
    PriceService service = new PriceService(tax);

    assertEquals(new BigDecimal("118.00"), service.total(new BigDecimal("100.00")));
    // Test output: passes when total equals 118.00.
}
```

Do not start Spring when ordinary object construction is sufficient.

## 3) MVC Slice Test

Spring Boot 4 provides focused test starters such as `spring-boot-starter-webmvc-test`.

```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ProductService productService;

    @Test
    void returnsProduct() throws Exception {
        given(productService.find(1)).willReturn(
                new ProductResponse(1, "Book", new BigDecimal("250.00")));

        mockMvc.perform(get("/api/products/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Book"));
        // Test output: HTTP 200 JSON containing name=Book.
    }
}
```

Import the application security configuration or a deliberate test configuration; never disable security accidentally.

## 4) Repository Slice

```java
@DataJpaTest
class ProductRepositoryTest {
    @Autowired
    private ProductRepository repository;

    @Test
    void findsExistingName() {
        repository.saveAndFlush(new Product("Book", new BigDecimal("250.00")));
        assertTrue(repository.existsByName("Book"));
        // Test output: passes when the database query returns true.
    }
}
```

Use Testcontainers when database-specific behavior matters; an in-memory database may hide SQL and transaction differences.

## 5) Full Integration Test

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ApplicationTest {
    @Test
    void contextStarts() {
        System.out.println("context started");
        // Output after successful startup: context started
    }
}
```

## 6) Test Quality

- use fixed clocks and deterministic IDs where needed
- verify observable behavior, not private implementation
- test validation, authorization, conflicts, and rollback paths
- keep tests independent and order-free
- do not mock value objects or every internal collaborator
