import { randomUUID } from "node:crypto";
import { mkdirSync } from "node:fs";

import Database from "better-sqlite3";
import { z } from "zod";

import type { Citation, ProviderId } from "@/lib/contracts";

type InteractionKind =
  "chat" | "tutor-generation" | "tutor-grade" | "code-review";

interface InteractionInput {
  kind: InteractionKind;
  provider: ProviderId;
  request: string;
  response: string;
  citations: Citation[];
  conversationId?: string;
  metadata?: Record<string, unknown>;
}

export interface ConversationTurn {
  role: "learner" | "assistant";
  content: string;
}

let database: Database.Database | undefined;

function databasePath(): string {
  const databaseUrl = process.env.DATABASE_URL ?? "file:./data/genius.sqlite";
  if (!databaseUrl.startsWith("file:")) {
    throw new Error("DATABASE_URL must use the file: scheme.");
  }

  const filePath = databaseUrl.slice("file:".length);
  if (filePath.length === 0) {
    throw new Error("DATABASE_URL must include a SQLite file path.");
  }
  if (
    !filePath.startsWith("./") &&
    !filePath.startsWith("/") &&
    !/^[A-Za-z]:[\\/]/.test(filePath)
  ) {
    throw new Error(
      "DATABASE_URL must contain an absolute path or a path beginning with ./.",
    );
  }

  return filePath;
}

function parentDirectory(filePath: string): string {
  const separatorIndex = Math.max(
    filePath.lastIndexOf("/"),
    filePath.lastIndexOf("\\"),
  );
  if (separatorIndex < 0) {
    return ".";
  }

  const directory = filePath.slice(0, separatorIndex);
  return directory.length === 0 ? "/" : directory;
}

function getDatabase(): Database.Database {
  if (database) {
    return database;
  }

  const filePath = databasePath();
  mkdirSync(parentDirectory(filePath), { recursive: true });
  database = new Database(filePath);
  database.pragma("journal_mode = WAL");
  database.pragma("foreign_keys = ON");
  database.exec(
    [
      "CREATE TABLE IF NOT EXISTS interactions (",
      "  id TEXT PRIMARY KEY,",
      "  kind TEXT NOT NULL,",
      "  provider TEXT NOT NULL,",
      "  request TEXT NOT NULL,",
      "  response TEXT NOT NULL,",
      "  citations TEXT NOT NULL,",
      "  conversation_id TEXT,",
      "  metadata TEXT NOT NULL DEFAULT '{}',",
      "  created_at TEXT NOT NULL",
      ");",
    ].join("\n"),
  );
  const columns = database
    .prepare("PRAGMA table_info(interactions)")
    .all() as Array<{ name: string }>;
  const columnNames = new Set(columns.map((column) => column.name));
  if (!columnNames.has("conversation_id")) {
    database.exec("ALTER TABLE interactions ADD COLUMN conversation_id TEXT");
  }
  if (!columnNames.has("metadata")) {
    database.exec(
      "ALTER TABLE interactions ADD COLUMN metadata TEXT NOT NULL DEFAULT '{}'",
    );
  }
  database.exec(
    "CREATE INDEX IF NOT EXISTS interactions_conversation_created_at ON interactions (conversation_id, created_at)",
  );

  return database;
}

export function recordInteraction(input: InteractionInput): string {
  const id = randomUUID();
  const createdAt = new Date().toISOString();
  const statement = getDatabase().prepare(
    [
      "INSERT INTO interactions (id, kind, provider, request, response, citations, conversation_id, metadata, created_at)",
      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    ].join(" "),
  );
  statement.run(
    id,
    input.kind,
    input.provider,
    input.request,
    input.response,
    JSON.stringify(input.citations),
    input.conversationId ?? null,
    JSON.stringify(input.metadata ?? {}),
    createdAt,
  );

  return id;
}

const storedChatRequestSchema = z
  .object({ message: z.string().min(1).max(8_000) })
  .passthrough();
const storedChatResponseSchema = z
  .object({ answer: z.string().min(1) })
  .strict();

export function readConversationTurns(
  conversationId: string,
  limit = 10,
): ConversationTurn[] {
  if (!conversationId) {
    throw new Error("Conversation id must not be empty.");
  }
  if (!Number.isInteger(limit) || limit < 1 || limit > 50) {
    throw new Error(
      "Conversation history limit must be an integer from 1 to 50.",
    );
  }

  const rows = getDatabase()
    .prepare(
      [
        "SELECT request, response",
        "FROM interactions",
        "WHERE kind = 'chat' AND conversation_id = ?",
        "ORDER BY created_at DESC",
        "LIMIT ?",
      ].join(" "),
    )
    .all(conversationId, limit) as Array<{ request: string; response: string }>;

  const turns: ConversationTurn[] = [];
  for (const row of rows.reverse()) {
    const request = storedChatRequestSchema.parse(JSON.parse(row.request));
    const response = storedChatResponseSchema.parse(JSON.parse(row.response));
    turns.push(
      { role: "learner", content: request.message },
      { role: "assistant", content: response.answer },
    );
  }
  return turns;
}

export function closeDatabase(): void {
  if (!database) {
    return;
  }
  database.close();
  database = undefined;
}
