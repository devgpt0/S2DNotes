# Micro-Frontends and Team Boundaries

## Idea

Micro-frontends let teams independently own and deliver parts of a frontend.
They solve organizational scaling problems, not ordinary component reuse.

## Visual model

```text
shell: routing, identity, navigation, shared contracts
  +-> domain A frontend (owned/released by team A)
  +-> domain B frontend (owned/released by team B)
```

## Design steps

1. Prove independent ownership/release is worth the runtime complexity.
2. Split by user/business domain, not arbitrary page sections.
3. Choose build-time packages, server composition, or runtime loading.
4. Define routing, authentication, design tokens, events, and dependency rules.
5. Isolate failures and enforce performance budgets per domain.
6. Provide contract tests, local integration, canary releases, and rollback.

## When to use it

Use it for several autonomous teams with stable domain boundaries and conflicting
release needs. Prefer a modular frontend for one or a few closely coordinated teams.

## Trade-offs

Independent delivery increases autonomy but duplicates dependencies, fragments
UX, complicates routing/state, and makes end-to-end debugging harder.

## Integration rules

- Share narrow contracts, not mutable global stores.
- Version shared libraries and avoid forced lockstep upgrades.
- Let the shell own global navigation/error boundaries, not domain business logic.
- Trace one user action across fragments and backend services.

## Common mistakes

- Multiple frameworks only because teams prefer them.
- Runtime integration for components that could be build-time packages.
- One global event bus with undocumented messages.
- No owner for cross-domain performance and accessibility.
