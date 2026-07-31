import { NextResponse } from "next/server";

import { RagServiceError, errorResponse } from "@/lib/errors";
import { getProviderStatuses } from "@/lib/providers";
import { getLearningCatalog, getRagHealth } from "@/lib/rag";

export const runtime = "nodejs";

export async function GET(): Promise<NextResponse> {
  try {
    const providers = getProviderStatuses();
    try {
      const [catalog, health] = await Promise.all([
        getLearningCatalog(),
        getRagHealth(),
      ]);
      return NextResponse.json({
        providers,
        rag: {
          available: true,
          message:
            catalog.files.length === 0
              ? "No learning files are indexed yet. Index the corpus to enable retrieval."
              : null,
          files: catalog.files,
          tree: catalog.tree,
          upstashAvailable: health.upstashAvailable,
        },
      });
    } catch (error) {
      if (error instanceof RagServiceError) {
        return NextResponse.json({
          providers,
          rag: {
            available: false,
            message: error.message,
            files: [],
            tree: [],
            upstashAvailable: false,
          },
        });
      }

      throw error;
    }
  } catch (error) {
    return errorResponse(error);
  }
}
