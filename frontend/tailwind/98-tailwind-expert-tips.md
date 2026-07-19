# Tailwind CSS Expert Tips and Production Patterns

## Architecture

- Learn and use design tokens before arbitrary values.
- Keep class composition near the component that owns the markup.
- Extract a component when markup/behavior repeats; extract a class abstraction only for a CSS contract.
- Centralize variant mapping with complete static strings.
- Use a deliberate class merge utility only when consumer overrides are a real API.
- Keep component primitives small; avoid a universal component with dozens of boolean style props.

## Responsive Design

- Unprefixed utilities form the mobile baseline.
- Use intrinsic Grid patterns when content can adapt without named breakpoints.
- Use container variants for components reused in different page regions.
- Test zoom, long localization, RTL, keyboard, forced colors, reduced motion, and touch.
- Do not hide primary functionality at smaller breakpoints.
- Keep DOM order meaningful even if Grid/Flex utilities reorder visually.

## Theme and Dark Mode

- Define semantic brand/surface/text tokens through `@theme` and CSS variables.
- Avoid scattering near-identical arbitrary colors across components.
- Test every interaction state in light/dark/high-contrast modes.
- Set `color-scheme` so native controls match the active theme.
- For user-selected themes, apply the theme marker before paint to prevent flashing.

## Class Management

- Prefer multiline/grouped class formatting for long lists.
- Order utilities consistently: layout -> box -> spacing -> typography -> visual -> state -> responsive.
- Conditional libraries should receive trusted finite variants, not raw user class names.
- Understand that CSS generation order, not HTML class-string order alone, resolves conflicts.
- Arbitrary variants/selectors are powerful but can make ownership and specificity hard to see.

## Production Output

- Verify content/source detection for monorepos, packages, generated templates, and unusual file types.
- Avoid massive safelists; they defeat on-demand output.
- Inspect final compressed CSS and caching.
- Keep third-party and custom CSS in intentional layers.
- Check source maps and browser targets through the complete build pipeline.
- Measure real render-blocking delivery and unused CSS, not raw class count.

## Accessibility and Browser Tips

- Utilities cannot add semantic behavior to a `div`; choose native elements first.
- Use `focus-visible`, disabled, invalid, expanded, selected, busy, and reduced-motion states deliberately.
- Do not remove outline globally.
- Verify touch target size and contrast rather than assuming palette names are accessible.
- Use DevTools Computed view to translate a utility conflict back into CSS.
- Test target browsers because Tailwind may generate a feature an older browser cannot use.

## Expert Debugging

1. Confirm the complete token exists in source and generated CSS.
2. Inspect computed property and competing rule.
3. Check responsive/state/container conditions.
4. Check class merging and variant selection.
5. Check arbitrary value syntax.
6. Rebuild production mode and inspect output rather than trusting dev hot reload.

## Expert Code Snippets Used in Production

### Type-Safe Variant Map

```typescript
const buttonVariants = {
  primary: "bg-blue-700 text-white hover:bg-blue-600",
  danger: "bg-red-700 text-white hover:bg-red-600",
  ghost: "bg-transparent text-slate-900 hover:bg-slate-100",
} as const;
type ButtonVariant = keyof typeof buttonVariants;
export const buttonClass = (variant: ButtonVariant): string => `rounded-md px-4 py-2 font-semibold focus-visible:outline-2 ${buttonVariants[variant]}`;
console.log(buttonClass("primary"));
// Console output includes the complete statically discoverable primary utility string.
```

### Conditional Class Helper

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]): string { return twMerge(clsx(inputs)); }
console.log(cn("px-2", true && "px-4", "text-sm"));
// Console output: px-4 text-sm (conflicting Tailwind padding is merged intentionally).
```

Use a merge helper only where accepting/combining classes is part of the component API.

### Data-State Styling

```html
<button aria-expanded="false" data-state="closed" class="rounded px-3 py-2 data-[state=open]:bg-blue-100 aria-expanded:text-blue-800">Menu</button>
<!-- Browser result: styling follows explicit component/ARIA state without custom CSS selector files. -->
```

### Theme Token Bridge

```css
@import "tailwindcss";
@theme { --color-brand: var(--app-brand); }
:root { --app-brand: oklch(52% .2 260); }
[data-theme="dark"] { --app-brand: oklch(72% .14 260); }
/* Result: bg-brand/text-brand utilities follow runtime theme custom properties. */
```
