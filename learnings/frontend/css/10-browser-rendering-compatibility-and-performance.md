# 10 - Browser Rendering, Compatibility, Performance, and DevTools

## Rendering Pipeline

```text
style calculation -> layout -> paint -> compositing
# Result: CSS changes may affect one or several rendering stages.
```

- style: determine computed rules
- layout: calculate sizes and positions
- paint: draw pixels into layers
- composite: combine layers on screen

## Avoid Layout Thrashing

JavaScript that repeatedly writes style and then reads layout can force synchronous layout.

```javascript
const width = panel.getBoundingClientRect().width;
panel.style.width = `${width + 10}px`;
console.log(panel.style.width);
// Console output: previous rendered width plus 10px, such as "310px".
```

Batch reads, then writes. Prefer classes and CSS for visual state.

## Selector Performance

Most normal selectors are fast enough. Prioritize maintainability, small CSS, and fewer unused rules before micro-optimizing selectors. Avoid huge DOM trees and selectors that encode deep structure.

## Browser Compatibility

- check MDN and Can I Use support data
- define supported browser versions from real users/product needs
- use progressive enhancement
- use Autoprefixer through the build pipeline when needed
- test rendering and interaction, not just syntax support
- provide fallback only when the experience would otherwise break

```css
.title { color: #3857d6; color: oklch(50% .2 265); }
/* Browser result: older browser uses hex; supporting browser uses the later OKLCH value. */
```

## Containment and Content Visibility

```css
.offscreen-section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}
/* Browser result: browser may skip off-screen rendering while reserving estimated space. */
```

Measure before using containment; it can affect sizing, positioning, and accessibility/browser behavior.

## DevTools Workflow

1. Inspect the element and matched/computed CSS.
2. Toggle declarations instead of editing blindly.
3. Enable Grid/Flex overlays.
4. Emulate viewport, touch, color scheme, and reduced motion.
5. Record Performance and identify long layout/paint tasks.
6. Check rendering tools for paint flashing/layout shifts.
7. Test Network throttling and Coverage.

## Optimization Order

Correct semantics/accessibility -> responsive layout -> reduce bytes/requests -> optimize critical rendering -> measure layout/paint -> apply targeted improvements.

Never sacrifice readable code or accessibility for an unmeasured micro-optimization.
