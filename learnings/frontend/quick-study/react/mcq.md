# React interview MCQs with explanations

Answer each question before reading the explanation.

## 1. What is a React component commonly written as?

- A. A SQL query
- B. A function that returns UI
- C. A CSS selector
- D. An HTTP server

**Answer: B — A function that returns UI.** A component receives props and returns React elements, usually written with JSX, describing what should appear.

## 2. How should props be treated?

- A. As mutable global values
- B. As read-only inputs
- C. As browser storage
- D. As DOM nodes

**Answer: B — Read-only inputs.** The parent owns the values. A child requests changes through callbacks instead of modifying its props.

## 3. What is React state?

- A. Static CSS
- B. Data that changes over time and affects UI
- C. Server data only
- D. Another name for props

**Answer: B — Changing component data.** Updating state asks React to render a new UI snapshot based on the new value.

## 4. What happens when a state setter is called?

- A. The current render's variable changes immediately
- B. React schedules another render
- C. The browser reloads
- D. Props are mutated

**Answer: B — React schedules a render.** The current event handler still sees its existing state snapshot; the new value appears in a later render.

## 5. Which form should be used when new state depends on previous state?

- A. Direct mutation
- B. A functional updater
- C. A global variable
- D. A ref only

**Answer: B — A functional updater.** `setCount(current => current + 1)` receives the latest queued value and remains correct when React batches several updates.

## 6. Why should React state be updated immutably?

- A. React relies on predictable snapshots and new references
- B. JavaScript cannot mutate objects
- C. The DOM requires JSON
- D. CSS requires immutable values

**Answer: A — Predictable snapshots and identity.** Mutation can corrupt past render data and keep the same reference, making changes harder for React and memoized components to detect.

## 7. Which special prop identifies list items across renders?

- A. `id` automatically
- B. `key`
- C. `className`
- D. `index`

**Answer: B — `key`.** React uses keys to match each previous child with its next version during reconciliation.

## 8. What is the best key for a list that can be reordered?

- A. A random number created during render
- B. The array index
- C. A stable ID from the data
- D. The item's current position

**Answer: C — A stable data ID.** It follows the same logical item across reordering. Index and random keys can attach state to the wrong item or reset it.

## 9. Where should a list key be placed?

- A. Inside child state
- B. On the top-level element returned by `map`
- C. On every descendant
- D. In CSS

**Answer: B — On the mapped element.** The parent list needs the key where it compares siblings; placing it deeper does not identify that sibling entry.

## 10. What is an effect intended for?

- A. Calculating every derived value
- B. Synchronizing with an external system
- C. Returning JSX
- D. Declaring props

**Answer: B — External synchronization.** Examples include subscriptions, timers, network work, or imperative browser APIs. Pure calculations belong during render.

## 11. When do effects normally run?

- A. During pure rendering
- B. After React commits UI changes
- C. Before the component function
- D. Only on a server

**Answer: B — After the commit.** Keeping effects after rendering allows component render functions to remain pure and restartable.

## 12. What should a subscribing effect return?

- A. JSX
- B. A cleanup function
- C. A Promise
- D. State

**Answer: B — A cleanup function.** Cleanup removes the previous subscription before rerunning and when the component unmounts, preventing duplicate listeners and leaks.

## 13. What does an empty effect dependency array usually mean?

- A. Run after every render
- B. Run after mount, then clean up on unmount
- C. Never run
- D. Track all values automatically

**Answer: B — One setup for that mount.** In development Strict Mode, React may deliberately perform an extra setup/cleanup cycle to detect unsafe effects.

## 14. Where should filtered data derived only from props and state usually be calculated?

- A. In duplicate state
- B. During render
- C. In an effect
- D. In a global variable

**Answer: B — During render.** Duplicate derived state can become stale and creates an unnecessary extra render. Memoize only if the calculation is genuinely expensive.

## 15. What does “lifting state up” mean?

- A. Move state to the nearest shared parent
- B. Move state into the DOM
- C. Put all state in Context
- D. Persist all state

**Answer: A — Move it to the common owner.** The parent can pass a consistent value and update callbacks to every child that needs it.

## 16. Where does a controlled input get its current value?

- A. Only from the browser
- B. From React state or props
- C. From CSS
- D. Only from the URL

**Answer: B — React data.** The input receives `value` or `checked`, while an event handler updates the source of truth.

## 17. What does changing `ref.current` normally cause?

- A. A rerender
- B. No rerender
- C. A component remount
- D. A page reload

**Answer: B — No rerender.** A ref stores mutable information across renders. Use state instead when changing the value must update visible UI.

## 18. What is Context best suited for?

- A. Every local Boolean
- B. Values needed throughout a component subtree
- C. DOM animation only
- D. Fetching only

**Answer: B — Broadly shared values.** Theme, locale, or authenticated-user information are common examples. Local state should usually remain local.

## 19. What does a custom hook share?

- A. One global state instance
- B. Reusable stateful logic
- C. JSX only
- D. CSS

**Answer: B — Reusable hook logic.** Each call receives its own state; custom hooks do not automatically share one state value between components.

## 20. When is `useReducer` particularly useful?

- A. When there is no state
- B. When related transitions benefit from explicit actions
- C. For styling
- D. For every counter

**Answer: B — Complex related transitions.** A reducer centralizes how actions move state from one valid shape to another and is easy to test as a pure function.

## 21. Where may hooks be called?

- A. Inside any loop
- B. At the top level of a component or custom hook
- C. Only inside event handlers
- D. Inside class methods

**Answer: B — At the top level.** React relies on calls occurring in the same order on every render to associate each hook with its state.

## 22. Why must hooks not be called conditionally?

- A. React relies on stable hook call order
- B. Conditions are too slow
- C. TypeScript forbids all conditions
- D. JSX cannot contain branches

**Answer: A — Hook order identifies state.** If a conditional call appears or disappears, every later hook could be matched with the wrong stored state.

## 23. What does `memo` attempt to skip?

- A. A network request
- B. A child render when its props are unchanged
- C. A state update
- D. Effect cleanup

**Answer: B — A render with unchanged props.** It is a performance optimization and does not stop renders caused by the component's own state or consumed context.

## 24. When should memoization usually be introduced?

- A. Everywhere by default
- B. After measuring a real problem or when identity is required
- C. Before correctness
- D. Only for strings

**Answer: B — When evidence justifies it.** Memoization has code and comparison costs, and new object or function dependencies can make it ineffective.

## 25. When does React normally preserve a component's state?

- A. While the same component type remains at the same tree position
- B. While its variable name stays the same
- C. While its CSS stays the same
- D. While it remains in the same file

**Answer: A — Same type and tree position.** React associates state with a place in the rendered tree, not with the source-code variable name.

## 26. How can a parent intentionally reset a child's state?

- A. Change the child's `key`
- B. Mutate its props
- C. Call the component as a normal function
- D. Remove Strict Mode

**Answer: A — Change its key.** React then treats it as a different component identity, unmounting the old instance and mounting a fresh one.

## 27. What do Strict Mode's extra development checks help reveal?

- A. CSS syntax mistakes
- B. Impure rendering and missing effect cleanup
- C. Database schema errors
- D. Type errors only

**Answer: B — Purity and cleanup bugs.** Extra render and effect cycles expose code that incorrectly depends on running only once. These checks are development-only.

## 28. What do error boundaries catch?

- A. Every asynchronous failure
- B. Rendering errors in descendant components
- C. Every event-handler error
- D. HTTP error responses automatically

**Answer: B — Descendant rendering errors.** They display fallback UI for render lifecycle failures, but ordinary event or asynchronous errors need their own handling.

## 29. How does React handle text inserted with JSX expressions?

- A. It parses the text as raw HTML
- B. It escapes the text by default
- C. It executes the text as JavaScript
- D. It removes every HTML character

**Answer: B — It escapes text.** This prevents ordinary string values from becoming markup. `dangerouslySetInnerHTML` bypasses this protection and requires trusted, sanitized HTML.

## 30. What is the best style for testing React UI?

- A. Assert private component state
- B. Query and interact as a user would
- C. Count hook calls
- D. Use snapshots for every behavior

**Answer: B — Test observable behavior.** Queries by accessible role and name make tests reflect real use and remain stable when implementation details change.
