# 03 - Tailwind Theme, Dark Mode, Arbitrary Values, and Components

## CSS-First Theme

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(60% .18 260);
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 120rem;
}
/* Result: utilities such as bg-brand-500, font-display, and 3xl:* become available. */
```

Theme tokens should express a design system, not arbitrary one-off choices.

## Dark Mode

```html
<article class="bg-white text-slate-900 dark:bg-slate-900 dark:text-slate-100">
  Theme-aware card
</article>
<!-- Browser result: light colors normally and dark colors under configured dark-mode behavior. -->
```

Test contrast in both themes and set native control `color-scheme` where appropriate.

## Arbitrary Values

```html
<div class="grid grid-cols-[12rem_minmax(0,1fr)] gap-[clamp(1rem,3vw,2rem)]">Layout</div>
<!-- Browser result: exact custom grid tracks and fluid gap. -->
```

Arbitrary values are escape hatches. Repeated values belong in theme tokens or standard CSS.

## Reusable Components

In component frameworks, extract markup into a component and map variants to full class strings.

```typescript
const buttonStyles = {
  primary: "bg-blue-700 text-white hover:bg-blue-600",
  danger: "bg-red-700 text-white hover:bg-red-600",
} as const;
console.log(buttonStyles.primary);
// Console output: bg-blue-700 text-white hover:bg-blue-600
```

Use `@apply` sparingly for integration with third-party markup or genuinely shared CSS rules. Excessive `@apply` recreates component CSS while losing visible utility composition.

## Class Conflict Management

When accepting consumer classes, define an explicit merge policy. Later utilities do not always win as expected when generated rule order and conflicting properties differ. Framework-specific class-merging libraries can help, but add them only when necessary.
