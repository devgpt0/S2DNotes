# Java Stream API - Complete Learning Roadmap

Streams describe data-processing pipelines. They do not store elements and they do not replace collections.

## Learning Order

1. [Stream mental model and pipeline](01-stream-mental-model-and-pipeline.md)
2. [Creating streams](02-creating-streams.md)
3. [Stateless intermediate operations](03-stateless-intermediate-operations.md)
4. [Stateful and short-circuit operations](04-stateful-and-short-circuit-operations.md)
5. [Terminal operations and reduction](05-terminal-operations-and-reduction.md)
6. [`map`, `flatMap`, and `Optional`](06-map-flatmap-and-optional.md)
7. [Collectors](07-collectors.md)
8. [Grouping, partitioning, and downstream collectors](08-grouping-partitioning-and-downstream-collectors.md)
9. [Primitive streams and numeric work](09-primitive-streams-and-numeric-work.md)
10. [Parallel streams](10-parallel-streams.md)
11. [Debugging, errors, and performance](11-debugging-errors-and-performance.md)
12. [Recipes, interview questions, and practice](12-recipes-interview-and-practice.md)

## Core Rule

A stream pipeline should be a clear, side-effect-free transformation. If a loop is easier to read or requires complex mutation and early control flow, use the loop.
