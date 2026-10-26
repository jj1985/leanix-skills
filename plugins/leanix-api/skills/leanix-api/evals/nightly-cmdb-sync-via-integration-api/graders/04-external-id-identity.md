---
type: llm
focus: trace
weight: 1
---

Server content items use the CSV serial as their id, the processors identify fact sheets by external id (identifier.external with an external-id field), and the relation resolves the Application by its app_id external id, so re-runs update instead of duplicating; Application items may be opt-in
