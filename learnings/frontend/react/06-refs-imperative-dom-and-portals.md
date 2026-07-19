# 06 - Refs, Imperative DOM, and Portals

## Ref as a Stable Box

A ref persists between renders without requesting a render when changed.

```tsx
function Stopwatch() {
  const startedAt = useRef<number | null>(null);
  return <button onClick={() => { startedAt.current = performance.now(); console.log(startedAt.current); }}>Start</button>;
}
// Console result after click: current high-resolution timestamp; changing ref does not rerender.
```

Use state for information shown in UI; use refs for imperative handles/instance-like values.

## DOM Ref

```tsx
function Search() {
  const inputRef = useRef<HTMLInputElement>(null);
  return <><input ref={inputRef} /><button onClick={() => inputRef.current?.focus()}>Focus search</button></>;
}
// Browser result: button moves keyboard focus to the search input.
```

Use refs for focus, selection, measurement, scroll, media playback, and third-party widgets—not normal DOM rendering.

## Exposing a Small Imperative Handle

```tsx
type SearchHandle = { focus(): void };
const SearchInput = forwardRef<SearchHandle>((_, ref) => {
  const input = useRef<HTMLInputElement>(null);
  useImperativeHandle(ref, () => ({ focus: () => input.current?.focus() }), []);
  return <input ref={input} />;
});
// Result: parent receives only a focus() capability rather than the complete DOM node.
```

React 19 also supports ref as a prop for function components in supported patterns; understand the project's compatibility/API style.

## Portals

```tsx
function Modal({ children }: { children: ReactNode }) {
  return createPortal(<div role="dialog" aria-modal="true">{children}</div>, document.body);
}
// Browser result: dialog DOM is placed under body while remaining in the same React tree for context/event behavior.
```

A portal does not implement focus trapping, labelling, Escape, scroll locking, or restoration. Prefer a tested accessible dialog primitive/native dialog.

## Measurement

Use ResizeObserver when size can change. Repeated `getBoundingClientRect` in render is invalid; measurement happens after commit and must avoid feedback loops.
