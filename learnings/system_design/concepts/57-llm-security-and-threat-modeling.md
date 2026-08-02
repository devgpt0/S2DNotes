# LLM Security and Threat Modeling

## Idea

An LLM can interpret data as instructions. Therefore user text, retrieved documents, model output, and tool output must all be treated as untrusted.

Prompts can guide behavior, but they are not a security boundary.

## Visual model

```text
untrusted inputs
user / web / files / tools
          |
provenance + validation + policy checks
          |
         model
          |
structured validation + authorization
          |
sandboxed tools with least privilege
```

## Design steps

1. List protected assets, trust boundaries, actors, and allowed actions.
2. Separate instructions from untrusted content in the application protocol.
3. Give each tool the minimum permissions, time, data, and network access required.
4. Validate structured model output before any action.
5. Authorize the requested action using application identity and policy.
6. Require confirmation for destructive, financial, external, or high-impact actions.
7. Restrict network egress and defend fetchers against SSRF.
8. Log decisions and tool calls without exposing secrets or unnecessary personal data.
9. Red-team the full system, including retrieval, tools, plugins, and supply chain.

## Critical threats

- Direct and indirect prompt injection.
- Sensitive-data extraction and cross-tenant leakage.
- Unauthorized tool use or excessive agency.
- SSRF, command injection, and unsafe code execution.
- Retrieval or training-data poisoning.
- Denial of service through huge inputs or expensive tool loops.
- Malicious model, dependency, dataset, or adapter artifacts.

## Security controls

- Treat model output as a proposal, never as authorization.
- Use allowlisted structured tool schemas.
- Run risky computation in isolated sandboxes.
- Keep credentials outside prompts and model-visible logs.
- Scan and verify model and data artifacts.
- Rate-limit by user, tenant, tool, and cost.

## Common mistakes

- Trying to solve prompt injection with a stronger system prompt alone.
- Giving one agent broad permanent credentials.
- Executing generated SQL, shell, HTML, or URLs without validation.
- Trusting retrieved documents because they came from an internal index.
- Hiding security decisions inside probabilistic model behavior.
