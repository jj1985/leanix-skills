---
type: llm
focus: trace
weight: 1
---

setup.md sends Authorization: Bearer <JWT> to https://acme-eu.leanix.net/services/pathfinder/v1/graphql with an allFactSheets query restricted to Application (FactSheetTypes facet or factSheetType argument) that selects relApplicationToITComponent { edges { node { factSheet { ... } } } } inside an inline fragment ... on Application
