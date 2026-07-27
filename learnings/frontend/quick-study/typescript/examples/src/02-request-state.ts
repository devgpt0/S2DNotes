type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };

function assertNever(value: never): never {
  throw new Error(`Unhandled state: ${JSON.stringify(value)}`);
}

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

const states: RequestState<{ name: string }>[] = [
  { status: "idle" },
  { status: "loading" },
  { status: "success", data: { name: "Asha" } },
  { status: "error", message: "Request failed" },
];

for (const state of states) {
  console.log(describe(state));
}
