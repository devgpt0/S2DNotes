# Security and Privacy

## Idea

Security is a system property: authenticate identity, authorize each action,
validate input, protect data, and preserve auditable boundaries.

## Classroom board

```text
untrusted request -> edge limits -> authentication -> authorization
                  -> validation -> least-privilege service -> encrypted data
```

## Design steps

1. Threat-model assets, actors, trust boundaries, and abuse cases.
2. Centralize identity but enforce resource authorization near data.
3. Encrypt in transit/at rest and rotate secrets through a manager.
4. Minimize data, define retention/deletion, and audit sensitive operations.

## When to use it

Always; depth increases for payments, health, identity, children, and AI data.

## Trade-offs and mistakes

Do not rely on hidden IDs, log tokens/prompts with PII, trust internal traffic,
or add privacy deletion after data has spread to uncontrolled derived stores.
