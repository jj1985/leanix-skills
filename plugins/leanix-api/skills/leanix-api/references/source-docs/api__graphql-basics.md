<!-- Source: https://help.sap.com/docs/leanix/ea/graphql-basics -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# GraphQL Basics

Learn the GraphQL basics. Create and execute your first queries and
mutations.

This topic provides an overview of basic GraphQL concepts to help you get started. To learn about
GraphQL and how it works, refer to the [GraphQL documentation![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2Flearn%2F "https://graphql.org/learn/").

To create and test your first queries and mutations, you can use the [GraphiQL Tool](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__graphiql_tool) in your workspace.

To explore the GraphQL schema, navigate to the Documentation Explorer section in the
GraphiQL tool. In the schema, an exclamation mark next to an attribute indicates that the
attribute is required (cannot be `null`).

**Tip**

To explore example queries and mutations for the SAP LeanIX GraphQL API,
see [Sample Queries](https://help.sap.com/docs/leanix/ea/sample-queries?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the GraphQL API using example queries and mutations.").

## Queries

GraphQL queries allow you to retrieve data, similar to `GET` methods in REST
APIs. To learn more about queries, see [Queries and Mutations![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2Flearn%2Fqueries%2F "https://graphql.org/learn/queries/") in
the GraphQL documentation.

To explore queries available within the SAP LeanIX GraphQL API,
navigate to the Documentation Explorer section in the [GraphiQL tool](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__graphiql_tool).

As an example, let's retrieve a Fact Sheet by its ID using the `factSheet`
query. `id` is a required argument for this query. To get the ID of a Fact
Sheet, navigate to the Fact Sheet page in the application user interface and copy the ID
from the URL.

In the example, we request the following Fact Sheet attributes to be returned in the
response: `id`, `name`, and `type`. You can
modify the query to retrieve the data you need.

Example query:

```graphql
{
  factSheet(id: "28fe4aa2-6e46-41a1-a131-72afb3acf256") {
    id
    name
    type
  }
}
```

Example response:

```json
{
  "data": {
    "factSheet": {
      "id": "28fe4aa2-6e46-41a1-a131-72afb3acf256",
      "name": "AC Management",
      "type": "Application"
    }
  }
}
```

## Mutations

GraphQL mutations allow you to modify data, similar to `POST`,
`PUT`, `PATCH`, and `DELETE` methods in REST
APIs. To learn more about mutations, see [Mutations![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2Flearn%2Fmutations%2F "https://graphql.org/learn/mutations/") in the
GraphQL documentation.

To explore mutations available within the SAP LeanIX GraphQL API,
navigate to the Documentation Explorer section in the [GraphiQL tool](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__graphiql_tool).

As an example, let's create an Application Fact Sheet using the
`createFactSheet` mutation. The fields `name` and
`type` of the `BaseFactSheetInput` input argument are
required for this mutation. We pass these fields using the `$input`
variable.

To retrieve specific Fact Sheet attributes in the response, use the
`factSheet` query. In the example, we retrieve the following attributes:
`id`, `name`, and `type`.

Example mutation with a variable:

```graphql
mutation ($input: BaseFactSheetInput!) {
  createFactSheet(input: $input) {
    factSheet {
      id
      name
      type
    }
  }
}
```

The mutation requires an `$input` variable. Define the variable in JSON
format.

We recommend using variables in mutations with a large number of input parameters.

Variables:

```json
{
  "input":{"name":"New Fact Sheet", "type": "Application"}
}
```

Alternatively, you can create a mutation without a variable.

Example mutation without a variable:

```graphql
mutation {
  createFactSheet(input: {name: "New Fact Sheet", type: Application}) {
    factSheet {
      id
      name
      type
    }
  }
}
```

Once you have executed the request, you get a response that contains the details of the new
Fact Sheet. The `id` is generated automatically.

Example response:

```json
{
  "data": {
    "createFactSheet": {
      "factSheet": {
        "id": "16fdc1a9-ae59-4d0a-b6ce-bb717baa74f3",
        "name": "New Fact Sheet",
        "type": "Application"
      }
    }
  }
}
```

## Including Multiple Mutations in a Single Request Using Aliases

To make your program run faster and deal with delays caused by network connection, you can
include multiple mutations in one request by using mutation aliases.

When using aliases in mutations, follow these guidelines:

- Choose a unique alias for each mutation.

- Split your mutations into manageable chunks to prevent execution disruption caused by
HTTP timeouts. Depending on the complexity of specific mutations, 50 is a reasonable chunk
size to start with.

In the example mutation, we create two Application Fact Sheets using mutation aliases
`fs1` and `fs2`.

Example mutation:

```graphql
mutation {
  fs1: createFactSheet(input: {name: "fs1", type:Application}) {
    factSheet { id }
  },
  fs2: createFactSheet(input: {name: "fs2", type:Application}) {
    factSheet { id }
  }
}
```

Example response:

```json
{
  "data": {
    "fs1": {
      "factSheet": {
        "id": "8acea607-94c6-4818-9c64-2af5ecd0be98"
      }
    },
    "fs2": {
      "factSheet": {
        "id": "6fe9bd88-dd6b-461d-ab35-db139961b48f"
      }
    }
  }
}
```

## Retrieving a List of Filtering Facet Keys

The following example shows how to retrieve a list of all facet keys within a
workspace.

Example query:

```graphql
{
  allFactSheets{
    filterOptions {
      facets {
        facetKey
        results {
          name
          key
        }
      }
    }
  }
}
```

Example response:

```json
{
  "data": {
    "allFactSheets": {
      "filterOptions": {
        "facets": [
          {
            "facetKey": "FactSheetTypes",
            "results": [
              {
                "name": "BusinessCapability",
                "key": "BusinessCapability"
              },
              {
                "name": "Process",
                "key": "Process"
              },
              {
                "name": "UserGroup",
                "key": "UserGroup"
              },
              {
                "name": "Project",
                "key": "Project"
              },
              {
                "name": "Application",
                "key": "Application"
              },
              {
                "name": "Interface",
                "key": "Interface"
              },
              {
                "name": "DataObject",
                "key": "DataObject"
              },
              {
                "name": "ITComponent",
                "key": "ITComponent"
              },
              {
                "name": "Provider",
                "key": "Provider"
              },
              {
                "name": "TechnicalStack",
                "key": "TechnicalStack"
              }
            ]
          },
          {
            "facetKey": "hierarchyLevel",
            "results": [
              {
                "name": "1",
                "key": "1"
              },
              {
                "name": "2",
                "key": "2"
              },
              {
                "name": "3",
                "key": "3"
              }
            ]
          },
          {
            "facetKey": "DataQuality",
            "results": [
              {
                "name": "noResponsible",
                "key": "_noResponsible_"
              },
              {
                "name": "qualitySealBroken",
                "key": "_qualitySealBroken_"
              },
              {
                "name": "noDescription",
                "key": "_noDescription_"
              },
              {
                "name": "noLifecycle",
                "key": "_noLifecycle_"
              }
            ]
          },
          {
            "facetKey": "_TAGS_",
            "results": [
              {
                "name": "Headquarter",
                "key": "aa51ccc9-db61-48df-89d1-f217f37757ea"
              },
              {
                "name": "Tag2",
                "key": "819d3d4f-f044-470a-8f5d-c11bc15eff67"
              }
            ]
          }
        ]
      }
    }
  },
  "errors": null
}
```

## Pagination in GraphQL

The SAP LeanIX GraphQL API
employs the concept of [relay cursor connections![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Frelay.dev%2Fgraphql%2Fconnections.htm "https://relay.dev/graphql/connections.htm") for pagination, allowing for efficient
and flexible data retrieval. In this pagination model, instead of using offsets, the API
uses cursors to navigate through the data set. For more details, see [Pagination in GraphQL](https://help.sap.com/docs/leanix/ea/pagination-in-graphql?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how pagination in GraphQL works and how to paginate results in your queries.").
