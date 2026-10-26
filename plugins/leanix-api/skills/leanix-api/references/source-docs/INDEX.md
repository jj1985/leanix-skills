# SAP LeanIX Official Documentation Snapshot

This folder is an offline snapshot of 30 official SAP LeanIX documentation pages, captured on
**2026-10-26** from the SAP Help Portal (`https://help.sap.com/docs/leanix/ea/...`), which is the
current home of both the SAP LeanIX user/administrator guide and the Developer Guide (API reference).
The content is owned by SAP SE and is reproduced here for offline reference inside this skill only.
Pages change frequently; always check the live documentation for the current version. Each file starts
with a three-line HTML comment giving the source URL, the capture date and the product. Site chrome
(navigation, header/footer, cookie banner, feedback widget, "On this page" box, icon-font glyphs) was
removed; all headings, body text, tables, code samples, parameter descriptions and example payloads were
kept as rendered, and images are kept as links to their original SAP Help Portal URLs. Total size is
about 335 KB.

File naming: `docs__<slug>.md` = user/administrator documentation; `api__<slug>.md` = developer/API
reference. The `<slug>` is the last path segment of the source URL.

## Documentation hubs used

| Hub | Role | Notes |
| --- | --- | --- |
| https://help.sap.com/docs/leanix | SAP LeanIX product documentation on the SAP Help Portal | Canonical location of every page in this snapshot (`/docs/leanix/ea/<slug>`). User guide, administrator guide and Developer Guide all live here. |
| https://help.sap.com/docs/leanix/ea/developer-guide | Developer Guide landing page | Entry point to Basics (authentication, base URL), Guides and Tutorials, SAP LeanIX APIs, Reporting Library and Custom Report Tools, MCP Server. |
| https://help.sap.com/docs/leanix/ea/sap-leanix-apis | SAP LeanIX APIs overview | Index of REST, GraphQL and Integration APIs (captured as `api__sap-leanix-apis.md`). |
| https://app.leanix.net/openapi-explorer/ | OpenAPI (Swagger) explorer for all REST services | Interactive JavaScript application linked from the docs (Help menu > Developer Tools > OpenAPI Documentation). It has no static documentation page and was therefore not captured. |
| https://docs-eam.leanix.net/ and https://docs.leanix.net/ | Former SAP LeanIX documentation hosts | Both now redirect permanently to the SAP Help Portal (see below). |

## URL redirects observed (2026-10-26)

| Requested URL | Response | Redirect target |
| --- | --- | --- |
| `https://docs-eam.leanix.net/docs/<slug>` (e.g. `/docs/technical-users`) | HTTP 301 | `https://help.sap.com/docs/leanix/ea/<slug>` |
| `https://docs.leanix.net/docs/<slug>` | HTTP 301 | `https://help.sap.com/docs/leanix/ea/<slug>` |
| `https://docs-eam.leanix.net/reference` | HTTP 301 | `https://help.sap.com/docs/leanix/ea/developer-guide` |
| `https://docs-eam.leanix.net/reference/<slug>` | HTTP 301 | `https://help.sap.com/docs/leanix/ea/<slug>` (same slug namespace as `/docs/`) |

Links inside the captured pages point to `help.sap.com` URLs with the query string
`?locale=en-US&state=PRODUCTION&version=CLOUD`; these are the live pages and are left untouched.
Links to non-SAP sites are routed through `https://help.sap.com/docs/link-disclaimer?site=...` by the portal.

## User and administration documentation (`docs__`)

| File | Title | Source URL | Status | Size (approx KB) |
| --- | --- | --- | --- | --- |
| `docs__authorization-model.md` | Authorization Model | https://help.sap.com/docs/leanix/ea/authorization-model | Captured (HTTP 200) | 19.9 |
| `docs__importing-and-exporting-data.md` | Importing and Exporting Data | https://help.sap.com/docs/leanix/ea/importing-and-exporting-data | Captured (HTTP 200) | 4.3 |
| `docs__meta-model-configuration.md` | Meta Model Configuration | https://help.sap.com/docs/leanix/ea/meta-model-configuration | Captured (HTTP 200) | 19.5 |
| `docs__technical-users.md` | Technical Users | https://help.sap.com/docs/leanix/ea/technical-users | Captured (HTTP 200) | 4.6 |
| `docs__user-roles-and-permissions.md` | User Roles and Permissions | https://help.sap.com/docs/leanix/ea/user-roles-and-permissions | Captured (HTTP 200) | 13.3 |
| `docs__workspace-administration.md` | Workspace Administration | https://help.sap.com/docs/leanix/ea/workspace-administration | Captured (HTTP 200) | 5.5 |

## Developer and API reference (`api__`)

| File | Title | Source URL | Status | Size (approx KB) |
| --- | --- | --- | --- | --- |
| `api__authentication-to-sap-leanix-services.md` | Authentication to SAP LeanIX Services | https://help.sap.com/docs/leanix/ea/authentication-to-sap-leanix-services | Captured (HTTP 200) | 9.6 |
| `api__base-url.md` | Base URL | https://help.sap.com/docs/leanix/ea/base-url | Captured (HTTP 200) | 0.7 |
| `api__connecting-to-mcp-server.md` | Connecting to the MCP Server | https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server | Captured (HTTP 200) | 7.2 |
| `api__custom-reports.md` | Custom Reports | https://help.sap.com/docs/leanix/ea/custom-reports | Captured (HTTP 200) | 3.9 |
| `api__error-handling-in-graphql.md` | Error Handling in GraphQL | https://help.sap.com/docs/leanix/ea/error-handling-in-graphql | Captured (HTTP 200) | 5.0 |
| `api__filtering-in-graphql.md` | Filtering in GraphQL | https://help.sap.com/docs/leanix/ea/filtering-in-graphql | Captured (HTTP 200) | 16.4 |
| `api__getting-started-with-integration-api.md` | Getting Started with the Integration API | https://help.sap.com/docs/leanix/ea/getting-started-with-integration-api | Captured (HTTP 200) | 8.8 |
| `api__graphql-api.md` | GraphQL API | https://help.sap.com/docs/leanix/ea/graphql-api | Captured (HTTP 200) | 12.1 |
| `api__graphql-basics.md` | GraphQL Basics | https://help.sap.com/docs/leanix/ea/graphql-basics | Captured (HTTP 200) | 9.8 |
| `api__inbound-processors.md` | Inbound Processors | https://help.sap.com/docs/leanix/ea/inbound-processors | Captured (HTTP 200) | 61.8 |
| `api__integration-api.md` | Integration API | https://help.sap.com/docs/leanix/ea/integration-api | Captured (HTTP 200) | 20.2 |
| `api__integration-rest-api.md` | Integration REST API | https://help.sap.com/docs/leanix/ea/integration-rest-api | Captured (HTTP 200) | 11.5 |
| `api__mcp-server.md` | MCP Server | https://help.sap.com/docs/leanix/ea/mcp-server | Captured (HTTP 200) | 5.8 |
| `api__metrics.md` | Metrics | https://help.sap.com/docs/leanix/ea/metrics | Captured (HTTP 200) | 7.5 |
| `api__migrating-from-fact-sheets-rest-api-to-graphql-api.md` | Migrating from the Fact Sheets REST API to the GraphQL API | https://help.sap.com/docs/leanix/ea/migrating-from-fact-sheets-rest-api-to-graphql-api | Captured (HTTP 200) | 16.7 |
| `api__pagination-in-graphql.md` | Pagination in GraphQL | https://help.sap.com/docs/leanix/ea/pagination-in-graphql | Captured (HTTP 200) | 5.1 |
| `api__quick-start-guide-for-mcp-server.md` | Quick Start Guide for the MCP Server | https://help.sap.com/docs/leanix/ea/quick-start-guide-for-mcp-server | Captured (HTTP 200) | 6.3 |
| `api__rate-limiting.md` | Rate Limiting | https://help.sap.com/docs/leanix/ea/rate-limiting | Captured (HTTP 200) | 6.0 |
| `api__reporting-framework-and-cli.md` | Reporting Library and Custom Report Tools | https://help.sap.com/docs/leanix/ea/reporting-framework-and-cli | Captured (HTTP 200) | 6.4 |
| `api__rest-apis-overview.md` | REST APIs Overview | https://help.sap.com/docs/leanix/ea/rest-apis-overview | Captured (HTTP 200) | 9.7 |
| `api__sap-leanix-apis.md` | SAP LeanIX APIs | https://help.sap.com/docs/leanix/ea/sap-leanix-apis | Captured (HTTP 200) | 6.5 |
| `api__webhook-events.md` | Webhook Events | https://help.sap.com/docs/leanix/ea/webhook-events | Captured (HTTP 200) | 4.5 |
| `api__webhook-payloads.md` | Webhook Payloads | https://help.sap.com/docs/leanix/ea/webhook-payloads | Captured (HTTP 200) | 21.4 |
| `api__webhooks.md` | Webhooks | https://help.sap.com/docs/leanix/ea/webhooks | Captured (HTTP 200) | 4.6 |

## Not captured

No requested page failed to download (every fetched page returned HTTP 200). The following requested
topics have no dedicated official page, or exist only in a form that cannot be captured as a document:

| Topic | Reason / where to look instead |
| --- | --- |
| Regional hosts / instance list (EU, US, AU, CA, CH, AE, BR, demo) | No dedicated page exists on the SAP Help Portal (web search plus a scan of the full 688-page navigation found none). The official guidance is the **Base URL** page (`api__base-url.md`), which documents the pattern `https://{SUBDOMAIN}.leanix.net` and says to copy the subdomain from the workspace URL. The MCP pages document the separate host `mcp.leanix.net`. |
| REST `models/dataModel` endpoint reference | REST endpoint parameters are published only in the interactive OpenAPI explorer (`https://app.leanix.net/openapi-explorer/`), a JavaScript application with no static page. The user documentation of the same concepts was captured instead (`docs__meta-model-configuration.md`). |
| MTM / user-management REST API reference | Same reason (OpenAPI explorer only). `api__rest-apis-overview.md` lists the MTM API and its purpose, and `api__authentication-to-sap-leanix-services.md` documents its OAuth2 token endpoint (`/services/mtm/v1/oauth2/token`). |
| Pathfinder REST export API reference | Same reason (OpenAPI explorer only). `api__rest-apis-overview.md` lists the Pathfinder API; the Excel import/export user documentation was captured (`docs__importing-and-exporting-data.md`). |
| Developer Guide landing page (`https://help.sap.com/docs/leanix/ea/developer-guide`) | Fetched successfully but deliberately omitted: it is a short list of links only; its content is fully covered by `api__sap-leanix-apis.md` and `api__rest-apis-overview.md`. |

## Topic coverage map

| Requested topic | Files |
| --- | --- |
| 1. Authentication / access token with API token | `api__authentication-to-sap-leanix-services.md`, `api__base-url.md` |
| 2. Technical users / API tokens | `docs__technical-users.md` |
| 3. User roles and permissions | `docs__user-roles-and-permissions.md` |
| 4. Access control / data-level restrictions | `docs__authorization-model.md` (see also `docs__technical-users.md` for Access Control Entities on technical users) |
| 5. Regional hosts / instances | not available as a page; see `api__base-url.md` and "Not captured" |
| 6. Administration overview | `docs__workspace-administration.md` |
| 7. GraphQL API introduction / GraphiQL | `api__graphql-api.md`, `api__graphql-basics.md`, `api__sap-leanix-apis.md` |
| 8. GraphQL queries, filters, pagination | `api__filtering-in-graphql.md`, `api__pagination-in-graphql.md`, `api__graphql-basics.md` |
| 9. GraphQL mutations (create/update/patches/relations/archive) | `api__graphql-basics.md`, `api__migrating-from-fact-sheets-rest-api-to-graphql-api.md`, `api__error-handling-in-graphql.md` |
| 10. Data model / meta model configuration | `docs__meta-model-configuration.md` |
| 11. Integration API overview / LDIF | `api__integration-api.md`, `api__getting-started-with-integration-api.md` |
| 12. Inbound processors and JUEL expressions | `api__inbound-processors.md` |
| 13. Integration API runs / configuration / results | `api__integration-rest-api.md`, `api__getting-started-with-integration-api.md` |
| 14. Webhooks (subscriptions, events, payloads) | `api__webhooks.md`, `api__webhook-events.md`, `api__webhook-payloads.md` |
| 15. Metrics API | `api__metrics.md` |
| 16. MTM / user management API | `api__rest-apis-overview.md` (overview only; see "Not captured") |
| 17. Excel import/export, Pathfinder export | `docs__importing-and-exporting-data.md`, `api__rest-apis-overview.md` |
| 18. Rate limits | `api__rate-limiting.md` |
| 19. Reporting framework / custom reports | `api__reporting-framework-and-cli.md`, `api__custom-reports.md` |
| 20. MCP server / AI agent integration | `api__mcp-server.md`, `api__quick-start-guide-for-mcp-server.md`, `api__connecting-to-mcp-server.md` |
| 21. API index / landing page | `api__sap-leanix-apis.md`, `api__rest-apis-overview.md` |
