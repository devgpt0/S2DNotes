# shadcn/ui Concepts in Simple Words

## The One-Sentence Idea

The shadcn CLI copies accessible component source into your project, combining React composition, headless primitives, Tailwind utilities, and design tokens.

```text
CLI registry -> component source copied into project -> team edits/tests -> normal React/Tailwind build
# Result: no hidden runtime design-system package controls your component source.
```

## Key Terms

| Term | Simple meaning |
|---|---|
| primitive | low-level accessible behavior such as Dialog |
| component source | generated `.tsx` file your project owns |
| variant | named visual/size choice |
| `cn` | helper that conditionally joins and merges Tailwind classes |
| design token | named color/radius/spacing decision |
| `components.json` | CLI paths/style/configuration |
| registry | source definition the CLI can add |
| slot/trigger/content | composable parts of a headless component |

## First Button

```tsx
import { Button } from "@/components/ui/button";
export function SaveButton() {
  return <Button>Save course</Button>;
}
// Browser result: project-owned styled accessible HTML button.
```

## What shadcn/ui Does Not Do

- choose semantic page structure
- define your product's domain components
- validate server data
- guarantee every custom composition stays accessible
- replace responsive design or React knowledge
- automatically upgrade edited files

## Learning Test

Open `components/ui/button.tsx`. Identify its native element/primitive, variants, forwarded props/ref behavior, default classes, and the point where consumer `className` is merged.
