# 06 - JPA Entities, Repositories, and Transactions

## Beginner Meaning

- Entity: Java object mapped to a database table.
- Repository: interface used to load and save entities.
- Transaction: one business operation whose database changes commit together or roll back together.

Learn plain SQL and database keys before relying on JPA annotations.

## 1) Entity

```java
@Entity
@Table(name = "products")
class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 120)
    private String name;

    @Column(nullable = false, precision = 19, scale = 2)
    private BigDecimal price;

    protected Product() {
        // Result: JPA can construct the entity; application code uses the validating constructor.
    }

    Product(String name, BigDecimal price) {
        if (name == null || name.isBlank() || price == null || price.signum() <= 0) {
            throw new IllegalArgumentException("invalid product");
        }
        this.name = name;
        this.price = price;
    }
}
```

Database constraints are the final integrity boundary; application validation provides earlier errors.

## 2) Repository

```java
interface ProductRepository extends JpaRepository<Product, Long> {
    boolean existsByName(String name);
    // Result: Spring Data implements CRUD and the derived existence query.
}
```

## 3) Transactional Service

```java
@Service
final class ProductService {
    private final ProductRepository repository;

    ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    @Transactional
    Product create(String name, BigDecimal price) {
        if (repository.existsByName(name)) {
            throw new IllegalStateException("product name already exists");
        }
        return repository.save(new Product(name, price));
        // Result: insert commits if the method completes; runtime failure rolls it back.
    }

    @Transactional(readOnly = true)
    Product find(long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ProductNotFoundException(id));
        // Result: returns the entity or fails with ProductNotFoundException.
    }
}
```

Transactions belong around a complete business operation, usually in the service layer.

## 4) Transaction Pitfalls

- proxy-based `@Transactional` does not apply to a private method or ordinary self-invocation
- checked exceptions do not roll back by default unless configured
- remote calls inside a transaction hold database resources longer
- lazy relationships accessed after the transaction may fail
- `save` does not guarantee an immediate SQL statement; flush timing matters

Never return an entity merely to keep a lazy session open. Fetch and map the required data inside the transaction.
