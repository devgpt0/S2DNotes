# Design a Design System and Component Library

> **Difficulty:** Medium  
> **Main focus:** tokens, accessibility, versioning

## Interview prompt

Design a frontend platform used by many product teams for consistent accessible UI.

## 1. Clarify the experience

**What I would say first:** A design system is a product with contracts, governance, testing, and migration support—not only a component package.

### Functional requirements

- Provide design tokens, primitives, composed components, icons, and guidance.
- Support themes, responsiveness, internationalization, and accessibility.
- Release independently with safe upgrades and deprecations.
- Allow product variation without arbitrary forks.

### Browser and product constraints

- Many applications and framework versions consume the system.
- Visual regressions have a wide blast radius.
- Public component APIs become long-lived contracts.

## 2. State and API contracts

- Token package: semantic names such as color.text.danger, not raw brand values
- Component APIs define controlled/uncontrolled state, events, slots, and accessibility behavior
- Versioned package registry plus machine-readable migration metadata

## 3. Frontend architecture

```text
design source -> token pipeline -> platform token packages
                    |
component source -> primitives -> composed components -> package registry
                    |                |
                    +-> docs/examples +-> unit/a11y/visual/browser tests
                                             |
product apps <- versioned releases <- codemods/migration guides
```

## 4. Critical user flow

1. Design and engineering agree on semantic token intent and component behavior.
2. Generate platform-specific tokens from one validated source.
3. Build accessible unstyled primitives, then branded composed components.
4. Test behavior, keyboard use, screen readers, visual states, themes, and locales.
5. Release with changelog, compatibility range, migration guide, and staged adoption.

## 5. Deep dive

- Prefer composition and documented escape hatches over dozens of boolean props.
- Tokens separate semantic intent from theme values and make brand changes tractable.
- Breaking changes require a major version or an automated migration path.
- Adoption metrics, support issues, and accessibility defects guide the roadmap.

## 6. Performance, resilience, and observability

- Publish tree-shakeable modules and avoid hidden global CSS or large runtime styling costs.
- Run visual tests on a deliberate state matrix rather than every possible product page.
- Use prereleases and canary applications before stable promotion.
- Track bundle contribution, version fragmentation, adoption, regressions, and accessibility violations.

## 7. Security and accessibility

- Secure the package publication pipeline and sign or provenance-check releases.
- Components escape unsafe content by default and avoid dangerous HTML APIs.
- Keyboard, focus, contrast, zoom, reduced motion, and screen-reader behavior are acceptance criteria.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Highly configurable components | Flexible but complex APIs and inconsistent products. |
| Opinionated components | Consistent and accessible but need intentional escape hatches. |
| One forced version | Low fragmentation but difficult coordinated upgrades. |
| Versioned packages | Team autonomy with migration support cost. |

## 9. 60-second interview summary

I build semantic tokens, accessible primitives, and opinionated composed components as versioned contracts. Automated behavioral, visual, accessibility, and browser testing protects releases, while codemods and governance reduce forks and version fragmentation.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

