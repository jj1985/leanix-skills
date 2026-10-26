# Webhooks, Metrics, Import/Export, Pathfinder REST, MCP server and reporting

The services around the GraphQL and Integration APIs. All use the same base URL
`https://{SUBDOMAIN}.leanix.net` and the same bearer token (`auth-and-access.md`). Facts come from
the SAP Help Portal and the live OpenAPI specifications (October 2026); **(unconfirmed)** marks
inference or community sources. Every service has an interactive reference in the OpenAPI explorer
(help menu > Developer Tools > OpenAPI Documentation).

## Contents

1. [Webhooks API](#1-webhooks-api)
2. [Metrics API v2](#2-metrics-api-v2)
3. [Import/Export API (Excel, LDIF, OData)](#3-importexport-api-excel-ldif-odata)
4. [Pathfinder REST beyond GraphQL](#4-pathfinder-rest-beyond-graphql)
5. [MTM API](#5-mtm-api)
6. [MCP server](#6-mcp-server)
7. [Custom reports and the reporting library](#7-custom-reports-and-the-reporting-library)
8. [Surveys, to-dos, automations and the rest](#8-surveys-to-dos-automations-and-the-rest)

---

## 1. Webhooks API

Base `/services/webhooks/v1`. Webhooks are called **subscriptions**. Managing them needs an Admin
(Administration > **Webhooks** > **New Webhook**, or the API).

| Method and path | Purpose |
|---|---|
| `GET /subscriptions`, `GET /subscriptions/{id}` | List / read |
| `POST /subscriptions` | Create (body below); `PUT /subscriptions/{id}` update; `DELETE /subscriptions/{id}` |
| `GET /subscriptions/status`, `GET /subscriptions/{id}/status` | Health (error counts, last delivery status) |
| `GET /subscriptions/{id}/deliveries` | PUSH delivery log (request headers, payload, HTTP status, response, duration); kept 30 days |
| `GET /subscriptions/{id}/events?autoCommit=false` | PULL: next batch of events; `PUT /subscriptions/{id}/cursor` with `{"offset": N}` acknowledges them (or `autoCommit=true`, which waives at-least-once) |
| `GET /eventTags` | The event tags available for `tagSets` in this workspace |
| `GET/POST/PUT/DELETE /customEventTags` | Custom event tags for your own events |
| `POST /events`, `POST /events/batch` | Publish your own events into the webhook bus |

Subscription body (discriminator `deliveryType`):

```json
{
  "identifier": "cmdb-sync-listener",
  "description": "Forward fact sheet changes to the CMDB connector",
  "visibility": "WORKSPACE",
  "deliveryType": "PUSH",
  "targetUrl": "https://hooks.example.com/leanix",
  "targetMethod": "POST",
  "authorization": {"type": "AUTH_HEADER", "authHeader": "Bearer <shared secret>"},
  "callback": "",
  "tagSets": [["pathfinder", "FACT_SHEET_UPDATED"], ["pathfinder", "FACT_SHEET_ARCHIVED"]],
  "workspaceConstraint": "WORKSPACE",
  "payloadMode": "DEFAULT",
  "active": true,
  "ignoreError": false,
  "deactivationNotificationEnabled": true
}
```

- `visibility`: `PRIVATE` (only the creator) or `WORKSPACE` (any admin may edit).
- `deliveryType`: `PUSH` (HTTP POST to `targetUrl`; `targetMethod`; `authorizationHeader` or
  `authorization` of type `AUTH_HEADER` / `OAUTH` with `oauthUrl`, `clientId`, `clientSecret`,
  `scopes`, `credentialsLocation`; LeanIX fetches a token from your IdP before calling you) or
  `PULL` (`maxBatchSize` in KiB, default 512; you poll). The type cannot be changed after creation.
- `tagSets`: a list of tag lists (`string[][]`); a subscription fires when an event carries all
  tags of one set. Fact sheet events are tagged with the source service and the event type, as in
  `["pathfinder", "FACT_SHEET_UPDATED"]`; `GET /eventTags` lists the tags of the workspace. In the
  UI, fact sheet events can be narrowed to one fact sheet type and integration events to one
  integration.
- `workspaceConstraint`: `WORKSPACE` (events of this workspace), `NO_WORKSPACE`, `ANY`.
- `payloadMode`: `DEFAULT`, `WRAPPED_EVENT` (the whole webhook event object), `NO_PAYLOAD`.
- `callback`: optional JavaScript executed before delivery; it can rewrite `payload`,
  `targetUrl`, `targetMethod` or set `active = false` to drop an event (used to filter
  `FACT_SHEET_FIELD_UPDATED` to specific fields).
- Delivery: a failed PUSH delivery (unreachable target or non-2xx) is **retried every 50 seconds
  until it succeeds** (at-least-once); `ignoreError: true` disables the retry. PUSH subscriptions are
  **deactivated automatically after more than 10 days of failed deliveries**; enable
  `deactivationNotificationEnabled` to be mailed. There is no `maxDeliveryRetries` setting.

Events (payload `type` values look like `FactSheetUpdatedEvent`): `FACT_SHEET_CREATED`,
`FACT_SHEET_UPDATED` (also for relation changes), `FACT_SHEET_VIEWED`, `FACT_SHEET_ARCHIVED`,
`FACT_SHEET_DELETED`, `FACT_SHEET_RECOVERED`, `FACT_SHEET_FIELD_UPDATED`, `FACT_SHEET_TAG_ADDED` /
`_REMOVED`, `RELATION_CREATED` / `_UPDATED` / `_ARCHIVED` / `_DELETED` / `RELATION_SWITCH`,
`DOCUMENT_*`, `SUBSCRIPTION_*`, `COMMENT_CREATED` / `COMMENT_REPLY_ADDED` / `COMMENT_DELETED`,
`INTEGRATION_RUN_STARTED` / `_FINISHED` / `_ABORTED`, `CONFIGURATION_*`, `AUTOMATION_TRIGGERED`,
`POLL_RESULT_*`, `TODO_*`. A fact sheet payload contains the full fact sheet (`id`, `rev`, `name`,
`type`, `status`, `fields`, `relations`, `tags`, `subscriptions`, `permittedReadACL`, ...),
`userId`, `workspaceId`, `transactionSequenceNumber`; maximum payload size 20 MB. There is no
documented signature header: authenticate deliveries with the configured authorization header or
IP restrictions on your side.

## 2. Metrics API v2

Base `/services/metrics/v2`. Time series attached to fact sheets, shown as charts and KPIs
(Administration > **Metrics**). V1 URLs keep working; v2 requires explicit schemas.

| Method and path | Purpose |
|---|---|
| `GET /schemas`, `POST /schemas` | List / create schemas: `{"name": "Availability", "description": "...", "attributes": [{"name": "availability", "type": "metric", "unit": "%"}, {"name": "factSheetId", "type": "dimension"}]}` returns `uuid` |
| `GET /schemas/{uuid}`, `GET /schemas/find?name=...`, `DELETE /schemas/{uuid}` | Read / find / delete |
| `POST /schemas/{uuid}/points` | Create or overwrite one point: `{"timestamp": "2026-10-26T00:00:00Z", "availability": 99.95, "factSheetId": "<uuid>"}` (same timestamp overwrites) |
| `GET /schemas/{uuid}/points?begin&end&sort=asc&page=1&size=50` | Read points |
| `POST /schemas/{uuid}/points/aggregation` | Aggregations (`attribute`, `aggregation`, `distinct`) |
| `GET /schemas/{uuid}/trends` | Trend, difference and latest value |
| `DELETE /schemas/{uuid}/points?...`, `DELETE /schemas/{uuid}/points/{timestamp}` | Delete |
| `GET/POST/PUT/PATCH/DELETE /charts`, `/kpis`, `/kpis/validate`, `POST /jobs` | Charts and KPI definitions (KPIs are computed from inventory filters), recalculation jobs |

Attributes are `metric` (numeric) or `dimension` (string, used for filtering and for linking points
to fact sheets, typically `factSheetId` or an external id). The Integration API `inboundMetrics`
processor writes points from an LDIF. SAP's sample `importMetrics` script lives in
`SAP-samples/leanix-scripts`.

## 3. Import/Export API (Excel, LDIF, OData)

Base `/services/import-export/v1`. The service behind the inventory's Excel import/export and the
OData feed for BI tools; it counts against the 1,200 requests per minute per workspace budget for
internal services.

Exports (of a saved search / bookmark):

```text
POST /exports      {"sourceType": "BOOKMARK", "sourceIdentifier": {"id": "<bookmarkId>"}, "formats": ["XLSX"], "languageId": "en"}
                   -> {"id": "<exportId>", "status": "NEW|PENDING|DONE|ERROR|CANCELLED", "result": {...artifacts...}}
GET  /exports      list jobs;  GET /exports/{id}  poll;  GET /exports/{id}/XLSX  (or /LDIF) download (octet-stream)
```

`sourceIdentifier` is an untyped object in the spec; the bookmark id is the identifier the UI uses
**(unconfirmed field name)**. Bookmark ids come from `GET /services/pathfinder/v1/bookmarks?bookmarkType=INVENTORY`.

Excel imports:

```text
POST /imports                  multipart/form-data, field "file" (.xlsx)  -> validation result with importId
POST /imports/{importId}       execute;   GET /imports/{importId}  status;   POST /imports/{importId}/cancel
GET  /imports/{importId}/result   result file (row-level outcome)
```

Excel rules (official import guide): `.xlsx`, first sheet only, one fact sheet type per file,
row 1 technical keys, row 2 labels, columns `id`, `type`, `name` mandatory (empty `id` creates),
up to 10,000 rows (500 when relations or subscriptions are included), `;` separates multi-values,
values are case-sensitive technical keys, dates `yyyy-mm-dd`, relations by exact `displayName`,
multi-select / relations / tags columns **replace** the existing values, rows run top-down, column
`action` = `Archive` archives. The export file (inventory table view > Export) is the template.

OData (BI tools): service roots `/services/import-export/v1/odata/BookmarkService.svc/` (full
output) and `/BookmarkDataService.svc/` (key-value output); entity set name = bookmark UUID;
`$metadata`, `$count`, `$skip`, `$top`, `$skiptoken`. The OData endpoints are declared with
**basic** security in the spec (API token as Basic `apitoken:<token>`) **(unconfirmed in prose docs)**;
the bookmark must have OData enabled (`oDataEnabled`).

## 4. Pathfinder REST beyond GraphQL

Base `/services/pathfinder/v1`. SAP recommends GraphQL for fact sheets; these REST resources have
no GraphQL equivalent.

| Area | Endpoints |
|---|---|
| Fact sheets (legacy REST) | `GET /factSheets?type=Application&pageSize=5000&cursor=&fields=&relationTypes=&tags=true&subscriptions=true&archivedOnly=false`, `POST /factSheets`, `GET/PUT /factSheets/{id}`, `DELETE /factSheets/{id}` (archives), `GET /factSheets/hierarchy/{rootId}`, `GET/POST /factSheets/{id}/relations`, `PUT/DELETE /factSheets/{id}/relations/{relationId}` |
| Files on fact sheets | `POST /graphql/upload`, multipart form with parts `graphQLRequest` (JSON string holding the `createDocument` mutation and variables) and `file`; `documentType: "logo"` sets the fact sheet logo. Needs the optional feature "Uploading Files on Fact Sheets"; about 10 MB per file **(unconfirmed)** |
| Saved searches, reports, diagrams, dashboards | `GET /bookmarks?bookmarkType=INVENTORY|REPORTING|VISUALIZER|DASHBOARD|INVENTORY_EXPORT&oDataOnly=&groupKey=`, `POST /bookmarks`, `GET/PUT/DELETE /bookmarks/{id}`, `PATCH /bookmarks/{id}` (change owner), `GET /bookmarks/{id}/versions`, `GET/POST/DELETE /bookmarkShares`. A bookmark carries `type`, `name`, `state` (the filter/view definition), `permittedReadUserIds`, `permittedWriteUserIds`, `oDataEnabled`, `predefined` |
| Workspace exports | `POST /exports/fullExport?exportType=SNAPSHOT|AUDIT_LOG|AUDIT_LOG_LEGACY|ARCHIVE&startDate&endDate` starts a job (`{"data": {"jobId": ...}}`); `GET /exports?exportType=&pageSize=100&cursor=` lists jobs (`status` `STARTED|COMPLETED|DOWNLOADED|ERROR|DELETED|CANCELED`, `downloadKey`); `GET /exports/downloads/{workspaceId}?key=<downloadKey>` downloads the XLSX (one-time key; the file is deleted after about ten minutes) |
| Models | `GET /models/dataModel` (+ `PUT`, admin), `/models/dataModel/enriched`, `/models/viewModel`, `/models/languages/{id}`, `/models/authorization`, `/models/reportingModel`, `/models/factSheetResources`, `/models/accessControlEntities` (CRUD), `/models/metaModel`, `/models/metaModel/{factSheetType}`, `/models/metaModel/actionBatches`, `/models/metaModel/actions/audit-log` |
| Meta model actions | `GET /metaModel`, `GET/POST /metaModel/actions`, `GET /metaModel/actions/auditLog`, `GET /metaModel/jobs/{id}`, `GET /metaModel/permissionRoles?role=&factSheetType=` |
| Settings and features | `GET/PUT /settings`, `GET/PUT /settings/factSheets/{factSheetType}`, `GET /features`, `GET/POST /features/{id}` (Admin) |
| Assets, suggestions | `GET/POST/DELETE /assets/{asset}`, `GET /suggestions` |

Response envelope: `{"status": "OK"|"ERROR", "type": "...", "data": ..., "errors": [...], "total":
N, "endCursor": "..."}`.

## 5. MTM API

Base `/services/mtm/v1`: token endpoint, workspaces, users, permissions, technical users, SCIM,
long-lived tokens. Covered in `auth-and-access.md` sections 2, 4 and 9. Admin token for anything
beyond `/oauth2/token` and `/workspaces`.

## 6. MCP server

Official since November 2025, enabled by default, no AI units needed. Configure under
Administration > **MCP Server** (Enable MCP Server; User-Based Authentication; Technical Users;
Progressive tool discovery).

| Access | Endpoint | Authentication |
|---|---|---|
| Individual users (recommended) | `https://mcp.leanix.net/services/mcp-server/v1/mcp` or `https://mcp.leanix.net/services/mcp-server/v1/mcp/instance/{SUBDOMAIN}/workspace/{WORKSPACE_NAME}` | OAuth in the browser; session expires after 24 hours |
| Technical users / automation | `https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp` | `Authorization: Token <API token>` (also `Basic base64(apitoken:<token>)` or `Bearer <JWT>`) |

Transport is streamable HTTP. Client snippets from the docs: `claude mcp add --transport http leanix
https://mcp.leanix.net/services/mcp-server/v1/mcp`; for technical users a `mcp-remote` or
`streamableHttp` entry with the `Authorization: Token ...` header (Claude Desktop, Cline, Cursor,
Copilot). Toolsets: default `inventory`, `report_diagrams`, `roadmap_planning`, `surveys`,
`architecture_decisions`, `self_built_software`, `get_insights`; optional via `?toolsets=a,b`:
`discovery_inbox`, `calculations`, `automations`, `catalogs`, `custom_reports`,
`product_information`, `diagrams` (at most 10 toolsets per connection; `?ui=false` disables the
interactive MCP Apps). Permissions follow the user's role: read for all roles, write Admin only by
default (configurable), tools hidden when the feature is not permitted. SAP publishes
agent skills and a Claude Code plugin for the MCP server at `github.com/SAP/leanix-ai-plugins`
(`/plugin marketplace add SAP/leanix-ai-plugins`). Use the MCP server when an agent should explore a
workspace conversationally; use the APIs in this skill for deterministic integrations, bulk work and
administration.

## 7. Custom reports and the reporting library

Custom reports are React/TypeScript apps rendered inside the workspace. Tooling:
`npm create @sap/leanix-custom-report@latest` scaffolds a Vite project (report id, title, author,
workspace credentials), `npm run dev`, `npm run build`, `npm run upload` (builds and uploads to the
workspace, then Administration > Reports > Show report). Credentials live in `lxr.json`
(`{"host": "acme.leanix.net", "apitoken": "<technical user token>"}`, optional `proxyURL`), or in
the user-level `~/.leanix/lxr.json` written by `npx lxr login`; never commit the file. The older
`@leanix/reporting-cli` is deprecated. The in-app library `@leanix/reporting` exposes `lx.init()`,
`lx.ready(config)`, `lx.executeGraphQL(query, variablesJson)` (runs GraphQL with the viewer's
session), `lx.currentSetup.settings.dataModel` / `viewModel`, translation helpers, modals and
export to PDF/PNG. Behind the upload sits the Reports service `/services/reports/v1`
(`POST /customReportVersions/upload` with a `.tgz` of at most 50 MB, scan and build, then
`PATCH /customReportInstallations/{id}` to activate). Reports can be published to the SAP LeanIX
Extension Hub; "Custom Reports with AI" generates them from natural language through the MCP
server.

## 8. Surveys, to-dos, automations and the rest

| Service | Base | Notes |
|---|---|---|
| Survey API v1 | `/services/survey/v1` | Replaces the **Poll API v2** (`/services/poll/v2/polls`, `/pollRuns`, `/pollResults`), which is deprecated for March 2027 |
| To-do API | `/services/todo/v1` | To-dos and assignees (also writable through the Integration API `inboundToDo`) |
| Automations API | `/services/automations/v2` | Automation templates, instances, quota; automations are in-product JavaScript triggered by events and can call webhooks |
| Transformations / Impacts | `/services/transformations/v1`, `/services/impacts/v1` | Initiative transformations and impacts (`inboundImpact`) |
| Synclog API | `/services/synclog/v1` | Synchronization log items of integrations (Administration > Sync Logging) |
| Documents API | `/services/documents/v2` (`v1` is scheduled for removal in July 2027) | Architecture decisions and templates |
| Storage API | `/services/storage/v1` | File resources |
| Reference Data, Catalog | `/services/reference-data/v1`, `/services/catalog/v2` | Reference catalog links |
| Discovery APIs | `/services/discovery-saas/v1`, `/services/technology-discovery/v1`, SBOM endpoints (300 requests per minute per workspace) | SaaS discovery, self-built software (SBOM upload) |
| Integration ServiceNow / Signavio / Collibra / Apptio | `/services/integration-servicenow/v2`, `/services/integration-signavio/v3`, ... | Out-of-the-box integrations, configured in Administration |
| Notifications, Navigation (collections), Recon | `/services/notifications/v1`, `/services/navigation/v1`, `/services/recon/v1` | |

Each has a spec URL in the OpenAPI explorer (see `auth-and-access.md` section 8).
