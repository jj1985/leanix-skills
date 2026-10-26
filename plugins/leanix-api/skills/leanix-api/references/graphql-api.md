# SAP LeanIX GraphQL API (Pathfinder)

The GraphQL API is the recommended way to read and change fact sheets, relations, tags,
subscriptions, comments and documents. Researched against the SAP Help Portal developer guide, the
Pathfinder OpenAPI specification and SAP sample scripts (October 2026). Items marked
**(unconfirmed)** come from community code or inference; check them in the GraphiQL schema explorer
of the target workspace, which is authoritative because every workspace has its own schema.

## Contents

1. [Endpoint, authentication and tooling](#1-endpoint-authentication-and-tooling)
2. [Reading fact sheets](#2-reading-fact-sheets)
3. [Filtering](#3-filtering)
4. [Sorting, pagination and hierarchy](#4-sorting-pagination-and-hierarchy)
5. [Mutations and JSON patches](#5-mutations-and-json-patches)
6. [Tags, subscriptions, comments, documents, event log](#6-tags-subscriptions-comments-documents-event-log)
7. [Discovering the data model](#7-discovering-the-data-model)
8. [Errors, limits and batching](#8-errors-limits-and-batching)
9. [Worked examples](#9-worked-examples)

---

## 1. Endpoint, authentication and tooling

| Item | Value |
|---|---|
| Endpoint | `POST https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/graphql` |
| File uploads | `POST .../services/pathfinder/v1/graphql/upload` (multipart: GraphQL request + file, used by `createDocument` for files and logos) |
| Headers | `Authorization: Bearer <access token>`, `Content-Type: application/json`; optional `x-graphql-enable-extensions: true` to receive validation warnings in `extensions.warnings` |
| Body | `{"query": "...", "variables": {...}, "operationName": "..."}` (name operations when a document holds several) |
| Spec level | GraphQL October 2021 |
| Schema explorer | Help menu (question mark) > **Developer Tools > GraphQL Editor** (GraphiQL; no token needed inside the app; Admin only by default, grant "Developer tools" to other roles under Administration > User Roles and Permissions) |
| Query from the inventory | Inventory filter bar > arrow icon > **Copy as JSON Query** or **Open in GraphiQL** (same permission) |
| Introspection | `{ __schema { types { name kind fields { name } } } }`, `{ __type(name: "Application") { fields { name } } }` |

The access token comes from the MTM token endpoint (see `auth-and-access.md`), lives one hour, and
the endpoint answers `401` once it has expired. Role permissions apply exactly as in the UI: a
Viewer token can only query, hidden fields are absent, ACE-restricted fact sheets are invisible.

## 2. Reading fact sheets

### One fact sheet

```graphql
query ($id: ID!) {
  factSheet(id: $id) {
    id name displayName fullName type description status rev level category
    createdAt updatedAt lxState qualitySeal naFields
    completion { percentage }
    permissions { create read update delete self }
    tags { id name color tagGroup { id name shortName mode } }
    subscriptions { edges { node { id type user { id email firstName lastName } roles { id name comment } } } }
    documents { edges { node { id name url description origin } } }
    comments(filter: {status: ACTIVE}) { totalCount edges { node { id message createdAt user { email } } } }
    ... on Application {
      alias release
      externalId { externalId externalUrl comment status }
      lifecycle { asString phases { phase startDate milestoneId } }
      functionalSuitability technicalSuitability businessCriticality
      relApplicationToITComponent { edges { node { id activeFrom activeUntil description factSheet { id name type } } } }
      relApplicationToBusinessCapability { edges { node { id factSheet { id displayName } } } }
      relToParent { edges { node { factSheet { id name } } } }
      relToChild { edges { node { factSheet { id name } } } }
    }
  }
}
```

Rules that follow from the schema:

- Fields shared by every type (`id`, `name`, `displayName`, `fullName`, `type`, `description`,
  `status`, `rev`, `level`, `category`, `createdAt`, `updatedAt`, `lxState`, `qualitySeal`,
  `completion`, `permissions`, `tags`, `subscriptions`, `documents`, `comments`, `naFields`,
  `permittedReadACL`, `permittedWriteACL`) are selectable directly. Everything type-specific
  (`lifecycle`, `externalId`, `functionalSuitability`, every `rel...` connection, custom fields) needs
  an inline fragment `... on <FactSheetType> { ... }`.
- The fact sheet id is the UUID in the fact sheet URL. `rev` is the revision counter for optimistic
  locking. `status` is `ACTIVE` or `ARCHIVED` (archived fact sheets remain queryable through the
  `TrashBin` facet for 90 days). `lxState` is the quality seal: `DRAFT`, `APPROVED`, `REJECTED`,
  `BROKEN_QUALITY_SEAL`. `category` holds the subtype.
- `displayName` is the hierarchy path (`Parent / Child`); IT Component display names carry the
  provider prefix. Lifecycle phases in the default model: `plan`, `phaseIn`, `active`, `phaseOut`,
  `endOfLife`; `lifecycle { asString }` gives the current phase.
- Relations are connections `rel<From>To<To> { edges { node { id activeFrom activeUntil description
  <relation fields> factSheet { ... } } } }`. The node `id` is the **relation id** (needed to update
  or remove the relation); `factSheet` is the target. Generic ones: `relToParent`, `relToChild`,
  `relToSuccessor`, `relToPredecessor`, `relToRequires`, `relToRequiredBy`. `validityFilter:
  {activeFrom, activeUntil}` on a relation field keeps only relations active in that window.
- Relation attributes (`technicalSuitability` on `relApplicationToITComponent`, `supportType` on
  `relApplicationToBusinessCapability`, `usageType`, `dataFlowDirection`, `obsolescenceRiskStatus`,
  costs, custom fields) live on the relation node, not on the fact sheet.
- Attribute keys are the technical names from the meta model (Administration > Meta Model
  Configuration > field > Key), never UI labels or translations. Hidden ("unused") fields stay
  readable and writable through the API.

### Many fact sheets

```graphql
query ($filter: FilterInput, $first: Int, $after: String, $sort: [Sorting]) {
  allFactSheets(filter: $filter, first: $first, after: $after, sort: $sort) {
    totalCount
    pageInfo { hasNextPage endCursor }
    edges { node { id name type ... on ITComponent { category lifecycle { asString } } } }
  }
}
```

`allFactSheets(factSheetType: Application)` is a shorthand for one type; `filter` is needed for
anything else. `first: 0` with `totalCount` is a cheap count probe.

## 3. Filtering

`FilterInput` fields:

| Field | Meaning |
|---|---|
| `facetFilters: [{facetKey, operator, keys, dateFilter, subscriptionFilter, relationFieldsFilter, relationFieldsFilterOperator}]` | The same facets the inventory sidebar uses. `operator` is `OR` (default), `AND` or `NOR`. `keys` are facet values. |
| `fullTextSearch: "text"` | Name, description, alias and full-text-enabled custom fields, like the inventory search box. Treat it as a candidate generator and confirm matches in code. |
| `ids: ["<uuid>", ...]` | Restrict to these fact sheet ids. |
| `externalIds: ["externalId/<value>"]` | Look up by external id; the key is `<externalIdFieldKey>/<value>`. |
| `responseOptions: {maxFacetDepth: 5}` | Depth of facet results when you also select `filterOptions`. |
| `quickSearch: "text"` | Type-ahead style search **(unconfirmed, community code only)**. |

Global facet keys (every type):

| Facet key | Inventory filter | Keys |
|---|---|---|
| `FactSheetTypes` | Type | `Application`, `ITComponent`, `BusinessCapability`, ... (only `OR`) |
| `hierarchyLevel` | Hierarchy Level | `"1"`, `"2"`, `"3"` |
| `Subscriptions` | Subscriptions | user ids, `__me__`, `__missing__`; plus `subscriptionFilter: {type: RESPONSIBLE, roleId: "<uuid>"}` |
| `DataQuality` | Data Quality | `_noResponsible_`, `_qualitySealBroken_`, `_noDescription_`, `_noLifecycle_` (`OR`/`AND`/`NOR`) |
| `lxState` | Quality Seal | `DRAFT`, `APPROVED`, `REJECTED`, `BROKEN_QUALITY_SEAL` (`OR`/`NOR`) |
| `TrashBin` | Trash Bin | `archived` |
| `_TAGS_` | Other Tags | tag ids of **ungrouped** tags; grouped tags use the **tag group id** as `facetKey` with tag ids as keys |

Type-specific facets are the field keys of the type (`technicalSuitability`, `functionalSuitability`,
`businessCriticality`, `category`, `dataFlowDirection`, custom selects with "show in filters") and
the relation names (`relApplicationToITComponent` with **target fact sheet ids** as keys, or
`__missing__` for "has none", `__any__` for "has at least one"; `relationFieldsFilter: [{fieldName:
"supportType", values: ["leading"]}]` with `relationFieldsFilterOperator: INCLUSIVE` filters on
relation attributes). `lifecycle` takes `keys` = phase names and a `dateFilter {type: RANGE, from,
to}` (`TODAY`, `POINT`, `END_OF_MONTH`, `END_OF_YEAR` also exist). An **invalid facet key fails the
whole query**, so discover them first:

```graphql
{
  allFactSheets(factSheetType: Application, first: 0) {
    filterOptions {
      facets { facetKey possibleOperators operator results { name key } dateFilter { type from to minDate maxDate }
               relationFieldsFilterOperator relationFieldsFilter { fieldName values { key selected } } }
    }
  }
}
```

Example: applications with poor fits phasing in between 2023 and 2029, newest first:

```json
{
  "filter": {
    "facetFilters": [
      {"facetKey": "FactSheetTypes", "operator": "OR", "keys": ["Application"]},
      {"facetKey": "technicalSuitability", "operator": "OR", "keys": ["unreasonable"]},
      {"facetKey": "functionalSuitability", "operator": "NOR", "keys": ["perfect", "appropriate"]},
      {"facetKey": "lifecycle", "operator": "OR", "keys": ["phaseIn"],
       "dateFilter": {"type": "RANGE", "from": "2023-01-01", "to": "2029-12-31"}}
    ]
  },
  "sort": [{"key": "updatedAt", "order": "desc"}]
}
```

Other useful filters: applications without a Responsible
`{"facetKey": "Subscriptions", "operator": "OR", "keys": ["__missing__"], "subscriptionFilter": {"type": "RESPONSIBLE"}}`
(or `DataQuality` / `_noResponsible_`); archived applications `{"facetKey": "TrashBin", "keys": ["archived"]}`;
fact sheets carrying two tags `{"facetKey": "_TAGS_", "operator": "AND", "keys": ["<tagId1>", "<tagId2>"]}`;
IT components without applications `{"facetKey": "relITComponentToApplication", "keys": ["__missing__"]}`.
Shortcut: build the filter in the inventory and **Copy as JSON Query**.

## 4. Sorting, pagination and hierarchy

- `sort: [{key: "displayName", order: asc}]`; keys include `displayName`, `updatedAt`, `createdAt`,
  `level` and field keys. Sort explicitly when paginating.
- Pagination is relay-style and **forward only**: `first` plus `after` (the previous page's
  `pageInfo.endCursor`). `last`, `before`, `startCursor`, `hasPreviousPage` are not supported.
- Pages are live, not a snapshot: a long export can see an item twice or miss one if the workspace
  changes meanwhile; de-duplicate on `id`.
- Always pass `first`. The default page size is undocumented; an older tutorial capped a query at
  15,000 edges **(historical, unconfirmed today)**. 500 to 1,000 per page works for narrow
  selections; fewer when relations are expanded, because the complexity limit (section 8) counts
  the whole selection. The REST `GET /factSheets` sibling caps `pageSize` at 5,000.
- `totalCount` is cheap and useful for progress.
- Hierarchies: `allFactSheets(hierarchy: {mode: FULL_TREE}, filter: {ids: ["<rootId>"]})` returns
  the root and everything below it; `hierarchyLevel` facets and `relToParent` / `relToChild` give the
  structure.

## 5. Mutations and JSON patches

### createFactSheet

```graphql
mutation ($input: BaseFactSheetInput!, $patches: [Patch], $validateOnly: Boolean) {
  createFactSheet(input: $input, patches: $patches, validateOnly: $validateOnly) {
    factSheet { id name type rev }
  }
}
```

Variables: `{"input": {"name": "Payroll Portal", "type": "Application"}, "patches": [...]}`.
`BaseFactSheetInput` requires `name` and `type`; set everything else (description, external id,
subtype via `/category`, relations, tags, lifecycle) with patches in the same call. Fact sheets are
identified by UUID; duplicate names are not documented as rejected for GraphQL, so check for an
existing fact sheet (by external id or exact name) before creating.

### updateFactSheet

```graphql
mutation ($id: ID!, $rev: Long, $patches: [Patch]!, $validateOnly: Boolean, $comment: String) {
  updateFactSheet(id: $id, rev: $rev, patches: $patches, validateOnly: $validateOnly, comment: $comment) {
    factSheet { id name rev }
  }
}
```

- `patches`: `{op, path, value}` with `op` = `add`, `replace` or `remove`; `path` is `/<fieldKey>`
  or `/<relationName>/<relationId>`; **`value` is always a string**. Scalars as text (numbers
  `"2000"`), structured values (lifecycle, externalId, tags, relations, multi-select, ACLs) as a
  JSON-encoded string.
- `rev` (`Long`): optional optimistic lock. Pass the `rev` you read; a concurrent change fails
  with `extensions.errorType` `REVISION_CLASH` ("DB revision of Fact Sheet has changed"); re-read
  and retry. Omit it to overwrite unconditionally. The scalar name `Long` comes from SAP sample
  code and a community library **(unconfirmed)**; inlining the value (`rev: 42`), as SAP's own
  scripts do, avoids depending on it.
- `validateOnly: true`: validation and permission checks without writing. Use it as the dry run of
  every bulk job and as a write-permission probe (Viewer tokens fail here).
- `comment`: stored in the history; **required when archiving**.

### Patch cookbook

| Goal | Patch |
|---|---|
| Text / single select / number | `{"op": "replace", "path": "/description", "value": "New text"}`; single select takes the option key (`"adequate"`); numbers as strings (`"12000"`). `/name` supports only `replace`. |
| Multiple select | `{"op": "replace", "path": "/hostingType", "value": "[\"cloud\",\"onPremise\"]"}` |
| Lifecycle (replace-all) | `{"op": "replace", "path": "/lifecycle", "value": "{\"phases\":[{\"phase\":\"active\",\"startDate\":\"2025-01-01\"},{\"phase\":\"endOfLife\",\"startDate\":\"2028-12-31\"}]}"}`; omitted phases are deleted, `remove` clears all phases. Read and merge first. |
| External id | `{"op": "replace", "path": "/externalId", "value": "{\"type\":\"ExternalId\",\"externalId\":\"CMDB-4711\",\"externalUrl\":\"https://cmdb/ci/4711\",\"comment\":\"synced\"}"}` (`"forceWrite": true` to overwrite a linked id; `remove` with `"value": ""` clears). Custom external-id fields use their own key as path. |
| Tags | add: `{"op": "add", "path": "/tags", "value": "[{\"tagId\":\"<uuid>\"}]"}`; create-and-attach ungrouped tags: `[{\"tagName\":\"Demo\"}]`; remove: `op: remove` with the same list; `replace` sets the whole list. Single-mode groups: remove the old tag before adding. |
| Add relation | `{"op": "add", "path": "/relApplicationToITComponent/new_1", "value": "{\"factSheetId\":\"<itcId>\",\"activeFrom\":\"2025-01-01\",\"technicalSuitability\":\"adequate\"}"}`; use a different `new_<n>` suffix per relation in one call (errors are attributed per suffix). |
| Update relation | `{"op": "replace", "path": "/relToSuccessor/<relationId>", "value": "{\"factSheetId\":\"<targetId>\",\"description\":\"...\",\"activeUntil\":\"2026-11-29\"}"}` (always include `factSheetId`) |
| Remove relation | `{"op": "remove", "path": "/relToSuccessor/<relationId>", "value": ""}` |
| Relation intentionally empty | `{"op": "add", "path": "/naFields", "value": "[\"relToParent\"]"}` (counts as complete) |
| Subtype | `{"op": "replace", "path": "/category", "value": "saas"}` **(unconfirmed, community)** |
| Quality seal | `{"op": "replace", "path": "/lxState", "value": "APPROVED"}` |
| Archive | `updateFactSheet(id, comment: "Decommissioned", patches: [{op: add, path: "/status", value: "ARCHIVED"}])` |
| Recover | same with `"ACTIVE"` (within the 90-day retention) |
| Virtual workspace ACLs | `{"op": "replace", "path": "/permittedReadACL", "value": "[{\"id\":\"<aceId>\"}]"}` (replace only, whole list) **(unconfirmed, community)** |

Dates are `yyyy-mm-dd`. Relation attribute keys are the relation's field keys from the data model.
There is **no documented hard-delete mutation**; the REST `DELETE /factSheets/{id}` also archives.
Permanent deletion happens after the retention period or from the UI trash.

### Other confirmed mutations

```graphql
# Subscriptions (type: RESPONSIBLE | ACCOUNTABLE | OBSERVER; roleIds from allSubscriptionRoles)
{ allSubscriptionRoles(filter: {factSheetType: Application}) { edges { node { id name subscriptionType } } } }
mutation { createSubscription(factSheetId: "<fsId>", user: {email: "owner@example.com"}, type: RESPONSIBLE,
                              roleIds: ["<roleId>"]) { id type user { email } roles { id name } } }
mutation { updateSubscription(id: "<subscriptionId>", user: {id: "<userId>"}, type: RESPONSIBLE,
                              roles: [{id: "<roleId>", comment: "changed"}]) { id } }
mutation { deleteSubscription(id: "<subscriptionId>") { id } }

# Resources (links; files and logos go through /graphql/upload with documentType: "logo")
mutation { createDocument(factSheetId: "<fsId>", name: "Runbook", url: "https://wiki/runbook", description: "Ops") { id name url } }
mutation ($patches: [Patch]!) { updateDocument(id: "<docId>", patches: $patches) { id url } }
mutation { deleteDocument(id: "<docId>") { name } }

# Comments
mutation { createComment(factSheetId: "<fsId>", message: "Imported from CMDB", status: ACTIVE) { id message } }
```

`createTag`, `updateTag`, `deleteTag`, `createTagGroup`, `updateComment`, `deleteComment`,
`deleteFactSheet` appear in community code but not in the documentation **(unconfirmed)**; prefer the
UI or the Integration API `inboundTag` processor for tag administration, and introspect the
`Mutation` type before relying on them.

## 6. Tags, subscriptions, comments, documents, event log

```graphql
{ allTags { edges { node { id name description color status tagGroup { id name mode restrictToFactSheetTypes } } } } }
{ allTagGroups { edges { node { id name shortName mode restrictToFactSheetTypes tags { edges { node { id name } } } } } } }
{ allSubscriptionRoles { edges { node { id name subscriptionType restrictToFactSheetTypes } } } }
{ allLogEvents(factSheetId: "<fsId>", eventTypes: [FACT_SHEET_TAG_ADDED, FACT_SHEET_TAG_REMOVED]) {
    edges { node { id eventType path oldValue newValue message createdAt user { email technicalUser } } } } }
```

Tag group `mode` is `SINGLE` or `MULTIPLE`; `restrictToFactSheetTypes` lists allowed types; tags
created on the fly land in "Other tags" (facet `_TAGS_`). Subscription **types** are fixed;
subscription **roles** are workspace-specific. `allLogEvents` is the fact sheet history (REST has
no equivalent); `user.technicalUser` distinguishes integration changes. There is no `allUsers`
query: users come from the MTM REST API (`auth-and-access.md` section 9).

## 7. Discovering the data model

- REST `GET https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/models/dataModel` (bearer token,
  Admin recommended) returns `data.factSheets.<Type>.fields.<key>` (with `type` discriminators such
  as `SINGLE_SELECT` plus `values`, `MULTIPLE_SELECT`, `STRING`, `INTEGER`, `DOUBLE`, `LIFECYCLE`,
  `LOCATION`, `EXTERNAL_ID`, `PROJECT_STATUS`, `AGGREGATED` **(discriminator spellings unconfirmed)**,
  `mandatory`, `quickSearch`, `fullTextSearch`, `inFacet`, `inView`), `data.factSheets.<Type>.subtypes`
  and `data.relations.<relName>` with `from.factSheetType`, `to.factSheetType`, `multiplicity`, `fields`,
  `constraints`, plus `externalIdFields` and `validators`. The same JSON is behind Administration >
  Integration API > three-dot menu > **Get Data Model**.
- Related REST endpoints: `/models/dataModel/enriched`, `/models/viewModel` (UI layout),
  `/models/languages/{id}` (labels: field keys and option keys to translations), `/models/authorization`
  (role model; `PUT` overwrites everything), `/models/metaModel`, `/models/metaModel/{factSheetType}`,
  `/models/metaModel/actionBatches` (change history), `/metaModel/permissionRoles?role=MEMBER&factSheetType=Application`,
  `/models/accessControlEntities`, `/models/reportingModel`. All under `/services/pathfinder/v1`.
- GraphQL: `__type(name: "Application")` lists fields and relations; `filterOptions` lists facet
  keys and option keys with labels.
- UI: Administration > Meta Model Configuration > type > Fields tab > field > **Key**.

Standard fact sheet types (meta model v4): `Objective`, `Platform`, `Initiative`, `Organization`,
`BusinessCapability`, `BusinessContext`, `DataObject`, `Application`, `Interface`, `Provider`,
`ITComponent`, `TechnicalStack` (shown as "Tech Category"); newer workspaces add `System`,
`DataProduct`, `Contract` **(keys unconfirmed)**. Meta model v3 workspaces still have `Project`,
`Process`, `UserGroup`. Subtypes live in `category` (ITComponent: SaaS / IaaS / PaaS / Software /
Hardware / Services / AI Model; Initiative: Idea / Program / Project / Epic; ...). Common option
keys: `functionalSuitability` = `unreasonable`, `insufficient`, `appropriate`, `perfect`;
`technicalSuitability` = `inappropriate`, `unreasonable`, `adequate`, `fullyAppropriate`. TIME
classification is a tag group ("Time Model"), not a field. Read the real model rather than assuming.

## 8. Errors, limits and batching

- GraphQL errors come back as HTTP **200** with `{"data": null, "errors": [{"message", "path",
  "locations", "extensions": {"errorType": "BUSINESS_LOGIC" | "MODEL_COMPLIANT" | "REVISION_CLASH", "objectPath"}}]}`.
  Inspect `errors` on every response; absence means success. Typical messages:
  `Validation error of type FieldUndefined`, `The path '/descriptio' is invalid in FactSheet schema Application.`,
  `[FS_VALIDATION_RELATION_NOT_UNIQUE_OUTGOING] Outgoing relation occurred twice!`,
  `Expected a String input, but it was a 'Integer'`, `DB revision of Fact Sheet has changed`.
- Several mutations in one request (aliases `m1: updateFactSheet(...)`, `m2: ...`) run in one
  transaction: if one is invalid **none** are applied and the response ends with
  `Error in Request. Transaction is rolled back!`. Chunk to about 50 mutations and validate first.
- HTTP `401`: token expired or wrong host. HTTP `403`: role or permission denies the operation. HTTP
  `429` (`USER_INTERVAL_REQUEST_LIMIT_EXCEEDED`): user-based limit of **1,800 requests per minute per
  user or technical user** across GraphQL, REST and UI; honour `Retry-After`, otherwise back off
  exponentially; stay under roughly 25 requests per second.
- Complexity / token limit: very large documents are rejected (`The request contains too many
  characters. To prevent Denial Of Service attacks, parsing has been cancelled.`). Narrow the selection,
  reduce `first`, split by type.
- Prefer variables over string interpolation (quotes and the stricter validation since 2025 break
  interpolated documents).

## 9. Worked examples

Authenticate, page through every Application with its IT Components, write a CSV:

```python
import csv, requests
HOST, TOKEN = "https://acme.leanix.net", "..."  # API token of a technical user (Viewer is enough)
jwt = requests.post(f"{HOST}/services/mtm/v1/oauth2/token", auth=("apitoken", TOKEN),
                    data={"grant_type": "client_credentials"}, timeout=30).json()["access_token"]
H = {"Authorization": f"Bearer {jwt}"}
Q = """query ($after: String) {
  allFactSheets(filter: {facetFilters: [{facetKey: "FactSheetTypes", keys: ["Application"]}]},
                first: 500, after: $after, sort: [{key: "displayName", order: asc}]) {
    pageInfo { hasNextPage endCursor }
    edges { node { id name ... on Application {
      lifecycle { asString }
      relApplicationToITComponent { edges { node { factSheet { name } } } } } } }
  } }"""
rows, after, seen = [], None, set()
while True:
    body = requests.post(f"{HOST}/services/pathfinder/v1/graphql", json={"query": Q, "variables": {"after": after}}, headers=H, timeout=120).json()
    if body.get("errors"):
        raise SystemExit(body["errors"])
    page = body["data"]["allFactSheets"]
    for e in page["edges"]:
        n = e["node"]
        if n["id"] in seen:
            continue
        seen.add(n["id"])
        rows.append({"id": n["id"], "name": n["name"], "phase": (n["lifecycle"] or {}).get("asString"),
                     "itComponents": "; ".join(x["node"]["factSheet"]["name"] for x in n["relApplicationToITComponent"]["edges"])})
    if not page["pageInfo"]["hasNextPage"]:
        break
    after = page["pageInfo"]["endCursor"]
with open("applications.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
```

Validate, then apply, a description and lifecycle change with optimistic locking:

```python
M = """mutation ($id: ID!, $rev: Long, $patches: [Patch]!, $validateOnly: Boolean, $comment: String) {
  updateFactSheet(id: $id, rev: $rev, patches: $patches, validateOnly: $validateOnly, comment: $comment) {
    factSheet { id rev } } }"""
fs = requests.post(f"{HOST}/services/pathfinder/v1/graphql", headers=H, json={
    "query": 'query($id: ID!){ factSheet(id:$id){ id rev ... on Application { lifecycle { phases { phase startDate } } } } }',
    "variables": {"id": FS_ID}}).json()["data"]["factSheet"]
phases = {p["phase"]: p["startDate"] for p in (fs.get("lifecycle") or {}).get("phases", [])}
phases["endOfLife"] = "2027-12-31"                                  # merge, because lifecycle is replace-all
patches = [{"op": "replace", "path": "/description", "value": "Owned by HR IT"},
           {"op": "replace", "path": "/lifecycle",
            "value": json.dumps({"phases": [{"phase": k, "startDate": v} for k, v in phases.items()]})}]
for validate in (True, False):
    body = requests.post(f"{HOST}/services/pathfinder/v1/graphql", headers=H, json={"query": M, "variables": {
        "id": FS_ID, "rev": fs["rev"], "patches": patches, "validateOnly": validate, "comment": "API sync"}}).json()
    if body.get("errors"):
        raise SystemExit(body["errors"])
```

The bundled `scripts/leanix_api.py` wraps all of this (`list`, `get`, `search`, `query`, `create`,
`update`, `relate`, `tag`, `archive`, `model`, `tags`, `events`), with token refresh, 429 backoff,
revision retry and CSV output.
