---
type: llm
focus: trace
weight: 1
---

The script polls GET /synchronizationRuns/{id}/status until a terminal state that includes STOPPED as well as FINISHED and FAILED, reads /warnings, and exits with a non-zero code when the run fails or reports ERROR warnings
