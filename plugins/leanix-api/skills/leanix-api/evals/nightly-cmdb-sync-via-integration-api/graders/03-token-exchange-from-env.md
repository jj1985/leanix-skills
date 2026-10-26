---
type: llm
focus: trace
weight: 1
---

The script exchanges an API token read from an environment variable at /services/mtm/v1/oauth2/token with HTTP Basic apitoken:<token> and grant_type=client_credentials, sends Authorization: Bearer afterwards, and never prints the token
