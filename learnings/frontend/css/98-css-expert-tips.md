# CSS Expert Tips and Browser Optimization Playbook

## Cascade and Architecture

- Keep specificity low; design layers before adding stronger selectors.
- Put third-party CSS in an early layer so application rules can override it cleanly.
- Use `:where()` for zero-specificity defaults.
- Avoid IDs and DOM-depth selectors in reusable components.
- Prefer component ownership over a giant global override file.
- Tokens name design decisions; utilities express focused exceptions.
- Remove dead CSS through measured production coverage, not guesses.

## Layout Tricks

- Apply `box-sizing: border-box` universally.
- Use `minmax(0, 1fr)` for tracks that must shrink below content's automatic minimum.
- Set `min-inline-size: 0` on overflowing flex/grid children.
- Use `repeat(auto-fit, minmax(min(100%, X), 1fr))` for robust intrinsic card grids.
- Use `gap` instead of child margins for layout spacing.
- Prefer `margin-inline: auto` and logical properties for international layouts.
- Avoid fixed heights around text; use minimum height only when necessary.
- Sticky positioning depends on scroll container, inset, and available travel space.
- Diagnose z-index through stacking contexts, not larger numbers.

## Responsive Expert Habits

- Begin at 320px but test continuously, not only named breakpoints.
- Add a breakpoint where content fails, then choose the nearest maintainable token.
- Container queries make reusable components independent of page viewport.
- Test 200% zoom, large text, landscape, soft keyboard, and browser UI changes.
- Stress-test long words, translations, empty/huge lists, and missing images.
- Use `dvh` only when dynamic viewport behavior is desired; understand `svh/lvh` alternatives.
- Respect safe-area insets for edge-to-edge mobile UI where applicable.
- Never solve mobile design by removing essential actions/content.

## Typography and Color

- Use `rem` for scalable type/spacing and `ch` for readable line length.
- Use `clamp()` for bounded fluid values, not uncontrolled viewport scaling.
- Subset fonts, minimize weights, and choose `font-display` from product needs.
- Avoid layout shifts from late font metric changes; consider metric overrides/fallback tuning.
- Build colors in OKLCH for perceptual consistency, with support/fallback strategy.
- Measure contrast for normal, hover, focus, disabled, dark, forced-color, and high-contrast states.
- Do not use color alone to communicate status.

## Animation and Rendering

- Prefer transform/opacity for smooth visual movement when semantically suitable.
- `will-change` is a temporary measured hint, not a global optimization.
- Animate only exact properties, never `transition: all` by habit.
- Respect reduced motion and provide pause/stop controls.
- Use DevTools paint flashing, layer view, and performance traces.
- Batch DOM reads and writes to prevent forced synchronous layout.
- Large shadows, filters, blurs, masks, and fixed backgrounds can be paint-expensive on mobile GPUs.

## Compatibility

- Use progressive enhancement: useful baseline first, enhancement inside support checks when needed.
- Check MDN/Can I Use plus real target-browser tests.
- Let Browserslist/Autoprefixer match the product support policy.
- A parser fallback works when an older browser ignores a later unsupported declaration.
- Feature support does not guarantee identical accessibility, printing, or edge-case behavior.

## CSS Performance Priorities

1. Reduce critical CSS and render-blocking delivery.
2. Remove unused framework/component output.
3. Optimize images/fonts before selector micro-optimization.
4. Limit DOM size and expensive visual effects.
5. Prevent layout shifts with dimensions and stable content.
6. Measure style/layout/paint on representative mobile hardware.

## Expert DevTools Checklist

Inspect matched and computed styles, box-model diagram, Grid/Flex overlays, scroll containers, stacking contexts, accessibility tree, media emulation, coverage, performance trace, layout-shift regions, paint flashing, and network priority/cache behavior.

## Expert Code Snippets Used in Production

### Low-Specificity Component Defaults

```css
@layer reset, base, components, utilities;
@layer components {
  :where(.button) { border: 0; border-radius: .5rem; padding: .625rem 1rem; font: inherit; }
  :where(.button:focus-visible) { outline: .2rem solid Highlight; outline-offset: .2rem; }
}
/* Browser result: reusable button defaults remain easy to override because :where() adds zero specificity. */
```

### Intrinsic Grid That Cannot Overflow

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr));
  gap: clamp(.75rem, 2vw, 1.5rem);
}
/* Browser result: cards automatically wrap and fall back to one safe column narrower than 17rem. */
```

### Component Query with Fallback

```css
.media-card { display: grid; gap: 1rem; }
@supports (container-type: inline-size) {
  .media-card-wrapper { container-type: inline-size; }
  @container (min-width: 30rem) { .media-card { grid-template-columns: 10rem minmax(0, 1fr); } }
}
/* Browser result: stacked fallback; supporting browsers enhance the card when its container is wide enough. */
```

### Accessible Visually Hidden Utility

```css
.visually-hidden:not(:focus):not(:active) {
  position: absolute;
  inline-size: 1px; block-size: 1px;
  overflow: hidden; clip-path: inset(50%);
  white-space: nowrap;
}
/* Accessibility result: text remains available to assistive tech; focusable skip links become visible when focused. */
```

### Stable Scrollbar and Scroll Container

```css
html { scrollbar-gutter: stable; }
.table-scroll { overflow: auto; overscroll-behavior: contain; max-block-size: 70dvh; }
/* Browser result: reduced width shift when scrollbar appears and contained table scrolling. */
```

## High-Use Responsive Component Pattern

```css
.card-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); gap: var(--space-4, 1rem); }
.card { container-type: inline-size; display: flex; flex-direction: column; padding: var(--card-space, 1rem); border: 1px solid var(--border); border-radius: var(--radius, 0.75rem); }
.card__content { display: grid; gap: 1rem; min-inline-size: 0; }
.card__action { margin-block-start: auto; }
@container (min-width: 24rem) { .card__content { grid-template-columns: auto minmax(0, 1fr); } }
/* Result: reusable cards fit any parent, accept token overrides, align actions, and do not overflow narrow containers. */
```

This pattern is extendable through custom properties and composition. Add variants with explicit data attributes, not selectors tied to page position.
