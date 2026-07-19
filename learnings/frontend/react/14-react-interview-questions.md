# 14 - Most-Asked React Interview Questions with Answers

1. **What is React?** A library for deriving component UI trees from props/state and committing DOM changes.
2. **Virtual DOM?** In-memory element representation React compares/reconciles; performance comes from scheduling/batching/targeted commits, not the phrase alone.
3. **Props vs state?** Parent-provided read-only input vs component-owned memory.
4. **Why immutable updates?** New identities make changes predictable and support memoization/concurrent rendering.
5. **State snapshot?** Each render/handler closes over values from that render.
6. **Batching?** React groups updates to avoid unnecessary intermediate renders.
7. **Why functional setter?** Computes from latest queued prior state.
8. **Key purpose?** Stable sibling identity for reconciliation/state preservation.
9. **Why not index/random key?** Index breaks identity during reorder; random remounts every render.
10. **Controlled vs uncontrolled?** React state owns current value vs DOM owns it and code reads on demand.
11. **What is effect?** Post-commit synchronization with an external system.
12. **Effect cleanup?** Undo subscription/timer/request/widget work before rerun/unmount.
13. **Dependency array?** Reactive values used by effect determine when synchronization must rerun.
14. **useEffect vs useLayoutEffect?** After paint vs synchronous before paint for measurement correction.
15. **Ref vs state?** Stable mutable non-render value/DOM handle vs render-driving memory.
16. **Context downside?** Broad implicit dependency and rerenders when provider value changes.
17. **Reducer use?** Centralize complex related state transitions in a pure function.
18. **Custom hook?** Reusable stateful logic composition; each call has its own state.
19. **Rules of hooks?** Top-level stable order in React components/hooks.
20. **memo/useMemo/useCallback?** Skip component render, cache calculation, stabilize callback—only with measured benefit.
21. **Suspense?** Boundary fallback for compatible pending code/data resource.
22. **Transition?** Marks non-urgent update so urgent interaction stays responsive.
23. **useOptimistic?** Temporary optimistic state while action completes, requiring reconciliation.
24. **Error boundary?** Catches descendant render/lifecycle failure and provides fallback.
25. **Portal?** DOM placement elsewhere while preserving React tree context/event relationships.
26. **Hydration?** Attach React behavior to server-rendered HTML; output must match.
27. **Server vs Client Component?** Server-rendered no-client-implementation component vs interactive browser boundary in supporting framework.
28. **React security?** Escaped text by default; unsafe HTML/URLs, client auth assumptions, API data, dependencies remain risks.
29. **Testing approach?** User-observable behavior with accessible queries and realistic boundaries.
30. **Performance approach?** Profile first; fix ownership/context/expensive render/DOM/network before blanket memoization.

## Common Coding Prompt

Build a searchable list with controlled input, derived filtered results, stable keys, empty state, and accessible result count. Explain why filtered results are derived rather than synchronized through an effect.
