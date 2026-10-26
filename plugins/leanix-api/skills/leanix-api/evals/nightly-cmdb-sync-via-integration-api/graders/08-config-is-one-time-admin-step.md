---
type: llm
focus: trace
weight: 1
---

Installing or updating the processor configuration is a separate, one-time Admin step (UI or PUT /configurations) rather than something every nightly run does, so the nightly job is not forced to run with an Admin token just to upload configuration
