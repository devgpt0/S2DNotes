import "./styles.css";

function getProperty<T extends object, K extends keyof T>(object: T, key: K): T[K] {
  return object[key];
}

type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };

function describe<T>(state: RequestState<T>): string {
  switch (state.status) {
    case "idle":
      return "Ready";
    case "loading":
      return "Loading";
    case "success":
      return `Loaded: ${JSON.stringify(state.data)}`;
    case "error":
      return state.message;
    default:
      return assertNever(state);
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled state: ${JSON.stringify(value)}`);
}

type User = { id: string; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  return (
    "id" in value &&
    typeof value.id === "string" &&
    "name" in value &&
    typeof value.name === "string"
  );
}

function parseUser(value: unknown): User {
  if (!isUser(value)) throw new TypeError("Expected string fields: id and name");
  return value;
}

function requireElement<T extends Element>(
  selector: string,
  constructor: { new (): T },
): T {
  const element = document.querySelector(selector);
  if (!(element instanceof constructor)) {
    throw new Error(`Missing element: ${selector}`);
  }
  return element;
}

const getterOutput = requireElement("#getter-output", HTMLParagraphElement);
const stateSelect = requireElement("#request-state", HTMLSelectElement);
const stateOutput = requireElement("#state-output", HTMLOutputElement);
const jsonInput = requireElement("#json-input", HTMLTextAreaElement);
const validateButton = requireElement("#validate-button", HTMLButtonElement);
const validationOutput = requireElement("#validation-output", HTMLOutputElement);

const user = { id: "u1", age: 28 };
getterOutput.textContent = [
  `ID: ${getProperty(user, "id")}`,
  `age: ${getProperty(user, "age")}`,
].join("; ");

const requestStates: Record<string, RequestState<{ name: string }>> = {
  idle: { status: "idle" },
  loading: { status: "loading" },
  success: { status: "success", data: { name: "Asha" } },
  error: { status: "error", message: "Request failed" },
};

function showSelectedState(): void {
  const state = requestStates[stateSelect.value];
  if (!state) {
    throw new Error(`Unknown request state: ${stateSelect.value}`);
  }
  stateOutput.textContent = describe(state);
}

stateSelect.addEventListener("change", showSelectedState);
showSelectedState();

validateButton.addEventListener("click", () => {
  try {
    const value: unknown = JSON.parse(jsonInput.value);
    const parsedUser = parseUser(value);
    validationOutput.textContent = `Valid user: ${parsedUser.name} (${parsedUser.id})`;
  } catch (error: unknown) {
    validationOutput.textContent =
      error instanceof Error ? `Invalid: ${error.message}` : "Invalid input";
  }
});
