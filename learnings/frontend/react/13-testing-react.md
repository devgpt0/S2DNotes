# 13 - Testing React

## Testing Principle

Test what users can observe: roles, names, text, state, navigation, network outcomes, and accessibility. Avoid asserting internal hook state or component method calls.

## Component Test

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";

test("increments count", async () => {
  const user = userEvent.setup();
  render(<Counter />);
  await user.click(screen.getByRole("button", { name: /count: 0/i }));
  expect(screen.getByRole("button", { name: /count: 1/i })).toBeInTheDocument();
});
// Test output: passes when user-visible count changes from 0 to 1.
```

Prefer queries: role/name -> label -> text -> test ID as last resort.

## Async Test

```tsx
render(<CoursePage id="html" />);
expect(screen.getByText(/loading/i)).toBeInTheDocument();
expect(await screen.findByRole("heading", { name: "HTML" })).toBeInTheDocument();
// Test output: verifies loading then resolved course heading.
```

Mock network at the HTTP boundary (for example service-worker interception), not internal implementation functions when integration behavior matters.

## Test Layers

- pure unit: reducers, selectors, validation
- component: interaction/accessibility/rendering
- route/integration: loaders/actions/providers/network contracts
- end-to-end: critical browser journey
- visual/accessibility/performance: specialized regression checks plus human review

## Avoid Fragile Tests

- snapshots for large changing trees
- querying CSS class for behavior
- calling component functions directly
- testing React itself
- arbitrary sleep/timeouts
- one enormous test covering every path

## StrictMode and Cleanup

Render tests under production-equivalent providers and optionally StrictMode. Ensure effects/listeners/timers are cleaned and tests are independent.
