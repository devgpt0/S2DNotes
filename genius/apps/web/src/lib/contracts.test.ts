import { describe, expect, it } from "vitest";

import {
  chatRequestSchema,
  ragRetrieveResponseSchema,
  tutorGenerationResponseSchema,
} from "./contracts";

describe("web contracts", () => {
  it("requires a strict chat request with a conversation id", () => {
    const request = {
      provider: "gemini",
      message: "Explain binary search.",
      conversationId: "44c9b0e8-4d5a-4b11-bb81-5c1d43dcb1f8",
      useRag: true,
      ragBackend: "local",
      selectedFiles: ["algorithms/binary-search.md"],
    };

    expect(chatRequestSchema.parse(request)).toEqual(request);
    expect(
      chatRequestSchema.safeParse({ ...request, unexpected: true }).success,
    ).toBe(false);
  });

  it("accepts RAG metadata while retaining a strict service response", () => {
    const response = {
      query: "binary search",
      citations: [
        {
          path: "algorithms/binary-search.md",
          topic: "algorithms",
          heading: "Binary Search",
          checksum: "a".repeat(64),
          snippet: "Binary search halves a sorted range.",
          score: 0.92,
        },
      ],
      mode: "hybrid",
      backend: "local",
      reranked: true,
      indexed: true,
    };

    expect(ragRetrieveResponseSchema.parse(response)).toEqual(response);
    expect(
      ragRetrieveResponseSchema.safeParse({ ...response, other: "value" })
        .success,
    ).toBe(false);
  });

  it("requires five tutor questions", () => {
    const question = {
      id: "9f6bc1f2-d0b5-4ab5-87a3-c9a8b7c67cb4",
      prompt: "What is a stack?",
      choices: [],
    };
    const response = {
      questions: Array.from({ length: 5 }, (_, index) => ({
        ...question,
        id: `${index}f6bc1f2-d0b5-4ab5-87a3-c9a8b7c67cb4`,
      })),
      citations: [],
      interactionId: "d1f70fe6-bd52-45a6-bf88-063171ecd655",
    };

    expect(
      tutorGenerationResponseSchema.parse(response).questions,
    ).toHaveLength(5);
    expect(
      tutorGenerationResponseSchema.safeParse({
        ...response,
        questions: response.questions.slice(0, 4),
      }).success,
    ).toBe(false);
  });
});
