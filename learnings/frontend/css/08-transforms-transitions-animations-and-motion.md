# 08 - Transforms, Transitions, Animations, and Motion

## Transform

Transforms change visual position/shape without normal-flow layout.

```css
.card:hover { transform: translateY(-.25rem) scale(1.01); }
/* Browser result: hovered card moves slightly upward and grows. */
```

## Transition

```css
.button {
  background: navy;
  transition: background-color 150ms ease, transform 150ms ease;
}
.button:hover { background: royalblue; transform: translateY(-1px); }
/* Browser result: hover color and movement change smoothly over 150ms. */
```

List exact properties. Avoid `transition: all` because unintended changes may animate.

## Keyframe Animation

```css
@keyframes spin { to { transform: rotate(1turn); } }
.spinner { animation: spin 1s linear infinite; }
/* Browser result: spinner continuously rotates once per second. */
```

Animation should communicate state or relationship, not merely decorate.

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; }
  .button { transition: none; }
}
/* Browser result: users requesting less motion receive immediate state changes. */
```

## Performance

Transform and opacity are often composited without repeated layout/paint, but layers consume memory. Animating width, height, top, or left can trigger more layout/paint work.

Do not add `will-change` everywhere. Use it briefly and only for measured cases.

## Accessibility

- avoid flashing more than safe thresholds
- do not make essential information available only through animation
- allow pause/stop for long or auto-updating motion
- retain visible focus styles
- ensure hover interactions also work by keyboard/touch
