#!/usr/bin/env python3
"""SAP LeanIX API client and CLI (standard library only).

Covers the token exchange (MTM OAuth2 client credentials), the Pathfinder GraphQL API (fact sheets,
relations, tags, subscriptions, comments, event log, JSON-Patch mutations, cursor pagination), the
Pathfinder REST data model / bookmarks / export endpoints, the Integration API (LDIF synchronization
runs, warnings, processor configurations), the Webhooks API, the Metrics API v2, the Import/Export
API (Excel) and the MTM endpoints for workspaces, users, permissions and technical users.

Environment
  LEANIX_HOST          https://acme.leanix.net   (also accepts "acme.leanix.net" or just the subdomain
                       "acme"; regional instances: eu, us, de, uk, ch, au, ca, br, ae, jp, sg, app)
  LEANIX_API_TOKEN     API token of a technical user (Administration > Technical Users)
  LEANIX_TOKEN         optional: a bearer access token you already hold (skips the exchange)
  LEANIX_WORKSPACE_ID  optional: overrides the workspace id read from the token's JWT claims
  LEANIX_WORKSPACE     optional: expected workspace name; the client aborts if the token belongs
                       to another workspace (guards against running against production by mistake)
  LEANIX_TIMEOUT       seconds per request (default 120)
  LEANIX_CA_BUNDLE     PEM bundle for a private CA / TLS-inspecting proxy

Examples
  python leanix_api.py token                                   # exchange the API token, print expiry
  python leanix_api.py whoami                                  # workspace, role, user from the JWT
  python leanix_api.py probe                                   # read / write / admin permission probe (no changes)
  python leanix_api.py model types                             # fact sheet types in this workspace
  python leanix_api.py model fields Application                # fields of a type with their types/values
  python leanix_api.py model relations Application             # relation definitions touching a type
  python leanix_api.py facets Application                      # facet keys and option keys for filters
  python leanix_api.py list Application --fields "id name ... on Application { lifecycle { asString } }" --csv apps.csv
  python leanix_api.py list ITComponent --filter '{"facetFilters":[{"facetKey":"lifecycle","keys":["endOfLife"],"dateFilter":{"type":"RANGE","from":"2026-01-01","to":"2026-12-31"}}]}'
  python leanix_api.py search "SAP" --type Application
  python leanix_api.py get 28fe4aa2-6e46-41a1-a131-72afb3acf256
  python leanix_api.py query query.graphql --vars '{"first": 10}'
  python leanix_api.py create Application "Payroll Portal" --patches '[{"op":"add","path":"/description","value":"HR portal"}]'
  python leanix_api.py update <id> '[{"op":"replace","path":"/description","value":"new text"}]' --validate-only
  python leanix_api.py relate <appId> relApplicationToITComponent <itcId> --attrs '{"technicalSuitability":"adequate"}'
  python leanix_api.py tag <id> "Cloud" --group "Hosting"          # add a tag by name
  python leanix_api.py archive <id> --comment "Decommissioned 2026-10"
  python leanix_api.py recover <id> --comment "Archived by mistake"
  python leanix_api.py subscribe <id> owner@example.com RESPONSIBLE --role "Application Owner"
  python leanix_api.py events <id> --types FACT_SHEET_TAG_ADDED,FACT_SHEET_TAG_REMOVED
  python leanix_api.py sync ldif.json --test                   # Integration API dry run, waits, prints warnings
  python leanix_api.py sync ldif.json --wait                   # real run
  python leanix_api.py sync-status <runId> ; python leanix_api.py sync-warnings <runId>
  python leanix_api.py processors get --type cmdb-sync --id prod-cmdb
  python leanix_api.py processors put config.json
  python leanix_api.py webhooks list
  python leanix_api.py webhooks create-push my-hook https://hooks.example.com/lx --events FACT_SHEET_UPDATED,FACT_SHEET_ARCHIVED
  python leanix_api.py users                                   # workspace users with role and status (MTM, Admin)
  python leanix_api.py techusers list ; python leanix_api.py techusers create svc-cmdb MEMBER 2027-12-31 --description "CMDB sync"
  python leanix_api.py metrics schemas ; python leanix_api.py metrics point <schemaUuid> '{"timestamp":"2026-10-26T00:00:00Z","availability":99.9,"factSheetId":"<id>"}'
  python leanix_api.py bookmarks ; python leanix_api.py export-bookmark <bookmarkId> --format XLSX --download inventory.xlsx
  python leanix_api.py export --type SNAPSHOT --download snapshot.xlsx
  python leanix_api.py raw GET /services/pathfinder/v1/models/dataModel
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import mimetypes
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Iterator

JSON = "application/json"
TOKEN_PATH = "/services/mtm/v1/oauth2/token"
GRAPHQL_PATH = "/services/pathfinder/v1/graphql"
PATHFINDER = "/services/pathfinder/v1"
INTEGRATION = "/services/integration-api/v1"
WEBHOOKS = "/services/webhooks/v1"
METRICS = "/services/metrics/v2"
IMPORT_EXPORT = "/services/import-export/v1"
MTM = "/services/mtm/v1"
DEFAULT_PAGE = 500          # allFactSheets page size used by the iterators
RETRY_STATUSES = {429, 500, 502, 503, 504}
TERMINAL_RUN_STATES = {"FINISHED", "FAILED", "ABORTED", "CANCELLED", "CANCELED", "STOPPED"}


class LeanIXError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status = status
        self.payload = payload


class GraphQLError(LeanIXError):
    """Raised when the GraphQL response carries an `errors` array (the HTTP status is 200)."""

    @property
    def errors(self) -> list[dict]:
        return (self.payload or {}).get("errors") or [] if isinstance(self.payload, dict) else []

    @property
    def error_types(self) -> set[str]:
        return {str((e.get("extensions") or {}).get("errorType")) for e in self.errors}


# --------------------------------------------------------------------------- patch helpers
def patch(op: str, path: str, value: Any = None) -> dict:
    """Build one JSON-Patch entry for createFactSheet / updateFactSheet.

    The GraphQL `Patch` input takes `value` as a *string*: scalars are passed as text (numbers too),
    structured values (lifecycle, tags, relations, externalId, multi-select, ACLs) are JSON-encoded.
    `remove` patches still carry an empty value, as the official examples do."""
    p: dict[str, Any] = {"op": op, "path": path}
    if op == "remove" and value is None:
        p["value"] = ""
        return p
    if isinstance(value, (dict, list)):
        value = json.dumps(value)
    elif isinstance(value, bool):
        value = "true" if value else "false"
    elif value is not None and not isinstance(value, str):
        value = str(value)
    p["value"] = value
    return p


def lifecycle_patch(phases: dict[str, str]) -> dict:
    """phases: {"plan": "2025-01-01", "active": "2025-06-01", "endOfLife": "2030-12-31"} (ISO dates).
    The patch replaces ALL phases: read the current ones and merge before calling this."""
    return patch("replace", "/lifecycle", {"phases": [{"phase": k, "startDate": v} for k, v in phases.items() if v]})


def tags_patch(tag_ids: list[str], op: str = "add") -> dict:
    """op=add appends, op=remove detaches, op=replace sets the whole list. Tags are referenced by id;
    `[{"tagName": ...}]` would create ungrouped tags on the fly (use tag_names_patch)."""
    return patch(op, "/tags", [{"tagId": t} for t in tag_ids])


def tag_names_patch(tag_names: list[str]) -> dict:
    """Creates (if needed) and attaches ungrouped tags by name ("Other tags" group)."""
    return patch("add", "/tags", [{"tagName": n} for n in tag_names])


def external_id_patch(external_id: str, *, field: str = "externalId", external_url: str | None = None,
                      comment: str | None = None, status: str | None = None, force_write: bool = False) -> dict:
    """External id fields take a JSON object with "type": "ExternalId"; custom external-id fields use
    their own key as `field`. force_write=True overwrites an already linked id (SAP sample scripts)."""
    value: dict[str, Any] = {"type": "ExternalId", "externalId": external_id}
    if external_url:
        value["externalUrl"] = external_url
    if comment:
        value["comment"] = comment
    if status:
        value["status"] = status
    if force_write:
        value["forceWrite"] = True
    return patch("replace", f"/{field}", value)


def relation_patch(relation: str, target_id: str, attributes: dict | None = None, *, key: str | None = None) -> dict:
    """Adds a relation, e.g. relation_patch("relApplicationToITComponent", "<itc-id>",
    {"technicalSuitability": "adequate", "activeFrom": "2025-01-01"}). Each new relation in one
    mutation needs its own `new_<suffix>` path; a random suffix is generated by default."""
    value = {"factSheetId": target_id}
    if attributes:
        value.update(attributes)
    return patch("add", f"/{relation}/{key or 'new_' + uuid.uuid4().hex[:8]}", value)


def relation_update_patch(relation: str, relation_id: str, target_id: str, attributes: dict) -> dict:
    """Updates attributes of an existing relation; relation_id is the relation node id, and the
    target factSheetId must be repeated in the value."""
    value = {"factSheetId": target_id}
    value.update(attributes)
    return patch("replace", f"/{relation}/{relation_id}", value)


def relation_remove_patch(relation: str, relation_id: str) -> dict:
    return patch("remove", f"/{relation}/{relation_id}")


# --------------------------------------------------------------------------- client
class LeanIX:
    """Thin client: token exchange + caching, JSON transport with retries, GraphQL and REST helpers."""

    TOKEN_MARGIN = 120  # exchange a new token this many seconds before the current one expires

    def __init__(self, host: str, *, api_token: str | None = None, token: str | None = None,
                 workspace_id: str | None = None, expected_workspace: str | None = None,
                 ca_bundle: str | None = None, timeout: int = 120):
        host = host.strip().rstrip("/")
        if "://" not in host:
            host = f"https://{host}" if "." in host else f"https://{host}.leanix.net"
        self.base_url = host
        self.api_token = api_token
        self._token = token
        self._token_expiry = float("inf") if token else 0.0
        self._workspace_id = workspace_id
        self.expected_workspace = expected_workspace
        self.timeout = timeout
        # TLS is always verified; pass ca_bundle (LEANIX_CA_BUNDLE) when a private CA fronts the host.
        self._ctx = ssl.create_default_context(cafile=ca_bundle) if ca_bundle else ssl.create_default_context()
        self._data_model: dict | None = None

    @classmethod
    def from_env(cls, **overrides) -> "LeanIX":
        env = os.environ.get
        host = overrides.pop("host", None) or env("LEANIX_HOST") or env("LEANIX_SUBDOMAIN")
        if not host:
            raise LeanIXError("Set LEANIX_HOST (e.g. https://acme.leanix.net, or the subdomain such as us or acme)")
        kw = dict(api_token=env("LEANIX_API_TOKEN"), token=env("LEANIX_TOKEN"),
                  workspace_id=env("LEANIX_WORKSPACE_ID"), expected_workspace=env("LEANIX_WORKSPACE"),
                  ca_bundle=env("LEANIX_CA_BUNDLE"), timeout=int(env("LEANIX_TIMEOUT", "120")))
        kw.update({k: v for k, v in overrides.items() if v is not None})
        if not (kw.get("api_token") or kw.get("token")):
            raise LeanIXError("Set LEANIX_API_TOKEN (technical user API token) or LEANIX_TOKEN (bearer)")
        return cls(host, **kw)

    # ------------------------------------------------------------------ auth
    def ensure_token(self) -> str:
        if self._token and time.time() < self._token_expiry - self.TOKEN_MARGIN:
            return self._token
        if not self.api_token:
            if self._token:
                return self._token  # pre-issued bearer with unknown expiry; let the server reject it
            raise LeanIXError("No API token available to exchange (LEANIX_API_TOKEN)")
        return self.exchange_token()

    def exchange_token(self) -> str:
        """POST /services/mtm/v1/oauth2/token with HTTP Basic `apitoken:<API token>` and the form body
        grant_type=client_credentials. Returns a bearer JWT valid for `expires_in` seconds (3600)."""
        basic = base64.b64encode(f"apitoken:{self.api_token}".encode("utf-8")).decode("ascii")
        body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("ascii")
        req = urllib.request.Request(self.base_url + TOKEN_PATH, data=body, method="POST", headers={
            "Authorization": "Basic " + basic,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": JSON,
        })
        status, payload, _ = self._send(req)
        if status != 200 or not isinstance(payload, dict) or "access_token" not in payload:
            hint = " (check the host, the token, and that the technical user is not expired or replaced)" if status == 401 else ""
            raise LeanIXError(f"token exchange failed (HTTP {status}){hint}: {_short(payload)}", status, payload)
        self._token = payload["access_token"]
        self._token_expiry = time.time() + int(payload.get("expires_in", 3600))
        if self.expected_workspace:
            name = (self.token_info().get("principal") or {}).get("permission", {}).get("workspaceName")
            if name and name != self.expected_workspace:
                raise LeanIXError(f"token belongs to workspace {name!r}, expected {self.expected_workspace!r} (LEANIX_WORKSPACE)")
        return self._token

    def token_info(self) -> dict:
        """Decoded JWT claims of the current access token (no signature check; informational).
        SAP's sample scripts read principal.permission.workspaceId / workspaceName from here."""
        token = self.ensure_token()
        try:
            payload_b64 = token.split(".")[1]
            payload_b64 += "=" * (-len(payload_b64) % 4)
            return json.loads(base64.urlsafe_b64decode(payload_b64))
        except Exception as e:  # pragma: no cover - defensive
            raise LeanIXError(f"cannot decode access token: {e}")

    @property
    def workspace_id(self) -> str:
        if not self._workspace_id:
            claims = self.token_info()
            perm = (claims.get("principal") or {}).get("permission") or {}
            self._workspace_id = perm.get("workspaceId")
            if not self._workspace_id:
                raise LeanIXError("workspace id not found in token claims; set LEANIX_WORKSPACE_ID "
                                  "(Administration > API Tokens shows WorkspaceId)")
        return self._workspace_id

    def whoami(self) -> dict:
        claims = self.token_info()
        principal = claims.get("principal") or {}
        perm = principal.get("permission") or {}
        return {
            "host": self.base_url,
            "user": principal.get("username"),
            "userId": principal.get("id"),
            "accountRole": principal.get("role"),
            "workspaceId": perm.get("workspaceId"),
            "workspaceName": perm.get("workspaceName"),
            "workspaceRole": perm.get("role"),
            "permissionStatus": perm.get("status"),
            "customerRoles": perm.get("customerRoles"),
            "accessControlEntities": perm.get("accessControlEntities"),
            "tokenExpires": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(claims.get("exp", 0))),
            "issuer": claims.get("iss"),
        }

    # ------------------------------------------------------------------ transport
    def _send(self, req: urllib.request.Request) -> tuple[int, Any, dict]:
        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=self._ctx) as resp:
                raw = resp.read()
                return resp.status, _decode(raw, resp.headers.get("Content-Type", "")), dict(resp.headers)
        except urllib.error.HTTPError as e:
            raw = e.read()
            return e.code, _decode(raw, e.headers.get("Content-Type", "") if e.headers else ""), dict(e.headers or {})
        except urllib.error.URLError as e:
            raise LeanIXError(f"connection error to {req.full_url}: {e.reason}")

    def request_full(self, method: str, path: str, body: Any = None, *, query: dict | None = None,
                     headers: dict | None = None, raw_body: bytes | None = None,
                     content_type: str = JSON, retries: int = 4) -> tuple[int, Any, dict]:
        """Authenticated request. Retries 429/5xx with backoff (honours Retry-After), re-exchanges the
        token once on 401. Returns (status, decoded payload, headers); raises LeanIXError on 4xx/5xx."""
        url = path if path.startswith("http") else self.base_url + path
        if query:
            clean = {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in query.items() if v is not None}
            if clean:
                url += ("&" if "?" in url else "?") + urllib.parse.urlencode(clean, doseq=True)
        data = raw_body if raw_body is not None else (json.dumps(body).encode("utf-8") if body is not None else None)
        refreshed = False
        attempt = 0
        while True:
            hdrs = {"Authorization": "Bearer " + self.ensure_token(), "Accept": JSON}
            if data is not None:
                hdrs["Content-Type"] = content_type
            if headers:
                hdrs.update(headers)
            req = urllib.request.Request(url, data=data, method=method.upper(), headers=hdrs)
            status, payload, resp_headers = self._send(req)
            if status == 401 and not refreshed and self.api_token:
                refreshed = True
                self._token_expiry = 0.0  # force a new exchange
                continue
            if status in RETRY_STATUSES and attempt < retries:
                attempt += 1
                wait = float(resp_headers.get("Retry-After") or resp_headers.get("retry-after") or 0) or min(2 ** attempt, 30)
                print(f"HTTP {status} on {method} {path}; retry {attempt}/{retries} in {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if status >= 400:
                hint = ""
                if status == 403:
                    hint = " (role lacks permission: Viewer tokens are read-only, Administration-area APIs need Admin)"
                elif status == 401:
                    hint = " (token expired or issued by another instance)"
                raise LeanIXError(f"HTTP {status} {method} {path}{hint}: {_short(payload)}", status, payload)
            return status, payload, resp_headers

    def request(self, method: str, path: str, body: Any = None, **kw) -> Any:
        return self.request_full(method, path, body, **kw)[1]

    def _data(self, payload: Any) -> Any:
        """Unwraps the {"status": "OK", "data": ...} envelope used by Pathfinder REST and MTM."""
        return payload.get("data", payload) if isinstance(payload, dict) else payload

    # ------------------------------------------------------------------ GraphQL
    def graphql(self, query: str, variables: dict | None = None, *, raise_on_errors: bool = True,
                warnings: bool = False) -> Any:
        """POST /services/pathfinder/v1/graphql. Returns `data`; raises GraphQLError when `errors`
        is present (LeanIX answers HTTP 200 for GraphQL-level failures)."""
        headers = {"x-graphql-enable-extensions": "true"} if warnings else None
        status, payload, _ = self.request_full("POST", GRAPHQL_PATH, {"query": query, "variables": variables or {}},
                                               headers=headers)
        if isinstance(payload, dict) and payload.get("errors"):
            if raise_on_errors:
                msgs = "; ".join(str(e.get("message")) for e in payload["errors"])
                raise GraphQLError(f"GraphQL errors: {msgs}", status, payload)
            return payload
        if warnings and isinstance(payload, dict) and (payload.get("extensions") or {}).get("warnings"):
            print("GraphQL warnings: " + json.dumps(payload["extensions"]["warnings"]), file=sys.stderr)
        return payload.get("data") if isinstance(payload, dict) else payload

    def iter_fact_sheets(self, fact_sheet_type: str | None = None, *, filter: dict | None = None,
                         fields: str = "id name type", page_size: int = DEFAULT_PAGE,
                         sort: list[dict] | None = None, max_items: int | None = None) -> Iterator[dict]:
        """Cursor-paginates allFactSheets (forward-only relay cursors), de-duplicating on id because
        pages reflect live data. `fields` is the selection inside `node { ... }`; type-specific fields
        need an inline fragment, e.g. 'id name ... on Application { lifecycle { asString } }'."""
        flt: dict[str, Any] = dict(filter or {})
        if fact_sheet_type:
            facets = list(flt.get("facetFilters") or [])
            if not any(f.get("facetKey") == "FactSheetTypes" for f in facets):
                facets.append({"facetKey": "FactSheetTypes", "keys": [fact_sheet_type]})
            flt["facetFilters"] = facets
        q = """
        query ($filter: FilterInput, $first: Int, $after: String, $sort: [Sorting]) {
          allFactSheets(filter: $filter, first: $first, after: $after, sort: $sort) {
            totalCount
            pageInfo { hasNextPage endCursor }
            edges { node { %s } }
          }
        }""" % fields
        after = None
        seen: set[str] = set()
        count = 0
        while True:
            data = self.graphql(q, {"filter": flt or None, "first": page_size, "after": after,
                                    "sort": sort or [{"key": "displayName", "order": "asc"}]})
            page = data["allFactSheets"]
            for edge in page["edges"]:
                node = edge["node"]
                nid = node.get("id")
                if nid is not None:
                    if nid in seen:
                        continue
                    seen.add(nid)
                yield node
                count += 1
                if max_items and count >= max_items:
                    return
            if not page["pageInfo"]["hasNextPage"]:
                return
            after = page["pageInfo"]["endCursor"]

    def count_fact_sheets(self, fact_sheet_type: str | None = None, filter: dict | None = None) -> int:
        flt: dict[str, Any] = dict(filter or {})
        if fact_sheet_type:
            flt.setdefault("facetFilters", []).append({"facetKey": "FactSheetTypes", "keys": [fact_sheet_type]})
        data = self.graphql("query ($filter: FilterInput) { allFactSheets(filter: $filter, first: 0) { totalCount } }",
                            {"filter": flt or None})
        return data["allFactSheets"]["totalCount"]

    def facets(self, fact_sheet_type: str) -> list[dict]:
        """Facet keys, operators and option keys available for filtering a type. The type is inlined
        as an enum literal (as in SAP's examples) so no schema type name has to be guessed."""
        q = """{ allFactSheets(factSheetType: %s, first: 0) { filterOptions { facets {
                 facetKey possibleOperators operator results { name key } dateFilter { type minDate maxDate }
                 relationFieldsFilter { fieldName values { key } } } } } }""" % _enum(fact_sheet_type)
        return self.graphql(q)["allFactSheets"]["filterOptions"]["facets"]

    def fact_sheet(self, fact_sheet_id: str, fields: str = "id name type description status rev tags { id name }") -> dict:
        data = self.graphql("query ($id: ID!) { factSheet(id: $id) { %s } }" % fields, {"id": fact_sheet_id})
        return data["factSheet"]

    def search(self, text: str, fact_sheet_type: str | None = None, *, fields: str = "id name type displayName",
               limit: int = 50) -> list[dict]:
        return list(self.iter_fact_sheets(fact_sheet_type, filter={"fullTextSearch": text}, fields=fields,
                                          page_size=min(limit, DEFAULT_PAGE), max_items=limit))

    def find_by_name(self, fact_sheet_type: str, name: str) -> dict | None:
        """Exact (case-insensitive) name match within a type, using full-text search as the candidate set."""
        for fs in self.search(name, fact_sheet_type, fields="id name type rev", limit=200):
            if fs["name"].strip().lower() == name.strip().lower():
                return fs
        return None

    def find_by_external_id(self, external_id: str, *, field: str = "externalId",
                            fields: str = "id name type rev") -> list[dict]:
        """filter.externalIds takes '<externalIdFieldKey>/<value>'."""
        return list(self.iter_fact_sheets(filter={"externalIds": [f"{field}/{external_id}"]}, fields=fields))

    def create_fact_sheet(self, name: str, fact_sheet_type: str, *, patches: list[dict] | None = None,
                          validate_only: bool = False, fields: str = "id name type rev") -> dict:
        q = """
        mutation ($input: BaseFactSheetInput!, $patches: [Patch], $validateOnly: Boolean) {
          createFactSheet(input: $input, patches: $patches, validateOnly: $validateOnly) {
            factSheet { %s }
          }
        }""" % fields
        data = self.graphql(q, {"input": {"name": name, "type": fact_sheet_type}, "patches": patches or [],
                                "validateOnly": validate_only})
        return data["createFactSheet"]["factSheet"]

    def update_fact_sheet(self, fact_sheet_id: str, patches: list[dict], *, rev: int | None = None,
                          validate_only: bool = False, comment: str | None = None,
                          fields: str = "id name type rev", retries_on_rev_clash: int = 3) -> dict:
        """updateFactSheet with JSON-Patch entries. Pass `rev` (from a prior read) for optimistic
        locking; on a revision clash the current rev is re-read and the update retried."""
        attempt = 0
        while True:
            # rev is inlined as an integer literal (as SAP's sample scripts do) so the client does not
            # depend on the name of the revision scalar in the schema.
            rev_arg = f", rev: {int(rev)}" if rev is not None else ""
            q = """
            mutation ($id: ID!, $patches: [Patch]!, $validateOnly: Boolean, $comment: String) {
              updateFactSheet(id: $id%s, patches: $patches, validateOnly: $validateOnly, comment: $comment) {
                factSheet { %s }
              }
            }""" % (rev_arg, fields)
            try:
                data = self.graphql(q, {"id": fact_sheet_id, "patches": patches,
                                        "validateOnly": validate_only, "comment": comment})
                return data["updateFactSheet"]["factSheet"]
            except GraphQLError as e:
                clash = "REVISION_CLASH" in e.error_types or "revision" in str(e).lower()
                if rev is None or not clash or attempt >= retries_on_rev_clash:
                    raise
                attempt += 1
                rev = self.fact_sheet(fact_sheet_id, "id rev")["rev"]

    def archive_fact_sheet(self, fact_sheet_id: str, comment: str, *, validate_only: bool = False) -> dict:
        """Archives (soft-deletes) a fact sheet; a comment is required. Recoverable for 90 days."""
        return self.update_fact_sheet(fact_sheet_id, [patch("add", "/status", "ARCHIVED")],
                                      comment=comment, validate_only=validate_only, fields="id name status rev")

    def recover_fact_sheet(self, fact_sheet_id: str, comment: str, *, validate_only: bool = False) -> dict:
        return self.update_fact_sheet(fact_sheet_id, [patch("add", "/status", "ACTIVE")],
                                      comment=comment, validate_only=validate_only, fields="id name status rev")

    def add_relation(self, from_id: str, relation: str, to_id: str, attributes: dict | None = None,
                     *, validate_only: bool = False) -> dict:
        return self.update_fact_sheet(from_id, [relation_patch(relation, to_id, attributes)],
                                      validate_only=validate_only, fields="id name rev")

    def relations(self, fact_sheet_id: str, relation: str, fact_sheet_type: str,
                  fields: str = "id activeFrom activeUntil description factSheet { id name type }") -> list[dict]:
        q = "query ($id: ID!) { factSheet(id: $id) { id ... on %s { %s { edges { node { %s } } } } } }" % (
            fact_sheet_type, relation, fields)
        data = self.graphql(q, {"id": fact_sheet_id})
        return [e["node"] for e in data["factSheet"][relation]["edges"]]

    def events(self, fact_sheet_id: str, event_types: list[str] | None = None) -> list[dict]:
        """Fact sheet history via allLogEvents (eventTypes is an enum list, e.g. FACT_SHEET_TAG_ADDED)."""
        arg = ", eventTypes: [%s]" % ", ".join(event_types) if event_types else ""
        q = """query ($id: ID!) { allLogEvents(factSheetId: $id%s) { edges { node {
                 id eventType path oldValue newValue message createdAt user { id email displayName technicalUser } } } } }""" % arg
        return [e["node"] for e in self.graphql(q, {"id": fact_sheet_id})["allLogEvents"]["edges"]]

    # ------------------------------------------------------------------ tags, subscriptions, comments
    def tag_groups(self) -> list[dict]:
        q = """{ allTagGroups { edges { node { id name shortName mode restrictToFactSheetTypes
                 tags { edges { node { id name description color status } } } } } } }"""
        groups = []
        for e in self.graphql(q)["allTagGroups"]["edges"]:
            g = e["node"]
            g["tags"] = [t["node"] for t in g["tags"]["edges"]]
            groups.append(g)
        return groups

    def tags(self) -> list[dict]:
        q = "{ allTags { edges { node { id name description color status tagGroup { id name mode } } } } }"
        return [e["node"] for e in self.graphql(q)["allTags"]["edges"]]

    def tag_id(self, name: str, group: str | None = None) -> str:
        matches = [t for t in self.tags() if t["name"].lower() == name.lower()
                   and (group is None or ((t.get("tagGroup") or {}).get("name") or "").lower() == group.lower())]
        if not matches:
            raise LeanIXError(f"tag {name!r}" + (f" in group {group!r}" if group else "") + " not found; run `tags`")
        if len(matches) > 1:
            groups = ", ".join((m.get("tagGroup") or {}).get("name") or "Other tags" for m in matches)
            raise LeanIXError(f"tag {name!r} exists in several groups ({groups}); pass --group")
        return matches[0]["id"]

    def add_tags(self, fact_sheet_id: str, tag_ids: list[str], *, validate_only: bool = False) -> dict:
        return self.update_fact_sheet(fact_sheet_id, [tags_patch(tag_ids, "add")], validate_only=validate_only,
                                      fields="id name rev tags { id name }")

    def remove_tags(self, fact_sheet_id: str, tag_ids: list[str], *, validate_only: bool = False) -> dict:
        return self.update_fact_sheet(fact_sheet_id, [tags_patch(tag_ids, "remove")], validate_only=validate_only,
                                      fields="id name rev tags { id name }")

    def subscription_roles(self, fact_sheet_type: str | None = None) -> list[dict]:
        flt = "(filter: {factSheetType: %s})" % _enum(fact_sheet_type) if fact_sheet_type else ""
        q = "{ allSubscriptionRoles%s { edges { node { id name subscriptionType } } } }" % flt
        return [e["node"] for e in self.graphql(q)["allSubscriptionRoles"]["edges"]]

    def create_subscription(self, fact_sheet_id: str, email: str, sub_type: str = "RESPONSIBLE",
                            role_ids: list[str] | None = None) -> dict:
        """createSubscription as in the official examples; values are inlined (JSON-escaped strings,
        validated enum) so no input type names have to be guessed."""
        sub_type = _enum(sub_type.upper())
        if sub_type not in ("RESPONSIBLE", "ACCOUNTABLE", "OBSERVER"):
            raise LeanIXError(f"subscription type must be RESPONSIBLE, ACCOUNTABLE or OBSERVER, not {sub_type!r}")
        roles = ", roleIds: [%s]" % ", ".join(json.dumps(r) for r in role_ids) if role_ids else ""
        q = """mutation { createSubscription(factSheetId: %s, user: {email: %s}, type: %s%s) {
                 id type user { id email } roles { id name } } }""" % (json.dumps(fact_sheet_id), json.dumps(email), sub_type, roles)
        return self.graphql(q)["createSubscription"]

    def delete_subscription(self, subscription_id: str) -> Any:
        return self.graphql("mutation ($id: ID!) { deleteSubscription(id: $id) { id } }", {"id": subscription_id})

    def create_comment(self, fact_sheet_id: str, message: str) -> dict:
        q = "mutation ($fs: ID!, $m: String!) { createComment(factSheetId: $fs, message: $m, status: ACTIVE) { id message } }"
        return self.graphql(q, {"fs": fact_sheet_id, "m": message})["createComment"]

    def create_document(self, fact_sheet_id: str, name: str, url: str, description: str | None = None) -> dict:
        q = """mutation ($fs: ID!, $name: String!, $url: String, $desc: String) {
                 createDocument(factSheetId: $fs, name: $name, url: $url, description: $desc) { id name url } }"""
        return self.graphql(q, {"fs": fact_sheet_id, "name": name, "url": url, "desc": description})["createDocument"]

    # ------------------------------------------------------------------ data model (Pathfinder REST)
    def data_model(self, refresh: bool = False) -> dict:
        """GET /services/pathfinder/v1/models/dataModel: fact sheet types, fields, relations, validators."""
        if self._data_model is None or refresh:
            self._data_model = self._data(self.request("GET", f"{PATHFINDER}/models/dataModel"))
        return self._data_model

    def fact_sheet_types(self) -> list[str]:
        return sorted((self.data_model().get("factSheets") or {}).keys())

    def fields_of(self, fact_sheet_type: str) -> dict:
        fs = (self.data_model().get("factSheets") or {}).get(fact_sheet_type)
        if fs is None:
            raise LeanIXError(f"unknown fact sheet type {fact_sheet_type!r}; known: {', '.join(self.fact_sheet_types())}")
        return fs.get("fields") or {}

    def relations_of(self, fact_sheet_type: str) -> dict:
        rels = self.data_model().get("relations") or {}
        out = {}
        for name, rel in rels.items():
            frm, to = rel.get("from") or {}, rel.get("to") or {}
            if frm.get("factSheetType") == fact_sheet_type or to.get("factSheetType") == fact_sheet_type:
                out[name] = rel
        return out

    def translations(self, lang: str = "en") -> dict:
        """GET /models/languages/{lang}: labels for fact sheet types, fields and option keys."""
        return self._data(self.request("GET", f"{PATHFINDER}/models/languages/{lang}"))

    # ------------------------------------------------------------------ bookmarks and exports
    def bookmarks(self, bookmark_type: str = "INVENTORY") -> list[dict]:
        """Saved searches (INVENTORY), reports (REPORTING), diagrams (VISUALIZER), dashboards (DASHBOARD)."""
        return self._data(self.request("GET", f"{PATHFINDER}/bookmarks", query={"bookmarkType": bookmark_type}))

    def start_full_export(self, export_type: str = "SNAPSHOT", start_date: str | None = None,
                          end_date: str | None = None) -> dict:
        """POST /exports/fullExport?exportType=SNAPSHOT|AUDIT_LOG|AUDIT_LOG_LEGACY (asynchronous job)."""
        return self._data(self.request("POST", f"{PATHFINDER}/exports/fullExport",
                                       query={"exportType": export_type, "startDate": start_date, "endDate": end_date}))

    def exports(self, export_type: str | None = None, page_size: int = 100) -> list[dict]:
        return self._data(self.request("GET", f"{PATHFINDER}/exports", query={"exportType": export_type, "pageSize": page_size}))

    def download_export(self, download_key: str, dest: str) -> str:
        """GET /exports/downloads/{workspaceId}?key=<downloadKey> (one-time key from the export job)."""
        status, payload, _ = self.request_full("GET", f"{PATHFINDER}/exports/downloads/{self.workspace_id}",
                                               query={"key": download_key}, headers={"Accept": "*/*"})
        _write_binary(payload, dest)
        return dest

    def export_bookmark(self, bookmark_id: str, formats: list[str] | None = None, language: str = "en") -> dict:
        """Import/Export API: POST /exports for a saved search; formats XLSX and/or LDIF."""
        body = {"sourceType": "BOOKMARK", "sourceIdentifier": {"id": bookmark_id}, "formats": formats or ["XLSX"],
                "languageId": language}
        return self.request("POST", f"{IMPORT_EXPORT}/exports", body)

    def export_job(self, export_id: str) -> dict:
        return self.request("GET", f"{IMPORT_EXPORT}/exports/{export_id}")

    def download_export_artifact(self, export_id: str, fmt: str, dest: str) -> str:
        status, payload, _ = self.request_full("GET", f"{IMPORT_EXPORT}/exports/{export_id}/{fmt}", headers={"Accept": "*/*"})
        _write_binary(payload, dest)
        return dest

    def upload_excel_import(self, path: str) -> Any:
        """POST /services/import-export/v1/imports (multipart): validates the .xlsx and returns the import job."""
        boundary = "----leanix" + uuid.uuid4().hex
        with open(path, "rb") as fh:
            content = fh.read()
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        parts = [f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(path)}\"\r\n"
                 f"Content-Type: {ctype}\r\n\r\n".encode(), content, f"\r\n--{boundary}--\r\n".encode()]
        return self.request("POST", f"{IMPORT_EXPORT}/imports", raw_body=b"".join(parts),
                            content_type=f"multipart/form-data; boundary={boundary}")

    def execute_import(self, import_id: str) -> Any:
        return self.request("POST", f"{IMPORT_EXPORT}/imports/{import_id}")

    def import_status(self, import_id: str) -> Any:
        return self.request("GET", f"{IMPORT_EXPORT}/imports/{import_id}")

    # ------------------------------------------------------------------ Integration API
    def start_sync_run(self, ldif: dict, *, test: bool = False, start: bool = True) -> dict:
        """POST /synchronizationRuns?start=<bool>&test=<bool> with an LDIF body. Returns {id, ...}.
        test=True is a dry run (requires start=True)."""
        payload = self.request("POST", f"{INTEGRATION}/synchronizationRuns", ldif, query={"start": start, "test": test})
        if isinstance(payload, list):
            payload = payload[0] if payload else {}
        return payload

    def start_existing_run(self, run_id: str, *, test: bool = False) -> Any:
        return self.request("POST", f"{INTEGRATION}/synchronizationRuns/{run_id}/start", query={"test": test})

    def sync_status(self, run_id: str) -> dict:
        return self.request("GET", f"{INTEGRATION}/synchronizationRuns/{run_id}/status")

    def sync_progress(self, run_id: str) -> Any:
        return self.request("GET", f"{INTEGRATION}/synchronizationRuns/{run_id}/progress")

    def sync_results(self, run_id: str) -> Any:
        """Output LDIF of outbound / writeToLdif runs; None when the run produced none (HTTP 204)."""
        status, payload, _ = self.request_full("GET", f"{INTEGRATION}/synchronizationRuns/{run_id}/results")
        return None if status == 204 else payload

    def sync_warnings(self, run_id: str, *, limit: int = 100, max_pages: int = 50) -> list[dict]:
        """All warnings/errors of a run (offset must be a multiple of limit)."""
        out: list[dict] = []
        for page in range(max_pages):
            chunk = self.request("GET", f"{INTEGRATION}/synchronizationRuns/{run_id}/warnings",
                                 query={"offset": page * limit, "limit": limit}) or []
            out.extend(chunk)
            if len(chunk) < limit:
                break
        return out

    def stop_sync_run(self, run_id: str) -> Any:
        return self.request("POST", f"{INTEGRATION}/synchronizationRuns/{run_id}/stop")

    def wait_for_sync(self, run_id: str, *, poll: float = 5.0, timeout: float = 1800.0) -> dict:
        deadline = time.time() + timeout
        last: dict = {}
        while time.time() < deadline:
            last = self.sync_status(run_id)
            if str(last.get("status", "")).upper() in TERMINAL_RUN_STATES:
                return last
            time.sleep(poll)
        raise LeanIXError(f"synchronization run {run_id} still {last.get('status')} after {timeout:.0f}s", payload=last)

    def run_ldif(self, ldif: dict, *, test: bool = False, poll: float = 5.0, timeout: float = 1800.0) -> dict:
        """Start a run (dry run when test=True), wait, collect status, warnings and results."""
        run = self.start_sync_run(ldif, test=test)
        run_id = run.get("id")
        if not run_id:
            raise LeanIXError(f"no run id in response: {_short(run)}", payload=run)
        status = self.wait_for_sync(run_id, poll=poll, timeout=timeout)
        warnings = self.sync_warnings(run_id)
        results = None
        try:
            results = self.sync_results(run_id)
        except LeanIXError as e:
            results = {"error": str(e)}
        summary = {"errors": sum(1 for w in warnings if str(w.get("status", "")).upper() == "ERROR"),
                   "warnings": sum(1 for w in warnings if str(w.get("status", "")).upper() != "ERROR")}
        return {"runId": run_id, "test": test, "status": status, "summary": summary, "warnings": warnings, "results": results}

    def processor_configs(self, connector_type: str | None = None, connector_id: str | None = None,
                          connector_version: str | None = None, processing_direction: str | None = None,
                          processing_mode: str | None = None) -> Any:
        return self.request("GET", f"{INTEGRATION}/configurations", query={
            "connectorType": connector_type, "connectorId": connector_id, "connectorVersion": connector_version,
            "processingDirection": processing_direction, "processingMode": processing_mode})

    def put_processor_config(self, config: dict) -> Any:
        """PUT /configurations: creates or replaces the configuration identified by connectorType,
        connectorId, connectorVersion, processingDirection and processingMode (all in the body)."""
        for k in ("connectorType", "connectorId", "connectorVersion", "processingDirection"):
            if k not in config:
                raise LeanIXError(f"processor configuration needs {k!r}")
        status, payload, _ = self.request_full("PUT", f"{INTEGRATION}/configurations", config)
        return payload if payload is not None else {"status": status}

    def delete_processor_config(self, connector_type: str, connector_id: str, connector_version: str,
                                processing_direction: str = "inbound", processing_mode: str = "partial") -> Any:
        return self.request("DELETE", f"{INTEGRATION}/configurations", query={
            "connectorType": connector_type, "connectorId": connector_id, "connectorVersion": connector_version,
            "processingDirection": processing_direction, "processingMode": processing_mode})

    # ------------------------------------------------------------------ Webhooks
    def webhooks(self) -> Any:
        return self._data(self.request("GET", f"{WEBHOOKS}/subscriptions"))

    def webhook_statuses(self) -> Any:
        return self._data(self.request("GET", f"{WEBHOOKS}/subscriptions/status"))

    def event_tags(self) -> Any:
        return self._data(self.request("GET", f"{WEBHOOKS}/eventTags"))

    def create_webhook(self, subscription: dict) -> Any:
        """POST /subscriptions with a full subscription body (deliveryType PUSH or PULL)."""
        return self._data(self.request("POST", f"{WEBHOOKS}/subscriptions", subscription))

    def create_push_webhook(self, identifier: str, target_url: str, events: list[str], *,
                            auth_header: str | None = None, description: str = "", visibility: str = "WORKSPACE",
                            payload_mode: str = "DEFAULT", callback: str | None = None,
                            tag_sets: list[list[str]] | None = None, active: bool = True) -> Any:
        body: dict[str, Any] = {
            "identifier": identifier, "description": description, "visibility": visibility,
            "deliveryType": "PUSH", "targetUrl": target_url, "targetMethod": "POST",
            "tagSets": tag_sets or [["pathfinder", ev] for ev in events],
            "workspaceConstraint": "WORKSPACE", "payloadMode": payload_mode, "active": active,
            "ignoreError": False, "deactivationNotificationEnabled": True,
        }
        if auth_header:
            body["authorization"] = {"type": "AUTH_HEADER", "authHeader": auth_header}
        if callback:
            body["callback"] = callback
        return self.create_webhook(body)

    def delete_webhook(self, subscription_id: str) -> Any:
        return self.request("DELETE", f"{WEBHOOKS}/subscriptions/{subscription_id}")

    def webhook_deliveries(self, subscription_id: str) -> Any:
        return self._data(self.request("GET", f"{WEBHOOKS}/subscriptions/{subscription_id}/deliveries"))

    def pull_events(self, subscription_id: str, *, auto_commit: bool = False) -> Any:
        return self._data(self.request("GET", f"{WEBHOOKS}/subscriptions/{subscription_id}/events", query={"autoCommit": auto_commit}))

    def commit_cursor(self, subscription_id: str, offset: int) -> Any:
        return self.request("PUT", f"{WEBHOOKS}/subscriptions/{subscription_id}/cursor", {"offset": offset})

    # ------------------------------------------------------------------ Metrics v2
    def metrics_schemas(self) -> Any:
        return self.request("GET", f"{METRICS}/schemas")

    def create_metrics_schema(self, name: str, attributes: list[dict], description: str | None = None) -> Any:
        """attributes: [{"name": "availability", "type": "metric", "unit": "%"}, {"name": "factSheetId", "type": "dimension"}]"""
        return self.request("POST", f"{METRICS}/schemas", {"name": name, "description": description, "attributes": attributes})

    def write_point(self, schema_uuid: str, point: dict) -> Any:
        """point: {"timestamp": "2026-10-26T00:00:00Z", "<metric>": 12.5, "<dimension>": "<factSheetId>"}"""
        return self.request("POST", f"{METRICS}/schemas/{schema_uuid}/points", point)

    def points(self, schema_uuid: str, begin: str | None = None, end: str | None = None, size: int = 50) -> Any:
        return self.request("GET", f"{METRICS}/schemas/{schema_uuid}/points", query={"begin": begin, "end": end, "size": size})

    # ------------------------------------------------------------------ MTM (workspace, users, permissions, technical users)
    def workspace(self) -> dict:
        return self._data(self.request("GET", f"{MTM}/workspaces/{self.workspace_id}"))

    def workspaces(self) -> list[dict]:
        return self._data(self.request("GET", f"{MTM}/workspaces", query={"size": 100}))

    def permissions(self, status: str | None = None, include_technical_users: bool = True, page_size: int = 100) -> list[dict]:
        """Workspace permissions = users with their role and status (ACTIVE, INVITED, ARCHIVED, ...)."""
        out: list[dict] = []
        page = 1
        while True:
            payload = self.request("GET", f"{MTM}/workspaces/{self.workspace_id}/permissions",
                                   query={"page": page, "size": page_size, "status": status,
                                          "includeTechnicalUsers": include_technical_users})
            data = self._data(payload) or []
            out.extend(data)
            total = payload.get("total") if isinstance(payload, dict) else None
            if not data or len(data) < page_size or (total is not None and len(out) >= total):
                break
            page += 1
        return out

    def users(self, status: str | None = None) -> list[dict]:
        rows = []
        for p in self.permissions(status=status):
            u = p.get("user") or {}
            rows.append({"email": u.get("email"), "userName": u.get("userName"), "firstName": u.get("firstName"),
                         "lastName": u.get("lastName"), "role": p.get("role"), "status": p.get("status"),
                         "customerRoles": p.get("customerRoles"), "accessControlEntities": p.get("accessControlEntities"),
                         "lastLogin": p.get("lastLogin"), "technicalUser": u.get("technicalUser"),
                         "userId": u.get("id"), "permissionId": p.get("id")})
        return rows

    def find_user(self, email: str) -> dict | None:
        data = self._data(self.request("GET", f"{MTM}/users", query={"email": email, "size": 10})) or []
        for u in data:
            if (u.get("email") or "").lower() == email.lower():
                return u
        return data[0] if data else None

    def set_permission(self, user_id: str, role: str, *, status: str = "ACTIVE", customer_roles: str | None = None,
                       access_control_entities: str | None = None) -> Any:
        """POST /permissions: sets role (ADMIN | MEMBER | VIEWER) and status (ACTIVE | ARCHIVED | INVITED)
        of a user in the current workspace. Requires an Admin token. Users are archived, never deleted."""
        body: dict[str, Any] = {"user": {"id": user_id}, "workspace": {"id": self.workspace_id},
                                "role": role.upper(), "status": status.upper()}
        if customer_roles is not None:
            body["customerRoles"] = customer_roles
        if access_control_entities is not None:
            body["accessControlEntities"] = access_control_entities
        return self._data(self.request("POST", f"{MTM}/permissions", body))

    def invite_user(self, email: str, role: str, *, first_name: str | None = None, last_name: str | None = None,
                    silent: bool = False, host_user_id: str | None = None) -> Any:
        """POST /idm/invite?silent=. The schema requires host, user, workspace and permission."""
        host_id = host_user_id or (self.token_info().get("principal") or {}).get("id")
        body = {"host": {"id": host_id},
                "user": {"email": email, "userName": email, "firstName": first_name, "lastName": last_name},
                "workspace": {"id": self.workspace_id},
                "permission": {"role": role.upper(), "status": "INVITED"}}
        return self._data(self.request("POST", f"{MTM}/idm/invite", body, query={"silent": silent}))

    def technical_users(self) -> list[dict]:
        return self._data(self.request("GET", f"{MTM}/technicalusers", query={"workspaceId": self.workspace_id, "size": 100})) or []

    def create_technical_user(self, user_name: str, role: str, expiry: str, *, description: str | None = None,
                              customer_roles: str | None = None, access_control_entities: str | None = None) -> dict:
        """POST /technicalusers?workspaceId=: creates a technical user and returns the response that
        carries the API token ONCE (data.apiTokenData.token). expiry: ISO date or date-time."""
        if len(expiry) == 10:
            expiry += "T00:00:00Z"
        body: dict[str, Any] = {"userName": user_name, "permissionRole": role.upper(),
                                "apiTokenData": {"expiry": expiry, "description": description or ""}}
        if customer_roles:
            body["customerRoles"] = customer_roles
        if access_control_entities:
            body["accessControlEntities"] = access_control_entities
        return self.request("POST", f"{MTM}/technicalusers", body, query={"workspaceId": self.workspace_id})

    def replace_technical_user_token(self, technical_user_id: str) -> dict:
        return self.request("PUT", f"{MTM}/technicalusers/{technical_user_id}/replaceToken")

    def technical_user_changelog(self, technical_user_id: str) -> Any:
        return self._data(self.request("GET", f"{MTM}/technicalusers/{technical_user_id}/changelog"))

    # ------------------------------------------------------------------ diagnostics
    def probe(self) -> dict:
        """Checks what the credential can do without changing data: token exchange, workspace claims,
        a one-row read, data-model read, a validateOnly mutation (fails for Viewer tokens), and the
        Admin-only MTM / webhooks / Integration API listings."""
        out: dict[str, Any] = {"host": self.base_url}
        try:
            out["whoami"] = self.whoami()
        except LeanIXError as e:
            out["whoami"] = {"error": str(e)}
            return out
        sample = None
        try:
            data = self.graphql("{ allFactSheets(first: 1) { totalCount edges { node { id name type rev } } } }")
            out["read"] = {"ok": True, "totalFactSheets": data["allFactSheets"]["totalCount"]}
            sample = (data["allFactSheets"]["edges"] or [{}])[0].get("node")
        except LeanIXError as e:
            out["read"] = {"ok": False, "error": str(e)}
        try:
            self.data_model()
            out["dataModel"] = {"ok": True, "factSheetTypes": self.fact_sheet_types()}
        except LeanIXError as e:
            out["dataModel"] = {"ok": False, "status": e.status, "error": str(e)[:200]}
        if sample:
            try:
                self.update_fact_sheet(sample["id"], [patch("replace", "/description", "probe")], validate_only=True, fields="id")
                out["write"] = {"ok": True, "note": "validateOnly mutation accepted (Member or Admin role)"}
            except LeanIXError as e:
                out["write"] = {"ok": False, "error": str(e)[:300], "note": "expected for Viewer tokens"}
        for name, fn in (("mtmPermissions", lambda: self.permissions(page_size=1)),
                         ("webhooks", self.webhooks),
                         ("integrationApi", lambda: self.processor_configs())):
            try:
                fn()
                out[name] = {"ok": True, "note": "Admin-level access"}
            except LeanIXError as e:
                out[name] = {"ok": False, "status": e.status}
        return out


# --------------------------------------------------------------------------- helpers
def _decode(raw: bytes, content_type: str) -> Any:
    if not raw:
        return None
    if "json" in content_type.lower():
        try:
            return json.loads(raw.decode("utf-8"))
        except ValueError:
            return raw.decode("utf-8", "replace")
    if content_type.startswith("text/"):
        return raw.decode("utf-8", "replace")
    return raw


def _enum(value: str) -> str:
    """Validates a GraphQL enum literal (fact sheet type, subscription type) before inlining it."""
    if not value or not value.replace("_", "").isalnum() or not value[0].isalpha():
        raise LeanIXError(f"invalid GraphQL enum value {value!r}")
    return value


def _write_binary(payload: Any, dest: str) -> None:
    data = payload if isinstance(payload, (bytes, bytearray)) else (payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload).encode())
    with open(dest, "wb") as fh:
        fh.write(data)
    print(f"wrote {dest} ({len(data)} bytes)", file=sys.stderr)


def _short(payload: Any, limit: int = 600) -> str:
    if isinstance(payload, (bytes, bytearray)):
        return f"<{len(payload)} bytes>"
    text = payload if isinstance(payload, str) else json.dumps(payload, default=str)
    return text if len(text) <= limit else text[:limit] + "..."


def _dump(obj: Any, out: str | None = None) -> None:
    text = json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {out}", file=sys.stderr)
    else:
        print(text)


def _json_arg(value: str | None) -> Any:
    if value is None:
        return None
    if os.path.isfile(value):
        with open(value, encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(value)


def _flatten(node: Any, prefix: str = "") -> dict:
    """Flattens nested GraphQL nodes into dotted keys for CSV output; lists become JSON strings."""
    flat: dict[str, Any] = {}
    if isinstance(node, dict):
        for k, v in node.items():
            flat.update(_flatten(v, f"{prefix}{k}."))
    elif isinstance(node, list):
        flat[prefix.rstrip(".")] = json.dumps(node, ensure_ascii=False)
    else:
        flat[prefix.rstrip(".")] = node
    return flat


def _write_csv(rows: list[dict], path: str) -> None:
    flat = [_flatten(r) for r in rows]
    keys: list[str] = []
    for r in flat:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(flat)
    print(f"wrote {len(rows)} rows to {path}", file=sys.stderr)


def _poll(fn, done, *, poll: float = 5.0, timeout: float = 900.0):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        last = fn()
        if done(last):
            return last
        time.sleep(poll)
    raise LeanIXError(f"timed out after {timeout:.0f}s", payload=last)


# --------------------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="SAP LeanIX API client (GraphQL, Integration API, Webhooks, Metrics, Import/Export, MTM)")
    ap.add_argument("--host", help="overrides LEANIX_HOST")
    ap.add_argument("--out", help="write JSON output to this file instead of stdout")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("token", help="exchange the API token and print token metadata")
    sub.add_parser("whoami", help="workspace / role / user from the token claims")
    sub.add_parser("probe", help="non-destructive permission probe")
    sub.add_parser("workspace", help="workspace record (MTM)")
    sub.add_parser("workspaces", help="workspaces visible to the token (MTM)")

    p = sub.add_parser("model", help="data model: types | fields <Type> | relations <Type> | raw")
    p.add_argument("what", choices=["types", "fields", "relations", "raw"])
    p.add_argument("type", nargs="?")
    p = sub.add_parser("facets", help="facet keys and option keys of a type (for filters)")
    p.add_argument("type")
    p = sub.add_parser("translations", help="labels for keys (default language en)")
    p.add_argument("--lang", default="en")

    p = sub.add_parser("list", help="list fact sheets of a type (cursor-paginated, de-duplicated)")
    p.add_argument("type", help="fact sheet type, e.g. Application")
    p.add_argument("--fields", default="id name type displayName status", help="GraphQL selection inside node { }")
    p.add_argument("--filter", help="FilterInput JSON (or a file); the FactSheetTypes facet is added automatically")
    p.add_argument("--sort", help="Sorting JSON array, default [{\"key\":\"displayName\",\"order\":\"asc\"}]")
    p.add_argument("--page-size", type=int, default=DEFAULT_PAGE)
    p.add_argument("--limit", type=int, help="stop after N fact sheets")
    p.add_argument("--csv", help="write rows to this CSV file (nested fields flattened)")

    p = sub.add_parser("count", help="count fact sheets of a type / filter")
    p.add_argument("type", nargs="?")
    p.add_argument("--filter")

    p = sub.add_parser("search", help="full-text search")
    p.add_argument("text")
    p.add_argument("--type")
    p.add_argument("--limit", type=int, default=50)

    p = sub.add_parser("get", help="one fact sheet by id")
    p.add_argument("id")
    p.add_argument("--fields", default="id name type displayName description status rev category lxState createdAt updatedAt "
                                        "completion { percentage } tags { id name tagGroup { name } } "
                                        "subscriptions { edges { node { type user { email } roles { name } } } }")

    p = sub.add_parser("query", help="run a GraphQL document (string or file)")
    p.add_argument("query")
    p.add_argument("--vars", help="variables JSON (or file)")
    p.add_argument("--keep-errors", action="store_true", help="print the raw response instead of raising on errors")
    p.add_argument("--warnings", action="store_true", help="request validation warnings (x-graphql-enable-extensions)")

    p = sub.add_parser("create", help="create a fact sheet")
    p.add_argument("type")
    p.add_argument("name")
    p.add_argument("--patches", help="JSON array of patches (or file)")
    p.add_argument("--external-id", help="sets /externalId")
    p.add_argument("--validate-only", action="store_true")

    p = sub.add_parser("update", help="update a fact sheet with JSON patches")
    p.add_argument("id")
    p.add_argument("patches", help="JSON array of patches (or file)")
    p.add_argument("--rev", type=int, help="revision for optimistic locking (re-read and retried on clash)")
    p.add_argument("--comment")
    p.add_argument("--validate-only", action="store_true")

    p = sub.add_parser("relate", help="add a relation from one fact sheet to another")
    p.add_argument("from_id")
    p.add_argument("relation", help="e.g. relApplicationToITComponent")
    p.add_argument("to_id")
    p.add_argument("--attrs", help="relation attributes JSON, e.g. '{\"technicalSuitability\":\"adequate\"}'")
    p.add_argument("--validate-only", action="store_true")

    p = sub.add_parser("relations", help="list one relation of a fact sheet")
    p.add_argument("id")
    p.add_argument("type", help="fact sheet type of <id>, e.g. Application")
    p.add_argument("relation")

    p = sub.add_parser("tag", help="add a tag (by name) to a fact sheet")
    p.add_argument("id")
    p.add_argument("tag_name")
    p.add_argument("--group")
    p.add_argument("--remove", action="store_true", help="remove instead of add")
    p.add_argument("--validate-only", action="store_true")
    sub.add_parser("tags", help="list tag groups and tags with ids")

    p = sub.add_parser("archive", help="archive a fact sheet (comment required; recoverable 90 days)")
    p.add_argument("id")
    p.add_argument("--comment", required=True)
    p.add_argument("--validate-only", action="store_true")
    p = sub.add_parser("recover", help="recover an archived fact sheet")
    p.add_argument("id")
    p.add_argument("--comment", required=True)

    p = sub.add_parser("subscribe", help="add a subscription (RESPONSIBLE | ACCOUNTABLE | OBSERVER)")
    p.add_argument("id")
    p.add_argument("email")
    p.add_argument("type", nargs="?", default="RESPONSIBLE")
    p.add_argument("--role", help="subscription role name (resolved via allSubscriptionRoles)")
    p = sub.add_parser("subscription-roles", help="list subscription roles")
    p.add_argument("--type")
    p = sub.add_parser("comment", help="add a comment to a fact sheet")
    p.add_argument("id")
    p.add_argument("message")
    p = sub.add_parser("events", help="fact sheet history (allLogEvents)")
    p.add_argument("id")
    p.add_argument("--types", help="comma-separated EventTypes enum values")

    p = sub.add_parser("sync", help="Integration API: start a synchronization run from an LDIF file")
    p.add_argument("ldif", help="LDIF JSON file")
    p.add_argument("--test", action="store_true", help="dry run (no changes)")
    p.add_argument("--wait", action="store_true", help="poll until finished and print warnings (implied by --test)")
    p.add_argument("--poll", type=float, default=5.0)
    p.add_argument("--timeout", type=float, default=1800.0)
    p = sub.add_parser("sync-status", help="status of a synchronization run")
    p.add_argument("run_id")
    p = sub.add_parser("sync-warnings", help="warnings and errors of a synchronization run")
    p.add_argument("run_id")
    p = sub.add_parser("sync-results", help="output LDIF of a run (outbound / writeToLdif)")
    p.add_argument("run_id")
    p = sub.add_parser("sync-stop", help="stop a running synchronization run")
    p.add_argument("run_id")
    sub.add_parser("sync-list", help="status of all synchronization runs")

    p = sub.add_parser("processors", help="Integration API processor configurations: get | put <file> | delete")
    p.add_argument("action", choices=["get", "put", "delete"])
    p.add_argument("file", nargs="?", help="configuration JSON for put")
    p.add_argument("--type", dest="ctype")
    p.add_argument("--id", dest="cid")
    p.add_argument("--version", dest="cversion")
    p.add_argument("--direction", default=None, choices=[None, "inbound", "outbound"])
    p.add_argument("--mode", default=None, choices=[None, "partial", "full"])

    p = sub.add_parser("webhooks", help="list | status | event-tags | create <file> | create-push <identifier> <url> | delete <id> | deliveries <id> | pull <id>")
    p.add_argument("action", choices=["list", "status", "event-tags", "create", "create-push", "delete", "deliveries", "pull"])
    p.add_argument("arg", nargs="?")
    p.add_argument("arg2", nargs="?")
    p.add_argument("--events", help="comma-separated event types for create-push, e.g. FACT_SHEET_UPDATED,FACT_SHEET_ARCHIVED")
    p.add_argument("--auth-header", help="Authorization header value sent to the target (create-push)")
    p.add_argument("--description", default="")
    p.add_argument("--auto-commit", action="store_true", help="pull: mark events as consumed")

    p = sub.add_parser("metrics", help="schemas | create-schema <name> <attributes json> | point <schemaUuid> <point json> | points <schemaUuid>")
    p.add_argument("action", choices=["schemas", "create-schema", "point", "points"])
    p.add_argument("arg", nargs="?")
    p.add_argument("arg2", nargs="?")
    p.add_argument("--description")

    p = sub.add_parser("users", help="workspace users with role and status (MTM, Admin)")
    p.add_argument("--status", help="ACTIVE | INVITED | ARCHIVED | ...")
    p.add_argument("--csv")
    p = sub.add_parser("permission", help="set a user's role / status (MTM, Admin)")
    p.add_argument("email")
    p.add_argument("role", choices=["ADMIN", "MEMBER", "VIEWER", "admin", "member", "viewer"])
    p.add_argument("--status", default="ACTIVE")
    p = sub.add_parser("invite", help="invite a user (MTM, Admin)")
    p.add_argument("email")
    p.add_argument("role", choices=["ADMIN", "MEMBER", "VIEWER", "admin", "member", "viewer"])
    p.add_argument("--silent", action="store_true", help="no invitation email")
    p = sub.add_parser("techusers", help="list | create <userName> <role> <expiry YYYY-MM-DD> | replace-token <id> | changelog <id>")
    p.add_argument("action", choices=["list", "create", "replace-token", "changelog"])
    p.add_argument("arg", nargs="?")
    p.add_argument("arg2", nargs="?")
    p.add_argument("arg3", nargs="?")
    p.add_argument("--description")
    p.add_argument("--customer-roles")
    p.add_argument("--aces", help="access control entities")

    p = sub.add_parser("bookmarks", help="saved searches / reports / diagrams / dashboards")
    p.add_argument("--type", default="INVENTORY", choices=["INVENTORY", "REPORTING", "VISUALIZER", "DASHBOARD", "INVENTORY_EXPORT"])
    p = sub.add_parser("export-bookmark", help="Import/Export API: export a saved search as XLSX or LDIF")
    p.add_argument("bookmark_id")
    p.add_argument("--format", default="XLSX", choices=["XLSX", "LDIF"])
    p.add_argument("--download", help="file path to save the artifact to (waits for the job)")
    p = sub.add_parser("export", help="Pathfinder full export job (SNAPSHOT | AUDIT_LOG)")
    p.add_argument("--type", default="SNAPSHOT", choices=["SNAPSHOT", "AUDIT_LOG", "AUDIT_LOG_LEGACY"])
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--download", help="file path to save the export to (waits for the job)")
    p = sub.add_parser("import-excel", help="Import/Export API: upload, validate and (with --execute) run an Excel import")
    p.add_argument("file")
    p.add_argument("--execute", action="store_true")

    p = sub.add_parser("raw", help="arbitrary authenticated request")
    p.add_argument("method")
    p.add_argument("path")
    p.add_argument("--body", help="JSON body (or file)")
    p.add_argument("--query", action="append", default=[], help="key=value (repeatable)")

    a = ap.parse_args(argv)
    try:
        lx = LeanIX.from_env(host=a.host)
        out: Any = None
        if a.cmd == "token":
            lx.exchange_token() if lx.api_token else lx.ensure_token()
            claims = lx.token_info()
            out = {"expires_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(claims.get("exp", 0))),
                   "workspaceId": lx.workspace_id, "token_prefix": lx.ensure_token()[:12] + "..."}
        elif a.cmd == "whoami":
            out = lx.whoami()
        elif a.cmd == "probe":
            out = lx.probe()
        elif a.cmd == "workspace":
            out = lx.workspace()
        elif a.cmd == "workspaces":
            out = lx.workspaces()
        elif a.cmd == "model":
            if a.what == "types":
                out = lx.fact_sheet_types()
            elif a.what == "raw":
                out = lx.data_model()
            else:
                if not a.type:
                    ap.error("model fields|relations needs a <Type>")
                out = lx.fields_of(a.type) if a.what == "fields" else lx.relations_of(a.type)
        elif a.cmd == "facets":
            out = lx.facets(a.type)
        elif a.cmd == "translations":
            out = lx.translations(a.lang)
        elif a.cmd == "list":
            rows = list(lx.iter_fact_sheets(a.type, filter=_json_arg(a.filter), fields=a.fields, sort=_json_arg(a.sort),
                                            page_size=a.page_size, max_items=a.limit))
            if a.csv:
                _write_csv(rows, a.csv)
                out = {"rows": len(rows), "csv": a.csv}
            else:
                out = rows
        elif a.cmd == "count":
            out = {"type": a.type, "count": lx.count_fact_sheets(a.type, _json_arg(a.filter))}
        elif a.cmd == "search":
            out = lx.search(a.text, a.type, limit=a.limit)
        elif a.cmd == "get":
            out = lx.fact_sheet(a.id, a.fields)
        elif a.cmd == "query":
            q = open(a.query, encoding="utf-8").read() if os.path.isfile(a.query) else a.query
            out = lx.graphql(q, _json_arg(a.vars), raise_on_errors=not a.keep_errors, warnings=a.warnings)
        elif a.cmd == "create":
            patches = _json_arg(a.patches) or []
            if a.external_id:
                patches.append(external_id_patch(a.external_id))
            out = lx.create_fact_sheet(a.name, a.type, patches=patches, validate_only=a.validate_only)
        elif a.cmd == "update":
            out = lx.update_fact_sheet(a.id, _json_arg(a.patches), rev=a.rev, comment=a.comment, validate_only=a.validate_only)
        elif a.cmd == "relate":
            out = lx.add_relation(a.from_id, a.relation, a.to_id, _json_arg(a.attrs), validate_only=a.validate_only)
        elif a.cmd == "relations":
            out = lx.relations(a.id, a.relation, a.type)
        elif a.cmd == "tag":
            tid = lx.tag_id(a.tag_name, a.group)
            out = lx.remove_tags(a.id, [tid], validate_only=a.validate_only) if a.remove else lx.add_tags(a.id, [tid], validate_only=a.validate_only)
        elif a.cmd == "tags":
            out = lx.tag_groups()
        elif a.cmd == "archive":
            out = lx.archive_fact_sheet(a.id, a.comment, validate_only=a.validate_only)
        elif a.cmd == "recover":
            out = lx.recover_fact_sheet(a.id, a.comment)
        elif a.cmd == "subscribe":
            role_ids = None
            if a.role:
                roles = [r for r in lx.subscription_roles() if r["name"].lower() == a.role.lower()]
                if not roles:
                    raise LeanIXError(f"subscription role {a.role!r} not found; run `subscription-roles`")
                role_ids = [roles[0]["id"]]
            out = lx.create_subscription(a.id, a.email, a.type, role_ids)
        elif a.cmd == "subscription-roles":
            out = lx.subscription_roles(a.type)
        elif a.cmd == "comment":
            out = lx.create_comment(a.id, a.message)
        elif a.cmd == "events":
            out = lx.events(a.id, a.types.split(",") if a.types else None)
        elif a.cmd == "sync":
            ldif = _json_arg(a.ldif)
            out = lx.run_ldif(ldif, test=a.test, poll=a.poll, timeout=a.timeout) if (a.test or a.wait) else lx.start_sync_run(ldif)
        elif a.cmd == "sync-status":
            out = lx.sync_status(a.run_id)
        elif a.cmd == "sync-warnings":
            out = lx.sync_warnings(a.run_id)
        elif a.cmd == "sync-results":
            out = lx.sync_results(a.run_id)
        elif a.cmd == "sync-stop":
            out = lx.stop_sync_run(a.run_id) or {"stopped": a.run_id}
        elif a.cmd == "sync-list":
            out = lx.request("GET", f"{INTEGRATION}/synchronizationRuns")
        elif a.cmd == "processors":
            if a.action == "get":
                out = lx.processor_configs(a.ctype, a.cid, a.cversion, a.direction, a.mode)
            elif a.action == "put":
                if not a.file:
                    ap.error("processors put needs a configuration file")
                out = lx.put_processor_config(_json_arg(a.file))
            else:
                if not (a.ctype and a.cid and a.cversion):
                    ap.error("processors delete needs --type, --id and --version")
                out = lx.delete_processor_config(a.ctype, a.cid, a.cversion, a.direction or "inbound", a.mode or "partial")
        elif a.cmd == "webhooks":
            if a.action == "list":
                out = lx.webhooks()
            elif a.action == "status":
                out = lx.webhook_statuses()
            elif a.action == "event-tags":
                out = lx.event_tags()
            elif a.action == "create":
                out = lx.create_webhook(_json_arg(a.arg))
            elif a.action == "create-push":
                if not (a.arg and a.arg2 and a.events):
                    ap.error("create-push needs <identifier> <targetUrl> --events A,B")
                out = lx.create_push_webhook(a.arg, a.arg2, a.events.split(","), auth_header=a.auth_header, description=a.description)
            elif a.action == "delete":
                out = lx.delete_webhook(a.arg) or {"deleted": a.arg}
            elif a.action == "deliveries":
                out = lx.webhook_deliveries(a.arg)
            else:
                out = lx.pull_events(a.arg, auto_commit=a.auto_commit)
        elif a.cmd == "metrics":
            if a.action == "schemas":
                out = lx.metrics_schemas()
            elif a.action == "create-schema":
                out = lx.create_metrics_schema(a.arg, _json_arg(a.arg2), a.description)
            elif a.action == "point":
                out = lx.write_point(a.arg, _json_arg(a.arg2))
            else:
                out = lx.points(a.arg)
        elif a.cmd == "users":
            rows = lx.users(a.status)
            if a.csv:
                _write_csv(rows, a.csv)
                out = {"rows": len(rows), "csv": a.csv}
            else:
                out = rows
        elif a.cmd == "permission":
            user = lx.find_user(a.email)
            if not user:
                raise LeanIXError(f"no user with email {a.email!r}; use `invite`")
            out = lx.set_permission(user["id"], a.role, status=a.status)
        elif a.cmd == "invite":
            out = lx.invite_user(a.email, a.role, silent=a.silent)
        elif a.cmd == "techusers":
            if a.action == "list":
                out = lx.technical_users()
            elif a.action == "create":
                if not (a.arg and a.arg2 and a.arg3):
                    ap.error("techusers create needs <userName> <ADMIN|MEMBER|VIEWER> <expiry YYYY-MM-DD>")
                out = lx.create_technical_user(a.arg, a.arg2, a.arg3, description=a.description,
                                               customer_roles=a.customer_roles, access_control_entities=a.aces)
                print("The API token in data.apiTokenData.token is shown only once; store it securely.", file=sys.stderr)
            elif a.action == "replace-token":
                out = lx.replace_technical_user_token(a.arg)
            else:
                out = lx.technical_user_changelog(a.arg)
        elif a.cmd == "bookmarks":
            out = lx.bookmarks(a.type)
        elif a.cmd == "export-bookmark":
            job = lx.export_bookmark(a.bookmark_id, [a.format])
            out = job
            if a.download:
                job_id = job.get("id")
                final = _poll(lambda: lx.export_job(job_id), lambda j: str(j.get("status", "")).upper() in ("DONE", "ERROR", "CANCELLED"))
                if str(final.get("status", "")).upper() == "DONE":
                    lx.download_export_artifact(job_id, a.format, a.download)
                out = {"export": final, "file": a.download}
        elif a.cmd == "export":
            job = lx.start_full_export(a.type, a.start_date, a.end_date)
            out = job
            if a.download:
                job_id = (job or {}).get("id")
                def current():
                    return next((j for j in lx.exports(a.type) if j.get("id") == job_id), {})
                final = _poll(current, lambda j: str(j.get("status", "")).upper() in ("COMPLETED", "DOWNLOADED", "ERROR", "CANCELED", "DELETED"))
                if final.get("downloadKey"):
                    lx.download_export(final["downloadKey"], a.download)
                out = {"export": final, "file": a.download}
        elif a.cmd == "import-excel":
            job = lx.upload_excel_import(a.file)
            out = {"validation": job}
            if a.execute:
                import_id = (job or {}).get("id") or (job or {}).get("importId")
                if not import_id:
                    raise LeanIXError(f"no import id in validation response: {_short(job)}")
                out["execute"] = lx.execute_import(import_id)
                out["status"] = _poll(lambda: lx.import_status(import_id),
                                      lambda s: str((s or {}).get("status", "")).upper() in ("DONE", "FINISHED", "ERROR", "CANCELLED", "FAILED"))
        elif a.cmd == "raw":
            query = dict(kv.split("=", 1) for kv in a.query)
            status, payload, headers = lx.request_full(a.method, a.path, _json_arg(a.body), query=query or None)
            out = {"status": status, "body": payload if not isinstance(payload, (bytes, bytearray)) else f"<{len(payload)} bytes>"}
        _dump(out, a.out)
        return 0
    except LeanIXError as e:
        print(f"error: {e}", file=sys.stderr)
        if e.payload is not None and not isinstance(e.payload, (bytes, bytearray)) and not isinstance(e, GraphQLError):
            print(json.dumps(e.payload, indent=2, default=str)[:4000], file=sys.stderr)
        elif isinstance(e, GraphQLError):
            print(json.dumps(e.errors, indent=2, default=str)[:4000], file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON argument: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
