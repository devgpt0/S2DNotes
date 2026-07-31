import { afterEach, describe, expect, it } from "vitest";

import { getProviderStatuses, generateCompletion } from "./providers";

const originalProviderKeys = {
  cerebras: process.env.CEREBRAS_API_KEY,
  gemini: process.env.GEMINI_API_KEY,
  groq: process.env.GROQ_API_KEY,
};

afterEach(() => {
  if (originalProviderKeys.gemini === undefined) {
    delete process.env.GEMINI_API_KEY;
  } else {
    process.env.GEMINI_API_KEY = originalProviderKeys.gemini;
  }
  if (originalProviderKeys.cerebras === undefined) {
    delete process.env.CEREBRAS_API_KEY;
  } else {
    process.env.CEREBRAS_API_KEY = originalProviderKeys.cerebras;
  }
  if (originalProviderKeys.groq === undefined) {
    delete process.env.GROQ_API_KEY;
  } else {
    process.env.GROQ_API_KEY = originalProviderKeys.groq;
  }
});

describe("provider configuration", () => {
  it("reports configured and missing providers without exposing keys", () => {
    process.env.GEMINI_API_KEY = "test-key";

    const providers = getProviderStatuses();

    expect(
      providers.find((provider) => provider.id === "gemini"),
    ).toMatchObject({
      configured: true,
      model: "gemini-2.5-flash-lite",
    });
    expect(providers.find((provider) => provider.id === "groq")).toMatchObject({
      configured: false,
    });
    expect(JSON.stringify(providers)).not.toContain("test-key");
  });

  it("fails before a network request when the selected provider has no key", async () => {
    await expect(
      generateCompletion("groq", {
        systemPrompt: "You are concise.",
        userPrompt: "Hello",
      }),
    ).rejects.toThrow("GROQ_API_KEY");
  });
});
