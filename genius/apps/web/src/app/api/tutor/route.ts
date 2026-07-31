import { randomUUID } from "node:crypto";

import { NextResponse } from "next/server";
import { z } from "zod";

import {
  generatedTutorQuestionSchema,
  tutorRequestSchema,
  type Citation,
  type RagBackend,
  type TutorQuestion,
} from "@/lib/contracts";
import { recordInteraction } from "@/lib/database";
import { ProviderResponseError, errorResponse } from "@/lib/errors";
import { tutorGenerationPrompt, tutorGradePrompt } from "@/lib/prompts";
import { parseProviderJson } from "@/lib/provider-output";
import { generateCompletion } from "@/lib/providers";
import { retrieveCitations } from "@/lib/rag";
import { parseJsonRequest } from "@/lib/request";

const generatedQuestionSetSchema = z
  .object({
    questions: z.array(generatedTutorQuestionSchema).length(5),
  })
  .strict();
const tutorGradeOutputSchema = z
  .object({
    rating: z.number().int().min(1).max(5),
    feedback: z.string().min(1).max(8_000),
  })
  .strict();

function parseGeneratedQuestions(
  completion: string,
  mode: "short-answer" | "multiple-choice",
): TutorQuestion[] {
  let body: unknown;
  try {
    body = JSON.parse(completion);
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new ProviderResponseError(
        "The tutor returned an invalid assessment. Generate a new assessment.",
      );
    }

    throw error;
  }

  const result = generatedQuestionSetSchema.safeParse(body);
  if (!result.success) {
    throw new ProviderResponseError(
      "The tutor returned an assessment with an invalid schema.",
    );
  }

  return result.data.questions.map((question) => {
    if (mode === "multiple-choice") {
      if (!question.choices || question.choices.length !== 4) {
        throw new ProviderResponseError(
          "The tutor did not create four choices for every question.",
        );
      }

      return {
        id: randomUUID(),
        prompt: question.prompt,
        choices: question.choices,
      };
    }

    if (question.choices) {
      throw new ProviderResponseError(
        "The tutor returned choices for a short-answer assessment.",
      );
    }

    return {
      id: randomUUID(),
      prompt: question.prompt,
      choices: [],
    };
  });
}

async function citationsFor(
  query: string,
  useRag: boolean,
  backend: RagBackend,
  selectedFiles: string[],
): Promise<Citation[]> {
  if (!useRag) {
    return [];
  }

  return retrieveCitations({ query, backend, selectedFiles });
}

export const runtime = "nodejs";

export async function POST(request: Request): Promise<NextResponse> {
  try {
    const input = await parseJsonRequest(request, tutorRequestSchema);

    if (input.action === "generate") {
      const citations = await citationsFor(
        input.topic,
        input.useRag,
        input.ragBackend,
        input.selectedFiles,
      );
      const completion = await generateCompletion(
        input.provider,
        tutorGenerationPrompt(input.mode, input.topic, {
          selectedFiles: input.selectedFiles,
          citations,
        }),
      );
      const questions = parseGeneratedQuestions(completion, input.mode);
      const interactionId = recordInteraction({
        kind: "tutor-generation",
        provider: input.provider,
        request: JSON.stringify(input),
        response: JSON.stringify(questions),
        citations,
        metadata: { mode: input.mode, questionCount: questions.length },
      });

      return NextResponse.json({ questions, citations, interactionId });
    }

    const citations = await citationsFor(
      input.topic + " " + input.question.prompt,
      input.useRag,
      input.ragBackend,
      input.selectedFiles,
    );
    const completion = await generateCompletion(
      input.provider,
      tutorGradePrompt(input.mode, input.topic, input.question, input.answer, {
        selectedFiles: input.selectedFiles,
        citations,
      }),
    );
    const feedback = parseProviderJson(
      completion,
      tutorGradeOutputSchema,
      "tutor",
    );
    const interactionId = recordInteraction({
      kind: "tutor-grade",
      provider: input.provider,
      request: JSON.stringify(input),
      response: JSON.stringify(feedback),
      citations,
      metadata: { rating: feedback.rating, mode: input.mode },
    });

    return NextResponse.json({
      feedback: feedback.feedback,
      rating: feedback.rating,
      interactionId,
    });
  } catch (error) {
    return errorResponse(error);
  }
}
