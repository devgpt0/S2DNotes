import { chatRequestSchema } from "@/lib/contracts";
import { readConversationTurns, recordInteraction } from "@/lib/database";
import { ApplicationError, errorResponse } from "@/lib/errors";
import { chatPrompt } from "@/lib/prompts";
import { generateCompletionStream } from "@/lib/providers";
import { retrieveCitations } from "@/lib/rag";
import { parseJsonRequest } from "@/lib/request";

export const runtime = "nodejs";

const encoder = new TextEncoder();

function streamEvent(event: string, payload: unknown): Uint8Array {
  return encoder.encode(
    "event: " + event + "\ndata: " + JSON.stringify(payload) + "\n\n",
  );
}

function streamErrorMessage(error: unknown): string {
  if (error instanceof ApplicationError) {
    return error.message;
  }
  return "The chat stream ended unexpectedly. Try again.";
}

export async function POST(request: Request): Promise<Response> {
  try {
    const input = await parseJsonRequest(request, chatRequestSchema);
    const citations = input.useRag
      ? await retrieveCitations({
          query: input.message,
          backend: input.ragBackend,
          selectedFiles: input.selectedFiles,
        })
      : [];
    const history = readConversationTurns(input.conversationId, 5);
    const prompt = chatPrompt(
      input.message,
      {
        selectedFiles: input.selectedFiles,
        citations,
      },
      history,
    );
    const stream = new ReadableStream<Uint8Array>({
      async start(controller): Promise<void> {
        let answer = "";
        try {
          controller.enqueue(streamEvent("sources", { citations }));
          for await (const token of generateCompletionStream(
            input.provider,
            prompt,
          )) {
            answer += token;
            controller.enqueue(streamEvent("token", { token }));
          }
          if (!answer.trim()) {
            throw new ApplicationError(
              "The selected provider returned no usable completion text.",
              502,
            );
          }
          const interactionId = recordInteraction({
            kind: "chat",
            provider: input.provider,
            request: JSON.stringify(input),
            response: JSON.stringify({ answer }),
            citations,
            conversationId: input.conversationId,
          });
          controller.enqueue(streamEvent("complete", { interactionId }));
        } catch (error) {
          controller.enqueue(
            streamEvent("error", { error: streamErrorMessage(error) }),
          );
        } finally {
          controller.close();
        }
      },
    });

    return new Response(stream, {
      headers: {
        "Cache-Control": "no-cache, no-transform",
        Connection: "keep-alive",
        "Content-Type": "text/event-stream; charset=utf-8",
      },
    });
  } catch (error) {
    return errorResponse(error);
  }
}
