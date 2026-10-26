---
type: llm
focus: trace
weight: 1
---

eol_report.py authenticates via POST /services/mtm/v1/oauth2/token with HTTP Basic apitoken:<API token> and grant_type=client_credentials, then sends Authorization: Bearer to /services/pathfinder/v1/graphql
