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
  if (!isUser(value)) throw new TypeError("Invalid user response");
  return value;
}

const validResponse: unknown = { id: "u1", name: "Asha" };
console.log(parseUser(validResponse));

const invalidResponse: unknown = { id: 1, name: "Asha" };
try {
  parseUser(invalidResponse);
} catch (error: unknown) {
  if (!(error instanceof TypeError)) throw error;
  console.log(`Rejected invalid data: ${error.message}`);
}
