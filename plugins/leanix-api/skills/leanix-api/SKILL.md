---
name: leanix-api
description: >-
  Work with SAP LeanIX (formerly LeanIX) through its APIs, with emphasis on setting up API access
  correctly (technical users and API tokens, the OAuth2 token exchange, Admin/Member/Viewer roles,
  permissions, virtual workspaces) and on the GraphQL and Integration APIs. Use it whenever a task
  mentions LeanIX, leanix.net, enterprise architecture fact sheets, inventories of applications, IT
  components or business capabilities, GraphQL allFactSheets or updateFactSheet, LDIF, Integration
  API processors, webhooks, metrics, Excel import/export, the LeanIX MCP server, technical users or
  workspace administration, or automating, syncing, bulk-loading, reporting on or cleaning anything
  in a LeanIX workspace, even if the user never says "API". Covers step-by-step admin setup,
  401/403/429 troubleshooting, GraphQL queries, filters, pagination and JSON-Patch mutations,
  Integration API LDIF runs, webhooks, MTM user management, and includes references, an official
  docs snapshot, an OpenAPI spec and a Python client.
license: MIT
compatibility: Python 3.10+ for the bundled script (standard library only); curl examples otherwise.
metadata:
  author: jj1985
  version: "1.0.0"
  platform: SAP LeanIX (Application Portfolio Management / Enterprise Architecture Management, SaaS, meta model v3 and v4)
---

# SAP LeanIX API

SAP LeanIX is a SaaS enterprise architecture repository. Everything is a **fact sheet** (Application,
IT Component, Business Capability, ...) with fields, relations, tags, subscriptions and documents,
organised by a configurable **meta model**. Fact sheets are read and written through the **GraphQL
API**; bulk and recurring syncs go through the **Integration API** (LDIF); users, roles and
technical users live in the **MTM** service; webhooks, metrics, Excel import/export and an MCP
server complete the picture. Every API is gated by the same workspace roles as the UI, which is
where most integration failures start, so this skill leads with access setup.

## Pick the entry point

| Task | Use | Read |
|---|---|---|
| Set up API access: technical user, role, token exchange, first call | admin checklist, curl smoke tests | `references/auth-and-access.md` §11, then §1-4 |
| Decide which role an integration needs; custom roles, SSO, virtual workspaces / ACEs | permission model | `references/auth-and-access.md` §5-7 |
| Diagnose 401 / 403 / 429, tokens, host confusion | troubleshooting table | `references/auth-and-access.md` §12, `references/gotchas.md` |
| Read fact sheets, filter, paginate, export to CSV | GraphQL `allFactSheets` | `references/graphql-api.md` §2-4 |
| Create, update, relate, tag, subscribe, archive fact sheets | GraphQL mutations with JSON patches | `references/graphql-api.md` §5-6 |
| Learn the workspace's types, fields, relation names, option keys | data model (REST + GraphQL) | `references/graphql-api.md` §7 |
| Recurring sync from another system, bulk upserts by external id, deletions of stale data | Integration API (LDIF + processors) | `references/integration-api.md` |
| React to changes, push KPIs, Excel round-trips, saved searches, workspace exports | Webhooks, Metrics, Import/Export, Pathfinder REST | `references/other-apis.md` |
| Manage users, invitations, roles, technical users from code | MTM API | `references/auth-and-access.md` §4, §9 |
| Point an AI agent at a workspace | SAP LeanIX MCP server | `references/other-apis.md` §6 |
| Exact request/response shapes | OpenAPI spec | `references/leanix.openapi.yaml` |
| Official wording for one topic | docs snapshot (large; open one page, not all) | `references/source-docs/INDEX.md` |

## Core mechanics

**Base URL** `https://{SUBDOMAIN}.leanix.net`, where `{SUBDOMAIN}` is the first label of the
workspace URL `https://{SUBDOMAIN}.leanix.net/{WORKSPACE_NAME}/` (regional instances `eu`, `us`,
`de`, `uk`, `ch`, `au`, `ca`, `br`, `ae`, `jp`, `sg`, the original `app`, or an SSO company
domain). Service paths: `/services/mtm/v1`, `/services/pathfinder/v1`,
`/services/integration-api/v1`, `/services/webhooks/v1`, `/services/metrics/v2`,
`/services/import-export/v1`, `/services/mcp-server/v1`. Documentation lives at
`help.sap.com/docs/leanix/ea/...`; raw OpenAPI specs are public, for example
`/services/pathfinder/v1/api-docs/swagger.json` and `/services/mtm/v1/openapi.json`.

**Authentication.** One credential model: an Admin creates a **technical user** (Administration >
Technical Users > New Technical User: username, role Admin / Member / Viewer, expiry) and receives
an **API token** once. Exchange it for a one-hour JWT:
`POST /services/mtm/v1/oauth2/token` with HTTP Basic `apitoken:<API token>` and form body
`grant_type=client_credentials`; then send `Authorization: Bearer <JWT>` to every service. Cache the
JWT and renew it shortly before `expires_in` (3600 s); never request one per call. Personal API
tokens are deprecated (2022). Only the MCP server also accepts `Authorization: Token <API token>`.

**Roles.** Viewer reads; Member creates and edits fact sheets (and breaks quality seals of fact
sheets it is not subscribed to); Admin additionally owns the whole Administration area:
Integration API configuration, webhooks, user management (MTM), meta model, technical users, MCP
settings. Per-type permissions for Viewer/Member are configured under Meta Model Configuration >
type > Permissions; custom roles and fact-sheet-level access (virtual workspaces, ACEs) require
SSO-managed roles. Pick the lowest role that works, one technical user per integration, with an
expiry and rotation.

**GraphQL** (`POST /services/pathfinder/v1/graphql`, body `{"query", "variables"}`):
- `factSheet(id:)` for one; `allFactSheets(filter: {facetFilters: [{facetKey: "FactSheetTypes",
  keys: ["Application"]}], fullTextSearch, ids, externalIds}, first, after, sort)` for many, with
  `pageInfo { hasNextPage endCursor }` cursors (forward only; always pass `first`, 500 to 1,000).
- Type-specific fields and every relation need inline fragments: `... on Application { lifecycle
  { asString } relApplicationToITComponent { edges { node { id factSheet { id name } } } } }`.
- Mutations: `createFactSheet(input: {name, type}, patches)` and `updateFactSheet(id, rev, patches,
  validateOnly, comment)` with JSON patches `{op: add|replace|remove, path: "/field", value}` where
  **value is always a string** (JSON-encoded for lifecycle, tags `[{"tagId"}]`, external ids
  `{"type":"ExternalId","externalId"}`, relations `/relX/new_1` with `{"factSheetId"}`,
  multi-selects). Archive = `/status` `ARCHIVED` plus a `comment`; no hard delete.
- Errors arrive as HTTP 200 with `errors[]`; aliased batches roll back as a whole; `rev` gives
  optimistic locking (`REVISION_CLASH`); `validateOnly: true` is the dry run.
- Facet keys, field keys and option keys are technical names; discover them with
  `allFactSheets(factSheetType: X) { filterOptions { facets { facetKey results { key } } } }`,
  `GET /services/pathfinder/v1/models/dataModel`, or the in-app GraphiQL (help menu > Developer
  Tools > GraphQL Editor, Admin by default).

**Integration API.** Configure a processor (Administration > Integration API, or
`PUT /services/integration-api/v1/configurations`) keyed by `connectorType` + `connectorId` +
`connectorVersion` + direction + mode, then `POST /synchronizationRuns?start=true&test=true` with
the LDIF (`{connectorType, connectorId, connectorVersion, lxVersion, processingDirection,
processingMode, content: [{type, id, data}]}`), poll `GET /synchronizationRuns/{id}/status` until
`FINISHED`, read `/warnings`. `content[].id` is the external id (idempotent upserts), `run` levels
order processors (fact sheets in 0, relations and tags in 1), `processingMode: full` plus
`deletionScope` archives what the source stopped sending (guard with `maximumDeletionRatio`).

**Limits.** 1,800 requests per minute per user (human or technical) across GraphQL, REST and UI
(HTTP 429 `USER_INTERVAL_REQUEST_LIMIT_EXCEEDED`, optional `Retry-After`); 1,200 per minute per
workspace for the Integration API and Import/Export service toward Pathfinder; GraphQL complexity
limit on very large documents; LDIF bodies 50 MB.

## Domain essentials

- Meta model v4 types: `Objective`, `Platform`, `Initiative`, `Organization`, `BusinessCapability`,
  `BusinessContext`, `DataObject`, `Application`, `Interface`, `Provider`, `ITComponent`,
  `TechnicalStack` (UI label "Tech Category"); v3 workspaces still have `Project`, `Process`,
  `UserGroup`. Subtypes are the `category` field. Read the workspace's own model: types, fields,
  relations and option keys are customisable.
- Relations are named `rel<From>To<To>` (`relApplicationToITComponent`,
  `relApplicationToBusinessCapability`) plus `relToParent` / `relToChild` and
  `relToSuccessor` / `relToPredecessor`; attributes such as `activeFrom`, `activeUntil`,
  `technicalSuitability`, costs live on the relation.
- Lifecycle phases `plan`, `phaseIn`, `active`, `phaseOut`, `endOfLife` (`yyyy-mm-dd`); `status`
  `ACTIVE` / `ARCHIVED` (90-day recovery); quality seal `lxState` (`APPROVED`, `BROKEN_QUALITY_SEAL`,
  `DRAFT`, `REJECTED`); subscriptions of type `RESPONSIBLE`, `ACCOUNTABLE`, `OBSERVER` with
  workspace-defined roles; tags in groups (`SINGLE` / `MULTIPLE` mode) referenced by id; external
  ids per fact sheet for idempotent syncs; TIME classification is a tag group.
- Fact sheet ids are UUIDs (in the fact sheet URL); workspace id is in Administration > API Tokens.

## Workflow for a typical task

1. **Confirm scope**: subdomain and workspace, role of the technical user, read or write, which
   fact sheet types, one-off or recurring. Read `LEANIX_HOST` / `LEANIX_API_TOKEN` from the
   environment; never echo tokens.
2. **Check access before building**: `token`, `whoami` and `probe` in `scripts/leanix_api.py`
   (token exchange, workspace and role from the JWT, a one-row read, a `validateOnly` write, the
   Admin-only listings). Fix the role first; nothing else works otherwise.
3. **Inspect the data model**: `model types`, `model fields <Type>`, `model relations <Type>`,
   `facets <Type>`, `tags`, `subscription-roles`. Never hard-code ids or assume field keys; they
   differ between workspaces, including production and sandbox.
4. **Read before write**: query the fact sheet (with `rev` and the collections you will touch),
   build patches, run with `validateOnly: true`, then commit. For syncs, prefer the Integration API
   with external ids and a `test=true` run first.
5. **Batch and page sensibly**: `first` 500 to 1,000, de-duplicate on id, about 50 aliased
   mutations per request, back off on 429, stay under about 25 requests per second per technical
   user. Use the Integration API for more than a few hundred writes.
6. **Verify** by re-reading by id (not by search), check `/warnings` after Integration API runs, and
   point the user at the fact sheet history (`allLogEvents`) or Administration > Sync Logging.
7. **Destructive operations**: archive instead of delete (archiving is the only deletion), require a
   comment, count first, avoid `processingMode: full` without a tested `deletionScope`, and
   recommend a sandbox workspace for first runs.

## Scripts

`scripts/leanix_api.py` (standard library only): token exchange with caching and 401 retry, 429
backoff, JWT decoding (`whoami`), permission `probe`, data model and facet discovery, GraphQL
`query`, paginated `list` with CSV output, `search`, `get`, `create`, `update` (with revision
retry), `relate`, `tag`, `archive`, `recover`, `subscribe`, `comment`, `events`, Integration API
`sync` (create, start, poll, warnings, results), `processors`, `webhooks` (list, status, event
tags, create PUSH, deliveries, pull), `metrics` (schemas, points), Pathfinder `export` and
`bookmarks`, Import/Export `export-bookmark` and `import-excel`, MTM `users`, `permission`,
`invite`, `techusers` (list, create, replace token, changelog), and `raw` for anything else.
`python scripts/leanix_api.py --help`. Configure with `LEANIX_HOST` and `LEANIX_API_TOKEN`
(optional `LEANIX_WORKSPACE` as a production guard, `LEANIX_CA_BUNDLE` for private CAs).

## References

- `references/auth-and-access.md`: credential model, token exchange, hosts, technical users (UI and
  MTM API), roles and permissions, virtual workspaces / ACEs, least privilege per integration,
  admin tooling and workspace id, MTM user administration, rate limits and audit, the
  zero-to-first-call checklist and the 401/403/429 troubleshooting table.
- `references/graphql-api.md`: endpoint and tooling, reading fact sheets, facet filters, sorting
  and pagination, mutations and the patch cookbook, tags / subscriptions / comments / documents /
  event log, data model discovery, errors and limits, worked Python examples.
- `references/integration-api.md`: when to use it, concepts, LDIF format, processor anatomy,
  processor types with examples, JUEL cheat sheet, REST run lifecycle, safety (test runs, full
  mode, deletion scope, limits), a complete minimal example, troubleshooting.
- `references/other-apis.md`: webhooks (PUSH/PULL, events, payloads), Metrics v2, Import/Export
  (Excel, LDIF, OData), Pathfinder REST (bookmarks, exports, models), MCP server, custom reports,
  surveys and the remaining services.
- `references/gotchas.md`: failure causes and fixes, grouped by auth, GraphQL, Integration API and
  the other services.
- `references/leanix.openapi.yaml`: curated OpenAPI 3.1 for the token endpoint, GraphQL, the
  Pathfinder REST resources this skill uses, the Integration API, Webhooks, Metrics, Import/Export
  and the MTM user and technical user endpoints (derived from SAP's public specs).
- `references/source-docs/`: snapshot of 30 official SAP Help Portal pages (see `INDEX.md`). The
  inbound processors page alone is 60 KB: read the summaries above first and open a snapshot only
  to confirm a parameter or example. Check the live docs when a detail matters.

## Conventions when answering

- Show `METHOD /services/<service>/v1/path` with the JSON or GraphQL body; mention the bearer header
  once. Use placeholders `{SUBDOMAIN}`, `<fact sheet id>`, `<API token>` and say how to find them.
- Name the role a step needs and the UI path (`Administration > Technical Users > New Technical
  User`) when the user has to click something; Administration is Admin-only.
- Prefer GraphQL with variables (never string interpolation), `validateOnly` before commits,
  external ids for syncs, the Integration API for bulk, archiving over deletion, explicit `first`
  with cursors on lists; say why in one clause when you deviate.
- Flag meta model differences (v3 vs v4 type names, custom fields), anything marked
  **(unconfirmed)** in the references, and that the workspace's own GraphiQL schema is the final
  authority, so the user verifies on their workspace.
- Make deliverables self-contained. A runbook, script or README you write for the user must not
  tell them to open `references/...` or run `scripts/leanix_api.py` unless they have this skill
  installed; inline the facts and the curl/Python they need. Mention the bundled client only as an
  optional shortcut, by its path in the repository.
- Warn before any `processingMode: full` run, any `maximumDeletionRatio` above the default, any
  `/lifecycle` or `/tags` `replace` patch (they replace the whole collection), and any Admin token
  shared across integrations.
- For one-off questions answer from the references directly instead of walking the whole workflow.
