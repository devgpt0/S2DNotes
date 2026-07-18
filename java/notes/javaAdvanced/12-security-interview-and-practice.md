# 12 - Security, Interview Revision, and Practice

## 1) Cryptographically Secure Random Values

```java
SecureRandom random = new SecureRandom();
byte[] bytes = new byte[16];
random.nextBytes(bytes);
System.out.println(bytes.length);
// Output: 16
// Actual bytes are intentionally unpredictable.
```

Do not use `Random` for tokens, reset links, keys, or security decisions.

## 2) Password Handling

Store password hashes produced by a dedicated password-hashing algorithm such as Argon2, bcrypt, scrypt, or PBKDF2 with an appropriate work factor and random salt. Do not encrypt passwords for later recovery.

```java
char[] password = "temporary-example".toCharArray();
System.out.println(password.length);
Arrays.fill(password, '\0');
// Output: 17
// A real application passes the characters to a password-hashing library first.
```

## 3) Constant-Time Comparison

```java
byte[] expected = {1, 2, 3};
byte[] actual = {1, 2, 3};
System.out.println(MessageDigest.isEqual(expected, actual));
// Output: true
```

Use authenticated encryption such as AES-GCM when encryption is required. Key generation, rotation, access control, and storage are part of the design.

## 4) Interview Quick Answers

- Generics are invariant and mostly implemented using type erasure.
- Try-with-resources closes resources in reverse order.
- Reflection trades compile-time safety for runtime flexibility.
- `Instant` is appropriate for machine timestamps; `LocalDate` is not a timestamp.
- Records are shallowly immutable data carriers.
- Sealed types define a closed hierarchy.
- GC reclaims unreachable memory, not files or sockets.
- Virtual threads improve scalability for blocking I/O, not CPU throughput.

## 5) Practice Tasks

1. Write a generic `max` method using `Comparable` and print the result.
2. Read a UTF-8 file with try-with-resources and print numbered lines.
3. Validate an upload path remains inside a configured root.
4. Model success and failure using a sealed interface and exhaustive switch.
5. Parse a date strictly and demonstrate rejection of an impossible date.
6. Run three independent blocking tasks on virtual threads and print their results.

## 6) Production Checklist

- Validate every external input without implicit coercion.
- Use parameterized database queries and safe process APIs.
- Keep dependencies patched and verified.
- Restrict filesystem and network permissions.
- Never log credentials, tokens, keys, or sensitive payloads.
- Measure performance with production-like evidence before tuning.
