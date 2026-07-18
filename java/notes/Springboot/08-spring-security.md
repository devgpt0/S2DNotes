# 08 - Spring Security

## Beginner Meaning

Security answers two separate questions: “Who is calling?” and “Is that caller allowed to do this?” Spring Security applies these checks through a filter chain before protected controller code runs.

## 1) Authentication vs Authorization

- Authentication establishes who the caller is.
- Authorization decides what that caller may do.
- Both must be enforced server-side for every protected operation.

## 2) Security Filter Chain

```java
@Configuration(proxyBeanMethods = false)
@EnableMethodSecurity
class SecurityConfiguration {
    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers("/actuator/health").permitAll()
                        .requestMatchers(HttpMethod.GET, "/api/products/**").hasAuthority("product:read")
                        .anyRequest().authenticated())
                .httpBasic(Customizer.withDefaults())
                .build();
        // Result: health is public; product reads require product:read; all other requests require login.
    }
}
```

Do not disable CSRF for a browser session application. A stateless token API may configure CSRF differently only after confirming no browser cookie authentication is used.

## 3) Method Authorization

```java
@PreAuthorize("hasAuthority('product:write')")
public ProductResponse create(CreateProductRequest request) {
    return createValidatedProduct(request);
    // Result: callers without product:write receive HTTP 403.
}
```

Use method security for important business capabilities even when URL rules also exist.

## 4) Password Encoding

```java
@Bean
PasswordEncoder passwordEncoder() {
    return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    // Result: stored hashes include an algorithm prefix such as {bcrypt}.
}
```

Never store plaintext passwords and never build a custom password hashing algorithm.

## 5) Resource Server

```java
http.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
// Result: bearer JWTs are validated using configured issuer/JWK metadata.
```

Validate issuer, audience, signature, expiry, and authorization claims. Do not trust a JWT merely because it can be decoded.

## 6) Security Checklist

- deny by default
- use least-privilege authorities
- protect object ownership, not only endpoint paths
- validate redirect and callback URLs
- set secure cookies and transport HTTPS only
- configure CORS with exact trusted origins
- rate-limit authentication and expensive endpoints at an appropriate layer
- never log credentials, tokens, or authorization headers
