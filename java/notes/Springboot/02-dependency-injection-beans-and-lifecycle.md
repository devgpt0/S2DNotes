# 02 - Dependency Injection, Beans, and Lifecycle

## 1) Constructor Injection

```java
@Service
final class PriceService {
    private final TaxPolicy taxPolicy;

    PriceService(TaxPolicy taxPolicy) {
        this.taxPolicy = taxPolicy;
    }

    BigDecimal total(BigDecimal subtotal) {
        return subtotal.add(taxPolicy.tax(subtotal));
        // For subtotal 100.00 and 18% tax, result is 118.00.
    }
}
```

Required dependencies are explicit and fields can remain final. Avoid field injection.

## 2) Component Stereotypes

- `@Component`: general managed component
- `@Service`: application or domain service
- `@Repository`: persistence adapter; also enables exception translation
- `@Controller` / `@RestController`: web adapter
- `@Configuration`: bean definitions

## 3) Explicit Bean Definition

```java
@Configuration(proxyBeanMethods = false)
class PricingConfiguration {
    @Bean
    TaxPolicy taxPolicy() {
        return subtotal -> subtotal.multiply(new BigDecimal("0.18"));
        // Result: Spring registers one TaxPolicy bean with singleton scope by default.
    }
}
```

Use `proxyBeanMethods = false` when bean methods do not call one another.

## 4) Multiple Implementations

```java
interface MessageSender {
    void send(String message);
}

@Component("consoleSender")
final class ConsoleMessageSender implements MessageSender {
    public void send(String message) {
        System.out.println(message);
        // Output is the supplied message.
    }
}

@Service
final class AlertService {
    AlertService(@Qualifier("consoleSender") MessageSender sender) {
        sender.send("configured");
        // Output during construction: configured
    }
}
```

Prefer a domain-specific qualifier annotation when many call sites need the same choice.

## 5) Lifecycle and Scope

```java
@Component
final class StartupReporter {
    @EventListener(ApplicationReadyEvent.class)
    void ready() {
        System.out.println("application ready");
        // Output after startup: application ready
    }
}
```

Singleton beans are shared across requests and must not store request-specific mutable state. Use lifecycle callbacks for local resource setup/cleanup, not slow business workflows.

## 6) Circular Dependencies

Treat a circular dependency as a design error. Extract the shared responsibility or change the interaction; do not hide the problem with lazy injection.
