# Computer Architecture Roadmap

This track explains why the same source-level operation can have very different costs on real hardware.

1. [CPU execution, pipelines, branches, assembly, and compilers](01-cpu-execution-pipeline-branches-and-compilers.md)
2. [Caches, locality, virtual memory, TLB, alignment, and false sharing](02-memory-caches-locality-and-virtual-memory.md)
3. [SIMD, NUMA, and performance-aware parallel design](03-simd-numa-and-parallel-hardware.md)
4. [Architecture interview preparation and diagnosis](04-architecture-interview-preparation.md)

## Learning Flow

```text
instruction -> pipeline -> cache/TLB -> memory -> multiple cores -> NUMA nodes
```

## Mastery Outcome

You can explain latency versus throughput, predict why branchy or pointer-heavy work can be slow, reason about cache and NUMA locality, and turn a performance symptom into a measured hardware-aware hypothesis.

[Return to Computer Fundamentals](../README.md)

