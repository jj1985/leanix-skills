---
type: llm
focus: trace
weight: 1
---

setup.md states the access token lives 3600 seconds and that the job caches it and repeats the token exchange shortly before expiry or once on a 401, instead of requesting a new token for every call
