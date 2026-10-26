---
type: llm
focus: trace
weight: 1
---

sync_servers.py sends an LDIF document to POST .../services/integration-api/v1/synchronizationRuns (with start=true or a subsequent /start call) instead of creating fact sheets one by one with GraphQL createFactSheet
