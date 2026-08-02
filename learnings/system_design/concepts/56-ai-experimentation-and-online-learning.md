# AI Experimentation and Online Learning

## Idea

Offline evaluation estimates model quality on recorded data. Online experiments measure how a change affects real users and systems.

Online learning updates decisions from new feedback. It is useful only when feedback is trustworthy and exploration is safe.

## Visual model

```text
eligible subject -> stable random assignment
                       |          |
                    control    treatment
                       \          /
                    exposure events
                          |
              outcomes + guardrails
                          |
                    analysis and rollout
```

## Design steps

1. Write the hypothesis, primary metric, guardrails, and stopping rule first.
2. Choose a stable randomization unit such as user, account, or session.
3. Log assignment and actual exposure separately.
4. Keep model, prompt, retrieval, and policy versions in every event.
5. Estimate required sample size and experiment duration.
6. Detect sample-ratio mismatch and broken instrumentation early.
7. Analyze practical impact and uncertainty, not only statistical significance.
8. Roll out gradually and continue monitoring after the experiment.

## Online learning pattern

Use a contextual bandit when the system must choose among actions and can safely explore.

```text
context -> policy chooses action -> delayed reward
   ^                                  |
   |---------- controlled update -----|
```

Keep a fixed holdout group, cap exploration, and account for delayed or missing rewards.

## Trade-offs

- Longer tests increase confidence but delay decisions.
- Faster online updates adapt quickly but can amplify noisy or manipulated feedback.
- User-level assignment prevents cross-session switching but may require more samples.

## Common mistakes

- Changing several uncontrolled variables at once.
- Analyzing users who were assigned but never exposed as if they saw the feature.
- Stopping when a desirable result first appears.
- Ignoring interference between users or marketplace sides.
- Training directly on feedback that attackers can manipulate.
