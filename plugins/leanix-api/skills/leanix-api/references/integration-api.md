# SAP LeanIX Integration API (LDIF and processors)

The Integration API ingests or exports data in the LeanIX Data Interchange Format (LDIF). You send
plain JSON describing your source objects; **processors** configured in the workspace map them to
fact sheets, relations, tags, subscriptions, documents, metrics, impacts and to-dos. Researched
against the SAP Help Portal and the live OpenAPI specification (`/services/integration-api/v1`,
October 2026); items marked **(unconfirmed)** are inferred or community-sourced.

## Contents

1. [When to use it](#1-when-to-use-it)
2. [Concepts](#2-concepts)
3. [LDIF format](#3-ldif-format)
4. [Processor configuration anatomy](#4-processor-configuration-anatomy)
5. [Processor types and examples](#5-processor-types-and-examples)
6. [JUEL expression cheat sheet](#6-juel-expression-cheat-sheet)
7. [REST endpoints and the run lifecycle](#7-rest-endpoints-and-the-run-lifecycle)
8. [Safety: test runs, full mode, deletion scope, limits](#8-safety-test-runs-full-mode-deletion-scope-limits)
9. [Complete minimal example](#9-complete-minimal-example)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. When to use it

| Need | Pick |
|---|---|
| Recurring sync from another system, hundreds to tens of thousands of objects, keyed by an external id, idempotent re-runs | **Integration API** |
| Remove stale objects the source no longer sends | Integration API, `processingMode: full` with a `deletionScope` |
| Attributes on relations, tags with groups, subscriptions, documents, metrics in one feed | Integration API (one processor per entity kind, ordered by `run`) |
| Bulk export of a filtered inventory as JSON | Integration API outbound or `writeToLdif` processor |
| One-off reads, custom reports, a handful of targeted writes, anything needing immediate feedback | GraphQL (`graphql-api.md`) |
| Business users editing spreadsheets | Excel import/export (`other-apis.md`) |

The API tolerates bad rows (they are skipped and reported as warnings), runs asynchronously, retries
transient failures, and keeps mapping logic in the workspace configuration instead of in your code.
It has to be enabled for the workspace (ask the Customer Success Manager if Administration has no
**Integration API** section).

## 2. Concepts

- **Connector**: your middleware. It is identified by `connectorType` (the kind of source, e.g.
  `cmdb-sync`), `connectorId` (one deployment/instance of it, e.g. `prod-cmdb`) and
  `connectorVersion` (`n.n.n`). The triple plus `processingDirection` and `processingMode`
  selects the processor configuration. Both type and id must already be configured in the
  workspace, otherwise "Incoming data cannot be processed".
- **Processor configuration**: JSON with a `processors` array (and optional `variables`,
  `deletionScope`, `executionGroups`, ...) stored under Administration > **Integration API**. It is
  versioned; when the LDIF omits `connectorVersion`, the highest `n.n.n` version runs.
- **Processing direction**: `inbound` (external data into LeanIX) or `outbound` (LeanIX data to an
  LDIF you download). SAP recommends the `writeToLdif` inbound processor over outbound processors.
- **Processing mode**: `partial` (default, upserts only) or `full` (the LDIF is the complete truth;
  objects in the configured `deletionScope` that the run did not touch are archived).
- **Synchronization run**: one execution of one configuration with one LDIF. Create, start, poll
  status, read results and warnings. Only one run per `connectorId` executes at a time; order of
  runs for the same connector is not guaranteed unless `sequentialExecution: true` is set on the
  configuration.
- **Run levels**: each processor has `"run": N`; level 0 completes before level 1 starts. Create
  fact sheets in run 0, relations and tags in run 1, so targets exist.

## 3. LDIF format

```json
{
  "connectorType": "cmdb-sync",
  "connectorId": "prod-cmdb",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "lxWorkspace": "19fcafab-cb8a-4b7c-97fe-7c779345e20e",
  "description": "Nightly CMDB export",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {"runDate": "2026-10-26"},
  "content": [
    {"type": "Application", "id": "APP-1001",
     "data": {"name": "Payroll Portal", "description": "HR self-service", "owner": "jane@example.com",
              "phaseIn": "2019-02-01", "active": "2019-06-01", "endOfLife": null, "tags": ["HR", "Cloud"]}},
    {"type": "Server", "id": "SRV-77",
     "data": {"name": "pay-db-01", "appId": "APP-1001", "os": "Linux", "category": "hardware"}}
  ]
}
```

| Field | Notes |
|---|---|
| `connectorType`, `connectorId`, `processingDirection` | Required. Must match a stored configuration. |
| `connectorVersion` | Optional for `n.n.n` versions (highest wins); otherwise the exact string. |
| `lxVersion` | Integration API version the connector targets, `"1.0.0"`. |
| `lxWorkspace` | Optional safety check: the workspace **UUID**; the run is rejected if it does not match. |
| `processingMode` | `partial` (default) or `full`. |
| `description`, `customFields`, `chunkInformation` | Free text; a map usable in every processor as `${header.customFields.x}`; chunk markers for split LDIFs. |
| `content[]` | Each object needs `type` (your grouping, matched by processor filters), `id` (stable identity in the source; becomes the external id), `data` (flat or nested map; values are strings, lists or maps). |

Every header value except `content` is limited to 500 characters. Unknown fields are ignored
silently. Keep `id` unique per `type`, and reuse the same `connectorId` for the same source so
ownership and deletion scoping stay consistent.

## 4. Processor configuration anatomy

```json
{
  "processors": [
    {
      "processorType": "inboundFactSheet",
      "processorName": "Applications",
      "processorDescription": "Creates or updates Applications from CMDB apps",
      "type": "Application",
      "run": 0,
      "enabled": true,
      "logLevel": "warning",
      "filter": {"exactType": "Application"},
      "identifier": {"external": {"id": {"expr": "${content.id}"}, "type": {"expr": "externalId"}}},
      "updates": [
        {"key": {"expr": "name"}, "values": [{"expr": "${data.name}"}]},
        {"key": {"expr": "description"}, "values": [{"expr": "${data.description}"}], "optional": true},
        {"key": {"expr": "lifecycle.active"}, "values": [{"expr": "${data.active}"}]},
        {"key": {"expr": "category"}, "values": [
          {"expr": "${data.category}", "regexMatch": "(saas|cloud_service)", "regexReplace": {"match": "^.*$", "replace": "saas"}},
          {"expr": "${data.category}"}]}
      ],
      "variables": []
    }
  ],
  "variables": {},
  "deletionScope": {},
  "executionGroups": [],
  "sequentialExecution": false
}
```

| Section | Purpose |
|---|---|
| `filter` | Which content objects this processor handles. `exactType` (exact match, recommended), `type` (prefix/regex), `id` (regex), `advanced` (JUEL boolean, e.g. `${data.os != null}`), `onRead` (JUEL over values read from the existing fact sheet), `updatedInDuration` (`"P3D"`, only fact sheets changed recently). All filters must match (AND). |
| `identifier` | Which LeanIX entity to write. `external: {id, type}` upserts by external id (creates when missing; `type` is the external-id field key, `externalId` by default, or a custom one such as `serviceNowExternalId`); `internal: "${...}"` targets an existing fact sheet UUID; `search: {scope: {facetFilters, ids}, filter, multipleMatchesAllowed}` updates everything matching an inventory filter. `inboundRelation` uses `from` and `to` instead. |
| `updates` | List of `{key: {expr, regexReplace?}, values: [{expr, regexMatch?, regexReplace?, map?, forEach?}], optional?}`. The first value whose `regexMatch` matches (or without one) wins. Field keys are the data-model keys; nested keys use dots (`lifecycle.active`, `externalId.externalUrl`, `newUser.email`, `group.name`). |
| `mode` | `"delete"` archives the identified fact sheet (same as UI delete); default is create-or-update. |
| `run` | Execution level (integer). |
| `enabled`, `logLevel` | Switch the processor off; `off` / `warning` (default) / `debug` for per-object `debugInfo` in the output log. |
| `variables` (processor) and `variables` (global) | Collect values during a run (`key`, `value`, `forEach`) and read them later with `${integration.variables.<key>}`; used for aggregation across content objects. |
| `read` | Fields to read from the target fact sheet before updating (`"read": {"fields": ["name", "technicalSuitability"]}`), available as `${lx.factsheet.<field>}` and in `onRead` filters. |
| `deletionScope` (global) | For `processingMode: full`: `maximumDeletionRatio`, and per entity kind (`factSheets`, `relations`, `tags`, `subscriptions`, `documents`, `impacts`, `todos`) the scope (facet filters / types) of objects that may be archived when untouched. |
| `executionRestrictions` | Restrict who may run the configuration (`defaultTechnicalUser`, `userIds`) |
| `credentials` | `{"useTechnicalUser": true}` (auto-created technical user `INTEGRATION_API`), `{"technicalUserId": "<id>"}` or `{"apiToken": "..."}`: the run authenticates with this identity instead of the caller's JWT. Required for runs that outlive the caller's one-hour token, and the way to attribute every change to one integration user |
| `dataProvider` | `{"url": "<Azure Blob SAS URL>"}` reads the LDIF from storage instead of `content` (LDIF bodies are limited to 50 MB; see also `POST /synchronizationRuns/withUrlInput` and `GET /storages/azure`) |
| `executionGroups` | Names used by `POST /synchronizationRuns/withExecutionGroup` to run several configurations as one (REST only; processors merge, no ordering). |
| `description` keys | Allowed inside `identifier`, `variables`, `updates` and `values` purely as comments. |

Writable field types through `updates`: STRING, SINGLE_SELECT (option key), MULTIPLE_SELECT,
DOUBLE, INTEGER, LOCATION (address string or `"lat, lon"`; prefix `#` to accept the first match),
LIFECYCLE (`lifecycle.plan|phaseIn|active|phaseOut|endOfLife`, `yyyy-mm-dd`), EXTERNALID
(`externalId.externalId|externalUrl|comment|status|externalVersion`), PROJECT, MILESTONE,
FACTSHEETSTATE. Values must be the technical keys, never UI labels.

## 5. Processor types and examples

| `processorType` | Writes | Required keys |
|---|---|---|
| `inboundFactSheet` | Fact sheet of `type`; `mode: delete` archives | `type`, `identifier`, `updates` incl. `name` on create; external id mandatory for creation |
| `inboundRelation` | Relation `type` (e.g. `relApplicationToITComponent`, `relToParent`) between `from` and `to`; attributes `description`, `activeFrom`, `activeUntil` (ISO 8601), relation fields, `constrainingRelations` / `addConstrainingRelations` | `type`, `from`, `to` |
| `inboundTag` | Tag groups (create/update), tags (create/update/delete) and assignments | `factSheets` (identifier for the targets), `updates` with `name`, optional `description`, `color`, `group.name`, `group.shortName`, `group.description`, `group.mode` (`SINGLE`/`MULTIPLE`); tags without group go to "Other tags"; tags can only be removed globally |
| `inboundSubscription` | Subscription on the identified fact sheet | `user` or `newUser.*` (creates the user), `subscriptionType` (`RESPONSIBLE`/`ACCOUNTABLE`/`OBSERVER`), optional `subscriptionRoles` / `addSubscriptionRoles` (`map` of `roleName`, `comment`), `optional`, `comment`; Accountable is not replaced automatically |
| `inboundDocument` | Resource (link) on the fact sheet | `name` (mandatory), `description`, `url`, `origin` |
| `inboundMetrics` | One metrics point per content object | metric schema configuration, see the Metrics section of `other-apis.md` |
| `inboundImpact` | Transformation impacts (one per processor, `forEach` for lists) | impact-specific keys |
| `inboundToDo` | To-dos | to-do keys |
| `variableProcessor` | Collects variables only | `variables` |
| `writeToLdif` | Adds objects to an output LDIF available at `/results` after the run (export, transform, or read-then-write in one run) | `updates` with `content.id`, `content.type`, `data.*`; global LDIF header keys in the configuration |
| Outbound processors (`outboundFactSheet`, ...) | Export fact sheets in a `scope` to LDIF | prefer `writeToLdif` |

Relation example (run 1, after the fact sheets of run 0):

```json
{
  "processorType": "inboundRelation",
  "processorName": "App to IT Component",
  "type": "relApplicationToITComponent",
  "run": 1,
  "filter": {"exactType": "Server"},
  "from": {"external": {"id": {"expr": "${data.appId}"}, "type": {"expr": "externalId"}}},
  "to":   {"external": {"id": {"expr": "${content.id}"}, "type": {"expr": "externalId"}}},
  "updates": [
    {"key": {"expr": "description"}, "values": [{"expr": "Discovered by CMDB"}]},
    {"key": {"expr": "activeFrom"}, "values": [{"expr": "${data.since}"}]}
  ]
}
```

Tag example (array of tag names in `data.tags`):

```json
{
  "processorType": "inboundTag",
  "processorName": "Tags from CMDB",
  "run": 1,
  "filter": {"exactType": "Application"},
  "factSheets": {"external": {"ids": "${content.id}", "type": {"expr": "externalId"}}},
  "updates": [
    {"key": {"expr": "name"}, "values": [{"forEach": {"elementOf": "${data.tags}"}, "expr": "${integration.valueOfForEach}"}]},
    {"key": {"expr": "group.name"}, "values": [{"expr": "CMDB"}]},
    {"key": {"expr": "group.mode"}, "values": [{"expr": "MULTIPLE"}]}
  ]
}
```

Subscription example: keys `user` (email), `subscriptionType`, `subscriptionRoles` with a `map` of
`roleName`/`comment`, and `newUser.userName|email|firstName|lastName` to create missing users.

## 6. JUEL expression cheat sheet

| Expression | Meaning |
|---|---|
| `${content.id}`, `${content.type}` | The content object's id and type |
| `${data.name}`, `${data.owner.email}` | Values from the content `data` map (dot path) |
| `${header.processingMode}`, `${header.customFields.runDate}` | LDIF header values |
| `${data.plan == null ? '2014-01-01' : data.plan}` | Conditional defaults |
| `${content.id.replaceAll('/', '_')}` | Java string methods work on values |
| `${integration.valueOfForEach}` | Current element of a `forEach` over a list in `values` |
| `${integration.variables.valueOfForEach.target.id}` | Element of a `forEach` inside `variables` |
| `${integration.variables.myKey}` | Variable collected earlier in the run |
| `${integration.contentIndex}`, `${integration.maxContentIndex}` | Position of the content object (e.g. `${integration.contentIndex==0}` to run once) |
| `${integration.indexOfForEach}`, `${integration.keyOfForEach}` | Index (or map key) of the current `forEach` element |
| `${integration.now}` | Run timestamp (Java LocalDateTime: `.plusHours(1)`, `.getYear()`) |
| `${integration.toJson(obj)}`, `${integration.toObject(json)}` | Serialise / parse JSON |
| `${helper:toList('a','b')}`, `${helper:toList(data.tags.split(','))}` | Build lists (comma-separated strings into `forEach`) |
| `${helper:toActiveLifecyclePhase(lx.factsheet.lifecycle, integration.now)}` | Current lifecycle phase of a read fact sheet |
| `${helper:localDateTimeFromString(s, inFmt, outFmt)}`, `${helper:localDateTimeToString(integration.now, fmt)}`, `${helper:getDuration(t1, t2)}` | Date conversion |
| `${helper:addIfNotExisting(lx.factsheet.alias, 'marker')}` | Append a value once (owner markers for multi-source deletion) |
| `${math:abs(x)}`, `${math:round(x)}` | Arithmetic |
| `${variables.costs.sum()}`, `.distinct()`, `.join(', ')`, `.count()`, `.average()`, `.max()` | Aggregations over collected variables |
| `{"key": {"expr": "tagsReadOnly"}, "values": [{"expr": "${true}"}]}` | In `inboundTag`: only assign existing tags, never create |
| `${lx.factsheet.technicalSuitability}` | Field read from the existing fact sheet (`read.fields`) |
| `${lx.relations}` | Relations read from the fact sheet (identifier `search` processors) |
| `${integration.tags.getTagGroupId('Region')}`, `${integration.tags.getTagId('Region','APAC')}` | Resolve tag ids for facet filters |
| `regexMatch` / `regexReplace: {match, replace}` | Select a value only when it matches; rewrite it (used for mapping source values to option keys) |
| `"filter": "${true}"` inside `forEach` | Keep or drop elements |

Processor names must not contain operator characters (`+`, `*`, `>`, `=`).

## 7. REST endpoints and the run lifecycle

Base `https://{SUBDOMAIN}.leanix.net/services/integration-api/v1`, bearer token. Admin (or a
technical user the configuration's execution restrictions allow).

| Method and path | Purpose |
|---|---|
| `GET /configurations?connectorType&connectorId&connectorVersion&processingDirection&processingMode` | List processor configurations |
| `PUT /configurations` | Create or replace one (body: the configuration JSON plus `connectorType`, `connectorId`, `connectorVersion`, `processingDirection`, `processingMode`, optional `sequentialExecution`); 204 |
| `DELETE /configurations?...` | Delete one (all five selectors) |
| `POST /synchronizationRuns?start=true&test=false` | Create a run from an LDIF body. `start=true` enqueues it immediately; `test=true` (requires `start=true`) makes it a dry run. Response `{"id": "<runId>", ...}` |
| `POST /synchronizationRuns/{id}/start?test=false` | Start a run created with `start=false` (400 if already started) |
| `GET /synchronizationRuns/{id}/status` | `{"id": "...", "status": "CREATED" \| "SEQUENTIALIZED" \| "PENDING" \| "IN_PROGRESS" \| "FINISHED" \| "STOPPED" \| "FAILED", "description": "..."}` |
| `GET /synchronizationRuns/{id}/progress` | Counters per run level while executing |
| `GET /synchronizationRuns/{id}/results` | Output LDIF (outbound / `writeToLdif`); 204 when the run produced none |
| `GET /synchronizationRuns/{id}/resultsUrl` | Download URL for large results |
| `GET /synchronizationRuns/{id}/warnings?offset=0&limit=100` | Warnings and errors (`processor`, `content`, `message`, `detail`, `category`, `status` = `WARNING`/`ERROR`); `offset` must be a multiple of `limit` |
| `GET /synchronizationRuns/{id}/stats`, `/debug`, `/debugVariables` | Statistics, debug log, variable dumps (`logLevel: debug`) |
| `POST /synchronizationRuns/{id}/stop` | Cancel a pending or running run |
| `GET /synchronizationRuns` | Status of all runs of the workspace |
| `POST /synchronizationRuns/withConfig?start&test` | Run an inline configuration plus LDIF (testing only, per the spec) |
| `POST /synchronizationRuns/withExecutionGroup`, `/withUrlInput`, `/withExecutionGroupAndUrlInput` | Execution groups; LDIF fetched from a URL / Azure storage (`GET /storages/azure`) |
| `POST /fastSynchronizationRuns?test` | Synchronous "fast run" for small inbound LDIFs; returns the result report directly (no outbound support) |
| `GET /examples/starterExample`, `/examples/advancedExample` | Example configuration + input pairs |

Typical lifecycle:

```text
PUT /configurations (once, or from the UI)        -> 204
POST /synchronizationRuns?start=true&test=true     -> {"id": R}   dry run
GET  /synchronizationRuns/R/status  (poll)         -> FINISHED
GET  /synchronizationRuns/R/warnings               -> fix the mapping if needed
POST /synchronizationRuns?start=true&test=false    -> {"id": R2}  real run
GET  /synchronizationRuns/R2/status (poll) ; GET /warnings ; GET /results (if writeToLdif)
```

Webhook events `INTEGRATION_RUN_STARTED`, `INTEGRATION_RUN_FINISHED`, `INTEGRATION_RUN_ABORTED`
and `CONFIGURATION_*` exist for run monitoring, and Administration > **Sync Logging** shows run
history.

## 8. Safety: test runs, full mode, deletion scope, limits

- **Test first.** `test=true` validates the configuration against real data and fills the output
  log without writing. Use it in CI for every mapping change.
- **Full mode deletes.** With `processingMode: full`, every artifact the run creates or updates is
  marked "touched"; at the end everything inside `deletionScope` that was not touched is archived
  (fact sheets last). A truncated or partial LDIF in full mode means mass archiving.
  `maximumDeletionRatio` (percent per entity kind, **default 50**, `101` allows everything) aborts a
  kind's deletions when too much would go; keep it low in production, send complete data, and
  prefer `partial` plus an explicit `mode: delete` processor when you know what disappeared.
  Multi-source ownership uses owner markers (`${helper:addIfNotExisting(lx.factsheet.<field>, 'mySource')}`):
  a fact sheet is archived only when its marker list becomes empty.
- **Size and duration.** LDIF bodies up to 50 MB; above that use `dataProvider` (Azure Blob URL) or
  chunk with `chunkInformation`. A run that outlives the caller's one-hour JWT needs `credentials`
  (`useTechnicalUser`, `technicalUserId` or `apiToken`) in the configuration.
- **Archived fact sheets**: updating an archived fact sheet via external id creates a new one;
  via internal id reactivates the old one.
- **One run per connector at a time.** Wait for `FINISHED` before sending the next LDIF for the
  same `connectorId`, or stagger connectors.
- **Rate limits**: the Integration API itself is throttled toward Pathfinder (1,200 requests per
  minute per workspace for internal services) and reschedules automatically; your calls to the
  Integration API endpoints count against your technical user's 1,800 per minute.
- **Silent tolerance**: rows that fail validation are skipped, not fatal. Read `/warnings` after
  every run and alert on `status: ERROR`. Use `logLevel: debug` while developing, `warning` in
  production, `off` only for processors whose warnings are expected noise.
- **Idempotency**: identify by external id (`identifier.external`) with a stable `content.id`;
  re-running the same LDIF must produce no changes. Keep exactly one active fact sheet per external
  id; duplicates make matching ambiguous.
- **Attribution**: changes appear in fact sheet history under the technical user that created the
  run (or the configured default technical user).

## 9. Complete minimal example

Processor configuration (store once with `PUT /configurations` or in the UI):

```json
{
  "connectorType": "cmdb-sync", "connectorId": "prod-cmdb", "connectorVersion": "1.0.0",
  "processingDirection": "inbound", "processingMode": "partial",
  "processors": [
    {"processorType": "inboundFactSheet", "processorName": "Applications", "type": "Application", "run": 0,
     "filter": {"exactType": "Application"},
     "identifier": {"external": {"id": {"expr": "${content.id}"}, "type": {"expr": "externalId"}}},
     "updates": [
       {"key": {"expr": "name"}, "values": [{"expr": "${data.name}"}]},
       {"key": {"expr": "description"}, "values": [{"expr": "${data.description}"}], "optional": true},
       {"key": {"expr": "lifecycle.active"}, "values": [{"expr": "${data.active}"}], "optional": true}]},
    {"processorType": "inboundFactSheet", "processorName": "Servers", "type": "ITComponent", "run": 0,
     "filter": {"exactType": "Server"},
     "identifier": {"external": {"id": {"expr": "${content.id}"}, "type": {"expr": "externalId"}}},
     "updates": [
       {"key": {"expr": "name"}, "values": [{"expr": "${data.name}"}]},
       {"key": {"expr": "category"}, "values": [{"expr": "hardware"}]}]},
    {"processorType": "inboundRelation", "processorName": "App runs on Server", "type": "relApplicationToITComponent", "run": 1,
     "filter": {"exactType": "Server"},
     "from": {"external": {"id": {"expr": "${data.appId}"}, "type": {"expr": "externalId"}}},
     "to": {"external": {"id": {"expr": "${content.id}"}, "type": {"expr": "externalId"}}},
     "updates": []}
  ],
  "variables": {}
}
```

Python (standard library) to run and poll:

```python
import json, time, urllib.request, base64
HOST, API_TOKEN = "https://acme.leanix.net", "..."

def token():
    req = urllib.request.Request(f"{HOST}/services/mtm/v1/oauth2/token", data=b"grant_type=client_credentials", method="POST",
        headers={"Authorization": "Basic " + base64.b64encode(f"apitoken:{API_TOKEN}".encode()).decode(),
                 "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]

def call(method, path, body=None, jwt=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{HOST}/services/integration-api/v1{path}", data=data, method=method,
                                 headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
        return json.loads(raw) if raw else None

jwt = token()
ldif = json.load(open("ldif.json"))
run = call("POST", "/synchronizationRuns?start=true&test=true", ldif, jwt)      # dry run first
run_id = run["id"] if isinstance(run, dict) else run[0]["id"]
while True:
    status = call("GET", f"/synchronizationRuns/{run_id}/status", jwt=jwt)["status"]
    if status in ("FINISHED", "FAILED", "ABORTED", "CANCELLED"):
        break
    time.sleep(5)
warnings = call("GET", f"/synchronizationRuns/{run_id}/warnings?offset=0&limit=100", jwt=jwt) or []
print(status, len(warnings), "warnings"); print(json.dumps(warnings[:5], indent=2))
```

`scripts/leanix_api.py sync ldif.json --test` and `--wait` wrap this flow (create with start,
poll, print status and warnings); `processors put config.json` stores a configuration.

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Run stays `PENDING` | Another run of the same `connectorId` is active, or the platform queue is busy | Wait; check `GET /synchronizationRuns` |
| 403 on `/synchronizationRuns` | Token role not allowed (execution restrictions, non-admin) or Integration API not enabled | Use an Admin technical user or the configured default technical user; ask the CSM |
| "Incoming data cannot be processed" / no processors matched | `connectorType`/`connectorId` do not match a configuration, or filters never match the content `type` | Compare the LDIF header with the configuration; use `exactType` |
| Fact sheets created twice | External id changed, `type` of identifier points to another external-id field, or an archived fact sheet was re-sent (archived + external id = new fact sheet) | Keep `content.id` stable; use `internal` ids to reactivate archived ones |
| Relation not created | Target fact sheet does not exist yet (same run level), wrong relation name, duplicate relation | Put relations in `run: 1`; read the relation key from the data model |
| Field not written | Label used instead of key, wrong option key, value type (dates must be `yyyy-mm-dd`), field hidden for the role | Check `/warnings` and `Get Data Model`; set `logLevel: debug` |
| Mass archive after a run | `processingMode: full` with an incomplete LDIF | Use `partial`; set `maximumDeletionRatio`; recover from the trash within 90 days |
| `/results` returns 204 | Inbound run without `writeToLdif` | Expected; use `/warnings` and `/stats` for the outcome |
