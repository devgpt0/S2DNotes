# CSS interview MCQs with explanations

Answer each question before reading the explanation.

## 1. Which selector normally has the highest specificity?

- A. `p`
- B. `.note`
- C. `#note`
- D. `*`

**Answer: C — `#note`.** An ID selector outweighs class and element selectors. Prefer classes for normal styling so rules remain easy to override.

## 2. If two matching declarations have equal specificity, which wins?

- A. The first declaration
- B. The later declaration
- C. The shorter declaration
- D. The inherited declaration

**Answer: B — The later declaration.** Source order is the final tie-breaker after cascade origin, layer, importance, and specificity are equal.

## 3. What does `box-sizing: border-box` include in a declared width?

- A. Margin only
- B. Content only
- C. Content, padding, and border
- D. Padding and margin

**Answer: C — Content, padding, and border.** Margin remains outside the declared width. `border-box` makes component sizing more predictable.

## 4. Which box-model area lies outside the border?

- A. Content
- B. Padding
- C. Margin
- D. Background

**Answer: C — Margin.** From inside outward, the order is content, padding, border, and margin.

## 5. Which unit is relative to the root font size?

- A. `em`
- B. `rem`
- C. `vw`
- D. `px`

**Answer: B — `rem`.** `rem` uses the root element's font size. `em` depends on the current element's font size for most properties.

## 6. Which layout mode is best suited to a one-dimensional toolbar?

- A. Grid
- B. Flexbox
- C. Table layout
- D. Inline layout

**Answer: B — Flexbox.** Flexbox arranges and aligns items along one primary row or column, which matches most toolbar layouts.

## 7. Which layout mode controls rows and columns together?

- A. Grid
- B. Block
- C. Inline
- D. Float

**Answer: A — Grid.** Grid is two-dimensional and provides explicit row and column tracks. Flexbox focuses on one dimension at a time.

## 8. In a row flex container, which axis does `justify-content` control?

- A. Cross axis
- B. Main axis
- C. Stacking axis
- D. Block axis only

**Answer: B — Main axis.** With the default `flex-direction: row`, the main axis is horizontal. Changing flex direction also changes which physical direction is the main axis.

## 9. In a row flex container, which axis does `align-items` control?

- A. Main axis
- B. Cross axis
- C. Stacking axis
- D. Inline axis only

**Answer: B — Cross axis.** In a row, this normally means vertical alignment. Always reason from flex direction rather than memorizing horizontal versus vertical.

## 10. What does `gap` add?

- A. Space between layout items
- B. Margin outside the container
- C. Border width
- D. Text indentation

**Answer: A — Space between items.** Unlike child margins, gap does not add unwanted space around the outer edges of the collection.

## 11. An absolutely positioned element is normally positioned against what?

- A. Always the viewport
- B. Its nearest positioned ancestor
- C. Its next sibling
- D. The root font size

**Answer: B — Its nearest positioned ancestor.** If no qualifying ancestor exists, its containing block is usually the initial containing block.

## 12. A fixed element is normally positioned against what?

- A. Parent content
- B. The viewport
- C. A grid row
- D. The text baseline

**Answer: B — The viewport.** It stays at the same viewport position while the document scrolls, although certain transformed ancestors can change its containing block.

## 13. What does a sticky element need to visibly stick?

- A. A threshold such as `top: 0`
- B. `z-index: -1`
- C. `display: inline`
- D. `float: left`

**Answer: A — An inset threshold.** Without `top`, `bottom`, or a logical inset, the browser has no point at which sticky behavior should begin.

## 14. Why can a very large `z-index` still appear below another element?

- A. Large numbers are invalid
- B. The elements are in different stacking contexts
- C. Flexbox ignores z-index
- D. It requires `!important`

**Answer: B — Different stacking contexts.** A child's z-index is compared inside its own context and cannot escape the ordering of that context's parent.

## 15. Which property normally inherits from a parent?

- A. `margin`
- B. `border`
- C. `color`
- D. `width`

**Answer: C — `color`.** Many text-related properties inherit. Most box and layout properties do not.

## 16. What does `:focus-visible` select?

- A. Mouse clicks only
- B. Focus when a visible indicator is appropriate
- C. Disabled controls
- D. Hovered elements

**Answer: B — Focus needing an indicator.** Browsers commonly match it for keyboard focus, allowing strong keyboard feedback without always showing a ring after pointer interaction.

## 17. What is `::before`?

- A. A pseudo-class
- B. A pseudo-element
- C. A media query
- D. A combinator

**Answer: B — A pseudo-element.** It creates a styleable generated box before an element's content. Essential information should remain in real HTML.

## 18. How much specificity does `:where(...)` add?

- A. Zero
- B. One class
- C. One ID
- D. The specificity of its most specific argument

**Answer: A — Zero.** This makes `:where()` useful for defaults that consumers can override easily.

## 19. Which declaration creates responsive columns without a media query?

- A. `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr))`
- B. `position: fixed`
- C. `float: left`
- D. `white-space: nowrap`

**Answer: A — `repeat(auto-fit, minmax(...))`.** Grid creates as many minimum-sized columns as fit and lets them share remaining space.

## 20. What does `clamp(minimum, preferred, maximum)` do?

- A. Clips overflowing content
- B. Keeps a fluid value within limits
- C. Creates a grid
- D. Crops an image

**Answer: B — It bounds a fluid value.** The preferred value can respond to the viewport while the minimum and maximum prevent unusable extremes.

## 21. What does a container query respond to?

- A. Device brand
- B. The component container's size
- C. Network speed
- D. DOM depth

**Answer: B — Container size.** This lets a reusable component adapt to where it is placed instead of only to the viewport.

## 22. Which property is generally cheapest to animate?

- A. `width`
- B. `top`
- C. `transform`
- D. `grid-template-columns`

**Answer: C — `transform`.** Transforms and opacity can often be composited without recalculating document layout on every frame.

## 23. Why should `transition: all` usually be avoided?

- A. It is invalid CSS
- B. It can animate unintended or expensive properties
- C. It disables hover
- D. It prevents easing

**Answer: B — It is too broad.** Naming the intended property documents behavior and avoids accidental layout animation after future style changes.

## 24. Which media feature respects a user's reduced-motion preference?

- A. `prefers-color-scheme`
- B. `prefers-reduced-motion`
- C. `orientation`
- D. `hover`

**Answer: B — `prefers-reduced-motion`.** Use it to remove or simplify nonessential movement for users who can be harmed or distracted by animation.

## 25. What often fixes a flex child that refuses to shrink around long content?

- A. `min-width: 0`
- B. `width: 100vw`
- C. `position: absolute`
- D. `z-index: 1`

**Answer: A — `min-width: 0`.** Flex items default to an automatic minimum based on their content, which may prevent shrinking and cause overflow.

## 26. What is a CSS custom property?

- A. A Sass-only variable
- B. A cascading value such as `--color-brand`
- C. An HTML attribute
- D. A browser extension

**Answer: B — A cascading custom value.** It can inherit, vary by selector or theme, and be read with `var(--color-brand)`.

## 27. What does `overflow: auto` do?

- A. Always clips content
- B. Adds scrolling when needed
- C. Expands the viewport
- D. Hides the entire element

**Answer: B — It adds conditional scrolling.** Scrollbars appear when content exceeds the box instead of being shown unconditionally.

## 28. What is the usual mobile-first approach?

- A. Use only `max-width` queries
- B. Write narrow-screen defaults, then add `min-width` enhancements
- C. Detect device models in JavaScript
- D. Use fixed-width layouts

**Answer: B — Start narrow and enhance.** This gives small screens a simple default and introduces layout complexity only when enough space is available.

## 29. Which approach best supports maintainable CSS?

- A. Deep ID selector chains
- B. Many `!important` declarations
- C. Shallow component-focused classes
- D. Inline styles everywhere

**Answer: C — Shallow component classes.** They keep ownership clear and specificity predictable without tightly coupling CSS to the document hierarchy.

## 30. Why must focus indicators remain visible?

- A. They improve SEO
- B. Keyboard users need to know which control is active
- C. They load images
- D. They improve CSS parsing

**Answer: B — They show keyboard position.** Removing outlines without an equally visible replacement makes keyboard navigation confusing or unusable.
