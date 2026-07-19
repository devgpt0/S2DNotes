# 04 - shadcn/ui Theming, Dark Mode, and Design Tokens

## Token Model

shadcn components commonly use semantic CSS variables mapped into Tailwind theme utilities.

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(.18 .02 260);
  --primary: oklch(.50 .20 260);
  --primary-foreground: oklch(.98 0 0);
  --radius: .625rem;
}
.dark {
  --background: oklch(.16 .02 260);
  --foreground: oklch(.96 .01 260);
  --primary: oklch(.72 .14 260);
}
/* Browser result: semantic component colors/radius change through theme variables. */
```

Do not rename token meaning into component-specific colors (`--button-blue`) unless the design system requires a true component token.

## Theme Provider

```tsx
function applyTheme(theme: "light" | "dark") {
  document.documentElement.classList.toggle("dark", theme === "dark");
  document.documentElement.style.colorScheme = theme;
  localStorage.setItem("theme", theme);
}
applyTheme("dark");
console.log(document.documentElement.classList.contains("dark"));
// Console output: true
```

Apply the stored/system theme before first paint to prevent a flash. Validate stored values and handle storage failure.

## Theme Review

- semantic surface/text/border/input/ring/destructive/chart tokens
- light and dark contrast
- focus/hover/disabled/selected states
- native control `color-scheme`
- forced-colors/high contrast
- data visualization distinguishability
- no direct palette class that bypasses theme without a reason

## Brand Customization

Change tokens first, then variants, then component source. Avoid copying/editing every component for a global brand color.
