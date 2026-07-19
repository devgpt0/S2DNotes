# 08 - Custom Hooks

## What Is a Custom Hook?

A custom hook is a function beginning with `use` that composes React hooks to share stateful logic. It shares logic, not one state instance.

## Online Status Hook

```tsx
function useOnlineStatus(): boolean {
  const [online, setOnline] = useState(navigator.onLine);
  useEffect(() => {
    const update = () => setOnline(navigator.onLine);
    window.addEventListener("online", update);
    window.addEventListener("offline", update);
    return () => { window.removeEventListener("online", update); window.removeEventListener("offline", update); };
  }, []);
  return online;
}
function Status() {
  const online = useOnlineStatus();
  return <p>{online ? "Online" : "Offline"}</p>;
}
// Browser result: reusable online/offline status with correct cleanup.
```

## Rules of Hooks

- call hooks at the top level of React components/custom hooks
- do not call conditionally, in loops, event handlers, or ordinary functions
- call only from React functions
- use the official hooks lint rules

React relies on stable call order to associate hook state.

## API Design

- name the capability, not its implementation (`useOnlineStatus`, not `useWindowEvents`)
- accept explicit inputs and return the smallest useful output
- own setup/cleanup completely
- do not hide surprising global side effects
- return stable callbacks only when consumers benefit
- expose status/error/cancel behavior for async hooks

## Avoid Over-Abstraction

Two components both using `useState` is not duplication worth extracting. Extract when the lifecycle/state transition is conceptually the same and has a clear contract.

## Test Hooks Through Behavior

Prefer testing a small component that uses the hook when that matches user-visible behavior. Direct hook tests are appropriate for reusable library contracts and complex transitions.
