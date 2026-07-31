import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  generateCompletion: vi.fn(),
  recordInteraction: vi.fn(() => "405c0dac-4c13-483d-843d-e51aeef7b51d"),
  retrieveCitations: vi.fn(async () => []),
}));

vi.mock("@/lib/providers", () => ({
  generateCompletion: mocks.generateCompletion,
}));
vi.mock("@/lib/database", () => ({
  recordInteraction: mocks.recordInteraction,
}));
vi.mock("@/lib/rag", () => ({
  retrieveCitations: mocks.retrieveCitations,
}));

import { POST } from "./route";

describe("code review route", () => {
  beforeEach(() => {
    mocks.generateCompletion.mockReset();
    mocks.recordInteraction.mockClear();
    mocks.retrieveCitations.mockClear();
  });

  it("returns an LLM-only review with a persisted rating", async () => {
    mocks.generateCompletion.mockResolvedValue(
      JSON.stringify({
        rating: 4,
        review: "Use a hash map to reduce the nested loop to linear time.",
      }),
    );
    const response = await POST(
      new Request("http://localhost/api/code-review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider: "gemini",
          language: "cpp",
          code: "int solve() { return 0; }",
          goal: "Solve Two Sum in linear time.",
          useRag: true,
          ragBackend: "local",
          selectedFiles: ["algorithms/hash-maps.md"],
        }),
      }),
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body).toMatchObject({ rating: 4, review: expect.any(String) });
    expect(mocks.recordInteraction).toHaveBeenCalledWith(
      expect.objectContaining({
        kind: "code-review",
        metadata: { language: "cpp", rating: 4 },
      }),
    );
  });
});
