---
tags: [leanix-api]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We're building a nightly job that reads all Applications and their IT Components out of our SAP LeanIX workspace (it's at https://acme-eu.leanix.net/acmeprod) and loads them into our data warehouse. Security asked for a least-privilege service identity, not someone's personal login. Write me the full admin setup as setup.md: how to create the credential in LeanIX with the right role, how our script authenticates, and a curl sequence that proves it works end to end (get a token, then fetch one application with its IT components). Include what to do when the token stops working after a while.
