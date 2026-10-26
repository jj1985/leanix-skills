<!-- Source: https://help.sap.com/docs/leanix/ea/migrating-from-fact-sheets-rest-api-to-graphql-api -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Migrating from the Fact Sheets REST API to the GraphQL API

Mappings of REST API endpoints to GraphQL queries and mutations.

## Overview

In this migration guide, you can find examples showing how to transition from the [Fact Sheets REST API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets "https://app.leanix.net/openapi-explorer/#/factSheets") to the GraphQL API. For each operation that you can perform
on fact sheets through the API, we provide an example REST call and its equivalent GraphQL
query or mutation.

For the REST implementation, the result of an operation may vary depending on the provided
parameters. We illustrate requests for each specific parameter with examples, providing a
clear path for a seamless migration.

In the following sections are examples for each documented endpoint within the [OpenAPI Explorer![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FgetFactSheets "https://app.leanix.net/openapi-explorer/#/factSheets/getFactSheets").

## Before You Start

- In this guide, we provide examples for the fundamental combinations of existing
parameters.

- Example queries are basic. They do not contain separate GraphQL variables or pagination
parameters. To learn how to work with GraphQL queries and mutations, see [GraphQL Basics](https://help.sap.com/docs/leanix/ea/graphql-basics?locale=en-US&state=PRODUCTION&version=CLOUD "Learn the GraphQL basics. Create and execute your first queries and mutations.").

- All examples are based on the fact sheet type `Application`. If you want to use a
different fact sheet type, change the corresponding field.

- All queries include placeholders for variables, such as `{id}` or `{toId}`. Before you make API requests,
replace them with actual values.

- You can use the [GraphiQL tool](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__graphiql_tool) in your workspace to try out the provided examples. To open the tool, on the
help menu, select Developer Tools \> GraphQL
Editor.

- The examples usually contain simple queries that do not include all possible parameters.
If needed, you can include additional parameters in the query.

- Following GraphQL best practices, we recommend that you query minimal data to reduce the payload
size and response times. For other recommendations, see [Best Practices](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__best_practices).

## Get All Fact Sheets

| Method | Path | Reference |
| --- | --- | --- |
| GET | `/factSheets` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FgetFactSheets "https://app.leanix.net/openapi-explorer/#/factSheets/getFactSheets") |

In this section, we provide an example of retrieving all fact sheets of the
`Application` type and its relations to fact sheets of the
`ITComponent` type.

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets?relationTypes=relApplicationToITComponent&type=Application
```

GraphQL query:

```graphql
query {
 allFactSheets(filter: {responseOptions: {maxFacetDepth: 5}, facetFilters: [
   {facetKey: "FactSheetTypes",
     keys:["Application"],
     operator: OR
   }
 ]}, sort: [{key: "displayName", order: asc}]) {
   totalCount
   edges {
     node {
       id
       displayName
       description
       rev
       type
       permissions {
         create
         read
         update
         delete
         self
       }
       qualitySeal
       lxState
       updatedAt
       completion {
         percentage
       }
       tags {
         id
         name
         description
         color
         tagGroup {
           id
           name
           shortName
           mode
         }
       }
       subscriptions(filter: {userId: "{userId}"}) {
         edges {
           node {
             id
             user {
               id
               firstName
               lastName
               email
             }
             type
             roles {
               id
               comment
             }
           }
         }
       }
       status
       level
       category
       ... on Application {
         relApplicationToITComponent {
           edges {
             node {
               factSheet {
                       id
                 name
               }
             }
           }
         }
       }
     }
   }
 }
}
```

In the example request, we retrieve all fact sheets of the `Application`
type, including their default fields, `completion`, `tags`,
`subscriptions`, and more. For related fact sheets of the
`ITComponent` type, we only fetch their `id` and
`name`.

## Get a Fact Sheet Hierarchy by Root ID

| Method | Path | Reference |
| --- | --- | --- |
| GET | `/factSheets/hierarchy/{rootId}` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FgetFactSheetHierarchy "https://app.leanix.net/openapi-explorer/#/factSheets/getFactSheetHierarchy") |

You can retrieve all fact sheets equal to or below a specific root fact sheet.

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/hierarchy/{rootId}
```

GraphQL query:

```graphql
query {
 allFactSheets(hierarchy: {mode: FULL_TREE} filter: {ids: ["{rootId}"]}) {
   edges {
     node {
       id
       displayName
     }
   }
 }
}
```

## Get a Fact Sheet by ID

| Method | Path | Reference |
| --- | --- | --- |
| GET | `/factSheets/{id}` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FgetFactSheet "https://app.leanix.net/openapi-explorer/#/factSheets/getFactSheet") |

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}
```

GraphQL query:

```graphql
query {
 factSheet(id: "{id}") {
   id
   displayName
   description
   rev
   type
   permissions {
     create
     read
     update
     delete
     self
   }
   qualitySeal
   lxState
   updatedAt
   completion {
     percentage
   }
   tags {
     id
     name
     description
     color
     tagGroup {
       id
       name
       shortName
       mode
     }
   }
   comments(filter: {status: ACTIVE}) {
     totalCount
     edges {
       node {
         message
       }
     }
   }
   subscriptions(filter: {userId: "{userId}"}) {
     edges {
       node {
         id
         user {
           id
           firstName
           lastName
           email
         }
         type
         roles {
           id
           comment
         }
       }
     }
   }
   status
   level
   category
 }
}
```

To limit the results to only the `id` and `name` fields of a
fact sheet, use the following query:

```graphql
query {
 factSheet(id:"{id}") {
   id
   name
 }
}
```

## Get All Relations of a Fact Sheet

| Method | Path | Reference |
| --- | --- | --- |
| GET | `/factSheets/{id}/relations` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FgetFactSheetRelations "https://app.leanix.net/openapi-explorer/#/factSheets/getFactSheetRelations") |

In this section, we retrieve all relations of a fact sheet with the specified
`{id}`.

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}/relations
```

GraphQL query:

```graphql
query {
 factSheet(id: "{id}") {
   ... on Application {
     relToChild {
       edges {
         node {
           factSheet {
             id
             name
           }
         }
       }
     }
     relApplicationToITComponent {
       edges {
         node {
           factSheet {
             id
             name
           }
         }
       }
     }
     relToSuccessor {
       edges {
         node {
           factSheet {
             id
             name
           }
         }
       }
     }
   }
 }
}
```

In the example request, we retrieve the following relations of a fact sheet:
`relToChild`, `relApplicationToITComponent`, and
`relToSuccessor`. For the target fact sheet, we only fetch the
`id` and `name` fields.

While the REST endpoint provides all possible fields and data in a single call, GraphQL
requires you to add all the required relations and fields of the target fact sheet to your
query.

## Create a Fact Sheet

| Method | Path | Reference |
| --- | --- | --- |
| POST | `/factSheets` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FcreateFactSheet "https://app.leanix.net/openapi-explorer/#/factSheets/createFactSheet") |

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets
```

Example request body:

```json
{
  "name": "TestFactSheet",
  "description": "This is a demo fact sheet.",
  "type": "Application"
}
```

GraphQL mutation:

```graphql
mutation {
 createFactSheet(input: {
   name: "TestFactSheet"
   type: Application
 }
 patches: [
   {
     op: add
     path: "/description"
     value: "This is a demo fact sheet."
   }
 ]) {
   factSheet {
     id
     name
     type
     description
   }
 }
}
```

To update the `description` field, use a Patch operation.

## Update a Fact Sheet

| Method | Path | Reference |
| --- | --- | --- |
| PUT | `/factSheets/{id}` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FupdateFactSheet "https://app.leanix.net/openapi-explorer/#/factSheets/updateFactSheet") |

In this section, we provide an example of updating the description of a fact sheet.

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}
```

Example request body:

```json
{
  "name": "TestFactSheet",
  "description": "This is the updated demo fact sheet description.",
  "displayName": "TestFactSheet",
  "fullName": "TestFactSheet"
}
```

GraphQL mutation:

```graphql
mutation {
 updateFactSheet(id: "{id}"
 patches: [
   {
     op: replace
     path: "/description"
     value: "This is the updated description of a demo fact sheet."
   }
 ]) {
   factSheet {
     id
     name
     type
     description
   }
 }
}
```

Unlike the REST endpoint, the GraphQL mutation allows you to update data in a more granular
way. You don't need to pass fields that you don't want to modify. In this example, we only
update the `description`.

## Archive a Fact Sheet

| Method | Path | Reference |
| --- | --- | --- |
| DELETE | `/factSheets/{id}` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FarchiveFactSheet "https://app.leanix.net/openapi-explorer/#/factSheets/archiveFactSheet") |

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}
```

Example request body:

```json
{
  "comment": "This is a test archive."
}
```

GraphQL mutation:

```graphql
mutation {
 updateFactSheet(id: "{id}",
   comment: "This is a test archive.",
   patches: [{op: add, path: "/status", value: "ARCHIVED"}]) {
     factSheet {
       id
       name
       type
       description
       status
     }
 }
}
```

## Create a Fact Sheet Relation

| Method | Path | Reference |
| --- | --- | --- |
| POST | `/factSheets/{id}/relations` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FcreateFactSheetRelation "https://app.leanix.net/openapi-explorer/#/factSheets/createFactSheetRelation") |

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}/relations
```

Example request body:

```json
{
  "displayNameToFS": "TestRelation",
  "typeFromFS": "relToPredecessor",
  "typeToFS": "relToSuccessor",
  "activeFrom": "2023-11-29",
  "activeUntil": "2024-11-29",
  "constrainingRelations": [],
  "idsOfConstrainingRelations": [],
  "status": "ACTIVE",
  "fromId": "{id}",
  "toId": "{targetId}"
}
```

GraphQL mutation:

```graphql
mutation {
 updateFactSheet(id: "{id}", patches: [
   {
   op: add,
   path: "/relToSuccessor/new_{id}",
   value: "{\"factSheetId\":\"{targetId}\",\"activeFrom\":\"2023-11-29\",\"activeUntil\":\"2024-11-29\"}"
       }
 ]) {
   factSheet {
     id
     name
     type
   }
 }
}
```

## Update a Fact Sheet Relation

| Method | Path | Reference |
| --- | --- | --- |
| PUT | `/factSheets/{id}/relations/{relationId}` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FupdateFactSheetRelation "https://app.leanix.net/openapi-explorer/#/factSheets/updateFactSheetRelation") |

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}/relations/{relationId}
```

Example request body:

```json
{
  "id": "{relationId}",
  "displayNameToFS": "TestApp",
  "typeFromFS": "Application",
  "typeToFS": "Application",
  "permittedReadACL": [],
  "activeFrom": "2023-11-29",
  "activeUntil": "2025-11-29",
  "constrainingRelations": [],
  "fields": [],
  "status": "ACTIVE",
  "fromId": "{id}",
  "toId": "{targetFactSheetId}",
  "naFields": [],
  "type": "relToSuccessor"
}
```

GraphQL mutation:

```graphql
mutation updateRelation {
 updateFactSheet(id: "{id}", patches: [
   {
   op: replace,
   path: "/relToSuccessor/{relationId}",
   value: "{\"description\":\"This is a test description.\",\"factSheetId\":\"{targetFactSheetId}\",\"activeFrom\":\"2023-11-29\",\"activeUntil\":\"2026-11-29\"}"
}
 ]) {
   factSheet {
     id
     name
     type
     ... on Application {
       relToSuccessor {
         edges {
           node {
             id
             activeFrom
             activeUntil
             description
               factSheet {
               fullName
             }
           }
         }
       }
     }
   }
 }
}
```

In the example request, we update a relation for a fact sheet of the
`Application` type.

## Delete a Fact Sheet Relation

| Method | Path | Reference |
| --- | --- | --- |
| DELETE | `/factSheets/{id}/relations/{relationId}` | [Schema![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%23%2FfactSheets%2FdeleteFactSheetRelation "https://app.leanix.net/openapi-explorer/#/factSheets/deleteFactSheetRelation") |

REST call:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/factSheets/{id}/relations/{relationId}
```

GraphQL mutation:

```graphql
mutation {
 updateFactSheet(id: "{id}", patches: [
   {
   op: remove,
   path: "/relToSuccessor/{relationId}",
   value: ""
}
 ]) {
   factSheet {
     id
     name
     type
     ... on Application {
       relToSuccessor {
         edges {
           node {
             id
               factSheet {
               fullName
             }
           }
         }
       }
     }
   }
 }
}
```

In the example request, we delete a relation for a fact sheet of the
`Application` type.
