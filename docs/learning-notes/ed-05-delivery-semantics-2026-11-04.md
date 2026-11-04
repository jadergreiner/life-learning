# ED-05 — Reliability diagnostic: delivery guarantees (2026-11-04)

## Scope and authority

Technical learning notes for the Life Learning adaptive-method pilot. This file contains generalized engineering takeaways, **not** private student responses, personal assessment, or official session metadata. The Notion competency catalog is authoritative for individual evidence and the official cadence remains eight positions. The three-position model remains a consultative pilot, without migration.

## Design concepts exercised

- Transactional Outbox: a database commit and an external HTTP effect are distinct; an HTTP 200 followed by a crash before local acknowledgment creates an ambiguous outcome.
- Worker coordination: persisted ownership with lease expiry allows recovery eligibility; takeover must be atomic. A stale worker must not confirm work after losing ownership; conditional updates and fencing generations protect local state.
- At-least-once may fit high-criticality financial alerts where omission is less acceptable than a duplicate, provided business risk is assessed; it does not guarantee the recipient read or received the notice.
- At-most-once can fit marketing notifications where duplicates are costly and omission is acceptable. Persist a durable **attempt authorization before** the external call; avoid retries after uncertain outcomes. A reservation is not proof of delivery.
- A queue such as SQS Standard may redeliver; merely reading then inserting a control record is subject to race. Enforce unique business identity and atomic claim across workers.
- Reconciliation requires independent and trustworthy evidence; where a provider has neither status querying nor idempotency, uncertainty may be irreducible.

## Outstanding implementation exercise — ED-05 / Q1.13-A

Given two workers observing no attempt record for EVT-123 concurrently, specify an atomic database operation granting at most one attempt. State exactly what happens if the winner crashes after the durable reservation but before HTTP. Provide:
1. Schema, uniqueness constraints, and transaction boundaries.
2. Algorithm for attempting/not attempting HTTP.
3. Positive and negative concurrency tests (including worker crash and SQS duplicate redelivery).
4. Observable states, metrics, and explicit guarantee limitations.
5. Trade-off defense based on event criticality.

No implemented solution, reproducible tests, or N3 autonomy is asserted in this document.

See the [Notion competency catalog](https://app.notion.com/p/40c02f2729f981c2bb7acd89a631d32c) for the authoritative pedagogical evidence.
