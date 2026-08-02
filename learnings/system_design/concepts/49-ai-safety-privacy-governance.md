# AI Safety, Privacy, and Governance

## Idea

AI governance maps risk to controls across data, models, prompts, tools, outputs,
people, and vendors. Safety includes misuse, harmful mistakes, unfair outcomes,
privacy leakage, and loss of control over automated actions.

## Visual model

```text
use case risk -> data/model approval -> runtime guardrails -> monitoring
              -> human escalation -> incident response -> audit/retirement
```

## Design steps

1. Classify use case, affected users, autonomy, reversibility, and legal duties.
2. Document intended use, forbidden use, known limits, and accountable owner.
3. Minimize training/inference data and enforce consent, purpose, retention, deletion.
4. Evaluate harmful content, bias, privacy leakage, jailbreaks, and misuse.
5. Add layered input, tool, and output controls appropriate to risk.
6. Monitor incidents and provide appeal, correction, and shutdown paths.

## When to use it

Every AI system needs a baseline. Decisions affecting health, finance,
employment, education, identity, or safety require stronger review and human
accountability.

## Trade-offs

Strict filters reduce harmful output but can block legitimate use and create
unequal error rates. Human review improves accountability but creates sensitive
queues, delay, and reviewer-wellbeing concerns.

## Governance artifacts

- Data/model cards, risk assessment, evaluation evidence, approval record.
- Vendor/data residency and deletion commitments.
- Versioned policies, overrides, audits, incidents, and corrective actions.
- Clear owner with authority to disable the feature/model.

## Common mistakes

- Treating one moderation model as a complete safety system.
- Sending sensitive data to a provider without retention/training controls.
- Logging raw prompts and outputs indefinitely.
- No user recourse when an automated decision is wrong.
