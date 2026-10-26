# Gotchas and failure causes

Short list of the things that bite integrators. Each entry says what happens, why, and what to do.

## Authentication and access

- **401 from the token endpoint with a valid-looking token.** The username must be literally
  `apitoken`, the body form-encoded `grant_type=client_credentials`, and the host the one from the
  workspace URL. A replaced or deleted technical user's token stops working immediately.
- **401 after about an hour.** The JWT lives 3600 s. Cache it with its expiry and re-exchange a
  minute early (or once on 401); do not request a token per call, SAP asks for reuse.
- **Token from one instance used against another host.** Tokens are issued per instance; call the
  same `{SUBDOMAIN}.leanix.net` you exchanged on.
- **403 on mutations.** Viewer tokens are read-only. Member tokens may still lack per-type
  permissions (Create / Archive / Import / Export, field-level update) configured under Meta Model
  Configuration > type > Permissions. Anything in the Administration area (Integration API
  configuration, webhooks, user management, meta model, technical users, MCP settings) needs Admin.
- **"Admin > API Tokens" in a tutorial.** Personal API tokens were deprecated in 2022 and cannot be
  created. Create a technical user. The API Tokens page now only shows `WorkspaceId` and `UserId`.
- **Quality seals break unexpectedly.** Member tokens break the seal of fact sheets they are not
  subscribed to; Admin tokens never do. Choose the role deliberately.
- **Changes attributed to the wrong account.** One shared Admin token hides who did what. One
  technical user per integration; the fact sheet history and `allLogEvents` show
  `user.technicalUser = true`.
- **Custom roles or ACEs cannot be set on a technical user.** They require an SSO-managed workspace
  with roles managed in the identity provider (and the virtual workspaces feature for ACEs).
- **Docs links return 301.** `docs.leanix.net` and `docs-eam.leanix.net` moved to
  `help.sap.com/docs/leanix/ea/<slug>`; the Help Portal is JavaScript-rendered, so plain fetches
  return only a title. The old `/services/*/v1/docs/` Swagger pages are gone; use the OpenAPI
  explorer or the raw spec URLs.

## GraphQL

- **HTTP 200 with errors.** GraphQL reports every operational failure in `errors[]`; absence of the
  field is success. Check it on every response.
- **Batched mutations are all-or-nothing.** One invalid alias rolls back the whole request
  (`Error in Request. Transaction is rolled back!`). Keep batches around 50 or smaller, validate
  first.
- **`value` must be a string.** Numbers as `"12"`, booleans as `"true"`, and lifecycle, tags,
  relations, external ids, multi-selects as JSON-encoded strings. `Expected a String input, but it
  was a 'Integer'` is this error.
- **Lifecycle replace-all.** A `/lifecycle` patch replaces every phase; omitted phases are deleted.
  Read, merge, write.
- **Tags by id, not name.** `/tags` takes `[{"tagId": "..."}]` (or `[{"tagName": ...}]` to create
  ungrouped tags on the fly). `add`/`remove` work incrementally; `replace` sets the whole list.
  Single-mode tag groups accept one tag at a time; remove before adding.
- **External id shape.** `/externalId` value is `{"type":"ExternalId","externalId":"..."}` (plus
  optional `externalUrl`, `comment`, `status`, `forceWrite`); custom external-id fields use their
  own key as path.
- **Relations are patched on the fact sheet.** `add` to `/relX/new_1` with `{"factSheetId": ...}`;
  `replace` or `remove` on `/relX/<relationId>` (the relation node id, not the target id). Relation
  attributes live on the relation, not the fact sheet. Duplicate relations fail with
  `FS_VALIDATION_RELATION_NOT_UNIQUE_OUTGOING`.
- **`name` supports only `replace`.** Typos in paths fail with `The path '/descriptio' is invalid in
  FactSheet schema Application.`
- **Archiving needs a comment** (`updateFactSheet(..., comment: "...")`) and is a status patch
  (`/status` = `ARCHIVED`; `ACTIVE` recovers within the 90-day retention). There is no documented
  hard-delete mutation.
- **Stale revision.** Passing `rev` makes the update conditional; `REVISION_CLASH` (`DB revision of
  Fact Sheet has changed`) means re-read `rev` and retry (3 attempts is SAP's own guidance).
- **Facet keys must be valid.** Since 2023 an unknown facet key fails the whole query. Discover keys
  with `allFactSheets(factSheetType: X) { filterOptions { facets { facetKey results { key } } } }`.
  Tag groups use the group **UUID** as facet key; `_TAGS_` is only for ungrouped tags. Type names
  differ from UI labels (`TechnicalStack` is "Tech Category").
- **Field keys, not labels.** Patches, facets, Excel and LDIF all use technical keys
  (`functionalSuitability`, option key `perfect`), never translations.
- **Pagination is forward-only and live.** `first`/`after` only; pages are not a snapshot, so
  de-duplicate on `id`. Always pass `first` (the default page size is undocumented); 500 to 1000
  works for narrow selections, less when relations are expanded.
- **Complexity limit.** Deep selections times large pages are rejected (`The request contains too
  many characters...`). Narrow the selection or split by type.
- **No `allUsers`.** Users and roles come from the MTM REST API; `Subscriptions` facets take user
  ids from there.
- **Read-after-write by search may lag.** Re-read by `factSheet(id:)` after a mutation instead of by
  `fullTextSearch`.
- **GraphiQL in the app needs no token** and is Admin-only by default; a script needs a technical
  user regardless.

## Integration API

- **Nothing happens.** `connectorType`/`connectorId` are not configured, or the Integration API is
  not enabled for the workspace (Customer Success Manager).
- **Runs are asynchronous and serialized per connector.** Create, start, poll `/status`; one run
  per `connectorId` at a time; order between runs is not guaranteed without `sequentialExecution`.
- **Bad rows are skipped silently.** Always read `/warnings`; use `logLevel: debug` while building.
- **`processingMode: full` archives everything untouched in the deletion scope.** Send complete
  data, set `maximumDeletionRatio`, test with `test=true` first.
- **`test=true` needs `start=true`** on `POST /synchronizationRuns`.
- **Runs longer than an hour fail half-way** unless the configuration carries `credentials`
  (`useTechnicalUser: true`, `technicalUserId` or `apiToken`); otherwise the run uses the caller's
  one-hour JWT.
- **LDIF bodies are capped at 50 MB**; use `dataProvider` (Azure Blob URL) or chunk the content.
- **External id required to create** fact sheets via `inboundFactSheet`; archived fact sheets
  matched by external id are recreated, matched by internal id they are reactivated.
- **Processor names** must not contain `+ * > =`.
- **`lxWorkspace`** is the workspace **UUID** (from Administration > API Tokens), used as a guard;
  a mismatch rejects the LDIF.

## Excel import, webhooks, metrics, MCP

- **Excel import**: `.xlsx` only, one fact sheet type per file, up to 10,000 rows (500 when
  relations or subscriptions are included), first sheet only, technical keys in row 1, values are
  case-sensitive, `;` separates multi-values, multi-select/relations/tags are **replaced** by the
  cell content, rows run top-down (create before relating), `action` = `Archive` archives.
- **Webhooks**: failed PUSH deliveries are retried every 50 seconds (no retry cap) and the
  subscription is deactivated automatically after more than 10 days of failures (enable the
  notification flag); there is no signature header, so authenticate deliveries with the
  configured authorization header; PULL events are kept 30 days and must be acknowledged
  with the cursor (or `autoCommit`); `FACT_SHEET_UPDATED` also fires on relation changes and has
  large payloads (payload limit 20 MB); the delivery type cannot be changed after creation.
- **Metrics v2**: create the schema explicitly (`POST /schemas`) before writing points; points with
  the same timestamp overwrite each other; link to fact sheets with a dimension attribute such as
  `factSheetId`.
- **Poll API v2 is deprecated** (March 2027); use the Survey API v1 for new work.
- **MCP server**: technical-user auth uses the raw API token (`Authorization: Token ...`) on
  `https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp`; user OAuth uses `mcp.leanix.net`;
  write tools are Admin-only by default; the server honours the same permissions as the UI.

## Copilot / agent usage

- Never print or persist credentials; read `LEANIX_*` environment variables.
- Test in a sandbox or demo workspace (same host, own technical user); production workspaces have
  no undo beyond the 90-day trash.
- Hard-code nothing that differs between workspaces: tag ids, subscription role ids, user ids,
  ACE ids, custom field keys. Resolve them at run time.
