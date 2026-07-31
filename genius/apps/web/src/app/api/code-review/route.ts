import { NextResponse } from "next/server";
import { z } from "zod";

import { codeReviewRequestSchema } from "@/lib/contracts";
import { recordInteraction } from "@/lib/database";
import { errorResponse } from "@/lib/errors";
import { codeReviewPrompt } from "@/lib/prompts";
import { parseProviderJson } from "@/lib/provider-output";
import { generateCompletion } from "@/lib/providers";
import { retrieveCitations } from "@/lib/rag";
import { parseJsonRequest } from "@/lib/request";

export const runtime = "nodejs";

const codeReviewOutputSchema = z
  .object({
    rating: z.number().int().min(1).max(5),
    review: z.string().min(1).max(12_000),
  })
  .strict();

export async function POST(request: Request): Promise<NextResponse> {
  try {
    const input = await parseJsonRequest(request, codeReviewRequestSchema);
    const citations = input.useRag
      ? await retrieveCitations({
          query: input.goal.length > 0 ? input.goal : input.code,
          backend: input.ragBackend,
          selectedFiles: input.selectedFiles,
        })
      : [];
    const completion = await generateCompletion(
      input.provider,
      codeReviewPrompt(input.language, input.code, input.goal, {
        selectedFiles: input.selectedFiles,
        citations,
      }),
    );
    const review = parseProviderJson(
      completion,
      codeReviewOutputSchema,
      "code reviewer",
    );
    const interactionId = recordInteraction({
      kind: "code-review",
      provider: input.provider,
      request: JSON.stringify(input),
      response: JSON.stringify(review),
      citations,
      metadata: { rating: review.rating, language: input.language },
    });

    return NextResponse.json({
      review: review.review,
      rating: review.rating,
      citations,
      interactionId,
    });
  } catch (error) {
    return errorResponse(error);
  }
}
