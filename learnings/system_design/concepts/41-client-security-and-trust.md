# Client Security and Browser Trust Boundaries

## Idea

The browser and all client input are untrusted. Frontend controls reduce attack
surface and protect sessions, but authorization and business validation must
remain on the server.

## Visual model

```text
untrusted URL/form/third-party data -> parse/validate -> safe DOM/API use
browser credential -> CSRF/session controls -> server authorization
```

## Design steps

1. Map script, iframe, storage, cookie, URL, and third-party trust boundaries.
2. Render text with framework escaping; sanitize only when HTML is required.
3. Deploy a strict Content Security Policy and Trusted Types where supported.
4. Prefer secure, HttpOnly, SameSite cookies for browser sessions.
5. Add CSRF protection when credentials are sent automatically.
6. Pin/review dependencies and isolate risky third-party content.

## When to use it

Always. Increase controls for user-generated content, payments, admin tools,
embedded third parties, and applications handling sensitive data.

## Trade-offs

Strict CSP and iframe sandboxing can constrain integrations. Create explicit
allowlists and nonces rather than weakening policies globally.

## Critical threats

- XSS, DOM clobbering, unsafe URL schemes, prototype pollution.
- CSRF and confused-deputy actions.
- Token leakage through storage, logs, referrers, or third parties.
- Supply-chain compromise and malicious browser extensions.

## Common mistakes

- Storing long-lived tokens in `localStorage` without threat analysis.
- Using `innerHTML` with “trusted-looking” API content.
- Hiding a button and calling it authorization.
- Putting secrets into frontend bundles or build-time public variables.
