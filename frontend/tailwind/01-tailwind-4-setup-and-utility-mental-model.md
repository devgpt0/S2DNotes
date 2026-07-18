# 01 - Tailwind CSS 4 Setup and Utility Mental Model

## Install with Vite Plugin

```powershell
npm install tailwindcss @tailwindcss/vite
# Result: installs Tailwind 4 and its Vite integration.
```

```javascript
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({ plugins: [tailwindcss()] });
// Result: Vite processes Tailwind utilities found in project source files.
```

```css
@import "tailwindcss";
/* Result: imports Tailwind's generated theme, base, and utility layers. */
```

## Utility Mental Model

```html
<button class="rounded-md bg-blue-700 px-4 py-2 font-semibold text-white hover:bg-blue-600">
  Save
</button>
<!-- Browser result: padded rounded blue button with a lighter hover state. -->
```

- `rounded-md` -> border radius
- `bg-blue-700` -> background color
- `px-4 py-2` -> inline/block padding
- `font-semibold` -> font weight
- `hover:` -> pseudo-class variant

## Why Utilities?

- styles are colocated with markup
- constrained tokens improve consistency
- changing one component avoids unintended selector effects
- production output includes detected utilities rather than a huge full framework

Tradeoff: long class lists and repeated patterns require component extraction discipline.

## Important Detection Rule

Tailwind scans source text for complete class tokens. Dynamically building fragments may not be detected.

```javascript
const color = "red";
const unsafeClass = `bg-${color}-500`;
console.log(unsafeClass);
// Console output: bg-red-500
// Build warning: Tailwind may not generate a class assembled from fragments.
```

Map variants to complete class strings instead.

```javascript
const colors = { error: "bg-red-500", success: "bg-green-600" };
console.log(colors.error);
// Console output: bg-red-500
```
