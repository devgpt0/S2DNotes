# Design Systems, Accessibility, and Internationalization

## Idea

A design system is a governed contract of tokens, accessible primitives,
components, patterns, and documentation. Accessibility and internationalization
are architecture requirements, not final visual polish.

## Visual model

```text
design tokens -> accessible primitives -> product components -> applications
       |                |
 themes/platforms   tests/docs/versioning
```

## Design steps

1. Define semantic tokens for color, spacing, typography, motion, and layers.
2. Build primitives with keyboard, focus, semantics, and screen-reader behavior.
3. Compose product patterns without bypassing primitive contracts.
4. Version changes, publish migration guidance, and measure adoption.
5. Externalize messages and support pluralization, locale formats, RTL, and text growth.
6. Test automated rules plus real keyboard/screen-reader workflows.

## When to use it

A shared system pays off when multiple teams/products repeat UI patterns. Start
small with high-frequency primitives; do not create a component for every layout.

## Trade-offs

Consistency and accessibility improve, but governance can slow exceptions.
Allow documented escape hatches and feed valid product needs back into the system.

## Operational model

- Clear component owners and support policy.
- Visual, interaction, accessibility, and cross-browser regression tests.
- Usage telemetry/code search for safe deprecation.
- Token pipelines that keep design and code definitions synchronized.

## Common mistakes

- Treating a component gallery as a design system.
- Adding ARIA instead of using correct native semantics.
- Concatenating translated sentence fragments.
- Hardcoding left/right, fixed text widths, or color-only meaning.
