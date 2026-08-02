# Design a Micro-Frontend Platform

> **Difficulty:** Hard  
> **Main focus:** team boundaries, runtime isolation, shared contracts

## Interview prompt

Design a frontend architecture where independent teams own and deploy parts of one web product.

## 1. Clarify the experience

**What I would say first:** I will first verify that independent ownership and release needs justify micro-frontends. The architecture should follow business boundaries, not split every visual component.

### Functional requirements

- Allow domain teams to build, test, and release independently.
- Provide one coherent navigation, identity, design system, and observability layer.
- Prevent one domain failure from blanking the whole application.
- Control duplicate dependencies and incompatible contracts.

### Browser and product constraints

- Users should experience one application, not stitched websites.
- Runtime composition increases JavaScript and coordination cost.
- Shared state across domains is the main coupling risk.

## 2. State and API contracts

- App shell contract: route, mount element, auth context, locale, telemetry API
- Cross-domain events use versioned schemas; URLs own shareable navigation state
- Backend APIs remain domain-owned rather than one frontend reaching another team's private state

## 3. Frontend architecture

```text
browser
  |
app shell: routing, auth, navigation, errors, telemetry
  |-------------------|-------------------|
catalog frontend   checkout frontend   account frontend
  |                    |                   |
domain API           domain API          domain API
  |
shared design-system package and versioned platform SDK
```

## 4. Critical user flow

1. The shell authenticates, resolves the route, and loads only the owning domain bundle.
2. A domain mounts inside a bounded error and style boundary.
3. The shell passes small stable capabilities, not its internal store.
4. Cross-domain navigation uses URLs or versioned commands.
5. Deployment canaries measure shell and domain errors independently.

## 5. Deep dive

- Route-level composition is easier to isolate than arbitrary component-level composition.
- Share only stable large dependencies; forced singleton versions can block team autonomy.
- Avoid one global state store. The server or URL owns cross-domain durable state.
- Define failure UI, timeout, and rollback for every independently loaded domain.

## 6. Performance, resilience, and observability

- Set per-domain bundle budgets and preload only probable next routes.
- Use dependency reports to detect duplicated frameworks and libraries.
- Contract tests run consumer fixtures against provider changes.
- Track per-domain load, error, INP, rollback, and version compatibility.

## 7. Security and accessibility

- The shell owns security headers and trusted identity; domains receive minimum capabilities.
- Do not load unreviewed remote code from arbitrary origins.
- Preserve one focus order, landmark structure, language, and design-system accessibility contract.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Monolith frontend | Simple runtime and refactoring, coordinated team releases. |
| Micro-frontends | Independent ownership with runtime and governance cost. |
| Build-time composition | Safer optimization but less independent deployment. |
| Runtime composition | Maximum autonomy with loading and compatibility risk. |

## 9. 60-second interview summary

I use route-level micro-frontends only at stable business boundaries. A thin shell owns routing, identity, errors, telemetry, and accessibility; domains own their APIs and releases. Versioned contracts, bundle budgets, canaries, and isolation contain the added complexity.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

