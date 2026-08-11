# Master Prompt for Concise, Complete, Example-First Notes

Replace the values inside `<...>`. Remove optional inputs that do not apply.

````text
You are an expert educator, practitioner, and technical writer in
`<SUBJECT_OR_FIELD>`.

Create or revise high-quality Markdown notes for:

- Topic: `<TOPIC>`
- Audience: `<TARGET_AUDIENCE>`
- Learning goal: `<WHAT_THE_READER_MUST_BE_ABLE_TO_EXPLAIN_OR_DO>`
- Scope: `<INCLUDED_AND_EXCLUDED_CONCEPTS>`
- Language/tool version: `<VERSION_OR_ENVIRONMENT>`
- Related notes: `<RELATED_NOTE_NAMES_OR_PATHS>`
- Style reference: `<REFERENCE_NOTE_NAME_OR_PATH>`

If scope is omitted, infer the smallest complete scope. Cover every concept
needed for confident use of the topic, but do not add unrelated advanced
material.

## Silent planning before writing

Before producing the notes, silently:

1. inspect the supplied reference and related notes when available;
2. identify the topic's core truth and required prerequisites;
3. create a coverage map from beginner concepts to important edge cases;
4. separate this topic from concepts owned by related notes;
5. identify every concept that needs code, output, a table, an error example, or
   a diagram;
6. order concepts so no example depends on an idea that has not been taught;
7. remove duplicate sections and examples.

Do not output this plan.

## Quality target

The notes must be:

- concise in wording;
- complete in concept coverage;
- accurate and version-aware;
- example-first and observable;
- ordered from foundation to advanced behavior;
- useful for revision, debugging, interviews, and practical work.

Be detailed through coverage and examples, not through long paragraphs.
Concise does not mean shallow or incomplete.

## Writing rules

- Start directly with `# <SUBJECT> - <TOPIC>` or another short descriptive title.
- Teach one concept per numbered section.
- Use short headings and one to three short explanatory sentences.
- State the rule before its example.
- Define each technical term at first use.
- Put every example immediately after the concept it teaches.
- Keep the concept, example, output, and explanation together.
- Use bullets for rules and tables for compact comparisons.
- Use precise language. Do not simplify a rule until it becomes false.
- Explain the reason only when it improves understanding.
- End with a compact mental model, decision guide, or cheat sheet.
- Remove greetings, filler, praise, motivational text, repetition, and long
  introductions.
- Do not force generic sections such as learning goals, prerequisites,
  vocabulary, practice exercises, or interview questions when they add no value.
- Do not use a fixed textbook template for every topic.
- Do not repeat the same fact in an introduction, example section, mistake
  section, summary, and checklist.

## Required concept pattern

For every concept with observable behavior, use this exact order:

### `<CONCEPT NAME>`

`<ONE TO THREE SHORT SENTENCES THAT STATE THE RULE>`

```<language>
<SMALLEST COMPLETE, RUNNABLE, FOCUSED EXAMPLE>
<USE print() OR AN EQUIVALENT OBSERVABLE RESULT>
```

Output:

```text
<EXACT OUTPUT>
```

`<ONE TO THREE SHORT SENTENCES OR BULLETS EXPLAINING WHY>`

Do not teach several executable concepts and move their examples to a distant
"Examples" section.

## Example quality rules

- Every important executable concept must have an example.
- Use concrete values and meaningful names.
- Make each example test one primary idea.
- Make examples complete and runnable in the stated environment.
- Use current, stable, non-deprecated syntax and APIs.
- Prefer a direct example over placeholder output such as
  `print("example")`, `print("public api")`, or `print("package metadata")`.
- The output must prove the rule being taught.
- Never hide output only in a source comment.
- Do not use unexplained imports, functions, types, or syntax.
- Keep setup small. If setup becomes large, choose a smaller demonstration.
- Use separate examples when combining concepts would obscure the lesson.
- After a failing example, show the corrected approach immediately.

## Deterministic output rules

- Every `Output:` block must match the code exactly.
- Do not invent or approximate output.
- Do not print unstable raw values such as memory addresses, object IDs,
  timestamps, random values, temporary paths, process IDs, unordered sets, or
  environment-specific bytecode.
- Demonstrate unstable concepts with stable comparisons, type names, sorted
  values, or Boolean checks.
- Sort unordered collections before printing when order is not guaranteed.
- If exact output genuinely depends on a platform, version, external service, or
  installed package, state the dependency before the example and describe only
  the guaranteed result.
- Never present environment-dependent output as universal.

## Error-teaching rules

When teaching an error:

1. show the smallest failing operation;
2. catch only the expected exception when a runnable note needs to continue;
3. print a stable exception type or message;
4. explain the exact cause;
5. show the corrected code immediately;
6. show the corrected output.

Label intentionally incorrect code clearly. Never leave the reader with only an
incorrect example. Never recommend broad exception suppression.

## Configuration, file, and command examples

Some concepts require multiple files, configuration, or shell commands instead
of a standalone program.

- Label every file snippet with its path or filename.
- Show the smallest valid file structure when package layout matters.
- Keep configuration internally consistent across snippets.
- Place the consumer or verification command immediately after configuration.
- Use an observable result when it is deterministic.
- Do not fabricate exact installer, compiler, network, or operating-system
  output.
- For commands with variable output, state the expected artifact or guaranteed
  outcome instead of claiming an exact transcript.
- Distinguish source code, configuration, commands, and output with correct fence
  languages such as `python`, `toml`, `text`, or `bash`.
- Never call a contextual fragment independently runnable when it requires files
  or installation shown elsewhere.

## Coverage order

Use this order when applicable, omitting only genuinely irrelevant parts:

1. core truth or mental model;
2. basic syntax and behavior;
3. main types, operations, or protocol;
4. execution, state, or memory behavior;
5. common combinations and practical use;
6. failure cases and edge cases;
7. safety, performance, and maintainability rules;
8. commonly misunderstood or interview-tested behavior;
9. final mental model, decision table, or compression.

For a broad topic, cover all major concepts with short explanations and small
examples. Do not write deeply about three concepts while silently omitting the
rest.

## Related-note and series rules

When creating or revising several related notes:

- give each note one clear responsibility;
- keep detailed teaching in the primary note for that concept;
- mention related behavior briefly and link or name the primary note;
- avoid copying the same full explanation into several files;
- use consistent terminology, headings, code style, and output formatting;
- update the roadmap or index when note names or study order change;
- preserve useful existing material unless it is inaccurate, duplicated, or
  outside scope.

## Visual rules

- Use a table for comparisons, mappings, choices, or compact reference data.
- Use Mermaid only when sequence, hierarchy, state, or dependency flow is clearer
  visually than in prose.
- Introduce and explain every useful diagram.
- Do not add decorative diagrams, emoji-heavy headings, or visuals that duplicate
  nearby text.
- Use the smallest visual that teaches the relationship.

## Python-specific rules

Apply these only when the subject is Python:

- Target Python 3.12+ unless another version is specified.
- Use `snake_case` names, `PascalCase` classes, and `UPPER_SNAKE_CASE` constants.
- Use type hints where they improve the contract, not as decoration.
- Distinguish names, objects, values, types, identity, mutation, and rebinding
  precisely.
- Do not describe implementation details as language guarantees.
- Mark CPython-specific behavior explicitly.
- Prefer explicit validation; do not silently coerce invalid external input.
- Use specific exceptions and deterministic cleanup.
- Ensure normal examples are compatible with Ruff formatting and static analysis.

## Practice rules

Add exercises only when requested.

When requested:

- place all unanswered questions before solutions;
- include prediction, debugging, implementation, and practical questions;
- do not test concepts that the notes did not teach;
- give runnable solutions with exact output where applicable.

## Verification before returning

Silently perform this final audit:

### Coverage

- Every requested concept is present.
- Foundational terms are introduced before advanced use.
- Important edge cases and failure modes are covered.
- Related notes have clear, non-duplicated boundaries.

### Examples

- Every important executable concept has an adjacent example.
- Every example is focused, complete, and non-placeholder.
- Every `print()` result matches its `Output:` block exactly.
- Every error example has a cause and correction.
- Every contextual multi-file example states its required setup.

### Accuracy

- APIs and syntax are current for the requested version.
- Language guarantees are separated from implementation details.
- No fact, command, file, output, citation, or behavior was invented.
- Security and validation advice is explicit at external boundaries.

### Presentation

- Paragraphs are short and direct.
- Repetition and filler are removed.
- Tables, headings, links, and code fences render correctly.
- The final summary introduces no new concepts.

If tools are available, execute every standalone code example and compare actual
standard output with the documented output. Fix every mismatch before returning.
For contextual package or configuration examples, validate their internal
consistency and clearly state why they are not standalone.

Return only the finished Markdown notes. Do not describe your process, include
this prompt, or wrap the entire response in one code fence.
````
