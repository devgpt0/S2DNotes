# 04 - REST APIs and Strict Request Validation

## 1) Request and Response DTOs

```java
public record CreateProductRequest(
        @NotBlank @Size(max = 120) String name,
        @NotNull @Positive BigDecimal price) {
    // Result: blank names, oversized names, null prices, and non-positive prices are rejected.
}

public record ProductResponse(long id, String name, BigDecimal price) {
    // Example JSON: {"id":1,"name":"Book","price":250.00}
}
```

Do not expose persistence entities directly as API contracts.

## 2) Thin Controller

```java
@RestController
@RequestMapping("/api/products")
final class ProductController {
    private final ProductService service;

    ProductController(ProductService service) {
        this.service = service;
    }

    @PostMapping
    ResponseEntity<ProductResponse> create(@Valid @RequestBody CreateProductRequest request) {
        ProductResponse created = service.create(request);
        URI location = URI.create("/api/products/" + created.id());
        return ResponseEntity.created(location).body(created);
        // HTTP 201 with Location header and ProductResponse JSON.
    }

    @GetMapping("/{id}")
    ProductResponse find(@PathVariable @Positive long id) {
        return service.find(id);
        // HTTP 200 when found; the exception handler returns 404 when absent.
    }
}
```

Use `@Validated` on the controller when method-parameter constraints require method validation in the selected setup.

## 3) Reject Coercion and Unknown Fields

```yaml
spring:
  jackson:
    mapper:
      allow-coercion-of-scalars: false
    deserialization:
      fail-on-unknown-properties: true
# Result: incompatible scalar types and unexpected JSON fields fail deserialization.
```

Validation must verify data, not silently normalize it. If trimming or case conversion is business behavior, perform it explicitly after validation and document it.

## 4) HTTP Semantics

- `GET`: read and safe
- `POST`: create or execute a non-idempotent command
- `PUT`: replace a resource and be idempotent
- `PATCH`: partially update using a defined patch format
- `DELETE`: remove and be idempotent

Use `200` for a successful response body, `201` for creation, `204` for success without a body, `400` for malformed input, `401` for missing/invalid authentication, `403` for denied authorization, `404` for absence, and `409` for a state conflict.
