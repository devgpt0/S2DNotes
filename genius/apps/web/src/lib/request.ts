import { z } from "zod";

import { InvalidRequestError } from "@/lib/errors";

export async function parseJsonRequest<T>(
  request: Request,
  schema: z.ZodType<T>,
): Promise<T> {
  const contentType = request.headers.get("content-type");
  if (!contentType?.startsWith("application/json")) {
    throw new InvalidRequestError("Content-Type must be application/json.");
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new InvalidRequestError("Request body must contain valid JSON.");
    }

    throw error;
  }

  const result = schema.safeParse(body);
  if (!result.success) {
    throw new InvalidRequestError(
      "Request body does not match the required schema.",
    );
  }

  return result.data;
}
