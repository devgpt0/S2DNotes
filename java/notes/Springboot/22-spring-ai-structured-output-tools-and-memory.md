# 22 - Spring AI Structured Output, Tools, and Memory

## Three Ideas in Simple Words

- Structured output asks the model to return data matching a Java shape.
- A tool is approved Java code the model may request the application to run.
- Chat memory adds selected earlier messages to a later prompt.

The application remains responsible for validation, permissions, and data isolation.

**Why use them:** Structured output integrates with typed code, tools provide current/private capabilities, and memory supports multi-turn context.

**How to use them:** Validate mapped records, expose only least-privilege tools, authorize inside each tool, bind memory to an authenticated conversation owner, and limit retained context.

## Structured Output

```java
record Classification(String category, double confidence) {
    Classification {
        if (category == null || category.isBlank()) {
            throw new IllegalArgumentException("category must not be blank");
        }
        if (confidence < 0 || confidence > 1) {
            throw new IllegalArgumentException("confidence must be between 0 and 1");
        }
    }
}

Classification result = chatClient.prompt("Classify: payment failed")
        .call()
        .entity(Classification.class);
System.out.println(result.category());
// Example output: BILLING
// Parsed output still requires domain validation; model output is not authoritative.
```

Provider-native structured output can be requested only when the selected model supports it. Schema-conforming output is syntactically valid, not necessarily factually correct.

## Tool Calling

```java
final class InventoryTools {
    @Tool(description = "Return available quantity for a product ID")
    int available(long productId) {
        if (productId <= 0) throw new IllegalArgumentException("productId must be positive");
        return 5;
    }
}

String answer = chatClient.prompt("How many units of product 10 are available?")
        .tools(new InventoryTools())
        .call()
        .content();
System.out.println(answer != null);
// Output: true
// The model may invoke the validated tool and use its result in the response.
```

Tool descriptions and parameter schemas influence model selection. The application, not the model, must enforce authentication, authorization, ownership, amount limits, and idempotency.

## Chat Memory

Chat memory supplies selected prior messages to future prompts; it is not permanent business storage.

```java
ChatClient memoryClient = builder
        .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())
        .build();
String conversationId = "conversation-10";
String answer = memoryClient.prompt("Remember that my preferred language is Java")
        .advisors(advisor -> advisor.param(ChatMemory.CONVERSATION_ID, conversationId))
        .call()
        .content();
System.out.println(answer != null);
// Output: true
// The MessageChatMemoryAdvisor stores and retrieves messages for conversation-10.
```

Use an authenticated user-owned conversation identifier, retention limits, encryption/access controls, and deletion support. Never let one user choose another user's conversation ID.

## Advisors

Advisors intercept prompt/response flows for memory, RAG, safety, logging, or custom policy. Their order changes behavior. Avoid logging full prompts and responses by default.

## Tool Security Checklist

- expose the smallest tool set per request
- use typed bounded arguments
- authorize inside every side-effecting tool
- require confirmation for high-impact actions
- prevent arbitrary URL, path, SQL, and command execution
- set timeouts and output limits
- audit tool name, caller, decision, and result metadata without secrets
