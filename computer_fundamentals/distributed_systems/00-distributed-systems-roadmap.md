# Distributed Systems Roadmap

This track explains how independent machines coordinate despite latency, partial failure, duplication, and partitions.

1. [CAP, consensus, Raft, Paxos, and leader election](01-cap-consensus-raft-paxos-and-leader-election.md)
2. [Replication, partitioning, sharding, and consistent hashing](02-replication-sharding-partitioning-and-consistent-hashing.md)
3. [Event sourcing, Kafka, RabbitMQ, and Redis](03-events-streams-queues-and-redis.md)
4. [Exactly-once semantics, transactions, and interview preparation](04-exactly-once-semantics-and-interview-preparation.md)

## Learning Flow

```text
one-machine correctness -> replicas -> partitions -> coordination -> delivery semantics -> operations
```

## Mastery Outcome

You can distinguish consistency models from durability, choose a replication/partitioning strategy, explain consensus honestly, design idempotent message processing, and discuss failure behavior without claiming impossible guarantees.

[Return to Computer Fundamentals](../README.md)

