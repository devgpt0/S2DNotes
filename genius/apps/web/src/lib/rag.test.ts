import { afterEach, describe, expect, it, vi } from "vitest";

import { retrieveCitations } from "./rag";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("RAG client", () => {
  it("sends the selected file paths and backend to the retrieval service", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          query: "queues",
          citations: [
            {
              path: "collections/queues.md",
              topic: "collections",
              heading: "Queues",
              checksum: "b".repeat(64),
              snippet: "Queues are FIFO.",
              score: 0.8,
            },
          ],
          mode: "hybrid",
          backend: "upstash",
          reranked: true,
          indexed: true,
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    await expect(
      retrieveCitations({
        query: "queues",
        backend: "upstash",
        selectedFiles: ["collections/queues.md"],
      }),
    ).resolves.toEqual([
      {
        path: "collections/queues.md",
        heading: "Queues",
        snippet: "Queues are FIFO.",
        score: 0.8,
      },
    ]);

    const request = fetchMock.mock.calls[0]?.[1] as RequestInit;
    expect(JSON.parse(String(request.body))).toEqual({
      query: "queues",
      limit: 5,
      paths: ["collections/queues.md"],
      backend: "upstash",
    });
  });
});
