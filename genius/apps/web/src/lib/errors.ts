import { NextResponse } from "next/server";

export class ApplicationError extends Error {
  public constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApplicationError";
  }
}

export class InvalidRequestError extends ApplicationError {
  public constructor(message: string) {
    super(message, 400);
    this.name = "InvalidRequestError";
  }
}

export class ProviderConfigurationError extends ApplicationError {
  public constructor(message: string) {
    super(message, 503);
    this.name = "ProviderConfigurationError";
  }
}

export class ProviderResponseError extends ApplicationError {
  public constructor(message: string) {
    super(message, 502);
    this.name = "ProviderResponseError";
  }
}

export class RagServiceError extends ApplicationError {
  public constructor(message: string, status = 503) {
    super(message, status);
    this.name = "RagServiceError";
  }
}

export function errorResponse(error: unknown): NextResponse {
  if (error instanceof ApplicationError) {
    return NextResponse.json(
      { error: error.message },
      { status: error.status },
    );
  }

  throw error;
}
