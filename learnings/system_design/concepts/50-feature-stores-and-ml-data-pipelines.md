# Feature Stores and ML Data Pipelines

## Idea

An ML feature is a value used by a model, such as `orders_in_last_30_days`.

A reliable feature platform calculates features consistently for:

- training, where historical data is needed;
- inference, where the latest value is needed quickly.

The hardest problem is not storing features. It is preventing training data from accidentally using information that was unavailable at prediction time.

## Visual model

```text
Databases / events / files
           |
     batch + stream jobs
           |
   validated feature definitions
          / \
         /   \
offline store  online store
(training)     (inference)
      |             |
model training   prediction API
```

## Design steps

1. Define the entity, feature value, and event timestamp explicitly.
2. Validate source schemas and reject invalid records.
3. Use point-in-time joins so each training row sees only past information.
4. keep one feature definition for offline and online computation where practical.
5. Store feature versions, owners, lineage, and freshness expectations.
6. Support deterministic backfills and replay from immutable source data.
7. Monitor freshness, missing values, distribution drift, and training-serving skew.

## When to use it

Use a feature store when several models reuse features or predictions require fresh, low-latency values.

For one small batch model, a validated data pipeline may be simpler than a full feature platform.

## Important time concepts

- **Event time:** when the real-world event happened.
- **Processing time:** when the platform processed it.
- **Availability time:** when the value became usable by the model.

Training joins normally need event time and availability time to avoid leakage.

## Trade-offs

- Streaming features improve freshness but increase operational complexity.
- An online store reduces inference latency but adds cost and consistency work.
- Shared features improve reuse but need strong ownership and versioning.

## Common mistakes

- Using future information in training data.
- Implementing the same feature differently in training and inference.
- Overwriting data needed for replay or audits.
- Ignoring late and out-of-order events.
- Adding a feature store before reuse or latency justifies it.
