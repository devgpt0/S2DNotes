# 04 - Tailwind Responsive Design, Accessibility, Browser Behavior, and Optimization

## Responsive Rules Still Use CSS

Tailwind prefixes generate media/container queries. The same design principles apply:

- start mobile-first
- prefer flexible Grid/Flex layouts
- choose content-based breakpoints
- test zoom and long content
- do not hide essential content on mobile
- keep DOM order meaningful

```html
<section class="grid grid-cols-[repeat(auto-fit,minmax(min(100%,18rem),1fr))] gap-4">
  <article>Flexible card</article>
</section>
<!-- Browser result: intrinsic responsive cards without named device breakpoints. -->
```

## Accessibility

```html
<button class="min-h-11 rounded px-4 focus-visible:outline-2 focus-visible:outline-offset-2 motion-reduce:transition-none">
  Accessible action
</button>
<!-- Browser result: comfortable target, keyboard focus, and reduced-motion respect. -->
```

Utilities cannot repair incorrect HTML. Use real buttons, labels, headings, landmarks, alternative text, and ARIA only where needed.

## Production Generation

Tailwind generates utilities found in source files. Keep class names statically discoverable, configure additional source locations when required, and verify output in production builds.

## Browser Understanding

The browser receives normal CSS rules. Utility count alone is less important than final compressed CSS, unused output, DOM size, render-blocking delivery, and runtime layout/paint behavior.

## Performance Checklist

- inspect final CSS size and network caching
- avoid a huge safelist or generated arbitrary variants
- split routes only when it improves real loading behavior
- do not add classes through uncontrolled user input
- use responsive images and dimensions in HTML
- animate transform/opacity when suitable and respect reduced motion
- use DevTools Computed styles to understand which utility wins
- test target browsers because Tailwind cannot make unsupported CSS supported

## Security

Never allow users to provide arbitrary class strings when classes could load external URLs, obscure security UI, or break trusted layout. Treat content, style controls, and rich HTML as separately authorized/sanitized inputs.
