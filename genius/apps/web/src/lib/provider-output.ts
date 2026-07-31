import { z } from "zod";

import { ProviderResponseError } from "@/lib/errors";

export function parseProviderJson<T>(
  completion: string,
  schema: z.ZodType<T>,
  label: string,
): T {
  let body: unknown;
  try {
    body = JSON.parse(completion);
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new ProviderResponseError(
        "The " + label + " returned invalid JSON. Try again.",
      );
    }

    throw error;
  }

  const result = schema.safeParse(body);
  if (!result.success) {
    throw new ProviderResponseError(
      "The " + label + " returned a response with an invalid schema.",
    );
  }

  return result.data;
}
