# Prompt for Math DSA Notes

```text
Create or revise one concise Markdown note in `math_dsa` for Codeforces
mathematics rated approximately 0-2500.

Topic: <TOPIC>
Target rating band: <BAND>
Prerequisites: <LINKS_OR_CONCEPTS>
Related notes: <PATHS>

Before writing, inspect `math_dsa/README.md` and related notes. Give this note
one clear responsibility; link instead of duplicating a full explanation.

Requirements:
- Start with `# <topic>` and state the contest purpose in two sentences or less.
- Teach concepts in prerequisite order. For each: recognition cue, exact rule or
  invariant, preconditions, complexity, and one common wrong assumption.
- Use a table for formula or algorithm choice when it is clearer than prose.
- Add minimal Python 3.12+ only where implementation is error-prone or the
  reader must memorize a template. Use type hints and snake_case names.
- Every standalone executable example must use deterministic `print()` output
  followed immediately by an exact `Output:` block. Run it before finalizing.
- Label contextual templates as functions, state their input contract, and do
  not invent output for them.
- Never silently coerce invalid values. Raise `ValueError` for invalid template
  contracts when validation is part of the example.
- State modular assumptions precisely: prime versus composite modulus, coprime
  values, and bounds such as `n < modulus`.
- Prefer exact integer arithmetic. Explain any floating-point tolerance.
- End with a compact `## Checklist` of recognition cues and edge cases.

Do not add filler, generic exercises, placeholder code, duplicated theory,
unverified claims, or a long introduction. Update `math_dsa/README.md` if the
topic changes the study order or complete topic map.
```
