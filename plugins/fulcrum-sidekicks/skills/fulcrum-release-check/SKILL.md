---
name: fulcrum-release-check
description: "Track and verify an authorised software release through source, checks, publication, deployment and live behaviour. Use when release completion or a disputed deployment status needs evidence."
---

# Verify a release from source to live

Start from the authorised release scope and the project's runbook. Identify the source revision, required checks, publication target, expected deployed revision and health checks. Inspect current configuration and recent successful operations before choosing an access route.

Preserve the current release and a practical rollback reference. Check required migrations or other prerequisites before promoting an artifact. Use the established authenticated path; a failed connection is evidence about that attempt, not proof that every authorised route is unavailable.

Publish and deploy only within the user's existing authority. Do not change unrelated secrets, network policy or service configuration to make a release easier. Keep immutable revision or image identifiers rather than relying on a mutable latest tag.

Verify the rollout's actual revision, required service health and the user-visible behaviour. Account for caches and redirects when comparing content. If a timeout follows a mutation, inspect its result before issuing the mutation again.

Report source revision, checks, published revision, deployed revision and live verification separately. Mark unperformed stages pending. A confirmed blocker needs evidence and a concrete next action, not an invented ETA or a claim that waiting will resolve a missing prerequisite.

## Product reference

Use the [current product guide](https://fulcrumcortex.github.io/documentation/code/) for interface details. Discover the tools available in this environment; the skill itself supplies no credentials or integration.
