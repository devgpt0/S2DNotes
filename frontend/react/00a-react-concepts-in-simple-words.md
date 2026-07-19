# React Concepts in Simple Words

## The One-Sentence Idea

React calls components to calculate what the interface should look like for the current props and state, then commits necessary DOM changes.

```text
props + state -> render components -> React compares result -> commit DOM changes
# Result: UI is derived from data instead of manually kept in sync element by element.
```

## Core Terms

| Term | Simple meaning |
|---|---|
| component | function describing part of UI |
| JSX | syntax for describing element trees |
| props | read-only inputs from parent |
| state | component-owned memory that triggers rendering |
| hook | React function adding state/context/lifecycle capability |
| render | React calls components to calculate UI |
| commit | React applies changes to DOM |
| effect | synchronization with an external system after commit |
| ref | stable mutable holder or DOM handle |
| context | value available to a subtree without prop threading |
| key | stable sibling identity in a rendered list |

## First Component

```tsx
type GreetingProps = { name: string };
function Greeting({ name }: GreetingProps) {
  return <h1>Hello {name}</h1>;
}
// Browser result for <Greeting name="Asha" />: heading "Hello Asha".
```

## Data Flows Down, Events Flow Up

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(value => value + 1)}>Count: {count}</button>;
}
// Browser result: each activation increments the displayed count.
```

## What React Does Not Replace

HTML semantics, CSS layout, JavaScript, browser APIs, HTTP, runtime validation, accessibility, security, testing, and system architecture still matter.

## Learning Test

Before moving forward, explain why changing state requests a render, why props are read-only, and why a button remains a real HTML button rather than a clickable `div`.
