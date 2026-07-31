import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  generateCompletion: vi.fn(),
  recordInteraction: vi.fn(() => "56ed5b5d-0969-4eaf-8dd7-678c07fa9c5d"),
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

const question = {
  id: "13a27c3f-162c-4d9c-848e-8a00a728404f",
  prompt: "Which structure is first-in, first-out?",
  choices: ["Stack", "Queue", "Set", "Tree"],
};

function request(body: unknown): Request {
  return new Request("http://localhost/api/tutor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

function sourceSelection(): Record<string, unknown> {
  return {
    useRag: true,
    ragBackend: "local",
    selectedFiles: ["collections/queues.md"],
  };
}

describe("tutor route", () => {
  beforeEach(() => {
    mocks.generateCompletion.mockReset();
    mocks.recordInteraction.mockClear();
    mocks.retrieveCitations.mockClear();
  });

  it("creates a five-question MCQ session", async () => {
    mocks.generateCompletion.mockResolvedValue(
      JSON.stringify({
        questions: Array.from({ length: 5 }, (_, index) => ({
          prompt: "Question " + (index + 1),
          choices: ["A", "B", "C", "D"],
        })),
      }),
    );

    const response = await POST(
      request({
        action: "generate",
        provider: "gemini",
        mode: "multiple-choice",
        topic: "Queues",
        ...sourceSelection(),
      }),
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.questions).toHaveLength(5);
    expect(body.questions[0].choices).toHaveLength(4);
    expect(mocks.retrieveCitations).toHaveBeenCalledOnce();
    expect(mocks.recordInteraction).toHaveBeenCalledWith(
      expect.objectContaining({ kind: "tutor-generation" }),
    );
  });

  it("returns rated MCQ feedback and persists the result", async () => {
    mocks.generateCompletion.mockResolvedValue(
      JSON.stringify({ rating: 5, feedback: "Correct: queues are FIFO." }),
    );

    const response = await POST(
      request({
        action: "grade",
        provider: "groq",
        mode: "multiple-choice",
        topic: "Queues",
        question,
        answer: "Queue",
        ...sourceSelection(),
      }),
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body).toMatchObject({ rating: 5, feedback: expect.any(String) });
    expect(mocks.recordInteraction).toHaveBeenCalledWith(
      expect.objectContaining({
        kind: "tutor-grade",
        metadata: { mode: "multiple-choice", rating: 5 },
      }),
    );
  });

  it("returns a written-answer critique with a rating", async () => {
    mocks.generateCompletion.mockResolvedValue(
      JSON.stringify({
        rating: 4,
        feedback:
          "Good explanation. Also mention the front and rear operations.",
      }),
    );

    const response = await POST(
      request({
        action: "grade",
        provider: "cerebras",
        mode: "short-answer",
        topic: "Queues",
        question: { ...question, choices: [] },
        answer: "A queue processes items in arrival order.",
        ...sourceSelection(),
      }),
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body).toMatchObject({ rating: 4, feedback: expect.any(String) });
  });
});
