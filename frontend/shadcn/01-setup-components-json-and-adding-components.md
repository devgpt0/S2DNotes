# 01 - shadcn/ui Setup, components.json, and Adding Components

## Start from React + Tailwind

Use an existing supported React project with Tailwind configured, path aliases working, and TypeScript strict mode.

```powershell
npx shadcn@latest init
# Result: CLI asks setup questions and creates components.json plus shared styles/utilities as needed.
```

## Add Components

```powershell
npx shadcn@latest add button card input label dialog table sonner
# Result: component source files and required dependencies are added to the project.
```

Review the diff before accepting/committing generated code.

## `components.json`

It tells the CLI the style/base choice, React Server Component behavior where applicable, TypeScript use, Tailwind CSS path, aliases, icon library, and registry configuration.

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "tsx": true,
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui"
  }
}
```

Result: generated imports use the configured project aliases. Exact current fields depend on selected CLI setup.

## Folder Ownership

```text
src/
├─ components/ui/       # low-level generated/customized primitives
├─ components/course/   # product/domain components
├─ lib/utils.ts         # cn and shared focused helpers
├─ features/            # feature logic, schemas, API boundaries
└─ app or routes/       # route composition
# Result: UI primitives remain separate from business components.
```

## The `cn` Helper

```tsx
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
console.log(cn("px-2", "px-4", false && "hidden"));
// Console output: px-4
```

It handles conditional values and known conflicting Tailwind groups. It does not validate arbitrary user styles.

## Setup Verification

Render a Button, check keyboard focus, inspect generated source, run type check/tests/build, and confirm production Tailwind output contains the required utilities.
