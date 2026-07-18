# 05 - DOM, Events, Forms, and Accessible Interaction

## Select and Change Content

```html
<p id="status">Waiting</p>
<script type="module">
  const status = document.querySelector("#status");
  status.textContent = "Ready";
  console.log(status.textContent);
</script>
<!-- Browser result: paragraph and console both show Ready. -->
```

Prefer `textContent` for plain text. Do not put untrusted content into `innerHTML`; it can create XSS.

## Create Elements

```javascript
const item = document.createElement("li");
item.textContent = "JavaScript";
document.querySelector("ul").append(item);
console.log(item.outerHTML);
// Console output: <li>JavaScript</li>
```

## Events

```javascript
const button = document.querySelector("button");
button.addEventListener("click", event => {
  console.log(event.currentTarget.textContent);
});
// Console output after click: the button's visible text.
```

- target: deepest element that started the event
- currentTarget: element whose listener is running
- events normally capture down, reach target, then bubble up
- `preventDefault`: cancel a cancelable browser default
- `stopPropagation`: stop propagation; use rarely

## Event Delegation

```javascript
document.querySelector("#list").addEventListener("click", event => {
  const button = event.target.closest("button[data-id]");
  if (!button) return;
  console.log(button.dataset.id);
});
// Console output after delegated button click: its data-id value.
```

One ancestor listener can handle dynamic children.

## Forms

```javascript
const form = document.querySelector("form");
form.addEventListener("submit", event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const data = new FormData(form);
  console.log(data.get("email"));
});
// Console output on valid submission: entered email address.
```

The server must validate again.

## Accessible Dynamic UI

- use native button/input/dialog/details when possible
- keyboard and pointer should trigger the same action
- move focus only for a clear interaction reason
- return focus after dialogs
- update ARIA state with visual state
- announce important async status through a live region

```javascript
button.setAttribute("aria-expanded", String(!expanded));
menu.hidden = expanded;
console.log(button.getAttribute("aria-expanded"));
// Console output: true when opening, false when closing.
```

## DOM Performance

Batch changes, avoid huge DOM trees, use delegation, and do not repeatedly query/change layout inside tight loops. `DocumentFragment` can assemble many nodes before one insertion.
