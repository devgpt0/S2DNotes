import {
  ragIndexResponseSchema,
  ragHealthResponseSchema,
  ragRetrieveResponseSchema,
  ragTreeResponseSchema,
  type Citation,
  type LearningTreeNode,
  type RagBackend,
  type RagIndexResponse,
} from "@/lib/contracts";
import { RagServiceError } from "@/lib/errors";

interface RetrieveInput {
  query: string;
  backend: RagBackend;
  selectedFiles: string[];
}

export interface LearningCatalog {
  files: string[];
  tree: LearningTreeNode[];
}

export interface RagHealth {
  upstashAvailable: boolean;
}

function ragEndpoint(path: string): URL {
  const configuredUrl = process.env.RAG_API_URL ?? "http://localhost:8000";
  let baseUrl: URL;
  try {
    baseUrl = new URL(configuredUrl);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new RagServiceError("RAG_API_URL is not a valid URL.", 500);
    }

    throw error;
  }

  if (baseUrl.protocol !== "http:" && baseUrl.protocol !== "https:") {
    throw new RagServiceError("RAG_API_URL must use HTTP or HTTPS.", 500);
  }

  return new URL(path, baseUrl);
}

async function ragRequest(path: string, init?: RequestInit): Promise<unknown> {
  let response: Response;
  try {
    response = await fetch(ragEndpoint(path), {
      ...init,
      cache: "no-store",
      signal: AbortSignal.timeout(30_000),
    });
  } catch (error) {
    if (error instanceof TypeError || error instanceof DOMException) {
      throw new RagServiceError(
        "The retrieval service is unavailable. Start the RAG service and try again.",
      );
    }

    throw error;
  }

  if (!response.ok) {
    let message =
      "The retrieval service returned status " + response.status + ".";
    try {
      const payload: unknown = await response.json();
      if (
        typeof payload === "object" &&
        payload !== null &&
        "detail" in payload &&
        typeof payload.detail === "string" &&
        payload.detail.length > 0
      ) {
        message = payload.detail;
      }
    } catch (error) {
      if (!(error instanceof SyntaxError)) {
        throw error;
      }
    }
    throw new RagServiceError(message, response.status === 409 ? 409 : 502);
  }

  try {
    return await response.json();
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new RagServiceError(
        "The retrieval service returned invalid JSON.",
        502,
      );
    }

    throw error;
  }
}

export async function getLearningCatalog(): Promise<LearningCatalog> {
  const response = await ragRequest("/tree");
  const result = ragTreeResponseSchema.safeParse(response);
  if (!result.success) {
    throw new RagServiceError(
      "The retrieval service returned an invalid document tree.",
      502,
    );
  }

  return result.data;
}

export async function getRagHealth(): Promise<RagHealth> {
  const response = await ragRequest("/health");
  const result = ragHealthResponseSchema.safeParse(response);
  if (!result.success) {
    throw new RagServiceError(
      "The retrieval service returned an invalid health response.",
      502,
    );
  }
  return {
    upstashAvailable:
      result.data.indexed &&
      result.data.upstash_enabled &&
      result.data.upstash_synced,
  };
}

export async function retrieveCitations(
  input: RetrieveInput,
): Promise<Citation[]> {
  const response = await ragRequest("/retrieve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: input.query,
      limit: 5,
      paths: input.selectedFiles.length > 0 ? input.selectedFiles : undefined,
      backend: input.backend,
    }),
  });
  const result = ragRetrieveResponseSchema.safeParse(response);
  if (!result.success) {
    throw new RagServiceError(
      "The retrieval service returned invalid citations.",
      502,
    );
  }

  if (input.selectedFiles.length === 0) {
    return result.data.citations.map((citation) => ({
      path: citation.path,
      heading: citation.heading,
      snippet: citation.snippet,
      score: citation.score,
    }));
  }

  return result.data.citations.map((citation) => ({
    path: citation.path,
    heading: citation.heading,
    snippet: citation.snippet,
    score: citation.score,
  }));
}

export async function indexLearningCorpus(): Promise<RagIndexResponse> {
  const response = await ragRequest("/index", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
  const result = ragIndexResponseSchema.safeParse(response);
  if (!result.success) {
    throw new RagServiceError(
      "The retrieval service returned an invalid indexing result.",
      502,
    );
  }

  return result.data;
}
