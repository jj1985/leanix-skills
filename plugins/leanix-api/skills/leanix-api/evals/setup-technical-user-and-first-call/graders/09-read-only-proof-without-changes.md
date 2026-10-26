---
type: llm
focus: trace
weight: 1
---

setup.md includes a check that proves the credential cannot write, without changing data, such as an updateFactSheet call with validateOnly: true that must be refused, or decoding the JWT to show the VIEWER role
