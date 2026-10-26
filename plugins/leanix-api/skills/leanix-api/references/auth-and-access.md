# SAP LeanIX: authentication, technical users, roles, permissions and admin setup

Researched against the SAP Help Portal (help.sap.com/docs/leanix/ea, October 2026), the live
OpenAPI specifications served by the platform, the product update feed and SAP sample code. Items
marked **(unconfirmed)** come from community posts, third-party guides or inference.

## Contents

1. [The one credential model](#1-the-one-credential-model)
2. [Token exchange: API token to bearer JWT](#2-token-exchange-api-token-to-bearer-jwt)
3. [Hosts, subdomains and the workspace URL](#3-hosts-subdomains-and-the-workspace-url)
4. [Technical users (UI and MTM API)](#4-technical-users-ui-and-mtm-api)
5. [Roles and permissions](#5-roles-and-permissions)
6. [Fact-sheet-level access: virtual workspaces and ACEs](#6-fact-sheet-level-access-virtual-workspaces-and-aces)
7. [Least privilege per integration type](#7-least-privilege-per-integration-type)
8. [Administration: workspace id, developer tools, feature toggles](#8-administration-workspace-id-developer-tools-feature-toggles)
9. [User administration through the MTM API](#9-user-administration-through-the-mtm-api)
10. [Rate limits, audit trail, network](#10-rate-limits-audit-trail-network)
11. [Zero-to-first-call checklist](#11-zero-to-first-call-checklist)
12. [Troubleshooting 401 / 403 / 404 / 429](#12-troubleshooting-401--403--404--429)

---

## 1. The one credential model

SAP LeanIX has a single customer-facing API credential: the **API token of a technical user**. It is
exchanged for a short-lived **bearer JWT** through an OAuth 2.0 client-credentials call, and the JWT
is sent as `Authorization: Bearer ...` to every service (GraphQL, Pathfinder REST, Integration API,
Webhooks, Metrics, MTM, Import/Export, Survey, ...).

| What | Value |
|---|---|
| Credential | API token, created with a technical user by a workspace **Admin** (Administration > Technical Users) |
| Exchange | `POST https://{SUBDOMAIN}.leanix.net/services/mtm/v1/oauth2/token`, HTTP Basic `apitoken:<API token>`, body `grant_type=client_credentials` |
| Result | JWT access token, `expires_in` 3600 s (shown as 3599), no refresh token for customers |
| Use | `Authorization: Bearer <JWT>` on every request |
| Scope | The technical user's workspace **role** (Admin / Member / Viewer, plus optional SSO custom roles and access control entities). Permissions apply to APIs exactly as to the UI. |
| Not available | client_id/client_secret OAuth clients, SAP BTP / IAS-issued API credentials, personal API tokens (deprecated 2022). The MCP server is the only service that also accepts the raw API token (`Authorization: Token <API token>`). |

There is no sandbox API host: tests run against a sandbox or demo **workspace** on the same
regional host, with its own technical user.

## 2. Token exchange: API token to bearer JWT

```bash
curl -u apitoken:$LEANIX_API_TOKEN \
  --request POST https://{SUBDOMAIN}.leanix.net/services/mtm/v1/oauth2/token \
  --data grant_type=client_credentials
# {"scope":"","expired":false,"access_token":"eyJhbGciOiJSUzI1NiJ9...","token_type":"bearer","expires_in":3599}
```

```python
import requests
r = requests.post(f"https://{SUBDOMAIN}.leanix.net/services/mtm/v1/oauth2/token",
                  auth=("apitoken", API_TOKEN), data={"grant_type": "client_credentials"}, timeout=30)
r.raise_for_status()
jwt = r.json()["access_token"]
headers = {"Authorization": f"Bearer {jwt}"}
```

Rules that matter in scripts:

- The username is literally `apitoken`; the API token is the password. The body is form-encoded,
  not JSON.
- Reuse the token for its lifetime. SAP asks you not to request a new token while the current one is
  valid; cache it with its expiry and re-exchange about a minute before `exp`, or once on a `401`.
- The JWT payload (base64url, unsigned decode) carries `exp`, `iss`, `sub` and a `principal` object.
  SAP's own sample code reads `principal.permission.workspaceId` and `principal.permission.workspaceName`
  from it; the role is under `principal.permission.role` **(unconfirmed claim paths, used by SAP
  samples but not documented)**. Use them for logging and a "right workspace?" guard, not as a
  security control.
- A token is bound to the instance that issued it. Exchange it on the same host you call.
- Postman: Authorization type OAuth 2.0, grant Client Credentials, token URL as above, Client ID
  `apitoken`, Client Secret = API token, "Send as Basic Auth header".
- The MTM spec also lists `password`, `refresh_token`, `client_id`/`client_secret` body fields and a
  `refresh_token` response field; none of them is documented for customers **(unconfirmed)**.

Headers for the services: `Authorization: Bearer <JWT>`, `Content-Type: application/json` on
JSON bodies, `Accept: application/json`. GraphQL additionally accepts
`x-graphql-enable-extensions: true` to receive validation warnings in `extensions.warnings`.

## 3. Hosts, subdomains and the workspace URL

- Workspace URL: `https://{SUBDOMAIN}.leanix.net/{WORKSPACE_NAME}/`. The first label is the
  instance (subdomain) and is the base URL for every API call: `https://{SUBDOMAIN}.leanix.net`.
- Regional hosts on the official login page: `ae`, `au`, `br`, `ca`, `ch`, `de`, `eu`, `jp`, `sg`,
  `uk`, `us` (`.leanix.net`), plus `app.leanix.net` (the original instance) and dedicated SSO
  domains `{company}.leanix.net`. Numbered hosts such as `eu-1` or `demo-eu-1` exist but are not
  published **(unconfirmed)**.
- `mcp.leanix.net` hosts only the user-OAuth MCP endpoint. `help.sap.com/docs/leanix/ea/...` hosts
  the documentation; the old `docs.leanix.net` and `docs-eam.leanix.net` URLs redirect there.
- Programmatic discovery: `GET /services/mtm/v1/workspaces` lists the workspaces the token can see
  with `id`, `name`, `url`, `instance`, `type` (`LIVE`, `DEMO`, `SANDBOX`) and `product`
  (`EAM`, `VSM`, `SMP`).
- Service path prefixes under the base URL: `/services/mtm/v1`, `/services/pathfinder/v1`,
  `/services/integration-api/v1`, `/services/webhooks/v1`, `/services/metrics/v2`,
  `/services/import-export/v1`, `/services/survey/v1` (Poll v2 is deprecated for March 2027),
  `/services/mcp-server/v1`, `/services/mtm/v1/scim/v2`.

## 4. Technical users (UI and MTM API)

### UI (Admin only)

1. Profile menu > **Administration** > **Technical Users** (category Discovery and Integrations).
2. **New Technical User**, then fill in:
   - **Username** (shown as the author of API changes in fact sheet history).
   - **Description** (optional).
   - **Permission Role**: **Admin**, **Member** or **Viewer**.
   - **Customer Roles** (optional): SSO-managed custom roles, only when the workspace manages roles
     in the identity provider.
   - **Access Control Entities** (optional): ACE ids when virtual workspaces are in use.
   - **Expiry Date** of the API token (mandatory in the UI; no documented maximum).
3. **Save**. The API token is displayed **once**. Store it in a secrets manager.

Managing: **Replace token** (old token stops working immediately), edit (expiry can be extended
without changing the token), **History** (changelog of the user and its token), trash icon
(deletes user and token). Technical users can be subscribed to fact sheets and notifications; they
do not appear in the Users list but count in its totals. No documented limit on their number and
no documented seat cost.

### MTM REST (Admin token)

| Call | Purpose |
|---|---|
| `GET /services/mtm/v1/technicalusers?workspaceId=...&page=1&size=100` | List technical users of a workspace (`queryUserName`, `sort=userName-ASC`) |
| `POST /services/mtm/v1/technicalusers?workspaceId={workspaceId}` | Create one. Body `{"userName": "svc-cmdb-sync", "permissionRole": "MEMBER", "apiTokenData": {"expiry": "2027-12-31T00:00:00Z", "description": "CMDB sync"}, "customerRoles": "", "accessControlEntities": ""}`; the response carries `data.apiTokenData.token` once |
| `PUT /services/mtm/v1/technicalusers/{id}` | Update role, expiry, description |
| `PUT /services/mtm/v1/technicalusers/{id}/replaceToken` | Rotate the token |
| `GET /services/mtm/v1/technicalusers/{id}/changelog` | Audit events (`APITOKEN_CREATE`, `APITOKEN_UPDATE`, `TECHNICAL_USER_LOGIN`, ...) |
| `DELETE /services/mtm/v1/technicalusers/{id}` | Delete (409 while a permission still exists) |

`permissionRole` enum in the spec: `ADMIN`, `MEMBER`, `VIEWER`, `CONTACT`, `TRANSIENT` and internal
`SYSTEM_*` values; use the first three.

### Legacy personal API tokens

Deprecated February 2022, creation blocked since March 2022. The Administration > **API Tokens**
page now only shows the `WorkspaceId` and `UserId` values. Any tutorial that says "Admin > API
Tokens > create token" is stale; create a technical user instead.

## 5. Roles and permissions

### Standard workspace roles

| Role | Default fact sheet permissions | Typical API use |
|---|---|---|
| **Viewer** | View, subscribe to and comment on all fact sheets | Read-only reporting (GraphQL queries, REST reads) |
| **Member** | View, create and modify all fact sheets | Data writes: create/update/archive fact sheets, relations, tags, subscriptions, comments, documents |
| **Admin** | Everything a Member can do plus the whole Administration area | Integration API configuration, webhooks, user management (MTM), meta model, technical users, MCP settings |

Roles are enforced identically for the UI and for every API. The **Administration area is
hard-coded to Admin**; no other role can be given any part of it. Admin permissions cannot be
reduced. Admin tokens do not break quality seals when they edit fact sheets; Member tokens break the
seal of fact sheets they are not subscribed to (useful or harmful depending on the integration).

Other role values you will meet in the MTM API: `CONTACT` (people subscribed to fact sheets but
never invited; no access), `TRANSIENT` (SSO users who may only view Portals), internal `SYSTEM_*`.
Permission statuses: `NOTINVITED`, `INVITED`, `ACTIVE`, `REQUESTED`, `ARCHIVED`, `ANONYMIZED`.
Archived users are deleted automatically 90 days after archival (from July 2026).

### Configurable permissions for Viewer, Member and custom roles

- **Fact sheet permissions**: Administration > **Meta Model Configuration** > fact sheet type >
  **Permissions** tab > choose the role. Per type: Create / Read / Archive fact sheets, Inline
  table editing, Import, Export; per field and per relation: create / read / update / delete;
  global permissions for comments, resources, quality seal, subscriptions (scope All or Self);
  overrides **based on the user's subscription type** (for example only Responsible subscribers may
  edit a field) and **based on fact sheet tags**. "Read fact sheets" overrides field-level
  permissions. Hidden fields and types therefore also disappear from GraphQL for that role.
- **Permissions unrelated to fact sheets**: Administration > **User Roles and Permissions** > role >
  **Permissions** tab: dashboards, portals, collections, surveys, diagram templates, presentations,
  discovery inboxes, architecture decisions, SBOM, transformations and **Developer tools** (access
  to the GraphQL editor and "Copy as JSON Query"; Admin only by default since December 2025).
- **Custom roles** exist only when SSO is configured with roles managed in the identity provider
  (SAML/OIDC claims `role` = `VIEWER|MEMBER|ADMIN`, `customer_roles` = e.g. `AUDITOR`, `ace`).
  Create them under User Roles and Permissions > **New User Role** (uppercase technical name), then
  configure their permissions; a standard role is still required and the custom role takes
  precedence. Technical users can carry custom roles through the Customer Roles field.
- **Subscription types** are fixed: `RESPONSIBLE`, `ACCOUNTABLE` (enable under Administration >
  General), `OBSERVER`; **subscription roles** (Application Owner, IT Owner, ...) are configured under
  Administration > Subscription Roles. They drive permission overrides and the quality seal, not
  API authentication.

### Account-level roles

MTM `User.role` values: `ACCOUNTUSER` (every normal and technical user), `ACCOUNTADMIN` (granted by
SAP LeanIX Support; required for SCIM long-lived tokens and cross-workspace user administration),
internal `SUPERADMIN`, `SYSTEM`, `APICLIENT`, `TOKEN_EXCHANGE_CLIENT`. SAP for Me super/cloud
administrators handle provisioning outside the workspace.

## 6. Fact-sheet-level access: virtual workspaces and ACEs

The standard model works per fact sheet **type**; it cannot hide individual fact sheets. For that,
SAP LeanIX offers **virtual workspaces** (contract feature, requires SSO with roles managed in the
IdP):

- Administration > **Access Control** > **Add Entity**: access control entity id (uppercase, e.g.
  `FINANCE_DEPT`), display name, description. Users receive ACEs through the SAML attribute `ace`;
  technical users through the **Access Control Entities** field.
- Default per type: Administration > Meta Model Configuration > type > Edit > **Access Control**
  (Global unrestricted / Read & write restricted / Write restricted). Per fact sheet: the Access
  Control List section on the fact sheet, the Read access / Write access columns in the inventory
  table, or Excel import.
- Role precedence: Viewer reads within its ACEs; Member reads and edits within its ACEs and new fact
  sheets inherit the member's ACEs; Admin sees and edits everything and manages ACLs.
- API: `permittedReadACL` / `permittedWriteACL` on fact sheets (GraphQL selection and `replace`
  patches with `[{"id": "<aceId>"}]`), `GET /services/pathfinder/v1/models/accessControlEntities`
  to list ACEs, `GET /services/pathfinder/v1/metaModel/permissionRoles?role=MEMBER&factSheetType=Application`
  for the effective permission matrix. Since March 2026 technical users with ACEs can also use the
  MCP server.

## 7. Least privilege per integration type

| Integration need | Minimum role | Notes |
|---|---|---|
| Reporting, exports, dashboards fed from GraphQL / REST reads | **Viewer** | Subject to Viewer read permissions per type and field |
| Sync that creates, updates, relates, tags, subscribes or archives fact sheets | **Member** | Archive, import and export are per-type general permissions; check them for the Member role |
| Running Integration API synchronization runs from a script | Member works when the processor is unrestricted; **Admin** is the documented safe choice; processors can be limited to a default technical user **(minimum role unconfirmed)** | Integration API must be enabled for the workspace (Customer Success Manager) |
| Creating or editing Integration API processors, webhooks, MCP settings, meta model, feature toggles, ACEs | **Admin** | All live in the Administration area |
| Listing users and permissions, inviting users, changing roles, creating technical users (MTM) | **Admin** | "technical user with admin permissions" in the official how-to |
| SCIM long-lived tokens, account-wide user data | **ACCOUNTADMIN** | Support ticket |
| MCP server tools | Any role for read tools; write tools Admin only by default | Configurable per role |

Recommendations: one technical user per integration and environment, named after the system
(`svc-servicenow-sync`), with the lowest role that works; an expiry date; rotation with Replace
token; ACEs when virtual workspaces are in use; never share one Admin token across integrations
(the audit trail then cannot tell them apart).

## 8. Administration: workspace id, developer tools, feature toggles

- **Workspace id**: Administration > **API Tokens** > `WorkspaceId` (and `UserId`); or
  `GET /services/mtm/v1/workspaces`; or the JWT claim. The Integration API's optional
  `lxWorkspace` guard takes the workspace **UUID**.
- **GraphiQL**: help menu (question mark) > **Developer Tools > GraphQL Editor**. Admin only by
  default; grant "Developer tools" to other roles under User Roles and Permissions. The inventory
  filter bar offers **Copy as JSON Query** and **Open in GraphiQL**.
- **OpenAPI explorer**: help menu > Developer Tools > **OpenAPI Documentation**, or
  `https://app.leanix.net/openapi-explorer/?urls.primaryName=Pathfinder` (also `MTM`,
  `Integration%20API`, `Webhooks`, `Import%20Export`, `Metrics`). Raw specs are served without
  authentication, for example `/services/mtm/v1/openapi.json`,
  `/services/pathfinder/v1/api-docs/swagger.json`,
  `/services/integration-api/v1/api-docs/swagger.json`, `/services/webhooks/v1/openapi.json`,
  `/services/metrics/v2/openapi.json` (pattern not documented; the old `/services/*/v1/docs/`
  Swagger pages return 404).
- **Data model**: Administration > Integration API > processor page > three-dot menu > **Get Data
  Model**, or `GET /services/pathfinder/v1/models/dataModel`.
- **Toggles that affect integrations**: Integration API enablement (via Customer Success Manager);
  Administration > **MCP Server** (Enable MCP Server, User-Based Authentication, Technical Users,
  Progressive tool discovery); **Developer tools** permission per role; virtual workspaces /
  Access Control (contract); Maintenance Mode (blocks non-admin UI users; effect on tokens
  undocumented); invitation-only SSO mode.
- **SSO**: SAML 2.0 and OIDC through the self-service SSO configuration (migration of older SSO
  setups was due July 2026). SSO changes never affect the API token flow; technical users are not
  SSO identities, but custom roles and ACEs on technical users require an SSO-managed workspace.

## 9. User administration through the MTM API

Base `https://{SUBDOMAIN}.leanix.net/services/mtm/v1`, Admin token. One permission per user per
workspace; `role` is single-valued, `customerRoles` and `accessControlEntities` multi-valued.

```bash
# Users of a workspace with role and status (page size max 100)
GET /workspaces/{workspaceId}/permissions?status=ACTIVE&includeTechnicalUsers=true&page=1&size=100
# -> {"status":"OK","type":"Permission","total":N,"data":[{"id":"<permissionId>","user":{"id","userName","email","role":"ACCOUNTUSER","technicalUser":false},"workspaceId","role":"MEMBER","status":"ACTIVE","customerRoles":null,"accessControlEntities":null}]}

POST /workspaces/{workspaceId}/permissions/search   # body {"q": "doe", "status": "ACTIVE", "technicalUserOnly": false, "page": 1, "size": 100}
GET  /workspaces/{workspaceId}/permissions/stats     # counts by status x role
GET  /workspaces/{workspaceId}/permissions/export    # Excel download key
GET  /workspaces/{workspaceId}/users                 # lightweight user list without roles
GET  /users?email=jane@example.com                   # find the user id behind an email

# Change a role or archive/reactivate (users cannot be deleted, only archived)
POST /permissions
{"user": {"id": "<userId>"}, "workspace": {"id": "<workspaceId>"}, "role": "ADMIN", "status": "ACTIVE"}

# Invite (silent=true sends no email); field semantics beyond the schema are (unconfirmed)
POST /idm/invite?silent=false
{"host": {"id": "<inviting user id>"}, "user": {"email": "jane@example.com", "firstName": "Jane", "lastName": "Doe"},
 "workspace": {"id": "<workspaceId>"}, "permission": {"role": "MEMBER", "status": "INVITED"}}
```

Audit: `GET /users/{id}/events`, `GET /technicalusers/{id}/changelog`, the PII Change Audit Report
in Administration > Users. SCIM: `/services/mtm/v1/scim/v2/Users` with a long-lived token created by
`POST /services/mtm/v1/longlivedBearerTokens` (ACCOUNTADMIN technical user; one SCIM configuration
per account; not for sandboxes).

## 10. Rate limits, audit trail, network

- **1,800 requests per minute per user** (human or technical user) on the Pathfinder API, covering
  GraphQL, REST and the UI; **1,200 per minute per workspace** for the internal callers Import/Export
  API, Integration API, ServiceNow and Signavio integrations (they reschedule themselves);
  300 per minute per workspace on the Self-Built Software Discovery endpoints. Response: HTTP 429
  with a body such as `USER_INTERVAL_REQUEST_LIMIT_EXCEEDED` and an optional `Retry-After` header.
  Back off exponentially when the header is absent; keep a single technical user under about
  25 requests per second.
- GraphQL has an undisclosed complexity / token limit for large documents.
- Audit sources: fact sheet history (`allLogEvents` in GraphQL, `user { technicalUser }` tells
  integration changes apart), technical user History, MTM events, meta model audit log
  (`GET /services/pathfinder/v1/metaModel/actions/auditLog`), Sync Logging in Administration,
  webhooks for SIEM forwarding. Platform audit logs are obtained from SAP LeanIX Support.
- Network: TLS only; IP allow-listing is configured by SAP LeanIX Support on request; no published
  egress IP list for webhook deliveries.

## 11. Zero-to-first-call checklist

1. Identify the instance: copy `{SUBDOMAIN}` from the workspace URL
   `https://{SUBDOMAIN}.leanix.net/{WORKSPACE_NAME}/`.
2. Decide the role from section 7 (Viewer for reads, Member for data writes, Admin for admin APIs).
3. As an Admin: Administration > Technical Users > New Technical User > username, description, role,
   expiry > Save. Copy the token into the secrets store (environment variables `LEANIX_HOST`,
   `LEANIX_API_TOKEN` in this skill's scripts).
4. Exchange the token (section 2) and decode the JWT to confirm the workspace name and role.
5. Smoke test, read:
   ```bash
   curl -s -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
     https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/graphql \
     -d '{"query":"{ allFactSheets(first: 1) { totalCount edges { node { id name type } } } }"}'
   ```
6. Smoke test, write permission without changing data: run `updateFactSheet` with
   `validateOnly: true` on one fact sheet (Viewer tokens get a permission error).
7. For Integration API work: Administration > Integration API > New Processor Configuration
   (connector type, id, version, direction), save, **Test Run** in the UI, then call the REST
   endpoints with the same `connectorType` / `connectorId` / `connectorVersion`.
8. For webhooks: Administration > Webhooks > New Webhook, or `POST /services/webhooks/v1/subscriptions`.
9. Record the technical user's purpose and expiry; schedule token rotation.

`scripts/leanix_api.py token`, `whoami` and `probe` perform steps 4 to 6.

## 12. Troubleshooting 401 / 403 / 404 / 429

| Symptom | Likely cause | Fix |
|---|---|---|
| `401` from `/oauth2/token` | Wrong token, token replaced or expired technical user, wrong host, JSON body instead of form, username not `apitoken` | Regenerate / replace the token; use the subdomain from the workspace URL; send `grant_type=client_credentials` form-encoded with Basic auth |
| `401` from any service after it worked | JWT older than 3600 s, or JWT from another instance | Re-exchange; call the same host that issued the token |
| `403` on a GraphQL mutation or REST write | Viewer token; Member without create/archive/import permission for that type; ACE restriction on the fact sheet; Admin-only endpoint (Administration area, MTM, webhooks, meta model) | Use a technical user with the needed role; check Meta Model Configuration > type > Permissions for the role; add ACEs |
| GraphQL answers `200` with `errors` | Business or validation error, not auth: bad field path, missing comment on archive, revision clash, rolled-back batch | Read `errors[].message` / `extensions.errorType`; see `graphql-api.md` section 8 |
| Mutation silently skips fields | Field hidden for the role, or field in "Unused fields" | Check role permissions; hidden fields remain writable through the API only if the role may update them |
| `404` on `/services/*/v1/docs/` | Old Swagger UI paths removed | Use the OpenAPI explorer or the raw spec URLs in section 8 |
| `429 USER_INTERVAL_REQUEST_LIMIT_EXCEEDED` | More than 1,800 requests per minute from one user | Honour `Retry-After`, back off, batch with aliases, use the Integration API for bulk work |
| Integration API run never processes | `connectorType` / `connectorId` not configured, another run of the same connector active, Integration API not enabled | Create the processor configuration first; wait for the running sync; ask the CSM to enable the API |
| Token works in the UI's GraphiQL but a script fails | GraphiQL uses the browser session, not a token | Create a technical user; GraphiQL access itself is governed by the Developer tools permission |
| Changes attributed to the wrong user | Shared Admin token | One technical user per integration |
