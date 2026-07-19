# 07 - Testing, DevTools, Persistence, and Production Design

## Test Reducers as Pure State Transitions

```typescript
import { expect, test } from "vitest";

test("toggles a course", () => {
  const before = {
    items: [{ id: "ts", title: "TypeScript", planned: false }],
    selectedId: null,
  };
  const after = coursesReducer(before, courseToggled("ts"));

  expect(before.items[0]?.planned).toBe(false);
  expect(after.items[0]?.planned).toBe(true);
});
```

Test behavior, failure rules, and immutability. Do not test Immer implementation details.

## Test Selectors

```typescript
test("selects planned courses", () => {
  const state = createTestState({
    items: [
      { id: "ts", title: "TypeScript", planned: true },
      { id: "js", title: "JavaScript", planned: false },
    ],
  });
  expect(selectPlannedCourses(state).map((course) => course.id)).toEqual(["ts"]);
});
```

Selector tests are useful for domain derivation, not trivial property access.

## Component Integration Test

```tsx
const renderWithStore = (ui: ReactNode, store = createAppStore()) => {
  return render(<Provider store={store}>{ui}</Provider>);
};

test("plans a course", async () => {
  const user = userEvent.setup();
  renderWithStore(<CoursePage />);
  await user.click(screen.getByRole("button", { name: "Plan TypeScript" }));
  expect(screen.getByRole("button", { name: "Planned TypeScript" }))
    .toHaveAttribute("aria-pressed", "true");
});
```

Test visible behavior. Avoid asserting internal dispatch counts unless dispatch is the public contract under test.

## Test Async Logic

Mock the HTTP boundary with a request mocking tool, create a real test store, dispatch the thunk/query, and assert resulting state or UI.

Do not mock the slice reducer or typed hooks; that removes the integration you need confidence in.

## Redux DevTools

Toolkit enables DevTools in development. Use it to inspect:

- action order and payload
- state diff
- which component event dispatched an action
- thunk/query lifecycle actions
- selector/state shape

Never place secrets or unnecessary personal data in actions/state because DevTools, logs, persistence, and bug reports can expose them.

## Persistence Is a Separate Boundary

Redux memory disappears on reload. Persistence is not automatic.

Persist only state with a product requirement:

- safe user preferences
- an explicit offline draft
- a versioned workflow checkpoint

Do not persist:

- RTK Query cache by default
- loading flags and transient errors
- secrets/tokens
- DOM nodes or class instances
- data that the server should refresh

## Strict Persisted-State Parser

```typescript
type PersistedPreferences = Readonly<{
  version: 1;
  theme: "light" | "dark";
}>;

const parsePreferences = (value: unknown): PersistedPreferences => {
  if (typeof value !== "object" || value === null) {
    throw new TypeError("preferences must be an object");
  }
  if (!("version" in value) || value.version !== 1) {
    throw new TypeError("unsupported preferences version");
  }
  if (!("theme" in value) || (value.theme !== "light" && value.theme !== "dark")) {
    throw new TypeError("invalid theme");
  }
  return { version: 1, theme: value.theme };
};
```

Validation checks; migration transforms. Keep those operations separate and test each version path.

## Load Before Store Creation

```typescript
const loadPreferences = (): PersistedPreferences | undefined => {
  const text = localStorage.getItem("preferences");
  return text === null ? undefined : parsePreferences(JSON.parse(text));
};

const persisted = loadPreferences();
const store = configureStore({
  reducer,
  preloadedState: persisted === undefined
    ? undefined
    : { preferences: persisted },
});
```

If persisted data is invalid, stop or show an explicit recovery decision. Do not silently treat corruption as valid current state.

## Save Narrow State

Listener middleware can save only the changed preference after its action rather than serializing the entire store after every action.

```typescript
startAppListening({
  actionCreator: themeChanged,
  effect: (_action, api) => {
    const preferences = selectPreferences(api.getState());
    localStorage.setItem("preferences", JSON.stringify(preferences));
  },
});
```

Handle quota/security failures in the UI workflow that promises persistence.

## Persistence Stage Choice

| Requirement | Suitable start |
|---|---|
| reload-safe small preference | localStorage with parser/version |
| one-tab temporary draft | sessionStorage |
| large/offline structured data | IndexedDB |
| shareable filter | URL |
| authenticated authority | server session/database |

See the Chrome storage guide for full tradeoffs.

## Production Checklist

- store shape is cohesive and serializable
- actions contain safe minimum data
- reducers fail invalid transitions
- async work has cancellation and error states
- RTK Query owns remote cache
- selectors do not duplicate state
- persistence is narrow, versioned, and validated
- tests use a fresh real store
- DevTools data is safe to expose to developers
- performance is measured before memoization

## Final Rule

Test Redux as observable state and user behavior. Persist only what must survive, and treat persisted data as untrusted input on every load.
