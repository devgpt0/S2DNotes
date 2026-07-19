# 08 - Most-Asked shadcn/ui Interview Questions

1. **What is shadcn/ui?** A CLI/registry approach that adds customizable component source to your project.
2. **Library vs copied source?** Traditional package hides/versions implementation in dependency; shadcn source becomes project-owned.
3. **Why Tailwind knowledge required?** Components are styled with utilities/tokens and browser still receives CSS.
4. **Why React knowledge required?** Composition, props, refs, state, portals, forms, and lifecycle remain React concerns.
5. **What is `components.json`?** CLI project configuration for style/base, aliases, Tailwind, paths, icons, registries.
6. **What does `cn` do?** Conditional class joining plus Tailwind-aware conflict merging.
7. **What is CVA?** Utility for defining typed base classes and finite variants/defaults/compound variants.
8. **What does `asChild` do?** Composes behavior/classes onto one child element without extra DOM; child must accept forwarded props/ref.
9. **How theme works?** Semantic CSS variables mapped to Tailwind utilities, changed by root theme selector/class.
10. **How dark mode works?** Theme marker/system preference changes variables/utilities; native color-scheme and prepaint setup matter.
11. **Are components automatically accessible?** Primitives help, but names, descriptions, semantics, composition, focus, and custom changes remain team responsibility.
12. **How upgrade?** Generate/diff/migrate/test; do not blindly overwrite owned source.
13. **How create domain component?** Compose UI primitives into a product-specific API without polluting low-level primitives.
14. **Form approach?** Semantic controls plus schema/form-state library when justified and authoritative server errors.
15. **Data table?** Presentation primitives; sorting/filtering/pagination/virtualization require explicit state/library/server design.
16. **Server Components?** Keep interactive primitive boundary client-side as required; compose from server output in supporting framework.
17. **Performance risks?** Too many mounted portals/observers, large data UI, broad client boundaries, unused components/dependencies.
18. **Security risk?** Remote registry/source/dependency supply chain, unsafe HTML, client-only auth, unvalidated form/API data.
19. **Why not wrap everything?** Wrapper layers can hide native props/ref/accessibility and make upgrades harder.
20. **When not use shadcn?** When a maintained packaged design system, strict cross-product centralized updates, or non-React stack fits better.
