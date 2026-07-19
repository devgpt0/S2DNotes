# 08 - TypeScript Configuration, Builds, Testing, and Migration

## Important Compiler Options

- `strict`: strict family of safety checks
- `noUncheckedIndexedAccess`: indexed reads include undefined
- `exactOptionalPropertyTypes`: exact missing vs undefined behavior
- `noImplicitOverride`: requires explicit override keyword
- `noFallthroughCasesInSwitch`: detects unintentional fall-through
- `isolatedModules`: each file can be transpiled independently
- `verbatimModuleSyntax`: preserves explicit type/value import intent
- `module`/`moduleResolution`: must match runtime or bundler
- `target`/`lib`: emitted syntax and available platform type declarations

Do not copy a tsconfig blindly; align it with browser targets and build tools.

## Type Check vs Build

Many frontend tools transpile TypeScript without performing a complete type check. Run `tsc --noEmit` separately in CI.

```powershell
npx tsc --noEmit
npm test
npm run build
# Result: type checking, tests, and production bundling all run as separate required checks.
```

## Testing

```typescript
import { expect, test } from "vitest";
const total = (values: readonly number[]): number => values.reduce((sum, value) => sum + value, 0);
test("totals values", () => expect(total([10, 20])).toBe(30));
// Test output: passes with total 30.
```

## Library Public Types

Export minimal stable types, generate declarations, define package exports, test consumer compilation, and follow semantic versioning for type-level breaking changes.

## JavaScript Migration

1. Add TypeScript and allow JavaScript temporarily.
2. Enable checking on selected JS or convert leaf modules.
3. Type external boundaries and shared models.
4. Replace `any` with real types/unknown validation.
5. Enable strict flags progressively.
6. Add type checking to CI.
7. Remove unsafe assertions and temporary compatibility settings.

Do not begin by creating one massive global types file or by asserting every error away.

## Source Maps

Source maps connect runtime JavaScript stacks to TypeScript source. Decide production access based on error monitoring and source exposure. Protect source-map endpoints if they are not intended for public download.
