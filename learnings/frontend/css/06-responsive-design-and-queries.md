# 06 - Responsive Design and Queries

Responsive design adapts to available space, user preferences, input method, and content—not just a list of phone models.

## Mobile-First CSS

Write the small layout first, then add enhancements when space is available.

```css
.layout { display: grid; gap: 1rem; }

@media (min-width: 48rem) {
  .layout { grid-template-columns: 16rem minmax(0, 1fr); }
}
/* Browser result: one column on narrow screens, sidebar + content from 48rem upward. */
```

Use breakpoints where content becomes uncomfortable, not because a popular device has that width.

## Fluid Before Breakpoints

```css
.page { width: min(100% - 2rem, 75rem); margin-inline: auto; }
.cards { grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); }
/* Browser result: fluid page and cards need fewer breakpoint-specific rules. */
```

## Container Queries

Media queries inspect viewport/environment. Container queries let a component respond to its own available width.

```css
.card-wrapper { container-type: inline-size; }
.card { display: grid; gap: 1rem; }

@container (min-width: 32rem) {
  .card { grid-template-columns: 10rem 1fr; }
}
/* Browser result: card becomes two columns only when its container is at least 32rem. */
```

## User Preferences

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important; }
}
@media (prefers-color-scheme: dark) {
  :root { --surface: #121212; --text: #f5f5f5; }
}
/* Browser result: respects reduced-motion and dark-theme OS/browser preferences. */
```

Also consider `prefers-contrast`, `forced-colors`, hover capability, and pointer accuracy.

## Responsive Checklist

- test 320 CSS px through large desktops, including landscape
- zoom to 200% and increase text size
- avoid fixed heights for text containers
- use `min-width: 0` in flexible layouts
- allow wrapping and long unbroken content
- use logical properties for writing modes
- keep touch targets comfortably large
- do not hide essential content only because the viewport is small
- test onscreen keyboards, browser chrome, and safe areas

## Viewport Units

`100vh` may behave unexpectedly with mobile browser controls. Prefer `100dvh` for the current dynamic viewport, or `svh`/`lvh` when their specific behavior is required.
