import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

import { afterEach, describe, expect, it, vi } from "vitest";

const temporaryDirectories: string[] = [];
const originalDatabaseUrl = process.env.DATABASE_URL;

afterEach(() => {
  if (originalDatabaseUrl === undefined) {
    delete process.env.DATABASE_URL;
  } else {
    process.env.DATABASE_URL = originalDatabaseUrl;
  }
  vi.resetModules();
  for (const directory of temporaryDirectories.splice(0)) {
    rmSync(directory, { force: true, recursive: true });
  }
});

describe("SQLite interaction persistence", () => {
  it("stores and reads prior turns for a chat conversation", async () => {
    const directory = mkdtempSync(join(tmpdir(), "genius-web-"));
    temporaryDirectories.push(directory);
    process.env.DATABASE_URL = "file:" + join(directory, "genius.sqlite");
    const database = await import("./database");
    const conversationId = "1c087d8b-b2a9-4672-9879-43a7f0f8e4e3";

    database.recordInteraction({
      kind: "chat",
      provider: "gemini",
      request: JSON.stringify({ message: "What is a queue?" }),
      response: JSON.stringify({ answer: "A queue is first-in, first-out." }),
      citations: [],
      conversationId,
    });

    expect(database.readConversationTurns(conversationId)).toEqual([
      { role: "learner", content: "What is a queue?" },
      { role: "assistant", content: "A queue is first-in, first-out." },
    ]);
    database.closeDatabase();
  });
});
