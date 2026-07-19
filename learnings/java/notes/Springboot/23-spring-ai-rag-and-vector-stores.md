# 23 - Spring AI RAG and Vector Stores

Retrieval-Augmented Generation retrieves relevant trusted documents and supplies them as context to a model. It improves grounding but does not guarantee correctness.

## RAG in Five Steps

1. Split trusted source documents into useful chunks.
2. Convert each chunk to an embedding (a numeric meaning representation).
3. Store embeddings with source and security metadata.
4. Search for chunks related to the user's question.
5. Give those chunks to the model as context and ask for an answer.

RAG does not train the model. It supplies current context for one request.

**Why use it:** Models may lack current or private knowledge. Retrieval supplies approved source material without retraining.

**How to use it:** Build a versioned ingestion pipeline, attach tenant/security metadata, filter during retrieval, cite supporting chunks, and evaluate retrieval plus answer quality on a fixed dataset.

## PGvector Dependencies

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-pgvector</artifactId>
    <!-- Result: PGvector VectorStore auto-configuration is enabled. -->
</dependency>
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-vector-store-advisor</artifactId>
    <!-- Result: QuestionAnswerAdvisor support is available. -->
</dependency>
```

## Ingestion Pipeline

```java
Document document = new Document(
        "Refunds are allowed within 30 days.",
        Map.of("tenantId", "tenant-7", "source", "policy-v3"));
vectorStore.add(List.of(document));
System.out.println(document.getMetadata().get("source"));
// Output: policy-v3
```

Production ingestion stages: load -> validate -> clean -> split -> attach security/version metadata -> embed -> store. Make ingestion idempotent and remove obsolete chunks when a source changes.

## Similarity Search

```java
SearchRequest request = SearchRequest.builder()
        .query("How long is the refund period?")
        .topK(4)
        .filterExpression("tenantId == 'tenant-7'")
        .build();
List<Document> matches = vectorStore.similaritySearch(request);
System.out.println(matches.size() <= 4);
// Output: true
```

Security filtering must happen during retrieval, not after private chunks have entered the prompt.

## RAG Advisor

```java
ChatClient groundedClient = builder
        .defaultAdvisors(QuestionAnswerAdvisor.builder(vectorStore).build())
        .build();
String answer = groundedClient.prompt("What is the refund period?").call().content();
System.out.println(answer != null);
// Output: true
// Answer quality depends on ingestion, retrieval, prompt, model, and source quality.
```

## Retrieval Quality

Tune chunk size/overlap, embedding model, metadata filters, top-K, similarity threshold, hybrid keyword/vector search, reranking, and context ordering using an evaluation dataset.

## RAG Failure Modes

- missing relevant document
- stale or duplicate chunks
- cross-tenant leakage
- prompt injection inside retrieved content
- too much context hiding the answer
- embedding/model migration incompatibility
- answer without source support

Require citations for factual answers where appropriate and verify that cited chunks actually support the claim.
