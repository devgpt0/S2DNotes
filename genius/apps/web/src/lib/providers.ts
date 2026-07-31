import { z } from "zod";

import type { ProviderId, ProviderStatus } from "@/lib/contracts";
import {
  ProviderConfigurationError,
  ProviderResponseError,
} from "@/lib/errors";

interface CompletionInput {
  systemPrompt: string;
  userPrompt: string;
  temperature: number;
  maxOutputTokens: number;
}

interface ProviderAdapter {
  complete(input: CompletionInput): Promise<string>;
  stream(input: CompletionInput): AsyncGenerator<string>;
}

interface ProviderDefinition {
  label: string;
  apiKeyEnvironmentVariable: string;
  modelEnvironmentVariable: string;
  defaultModel: string;
}

interface ProviderSettings {
  model: string;
  apiKey: string | undefined;
}

const providerDefinitions: Record<ProviderId, ProviderDefinition> = {
  gemini: {
    label: "Gemini",
    apiKeyEnvironmentVariable: "GEMINI_API_KEY",
    modelEnvironmentVariable: "GEMINI_MODEL",
    defaultModel: "gemini-2.5-flash-lite",
  },
  cerebras: {
    label: "Cerebras",
    apiKeyEnvironmentVariable: "CEREBRAS_API_KEY",
    modelEnvironmentVariable: "CEREBRAS_MODEL",
    defaultModel: "llama-3.3-70b",
  },
  groq: {
    label: "Groq",
    apiKeyEnvironmentVariable: "GROQ_API_KEY",
    modelEnvironmentVariable: "GROQ_MODEL",
    defaultModel: "llama-3.3-70b-versatile",
  },
};
const providerIds: ProviderId[] = ["gemini", "cerebras", "groq"];

const openAiResponseSchema = z
  .object({
    choices: z
      .array(
        z
          .object({
            message: z
              .object({
                content: z.string().nullable().optional(),
              })
              .passthrough(),
          })
          .passthrough(),
      )
      .min(1),
  })
  .passthrough();

const geminiResponseSchema = z
  .object({
    candidates: z
      .array(
        z
          .object({
            content: z
              .object({
                parts: z
                  .array(
                    z
                      .object({
                        text: z.string().optional(),
                      })
                      .passthrough(),
                  )
                  .min(1),
              })
              .passthrough(),
          })
          .passthrough(),
      )
      .min(1),
  })
  .passthrough();

const openAiStreamResponseSchema = z
  .object({
    choices: z
      .array(
        z
          .object({
            delta: z
              .object({
                content: z.string().nullable().optional(),
              })
              .passthrough(),
          })
          .passthrough(),
      )
      .min(1),
  })
  .passthrough();

function providerSettings(provider: ProviderId): ProviderSettings {
  const definition = providerDefinitions[provider];
  return {
    apiKey: process.env[definition.apiKeyEnvironmentVariable],
    model:
      process.env[definition.modelEnvironmentVariable] ??
      definition.defaultModel,
  };
}

function requireConfiguredProvider(provider: ProviderId): ProviderSettings {
  const settings = providerSettings(provider);
  if (!settings.apiKey) {
    throw new ProviderConfigurationError(
      providerDefinitions[provider].label +
        " is not configured. Add " +
        providerDefinitions[provider].apiKeyEnvironmentVariable +
        " on the server.",
    );
  }
  if (!settings.model) {
    throw new ProviderConfigurationError(
      providerDefinitions[provider].label +
        " requires a non-empty " +
        providerDefinitions[provider].modelEnvironmentVariable +
        ".",
    );
  }

  return settings;
}

async function postProviderJson(
  endpoint: string,
  headers: HeadersInit,
  body: unknown,
): Promise<unknown> {
  let response: Response;
  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      cache: "no-store",
      signal: AbortSignal.timeout(45_000),
    });
  } catch (error) {
    if (error instanceof TypeError || error instanceof DOMException) {
      throw new ProviderResponseError(
        "The selected provider could not be reached. Try again shortly.",
      );
    }

    throw error;
  }

  if (!response.ok) {
    throw new ProviderResponseError(
      "The selected provider rejected the generation request with status " +
        response.status +
        ".",
    );
  }

  try {
    return await response.json();
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new ProviderResponseError(
        "The selected provider returned an invalid response.",
      );
    }

    throw error;
  }
}

async function postProviderStream(
  endpoint: string,
  headers: HeadersInit,
  body: unknown,
): Promise<Response> {
  let response: Response;
  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      cache: "no-store",
      signal: AbortSignal.timeout(60_000),
    });
  } catch (error) {
    if (error instanceof TypeError || error instanceof DOMException) {
      throw new ProviderResponseError(
        "The selected provider could not be reached. Try again shortly.",
      );
    }

    throw error;
  }

  if (!response.ok) {
    throw new ProviderResponseError(
      "The selected provider rejected the generation request with status " +
        response.status +
        ".",
    );
  }
  if (!response.body) {
    throw new ProviderResponseError(
      "The selected provider did not return a stream.",
    );
  }

  return response;
}

async function* ssePayloads(response: Response): AsyncGenerator<string> {
  if (!response.body) {
    throw new ProviderResponseError(
      "The selected provider did not return a stream.",
    );
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      const result = await reader.read();
      if (result.done) {
        break;
      }
      buffer += decoder
        .decode(result.value, { stream: true })
        .replaceAll("\r\n", "\n");

      let separator = buffer.indexOf("\n\n");
      while (separator >= 0) {
        const event = buffer.slice(0, separator);
        buffer = buffer.slice(separator + 2);
        const payload = event
          .split("\n")
          .filter((line) => line.startsWith("data:"))
          .map((line) => line.slice("data:".length).trimStart())
          .join("\n");
        if (payload) {
          yield payload;
        }
        separator = buffer.indexOf("\n\n");
      }
    }
    buffer += decoder.decode().replaceAll("\r\n", "\n");
    if (buffer.trim()) {
      const payload = buffer
        .split("\n")
        .filter((line) => line.startsWith("data:"))
        .map((line) => line.slice("data:".length).trimStart())
        .join("\n");
      if (payload) {
        yield payload;
      }
    }
  } catch (error) {
    if (error instanceof TypeError || error instanceof DOMException) {
      throw new ProviderResponseError(
        "The selected provider stream ended unexpectedly.",
      );
    }

    throw error;
  } finally {
    reader.releaseLock();
  }
}

class GeminiProviderAdapter implements ProviderAdapter {
  public constructor(private readonly settings: ProviderSettings) {}

  public async complete(input: CompletionInput): Promise<string> {
    if (!this.settings.apiKey) {
      throw new ProviderConfigurationError("Gemini is not configured.");
    }

    const endpoint =
      "https://generativelanguage.googleapis.com/v1beta/models/" +
      encodeURIComponent(this.settings.model) +
      ":generateContent?key=" +
      encodeURIComponent(this.settings.apiKey);
    const response = await postProviderJson(
      endpoint,
      { "Content-Type": "application/json" },
      {
        contents: [
          {
            role: "user",
            parts: [
              {
                text:
                  "System instructions:\n" +
                  input.systemPrompt +
                  "\n\nUser request:\n" +
                  input.userPrompt,
              },
            ],
          },
        ],
        generationConfig: {
          temperature: input.temperature,
          maxOutputTokens: input.maxOutputTokens,
        },
      },
    );
    const parsed = geminiResponseSchema.safeParse(response);
    const content = parsed.success
      ? parsed.data.candidates[0]?.content.parts
          .map((part) => part.text ?? "")
          .join("")
      : "";
    if (!content) {
      throw new ProviderResponseError(
        "Gemini returned no usable completion text.",
      );
    }

    return content;
  }

  public async *stream(input: CompletionInput): AsyncGenerator<string> {
    if (!this.settings.apiKey) {
      throw new ProviderConfigurationError("Gemini is not configured.");
    }

    const endpoint =
      "https://generativelanguage.googleapis.com/v1beta/models/" +
      encodeURIComponent(this.settings.model) +
      ":streamGenerateContent?alt=sse&key=" +
      encodeURIComponent(this.settings.apiKey);
    const response = await postProviderStream(
      endpoint,
      { "Content-Type": "application/json" },
      {
        contents: [
          {
            role: "user",
            parts: [
              {
                text:
                  "System instructions:\n" +
                  input.systemPrompt +
                  "\n\nUser request:\n" +
                  input.userPrompt,
              },
            ],
          },
        ],
        generationConfig: {
          temperature: input.temperature,
          maxOutputTokens: input.maxOutputTokens,
        },
      },
    );

    for await (const payload of ssePayloads(response)) {
      let body: unknown;
      try {
        body = JSON.parse(payload);
      } catch (error) {
        if (error instanceof SyntaxError) {
          throw new ProviderResponseError(
            "Gemini returned an invalid stream event.",
          );
        }

        throw error;
      }
      const parsed = geminiResponseSchema.safeParse(body);
      const content = parsed.success
        ? parsed.data.candidates[0]?.content.parts
            .map((part) => part.text ?? "")
            .join("")
        : "";
      if (content) {
        yield content;
      }
    }
  }
}

class OpenAiCompatibleProviderAdapter implements ProviderAdapter {
  public constructor(
    private readonly settings: ProviderSettings,
    private readonly endpoint: string,
  ) {}

  public async complete(input: CompletionInput): Promise<string> {
    if (!this.settings.apiKey) {
      throw new ProviderConfigurationError(
        "The selected provider is not configured.",
      );
    }

    const response = await postProviderJson(
      this.endpoint,
      {
        Authorization: "Bearer " + this.settings.apiKey,
        "Content-Type": "application/json",
      },
      {
        model: this.settings.model,
        messages: [
          { role: "system", content: input.systemPrompt },
          { role: "user", content: input.userPrompt },
        ],
        temperature: input.temperature,
        max_tokens: input.maxOutputTokens,
      },
    );
    const parsed = openAiResponseSchema.safeParse(response);
    const content = parsed.success
      ? parsed.data.choices[0]?.message.content
      : undefined;
    if (!content) {
      throw new ProviderResponseError(
        "The selected provider returned no usable completion text.",
      );
    }

    return content;
  }

  public async *stream(input: CompletionInput): AsyncGenerator<string> {
    if (!this.settings.apiKey) {
      throw new ProviderConfigurationError(
        "The selected provider is not configured.",
      );
    }

    const response = await postProviderStream(
      this.endpoint,
      {
        Authorization: "Bearer " + this.settings.apiKey,
        "Content-Type": "application/json",
      },
      {
        model: this.settings.model,
        messages: [
          { role: "system", content: input.systemPrompt },
          { role: "user", content: input.userPrompt },
        ],
        temperature: input.temperature,
        max_tokens: input.maxOutputTokens,
        stream: true,
      },
    );

    for await (const payload of ssePayloads(response)) {
      if (payload === "[DONE]") {
        return;
      }
      let body: unknown;
      try {
        body = JSON.parse(payload);
      } catch (error) {
        if (error instanceof SyntaxError) {
          throw new ProviderResponseError(
            "The selected provider returned an invalid stream event.",
          );
        }

        throw error;
      }
      const parsed = openAiStreamResponseSchema.safeParse(body);
      const content = parsed.success
        ? parsed.data.choices[0]?.delta.content
        : undefined;
      if (content) {
        yield content;
      }
    }
  }
}

function adapterFor(provider: ProviderId): ProviderAdapter {
  const settings = requireConfiguredProvider(provider);
  switch (provider) {
    case "gemini":
      return new GeminiProviderAdapter(settings);
    case "cerebras":
      return new OpenAiCompatibleProviderAdapter(
        settings,
        "https://api.cerebras.ai/v1/chat/completions",
      );
    case "groq":
      return new OpenAiCompatibleProviderAdapter(
        settings,
        "https://api.groq.com/openai/v1/chat/completions",
      );
  }
}

export function getProviderStatuses(): ProviderStatus[] {
  return providerIds.map((providerId) => {
    const definition = providerDefinitions[providerId];
    const settings = providerSettings(providerId);
    return {
      id: providerId,
      label: definition.label,
      model: settings.model,
      configured: Boolean(settings.apiKey && settings.model),
    };
  });
}

export async function generateCompletion(
  provider: ProviderId,
  input: Omit<CompletionInput, "temperature" | "maxOutputTokens">,
): Promise<string> {
  return adapterFor(provider).complete({
    ...input,
    temperature: 0.2,
    maxOutputTokens: 1_600,
  });
}

export async function* generateCompletionStream(
  provider: ProviderId,
  input: Omit<CompletionInput, "temperature" | "maxOutputTokens">,
): AsyncGenerator<string> {
  const adapter = adapterFor(provider);
  yield* adapter.stream({
    ...input,
    temperature: 0.2,
    maxOutputTokens: 1_600,
  });
}
