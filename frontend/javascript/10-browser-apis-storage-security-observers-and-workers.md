# 10 - Browser APIs, Storage, Security, Observers, and Workers

## URL and History

```javascript
const url = new URL("https://example.com/courses?page=2");
console.log(url.hostname, url.searchParams.get("page"));
// Console output: example.com 2
```

Use URL APIs rather than string concatenation. History APIs change client-side URL/history but require server fallback routing for direct navigation.

## Storage

```javascript
localStorage.setItem("theme", "dark");
console.log(localStorage.getItem("theme"));
localStorage.removeItem("theme");
// Console output: dark
```

- localStorage: synchronous string storage per origin; small preferences only
- sessionStorage: per-tab/session lifetime
- IndexedDB: asynchronous structured storage for larger offline data
- cookies: sent with matching HTTP requests; use Secure, HttpOnly, SameSite for server sessions as appropriate

Never store long-lived sensitive tokens in JavaScript-readable storage when an HttpOnly session design is available.

## IntersectionObserver

```javascript
const observer = new IntersectionObserver(entries => {
  for (const entry of entries) console.log(entry.target.id, entry.isIntersecting);
});
observer.observe(document.querySelector("#target"));
// Console output when visibility changes: target true or target false.
```

Use observers instead of constant scroll polling for visibility, resize, and DOM mutation cases.

## Web Worker

```javascript
// worker.js
self.onmessage = event => self.postMessage(event.data * 2);

// main.js
const worker = new Worker("./worker.js", { type: "module" });
worker.onmessage = event => console.log(event.data);
worker.postMessage(21);
// Console output: 42
```

Workers run off the main thread and cannot directly access the DOM. Messages use structured cloning or transferable objects.

## Security

- XSS: untrusted data becomes executable markup/script
- CSRF: attacker causes authenticated browser to send an unwanted request
- same-origin policy: restricts cross-origin reads
- CORS: server-declared cross-origin browser read permission
- CSP: limits allowed resource/script behavior
- prototype pollution: untrusted keys alter object prototypes

```javascript
output.textContent = untrustedText;
console.log(output.textContent);
// Console output: the text exactly; it is not interpreted as HTML.
```

Avoid `eval`, `new Function`, unsafe HTML sinks, and string-built script URLs. Sanitize rich HTML with a proven policy/library when rich content is truly required.

## Other Important APIs

Geolocation, Clipboard, Notifications, MediaDevices, WebSocket, Service Worker, Cache API, and File APIs require permission, lifecycle, privacy, error, and compatibility handling. Use feature detection and provide fallback.
