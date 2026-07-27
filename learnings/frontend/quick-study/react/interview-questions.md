# React: 10 most-asked interview questions

## 1. What is the difference between props and state?

Props are read-only inputs passed by a parent. State belongs to a component instance and changes through a setter/reducer, causing React to render again. Shared state should live at the nearest common owner.

## 2. Why should React state be immutable?

Each render uses a state snapshot, and React uses identity changes to detect work and support predictable rendering. Mutating an existing object can preserve its reference, corrupt past snapshots, and make updates or memoization fail.

## 3. What is reconciliation, and why are keys important?

React compares the new element tree with the previous one to update the DOM. Keys identify sibling list items across inserts, removals, and reorders. Stable domain IDs preserve the right component state; index/random keys can mismatch or reset it.

## 4. What is `useEffect` for?

It synchronizes a committed React component with something outside React: subscriptions, timers, network work, or imperative browser APIs. It is not for ordinary derived calculations or code caused directly by one user event.

## 5. How does the effect dependency array work?

Every reactive value read by an effect belongs in its dependency list. React reruns setup when one changes and runs the previous cleanup first. Missing dependencies produce stale closures; restructuring is better than disabling the lint rule.

## 6. Controlled versus uncontrolled components?

A controlled input receives its current value from React and reports changes through an event, enabling validation and coordination. An uncontrolled input keeps its value in the DOM and is read through a ref or form submission; it can suit simple forms.

## 7. `useMemo`, `useCallback`, and `memo`?

`useMemo` caches a calculated value, `useCallback` caches a function identity, and `memo` may skip rendering when props are unchanged. They are performance tools, not correctness tools, and their overhead is justified only by measurement or a known identity requirement.

## 8. Context versus state management library?

Context transports a value through a subtree and is good for relatively stable global concerns. It does not automatically provide normalized updates, selectors, caching, or server-state behavior. Choose a library only when application needs justify those capabilities.

## 9. What are the Rules of Hooks?

Call hooks only at the top level of React components or custom hooks. Never call them conditionally, in loops, or ordinary functions. React associates hook state by consistent call order.

## 10. How do you prevent unnecessary renders?

First profile. Keep state local, avoid unnecessary effects, derive values during render, split components, and stabilize props only where a measured child benefits. A parent render normally calls children; that is not automatically a performance problem.
