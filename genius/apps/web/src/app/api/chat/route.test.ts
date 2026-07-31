import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  generateCompletionStream: vi.fn(),
  readConversationTurns: vi.fn(() => []),
  recordInteraction: vi.fn(() => "bf49e9b5-d816-4d41-93f1-49e2e78947c5"),
  retrieveCitations: vi.fn(async () => []),
}));

vi.mock("@/lib/providers", () => ({
  generateCompletionStream: mocks.generateCompletionStream,
}));
vi.mock("@/lib/database", () => ({
  readConversationTurns: mocks.readConversationTurns,
  recordInteraction: mocks.recordInteraction,
}));
vi.mock("@/lib/rag", () => ({
  retrieveCitations: mocks.retrieveCitations,
}));

import { POST } from "./route";

async function* tokens(): AsyncGenerator<string> {
  yield "Queues are ";
  yield "first-in, first-out.";
}

describe("streaming chat route", () => {
  beforeEach(() => {
    mocks.generateCompletionStream.mockReset();
    mocks.readConversationTurns.mockClear();
    mocks.recordInteraction.mockClear();
    mocks.retrieveCitations.mockClear();
    mocks.generateCompletionStream.mockReturnValue(tokens());
  });

  it("streams citations, tokens, and a completed persisted interaction", async () => {
    const response = await POST(
      new Request("http://localhost/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider: "gemini",
          message: "What is a queue?",
          conversationId: "26f0a6bc-3c3a-49cf-943e-d4d1b5068712",
          useRag: true,
          ragBackend: "local",
          selectedFiles: ["collections/queues.md"],
        }),
      }),
    );
    const body = await response.text();

    expect(response.headers.get("content-type")).toContain("text/event-stream");
    expect(body).toContain("event: sources");
    expect(body).toContain("event: token");
    expect(body).toContain("event: complete");
    expect(mocks.readConversationTurns).toHaveBeenCalledWith(
      "26f0a6bc-3c3a-49cf-943e-d4d1b5068712",
      5,
    );
    expect(mocks.recordInteraction).toHaveBeenCalledWith(
      expect.objectContaining({
        conversationId: "26f0a6bc-3c3a-49cf-943e-d4d1b5068712",
        kind: "chat",
        response: JSON.stringify({ answer: "Queues are first-in, first-out." }),
      }),
    );
  });
});
