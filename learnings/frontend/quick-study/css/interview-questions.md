# CSS: 10 most-asked interview questions

## 1. Explain the CSS box model.

From inside out it is content, padding, border, and margin. With the default `content-box`, width covers only content. With `border-box`, width includes content, padding, and border, which makes layout sizing predictable.

## 2. How does the cascade choose a winning declaration?

It considers relevance, origin/importance, cascade layer, specificity, scoping proximity, then source order. In ordinary author CSS, a more specific selector wins; equal specificity is resolved by the later declaration.

## 3. What is specificity?

Specificity is a selector’s priority weight: IDs outweigh classes/attributes/pseudo-classes, which outweigh elements/pseudo-elements. Inline styles are stronger than ordinary stylesheet rules. Keep specificity low and avoid `!important` battles.

## 4. Flexbox versus Grid: when do you use each?

Flexbox is ideal for one-dimensional alignment along a row or column. Grid controls rows and columns together. They complement each other: Grid can define a page/card layout while Flexbox aligns content inside a component.

## 5. Explain `relative`, `absolute`, `fixed`, and `sticky`.

Relative stays in normal flow and can anchor absolute descendants. Absolute leaves normal flow and uses the nearest positioned ancestor. Fixed normally uses the viewport. Sticky stays in flow until a threshold, then sticks within its scrolling/container limits.

## 6. Why does `z-index` sometimes not work?

`z-index` compares items within a stacking context. Properties such as transforms, opacity, and positioned elements with z-index can create new contexts. A child cannot out-rank elements outside its parent’s context merely by using a huge number.

## 7. What is responsive design?

It lets content adapt to available space and user preferences using fluid sizing, flexible layouts, responsive media, and media/container queries. Breakpoints should follow content needs, not named device models.

## 8. What is the difference between pseudo-class and pseudo-element?

A pseudo-class selects a state or structural condition, such as `:hover` or `:first-child`. A pseudo-element selects a generated or conceptual part, such as `::before` or `::first-line`.

## 9. How do you make CSS maintainable?

Use predictable component classes, low-specificity selectors, tokens/custom properties, clear ownership, normal flow, and a small number of documented layers. Remove dead rules and test long text, zoom, focus, and responsive states.

## 10. How do you improve CSS rendering performance?

Measure first. Keep stylesheets and selectors reasonable, avoid layout-heavy animation, and animate `transform`/`opacity` when possible. Reduce unused CSS and repeated DOM style changes; do not trade readability for unmeasured micro-optimizations.
