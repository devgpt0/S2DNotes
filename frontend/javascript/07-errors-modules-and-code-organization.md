# 07 - Errors, Modules, and Code Organization

## Throw Useful Errors

```javascript
const positive = (value) => {
  if (!Number.isFinite(value) || value <= 0) {
    throw new RangeError("value must be a positive finite number");
  }
  return value;
};
console.log(positive(5));
// Console output: 5
```

Validate at boundaries and fail immediately. Do not silently coerce invalid input unless business rules explicitly require it.

## Catch Only What You Can Handle

```javascript
try {
  JSON.parse("invalid");
} catch (error) {
  if (!(error instanceof SyntaxError)) throw error;
  console.log("Invalid JSON");
}
// Console output: Invalid JSON
```

`finally` is for cleanup. Avoid returning from it.

## Custom Error

```javascript
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}
const error = new ValidationError("Required", "email");
console.log(error.name, error.field);
// Console output: ValidationError email
```

## ES Modules

```javascript
// math.js
export const add = (left, right) => left + right;

// app.js
import { add } from "./math.js";
console.log(add(20, 22));
// Console output: 42
```

Modules have their own scope, strict mode, static import graph, and deferred browser execution.

## Dynamic Import

```javascript
const module = await import("./large-feature.js");
console.log(typeof module.start);
// Module console output: function (when large-feature exports start).
```

Dynamic import supports on-demand code loading. Split by user journeys, not every tiny file.

## Organization

- group by cohesive feature
- separate pure domain logic from DOM/network/storage adapters
- pass dependencies explicitly
- keep public module APIs small
- avoid circular imports
- expose errors meaningful to the caller
- never log tokens, passwords, or personal data
