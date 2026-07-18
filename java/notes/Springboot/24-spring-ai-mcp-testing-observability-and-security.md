# 24 - Spring AI MCP, Testing, Observability, and Security

## Beginner Meaning

MCP is a standard way for an AI application to discover and call external tools, read resources, and use prompt templates. An MCP server exposes capabilities; an MCP client connects to them.

Treat every MCP capability like a public API: authenticate, authorize, validate input, limit access, and audit important actions.

## MCP Server Starter

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server-webmvc</artifactId>
    <!-- Result: Spring AI configures an MCP server over WebMVC. -->
</dependency>
```

Use Streamable HTTP rather than the deprecated SSE server transport in Spring AI 2.0.

```yaml
spring:
  ai:
    mcp:
      server:
        protocol: STREAMABLE
        type: SYNC
# Result: a synchronous Streamable-HTTP MCP server is configured.
```

## Annotated MCP Tool

```java
@Component
final class CalculatorTools {
    @McpTool(name = "add", description = "Add two integers")
    int add(
            @McpToolParam(description = "First integer", required = true) int left,
            @McpToolParam(description = "Second integer", required = true) int right) {
        return Math.addExact(left, right);
        // Example tool result: add(20, 22) returns 42.
    }
}
```

MCP resources, prompts, and tools are remote capability boundaries. Authenticate the client, authorize every operation, validate parameters, isolate tenants, and constrain network/filesystem/process access.

## Testing Strategy

- deterministic unit tests for prompt construction, validation, tools, and output mapping
- stub model for predictable application tests
- provider integration tests kept small and separately tagged
- golden evaluation dataset for quality/regression
- adversarial tests for injection, data leakage, unsafe tool calls, and oversized input
- load tests for concurrency, rate limits, timeout, and cost controls

```java
@Test
void toolRejectsOverflow() {
    CalculatorTools tools = new CalculatorTools();
    assertThrows(ArithmeticException.class, () -> tools.add(Integer.MAX_VALUE, 1));
    // Test output: overflow is rejected instead of silently wrapping.
}
```

## Observability

Track request count, end-to-end latency, model latency, token usage, estimated cost, tool duration/failure, retrieval count/score, refusal rate, timeout, and evaluation quality. Never use raw prompts, documents, conversation IDs, or user text as metric tags.

## AI Threat Model

- prompt injection and indirect injection
- sensitive-data disclosure
- excessive agency/tool abuse
- insecure model output used as SQL/HTML/path/command
- poisoned knowledge documents
- denial of wallet or resource exhaustion
- model/provider supply-chain changes

Apply least privilege, human confirmation for high-impact actions, output encoding, explicit allow-lists, data classification, retention controls, model/version governance, and kill switches.
