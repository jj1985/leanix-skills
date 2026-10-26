<!-- Source: https://help.sap.com/docs/leanix/ea/pagination-in-graphql -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Pagination in GraphQL

Learn how pagination in GraphQL works and how to paginate results in your
queries.

## Overview

The SAP LeanIX GraphQL
API employs the concept of [relay cursor connections![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Frelay.dev%2Fgraphql%2Fconnections.htm "https://relay.dev/graphql/connections.htm") for pagination, allowing
for efficient and flexible data retrieval. In this pagination model, instead of using
offsets, the API uses cursors to navigate through the dataset. Cursor-based pagination
allows for immediate access to specific items within large datasets, unlike offset-based
pagination, which can be inefficient for high offset values.

This pagination method provides real-time data, reflecting the current state of the
dataset. Paginated requests don't create static snapshots of data. Instead, data is
delivered dynamically. Due to the real-time nature of the data, idempotence is not
guaranteed in paginated requests. This means that the same request with the same query
parameters may return different results if the underlying data has changed between requests,
ensuring you always receive the most up-to-date information.

For additional information on pagination in GraphQL, refer to the [GraphQL documentation![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2Flearn%2Fpagination%2F "https://graphql.org/learn/pagination/").

## Key Concepts

- Cursor: A unique identifier that points to a specific item in a dataset.

- Connection: A structure that provides metadata about the paginated data,
including edges, nodes, page info, and more.

## How Pagination Works

**Note**

The SAP LeanIX GraphQL
API supports forward pagination but does not support backward pagination. Therefore, the
following arguments for backward pagination are not supported: `last`,
`before`, `hasPreviousPage`, and
`startCursor`.

The following arguments for pagination are supported:

- `first`: Specifies the number
of items to be returned in the query.

- `after`: A cursor that
specifies the starting point for the next set of results. To retrieve the initial set of
results, you can omit this argument.

When querying a paginated field, the API returns a connection object that includes:

- `pageInfo`: An object that
provides metadata about the current page, including the `endCursor` and the `hasNextPage` boolean.

- `edges`: An array of objects
that contain the node (the actual data item).

## Retrieving the Initial Set of Results

The following query returns the first two fact sheets from the inventory list. The
`pageInfo` object contains information about the paging state:

- `hasNextPage`: Defines whether
more pages are available.

- `endCursor`: Shows the position
of the current paging cursor.

Example query:

```graphql
{
  allFactSheets(first: 2) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        name
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
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "bWl4OjEjRFhGMVpYSjVRVzVrUm1WMFkyZ0JBQUFBQUFISUJSb1dPRmhwT0dSWFlYVlNNRU55TlZGSVdYbExTVjlLWnc9PSUxNzA1NTY3MDg3Nzg2"
      },
      "edges": [
        {
          "node": {
            "name": "AC Management"
          }
        },
        {
          "node": {
            "name": "AC Management Cloud"
          }
        }
      ]
    }
  }
}
```

The response contains the following:

- `pageInfo`: Provides metadata
about the current page.

  - `hasNextPage`: Indicates
    whether there are more items available.

  - `endCursor`: The cursor of
    the last item in the current set. This cursor is used to fetch the next set of
    results.
- `edges`: An array of objects
containing data nodes.

## Retrieving the Next Set of Results

To fetch the next set of results, use the `endCursor` from the
`pageInfo` as the `after` argument in your next query.

Example query:

```graphql
{
  allFactSheets(first: 2, after: "bWl4OjEjRFhGMVpYSjVRVzVrUm1WMFkyZ0JBQUFBQUFISUJSb1dPRmhwT0dSWFlYVlNNRU55TlZGSVdYbExTVjlLWnc9PSUxNzA1NTY3MDg3Nzg2") {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        name
      }
    }
  }
}
```

The response provides the next set of fact sheets and the new `endCursor`
for subsequent queries.

Example response:

```json
{
  "data": {
    "allFactSheets": {
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "bWl4OjMjRFhGMVpYSjVRVzVrUm1WMFkyZ0JBQUFBQUFISUJoc1dPRmhwT0dSWFlYVlNNRU55TlZGSVdYbExTVjlLWnc9PSUxNzA1NTY3NDI2NDgy"
      },
      "edges": [
        {
          "node": {
            "name": "AC Management to HR Admin"
          }
        },
        {
          "node": {
            "name": "Accenture"
          }
        }
      ]
    }
  }
}
```
