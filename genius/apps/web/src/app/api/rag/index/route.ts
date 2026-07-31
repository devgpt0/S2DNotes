import { NextResponse } from "next/server";
import { z } from "zod";

import { errorResponse } from "@/lib/errors";
import { indexLearningCorpus } from "@/lib/rag";
import { parseJsonRequest } from "@/lib/request";

const indexRequestSchema = z.object({}).strict();

export const runtime = "nodejs";

export async function POST(request: Request): Promise<NextResponse> {
  try {
    await parseJsonRequest(request, indexRequestSchema);
    const result = await indexLearningCorpus();
    return NextResponse.json(result);
  } catch (error) {
    return errorResponse(error);
  }
}
