#!/usr/bin/env python3
"""Builds the curated leanix.openapi.yaml from the official SAP LeanIX specs in openapi/official/.

The official specs are large (the MTM spec alone has 123 paths). This script picks the operations
an integrator needs (token exchange, GraphQL, the Pathfinder REST resources the skill uses, the
Integration API, Webhooks, Metrics v2, Import/Export and the MTM user / technical user endpoints),
prefixes each path with its service base path so one document can hold every service, copies the
transitively referenced schemas (renamed with a service prefix to avoid collisions) and converts
OpenAPI 3.0 `nullable` into 3.1 type unions.

Usage:  python openapi/build_spec.py   (run from the repository root; needs PyYAML)
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent
OFFICIAL = ROOT / "official"
OUT = ROOT / "leanix.openapi.yaml"
SKILL_COPY = ROOT.parent / "plugins" / "leanix-api" / "skills" / "leanix-api" / "references" / "leanix.openapi.yaml"

# service -> (file, base path, schema prefix, tag, selected (method, path) pairs)
SERVICES = [
    ("MTM", "mtm-v1.openapi.json", "/services/mtm/v1", "Mtm", [
        ("post", "/oauth2/token"),
        ("get", "/workspaces"), ("get", "/workspaces/{id}"),
        ("get", "/workspaces/{id}/permissions"), ("post", "/workspaces/{id}/permissions/search"),
        ("get", "/workspaces/{id}/permissions/stats"), ("get", "/workspaces/{id}/permissions/export"),
        ("get", "/workspaces/{id}/users"),
        ("get", "/users"), ("get", "/users/{id}"), ("get", "/users/{id}/permissions"), ("get", "/users/{id}/events"),
        ("post", "/permissions"), ("get", "/permissions/{id}"),
        ("post", "/idm/invite"),
        ("get", "/technicalusers"), ("post", "/technicalusers"),
        ("get", "/technicalusers/{id}"), ("put", "/technicalusers/{id}"), ("delete", "/technicalusers/{id}"),
        ("put", "/technicalusers/{id}/replaceToken"), ("get", "/technicalusers/{id}/changelog"),
        ("get", "/longlivedBearerTokens"), ("post", "/longlivedBearerTokens"), ("post", "/longlivedBearerTokens/{id}/invalidate"),
    ]),
    ("Pathfinder", "pathfinder-v1.swagger.json", "/services/pathfinder/v1", "Pf", [
        ("post", "/graphql"), ("post", "/graphql/upload"),
        ("get", "/factSheets"), ("get", "/factSheets/{id}"), ("get", "/factSheets/hierarchy/{rootId}"),
        ("get", "/factSheets/{id}/relations"),
        ("get", "/models/dataModel"), ("get", "/models/dataModel/enriched"), ("get", "/models/viewModel"),
        ("get", "/models/languages/{id}"), ("get", "/models/authorization"), ("get", "/models/reportingModel"),
        ("get", "/models/metaModel"), ("get", "/models/metaModel/{factSheetType}"),
        ("get", "/models/metaModel/actionBatches"), ("get", "/metaModel/permissionRoles"),
        ("get", "/metaModel/actions/auditLog"),
        ("get", "/models/accessControlEntities"), ("post", "/models/accessControlEntities"),
        ("get", "/bookmarks"), ("post", "/bookmarks"), ("get", "/bookmarks/{id}"), ("put", "/bookmarks/{id}"), ("delete", "/bookmarks/{id}"),
        ("post", "/exports/fullExport"), ("get", "/exports"), ("get", "/exports/downloads/{workspaceId}"),
        ("get", "/features"), ("get", "/settings"),
    ]),
    ("Integration API", "integration-api-v1.oas3.json", "/services/integration-api/v1", "Iapi", [
        ("get", "/configurations"), ("put", "/configurations"), ("delete", "/configurations"),
        ("get", "/synchronizationRuns"), ("post", "/synchronizationRuns"),
        ("post", "/synchronizationRuns/{id}/start"), ("post", "/synchronizationRuns/{id}/stop"),
        ("get", "/synchronizationRuns/{id}/status"), ("get", "/synchronizationRuns/{id}/progress"),
        ("get", "/synchronizationRuns/{id}/results"), ("get", "/synchronizationRuns/{id}/resultsUrl"),
        ("get", "/synchronizationRuns/{id}/warnings"), ("get", "/synchronizationRuns/{id}/stats"),
        ("get", "/synchronizationRuns/{id}/debug"),
        ("post", "/synchronizationRuns/withConfig"), ("post", "/synchronizationRuns/withExecutionGroup"),
        ("post", "/synchronizationRuns/withUrlInput"), ("post", "/fastSynchronizationRuns"),
        ("get", "/examples/starterExample"), ("get", "/examples/advancedExample"),
    ]),
    ("Webhooks", "webhooks-v1.openapi.json", "/services/webhooks/v1", "Wh", [
        ("get", "/subscriptions"), ("post", "/subscriptions"), ("get", "/subscriptions/status"),
        ("get", "/subscriptions/{id}"), ("put", "/subscriptions/{id}"), ("delete", "/subscriptions/{id}"),
        ("get", "/subscriptions/{id}/status"), ("get", "/subscriptions/{id}/deliveries"),
        ("get", "/subscriptions/{id}/events"), ("put", "/subscriptions/{id}/cursor"),
        ("get", "/eventTags"), ("get", "/customEventTags"), ("post", "/customEventTags"),
        ("post", "/events"), ("post", "/events/batch"),
    ]),
    ("Metrics", "metrics-v2.openapi.json", "/services/metrics/v2", "Met", [
        ("get", "/schemas"), ("post", "/schemas"), ("get", "/schemas/find"),
        ("get", "/schemas/{uuid}"), ("delete", "/schemas/{uuid}"),
        ("get", "/schemas/{uuid}/points"), ("post", "/schemas/{uuid}/points"), ("delete", "/schemas/{uuid}/points"),
        ("get", "/schemas/{uuid}/points/{timestamp}"), ("delete", "/schemas/{uuid}/points/{timestamp}"),
        ("post", "/schemas/{uuid}/points/aggregation"), ("get", "/schemas/{uuid}/trends"),
        ("get", "/charts"), ("post", "/charts"), ("get", "/kpis"), ("post", "/kpis"), ("post", "/kpis/validate"),
    ]),
    ("Import Export", "import-export-v1-exports.openapi.yaml", "/services/import-export/v1", "Iex", [
        ("get", "/exports"), ("post", "/exports"), ("get", "/exports/{id}"), ("get", "/exports/{id}/{type}"),
    ]),
    ("Import Export", "import-export-v1-imports.openapi.yaml", "/services/import-export/v1", "Iim", [
        ("post", "/imports"), ("post", "/imports/{importId}"), ("get", "/imports/{importId}"),
        ("post", "/imports/{importId}/cancel"), ("get", "/imports/{importId}/result"),
    ]),
]

INFO_DESCRIPTION = """Curated OpenAPI description of the SAP LeanIX REST surface an integrator uses, assembled on
{date} from the public specifications served by the platform (`https://app.leanix.net/services/<service>/...`;
see `openapi/official/`). Paths carry their service base path so one document covers the MTM token endpoint,
the Pathfinder GraphQL endpoint and REST resources, the Integration API, Webhooks, Metrics v2 and the
Import/Export service. GraphQL queries and mutations themselves are documented in the skill's
`references/graphql-api.md`.

Authentication: `POST /services/mtm/v1/oauth2/token` with HTTP Basic `apitoken:<API token>` and form body
`grant_type=client_credentials` returns a JWT valid for 3600 s; every other operation expects
`Authorization: Bearer <JWT>`. Rate limit: 1800 requests per minute per user (HTTP 429, optional
`Retry-After`). SAP SE owns the underlying API and documentation; this file is a derived, trimmed
reference and is not an official SAP artifact.
"""

REF_RE = re.compile(r"^#/(components/schemas|definitions)/(.+)$")


def load(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    return json.loads(text)


def to_31(node):
    """Converts OpenAPI 3.0 constructs that are invalid in 3.1 (nullable, example on schemas kept)."""
    if isinstance(node, dict):
        if node.get("nullable") is True:
            node = dict(node)
            node.pop("nullable")
            t = node.get("type")
            if isinstance(t, str) and t != "null":
                node["type"] = [t, "null"]
            elif "$ref" in node:
                ref = node.pop("$ref")
                node = {"anyOf": [{"$ref": ref}, {"type": "null"}], **{k: v for k, v in node.items() if k not in ("$ref",)}}
        elif "nullable" in node:
            node = {k: v for k, v in node.items() if k != "nullable"}
        out = {}
        for k, v in node.items():
            if k == "x-nullable":
                continue
            out[k] = to_31(v)
        # 3.1 forbids `type: file` and `exclusiveMinimum: true`
        if out.get("type") == "file":
            out["type"] = "string"
            out["format"] = "binary"
        for key in ("exclusiveMinimum", "exclusiveMaximum"):
            if isinstance(out.get(key), bool):
                bound = out.get("minimum" if key == "exclusiveMinimum" else "maximum")
                if out[key] and bound is not None:
                    out[key] = bound
                    out.pop("minimum" if key == "exclusiveMinimum" else "maximum", None)
                else:
                    out.pop(key)
        return out
    if isinstance(node, list):
        return [to_31(x) for x in node]
    return node


def collect_refs(node, acc: set[str]):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                m = REF_RE.match(v)
                if m:
                    acc.add(m.group(2))
            else:
                collect_refs(v, acc)
    elif isinstance(node, list):
        for x in node:
            collect_refs(x, acc)


def rewrite_refs(node, prefix: str):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                m = REF_RE.match(v)
                out[k] = f"#/components/schemas/{prefix}_{m.group(2)}" if m else v
            else:
                out[k] = rewrite_refs(v, prefix)
        return out
    if isinstance(node, list):
        return [rewrite_refs(x, prefix) for x in node]
    return node


def resolve_param(spec: dict, p: dict) -> dict:
    if "$ref" in p and p["$ref"].startswith("#/components/parameters/"):
        return spec["components"]["parameters"][p["$ref"].split("/")[-1]]
    return p


def main() -> int:
    doc: dict = {
        "openapi": "3.1.0",
        "info": {
            "title": "SAP LeanIX APIs (curated)",
            "version": "1.0.0",
            "summary": "Token exchange, GraphQL endpoint, Pathfinder REST, Integration API, Webhooks, Metrics, Import/Export and MTM user management",
            "description": INFO_DESCRIPTION.format(date=dt.date.today().isoformat()),
            "license": {"name": "MIT (this derived file); SAP LeanIX API and documentation are owned by SAP SE", "identifier": "MIT"},
        },
        "servers": [{"url": "https://{subdomain}.leanix.net",
                     "description": "Your SAP LeanIX instance; the subdomain is the first label of the workspace URL",
                     "variables": {"subdomain": {"default": "app", "description": "e.g. app, eu, us, de, uk, ch, au, ca, br, ae, jp, sg or an SSO company domain"}}}],
        "security": [{"bearerAuth": []}],
        "tags": [],
        "paths": {},
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT",
                               "description": "Access token from POST /services/mtm/v1/oauth2/token (valid 3600 s)"},
                "apiTokenBasic": {"type": "http", "scheme": "basic",
                                  "description": "Only for the token endpoint: username literally `apitoken`, password = the technical user's API token"},
            },
            "schemas": {},
        },
    }
    seen_tags: set[str] = set()
    op_ids: set[str] = set()
    missing = []
    for tag, fname, base, prefix, selection in SERVICES:
        spec = load(OFFICIAL / fname)
        schemas = (spec.get("components") or {}).get("schemas") or spec.get("definitions") or {}
        if tag not in seen_tags:
            seen_tags.add(tag)
            doc["tags"].append({"name": tag, "description": f"Service base path `{base}` (source: {fname})"})
        needed: set[str] = set()
        for method, path in selection:
            src = (spec.get("paths") or {}).get(path, {}).get(method)
            if not src:
                missing.append(f"{tag} {method.upper()} {path}")
                continue
            op = copy.deepcopy(src)
            op["tags"] = [tag]
            # path-level parameters
            path_params = [resolve_param(spec, p) for p in (spec["paths"][path].get("parameters") or [])]
            params = [resolve_param(spec, p) for p in (op.get("parameters") or [])]
            all_params = path_params + params
            # drop header params the client always sets, keep the rest
            all_params = [p for p in all_params if not (p.get("in") == "header" and p.get("name", "").lower() == "authorization")]
            if all_params:
                op["parameters"] = all_params
            else:
                op.pop("parameters", None)
            op.pop("security", None)  # source specs name their schemes differently; the document-level bearerAuth applies
            comps = spec.get("components") or {}
            rb = op.get("requestBody")
            if isinstance(rb, dict) and str(rb.get("$ref", "")).startswith("#/components/requestBodies/"):
                op["requestBody"] = copy.deepcopy(comps["requestBodies"][rb["$ref"].split("/")[-1]])
            for code, resp in list((op.get("responses") or {}).items()):
                if isinstance(resp, dict) and str(resp.get("$ref", "")).startswith("#/components/responses/"):
                    resp = copy.deepcopy(comps["responses"][resp["$ref"].split("/")[-1]])
                    op["responses"][code] = resp
                if isinstance(resp, dict) and not resp.get("description"):
                    resp["description"] = {"200": "OK", "201": "Created", "204": "No Content", "400": "Bad Request",
                                           "401": "Unauthorized", "403": "Forbidden", "404": "Not Found",
                                           "default": "Response"}.get(str(code), f"HTTP {code}")
            if not op.get("summary"):
                text = (op.get("description") or f"{method.upper()} {path}").strip()
                op["summary"] = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0][:120]
            oid = op.get("operationId") or f"{method}{re.sub(r'[^A-Za-z0-9]+', '_', path)}"
            if oid in op_ids:
                oid = f"{prefix.lower()}_{oid}"
            op_ids.add(oid)
            op["operationId"] = oid
            if method == "post" and path == "/oauth2/token":
                op["security"] = [{"apiTokenBasic": []}]
                op["summary"] = "Exchange a technical user's API token for a bearer JWT"
                op["description"] = ("HTTP Basic with username `apitoken` and the API token as password; body "
                                     "`grant_type=client_credentials` (application/x-www-form-urlencoded). The JWT in "
                                     "`access_token` is valid for `expires_in` seconds (3600).")
            if "responses" not in op or not op["responses"]:
                op["responses"] = {"200": {"description": "OK"}}
            collect_refs(op, needed)
            op = rewrite_refs(to_31(op), prefix)
            full_path = base + path
            doc["paths"].setdefault(full_path, {})[method] = op
        # transitive schema closure
        queue = list(needed)
        closure: set[str] = set()
        while queue:
            name = queue.pop()
            if name in closure or name not in schemas:
                continue
            closure.add(name)
            more: set[str] = set()
            collect_refs(schemas[name], more)
            queue.extend(more - closure)
        for name in sorted(closure):
            doc["components"]["schemas"][f"{prefix}_{name}"] = rewrite_refs(to_31(copy.deepcopy(schemas[name])), prefix)
    ops = sum(len(v) for v in doc["paths"].values())
    yaml.SafeDumper.ignore_aliases = lambda self, data: True
    text = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=110)
    header = (f"# Curated SAP LeanIX OpenAPI 3.1 description, generated by openapi/build_spec.py on "
              f"{dt.date.today().isoformat()} from the public specs in openapi/official/.\n"
              f"# {len(doc['paths'])} paths, {ops} operations, {len(doc['components']['schemas'])} schemas. Do not edit by hand; re-run the script.\n")
    OUT.write_text(header + text, encoding="utf-8", newline="\n")
    SKILL_COPY.write_text(header + text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} and {SKILL_COPY}: {len(doc['paths'])} paths, {ops} operations, {len(doc['components']['schemas'])} schemas")
    if missing:
        print("missing operations:", *missing, sep="\n  ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
