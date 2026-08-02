# Design a Ride-Sharing Location and Dispatch Service

> **Difficulty:** Hard  
> **Main focus:** geospatial indexing, freshness, matching

## Interview prompt

Design driver location updates, nearby-driver search, and ride dispatch.

## 1. Clarify the scope

**What I would say first:** Location is high-volume ephemeral state, while trip assignment is a strongly controlled durable workflow.

### Functional requirements

- Receive frequent driver location and availability updates.
- Find suitable nearby drivers for a ride request.
- Offer a ride to drivers and commit exactly one assignment.
- Track trip state and tolerate mobile disconnections.

### Out of scope for the first version

- Exact route optimization and pricing models are separate services.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume millions of active drivers updating every few seconds.
- Location data expires quickly; stale drivers must not be dispatched.
- Dense city cells become hot while rural searches expand farther.

## 3. API and data model

### Main contracts

- PUT /v1/drivers/{id}/location {lat, lon, heading, timestamp, sequence}
- POST /v1/rides {pickup, destination, requestId}
- POST /v1/offers/{id}/accept

### Important data

- DriverPresence(driver_id, cell_id, location, last_sequence, expires_at, availability)
- Ride(ride_id, rider_id, pickup, destination, state, assigned_driver_id, version)
- Offer(offer_id, ride_id, driver_id, expires_at, state)

## 4. High-level design

```text
driver app -> location gateways -> stream -> regional geo index
                                              -> history archive

rider -> ride API -> dispatch orchestrator -> nearby search
                              |                    |
                              +-> offer service -> driver connections
                              +-> transactional ride database
```

## 5. Critical request flow

1. Driver updates include monotonic sequence numbers; reject older coordinates.
2. Dispatch queries nearby cells, filters stale or unsuitable drivers, and ranks candidates.
3. Offer to a small batch with short expiries rather than broadcasting to everyone.
4. Accept uses an atomic compare-and-set on the ride and driver availability.
5. Notify winner and losers, then persist every trip state transition.

## 6. Deep dive

- Use geohash, S2, or H3-like hierarchical cells so nearby search expands ring by ring.
- The geo index is disposable derived state; rebuild it from fresh driver streams.
- Assignment correctness lives in the ride database, not the eventually consistent geo index.
- Location timestamps use server receipt plus device timestamp checks to resist replay.

## 7. Scaling, failures, and observability

- If a driver disconnects before pickup, the workflow can time out and rematch.
- Regional dispatch stays local for latency; cross-region ride state needs clear ownership.
- Backpressure drops intermediate location updates but preserves each driver's newest state.
- Monitor location age, offer acceptance latency, rematch rate, hot cells, and assignment conflicts.

## 8. Security and privacy

- Authorize drivers and riders, minimize precise-location retention, and restrict employee access.
- Detect impossible movement and spoofed updates.
- Hide exact driver location until product policy allows disclosure.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Broadcast offers | Fast match but poor driver experience and high traffic. |
| Small sequential batches | Controlled load with potentially longer matching. |
| Strong location consistency | Unnecessary and too expensive. |
| Strong assignment transaction | Required to prevent double booking. |

## 10. 60-second interview summary

Fresh driver locations live in a regional hierarchical geo index, while durable trip state lives in a transactional database. Dispatch searches and ranks nearby candidates, then an atomic acceptance transition guarantees only one driver wins.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

