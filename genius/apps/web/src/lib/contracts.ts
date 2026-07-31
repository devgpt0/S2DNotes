import { z } from "zod";

export const providerIdSchema = z.enum(["gemini", "cerebras", "groq"]);
export type ProviderId = z.infer<typeof providerIdSchema>;

export const ragBackendSchema = z.enum(["local", "upstash"]);
export type RagBackend = z.infer<typeof ragBackendSchema>;

const filePathSchema = z.string().min(1).max(500);

export interface LearningTreeNode {
  name: string;
  path: string;
  children: LearningTreeNode[];
}

export const learningTreeNodeSchema: z.ZodType<LearningTreeNode> = z.lazy(() =>
  z
    .object({
      name: z.string().min(1).max(500),
      path: filePathSchema,
      children: z.array(learningTreeNodeSchema),
    })
    .strict(),
);
const sourceSelectionSchema = z.object({
  useRag: z.boolean(),
  ragBackend: ragBackendSchema,
  selectedFiles: z.array(filePathSchema).max(20),
});

export const citationSchema = z
  .object({
    path: filePathSchema,
    heading: z.string().min(1).max(500),
    snippet: z.string().min(1).max(4_000),
    score: z.number().finite(),
  })
  .strict();
export type Citation = z.infer<typeof citationSchema>;

export const providerStatusSchema = z
  .object({
    id: providerIdSchema,
    label: z.string().min(1),
    model: z.string().min(1),
    configured: z.boolean(),
  })
  .strict();
export type ProviderStatus = z.infer<typeof providerStatusSchema>;

export const providerCatalogResponseSchema = z
  .object({
    providers: z.array(providerStatusSchema),
    rag: z
      .object({
        available: z.boolean(),
        message: z.string().nullable(),
        files: z.array(filePathSchema),
        tree: z.array(learningTreeNodeSchema),
        upstashAvailable: z.boolean(),
      })
      .strict(),
  })
  .strict();
export type ProviderCatalogResponse = z.infer<
  typeof providerCatalogResponseSchema
>;

export const chatRequestSchema = z
  .object({
    provider: providerIdSchema,
    message: z.string().min(1).max(8_000),
    conversationId: z.string().uuid(),
    ...sourceSelectionSchema.shape,
  })
  .strict();

export const tutorQuestionSchema = z
  .object({
    id: z.string().uuid(),
    prompt: z.string().min(1).max(1_500),
    choices: z.array(z.string().min(1).max(500)).max(4),
  })
  .strict();
export type TutorQuestion = z.infer<typeof tutorQuestionSchema>;

export const generatedTutorQuestionSchema = z
  .object({
    prompt: z.string().min(1).max(1_500),
    choices: z.array(z.string().min(1).max(500)).max(4).optional(),
  })
  .strict();

const tutorGenerationRequestSchema = z
  .object({
    action: z.literal("generate"),
    provider: providerIdSchema,
    mode: z.enum(["short-answer", "multiple-choice"]),
    topic: z.string().min(1).max(160),
    ...sourceSelectionSchema.shape,
  })
  .strict();

const tutorGradeRequestSchema = z
  .object({
    action: z.literal("grade"),
    provider: providerIdSchema,
    mode: z.enum(["short-answer", "multiple-choice"]),
    topic: z.string().min(1).max(160),
    question: tutorQuestionSchema,
    answer: z.string().min(1).max(4_000),
    ...sourceSelectionSchema.shape,
  })
  .strict();

export const tutorRequestSchema = z.discriminatedUnion("action", [
  tutorGenerationRequestSchema,
  tutorGradeRequestSchema,
]);
export type TutorRequest = z.infer<typeof tutorRequestSchema>;

export const tutorGenerationResponseSchema = z
  .object({
    questions: z.array(tutorQuestionSchema).length(5),
    citations: z.array(citationSchema),
    interactionId: z.string().uuid(),
  })
  .strict();
export type TutorGenerationResponse = z.infer<
  typeof tutorGenerationResponseSchema
>;

export const tutorGradeResponseSchema = z
  .object({
    feedback: z.string().min(1),
    rating: z.number().int().min(1).max(5),
    interactionId: z.string().uuid(),
  })
  .strict();
export type TutorGradeResponse = z.infer<typeof tutorGradeResponseSchema>;

export const codingLanguageSchema = z.enum([
  "cpp",
  "java",
  "python",
  "go",
  "rust",
]);
export type CodingLanguage = z.infer<typeof codingLanguageSchema>;

export const codeReviewRequestSchema = z
  .object({
    provider: providerIdSchema,
    language: codingLanguageSchema,
    code: z.string().min(1).max(30_000),
    goal: z.string().max(1_000),
    ...sourceSelectionSchema.shape,
  })
  .strict();

export const codeReviewResponseSchema = z
  .object({
    review: z.string().min(1),
    rating: z.number().int().min(1).max(5),
    citations: z.array(citationSchema),
    interactionId: z.string().uuid(),
  })
  .strict();
export type CodeReviewResponse = z.infer<typeof codeReviewResponseSchema>;

export const ragTreeResponseSchema = z
  .object({
    files: z.array(filePathSchema),
    tree: z.array(learningTreeNodeSchema),
  })
  .strict();

export const ragRetrieveResponseSchema = z
  .object({
    query: z.string(),
    citations: z.array(
      citationSchema
        .extend({
          topic: z.string().min(1).max(500),
          checksum: z.string().min(1).max(256),
        })
        .strict(),
    ),
    mode: z.enum(["hybrid", "bm25", "unavailable"]),
    backend: ragBackendSchema,
    reranked: z.boolean(),
    indexed: z.boolean(),
  })
  .strict();

export const ragIndexResponseSchema = z
  .object({
    state: z.literal("indexed"),
    document_count: z.number().int().nonnegative(),
    chunk_count: z.number().int().nonnegative(),
    embedding_status: z.enum(["ready", "unavailable"]),
    vector_backend: z.enum(["faiss", "numpy", "disabled"]),
    upstash_synced: z.boolean(),
    warnings: z.array(z.string()),
  })
  .strict();
export type RagIndexResponse = z.infer<typeof ragIndexResponseSchema>;

export const ragHealthResponseSchema = z
  .object({
    status: z.enum(["ok", "degraded"]),
    index_state: z.enum(["idle", "indexing", "indexed", "failed"]),
    indexed: z.boolean(),
    upstash_enabled: z.boolean(),
    upstash_synced: z.boolean(),
  })
  .passthrough();
