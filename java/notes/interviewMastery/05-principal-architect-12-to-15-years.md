# 05 - Principal / Architect Coverage: 12 to 15 Years

## Architecture Portfolio

- target architecture tied to business capabilities
- modernization sequencing and coexistence with legacy systems
- platform strategy, golden paths, and exception governance
- data governance, residency, privacy, retention, and lineage
- multi-region and disaster-recovery strategy
- dependency concentration and vendor risk

## Economics and Risk

- total cost of ownership and engineering opportunity cost
- unit economics per request/customer/workload
- capacity commitments vs elasticity
- security and compliance risk acceptance
- reversible vs irreversible decisions
- decommissioning plan and migration completion criteria

## Evolutionary Architecture

Use fitness functions to automatically verify important properties such as dependency rules, API compatibility, vulnerability thresholds, latency budgets, and module boundaries.

```java
@Test
void domainDoesNotDependOnWeb() {
    noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAPackage("..web..")
            .check(importedClasses);
    // Test output: passes only while the dependency direction remains valid.
}
```

## Principal-Level Interview Signals

- navigates technical and organizational constraints
- changes direction when evidence disproves an assumption
- creates leverage across multiple teams
- balances standardization with local autonomy
- can go from executive outcome to JVM/database/incident detail
- owns long-term outcomes, not only architecture documents

Avoid presenting scale, microservices, cloud, AI, or event-driven design as goals by themselves. State the business and reliability problem they solve.
