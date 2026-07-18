# 14 - Production Deployment and Operations

## 1) Build an Executable JAR

```powershell
.\mvnw.cmd clean verify
# Output: tests run and target/<artifact>-<version>.jar is created on success.
```

Run the exact verified artifact:

```powershell
java -jar target\notes-0.0.1-SNAPSHOT.jar
# Output includes: Started NotesApplication
```

## 2) Container Image

Spring Boot buildpacks avoid maintaining a handwritten Dockerfile.

```powershell
.\mvnw.cmd spring-boot:build-image -Dspring-boot.build-image.imageName=example/notes:1.0.0
# Output: OCI image example/notes:1.0.0 is created.
```

Use immutable version tags and deploy by digest where possible.

## 3) Graceful Shutdown

```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 20s
# Result: shutdown stops new work and allows up to 20 seconds for an orderly phase.
```

## 4) Database Migrations

Run versioned, reviewed migrations. Make changes compatible with both old and new application versions during rolling deployment:

1. expand schema
2. deploy compatible code
3. migrate/backfill data
4. remove obsolete schema later

## 5) Production Checklist

- run as a non-root user with a read-only filesystem where practical
- use HTTPS at the trusted ingress and secure internal traffic as required
- set CPU, memory, connection pool, request size, and timeout limits
- keep secrets outside the image
- expose bounded readiness and liveness probes
- centralize logs and export metrics/traces
- scan dependencies and images for vulnerabilities
- generate an SBOM and retain build provenance
- test backup restoration, rollback, and disaster recovery
- use zero-downtime-compatible migrations

## 6) Never Do This

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: validate
# Result: production startup verifies schema compatibility; do not use create or create-drop.
```

Do not expose every Actuator endpoint, enable debug mode, return stack traces, or use default development credentials in production.
