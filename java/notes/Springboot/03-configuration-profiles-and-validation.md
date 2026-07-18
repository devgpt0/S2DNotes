# 03 - Configuration, Profiles, and Validation

## 1) Type-Safe Configuration

```java
@ConfigurationProperties("payment")
@Validated
public record PaymentProperties(
        @NotBlank String baseUrl,
        @DurationMin(seconds = 1) Duration timeout) {
    // Result: startup fails if base-url is blank or timeout is less than one second.
}
```

Register it explicitly:

```java
@ConfigurationPropertiesScan
@SpringBootApplication
public class NotesApplication {
    public static void main(String[] args) {
        SpringApplication.run(NotesApplication.class, args);
        // Output: configuration is bound and validated during startup.
    }
}
```

## 2) Application Configuration

```yaml
payment:
  base-url: https://payments.example.com
  timeout: 3s
# Result: PaymentProperties("https://payments.example.com", Duration.ofSeconds(3)).
```

Use environment variables for deployment-specific values:

```yaml
payment:
  base-url: ${PAYMENT_BASE_URL}
  timeout: ${PAYMENT_TIMEOUT:3s}
# Result: startup fails if PAYMENT_BASE_URL is missing; timeout defaults to 3s.
```

## 3) Profiles

```yaml
spring:
  config:
    activate:
      on-profile: local
payment:
  base-url: http://localhost:9090
# Result: these values apply only when the local profile is active.
```

Profiles select environment behavior. They should not be used to scatter core business rules across configurations.

## 4) Precedence

Command-line arguments, system properties, environment variables, and configuration files participate in a defined precedence. Prefer one deployment-owned source instead of relying on complicated overrides.

## 5) Secrets

- never commit secrets to Git
- use a platform secret manager
- rotate credentials
- restrict who can read them
- never expose all configuration through Actuator
- never log bound secrets

## 6) `@Value` vs Configuration Properties

Use `@Value` for a rare single value. Use `@ConfigurationProperties` for related settings because it provides type safety, validation, metadata, and easier testing.
