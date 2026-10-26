<!-- Source: https://help.sap.com/docs/leanix/ea/graphql-api -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# GraphQL API

Get started with the SAP LeanIX GraphQL
API.

## Overview

GraphQL is a query language for APIs that allows clients to request precisely the
data they need. It was developed by Facebook to provide a more efficient and
flexible alternative to traditional REST APIs. To learn more about GraphQL, visit
the [GraphQL website![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2F "https://graphql.org/").

The SAP LeanIX
GraphQL API allows you to work with your fact sheets and related data. You can
retrieve and manipulate fact sheet data using GraphQL [queries and mutations![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2Flearn%2Fqueries%2F "https://graphql.org/learn/queries/"). To explore more examples, see [Use Cases](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__use_cases).

The SAP LeanIX
GraphQL API adheres to the [October 2021 specification![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fspec.graphql.org%2FOctober2021%2F "https://spec.graphql.org/October2021/") for
GraphQL.

## Benefits

GraphQL has several benefits, such as:

- You can summarize required related data in a single request. This allows you to
focus on the business logic instead of combining call results and handling
different transactions.

- For large volumes of data, such as in reports or analytics, GraphQL
significantly increases performance. You can transfer exactly the attributes
that you need through the network, without extra latency.

- The GraphQL schema is strongly typed. It's an advantage because strong typing
implies that the API is largely self-documented. You can see what the immediate
response to the query will be. The schema provides descriptions for all API
components, making it easier for the user to navigate the reference
documentation.

- Because everything in GraphQL is schema-driven, it's easy to extend an API. You
can add new fields or types without affecting existing ones.

- In GraphQL, the `@deprecated` annotation is used to mark a field or type as
deprecated. This eliminates the need for versioning an API.

## Use Cases

With our GraphQL API, you can complete various tasks, such as:

- Retrieve a single fact sheet or a list of fact sheets

- Retrieve Applications with specific attributes

- Manage relations between fact sheets

- Update specific attributes on fact sheets

- Fetch data from your workspaces to build custom reports

To explore more examples, see [Sample Queries](https://help.sap.com/docs/leanix/ea/sample-queries?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the GraphQL API using example queries and mutations.").

## GraphQL Basics

To learn the basics of GraphQL, see the following:

- [GraphQL Basics](https://help.sap.com/docs/leanix/ea/graphql-basics?locale=en-US&state=PRODUCTION&version=CLOUD "Learn the GraphQL basics. Create and execute your first queries and mutations."):
Understand how queries and mutations work.

- [Using GraphQL with Python](https://help.sap.com/docs/leanix/ea/using-graphql-with-python?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to run GraphQL queries and mutations using Python."): Learn how to run GraphQL queries and mutations using
Python.

- [Sample Queries](https://help.sap.com/docs/leanix/ea/sample-queries?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the GraphQL API using example queries and mutations."): View
examples and try them out in your workspace.

For comprehensive information about GraphQL, refer to the [GraphQL documentation![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgraphql.org%2Flearn%2F "https://graphql.org/learn/").

## GraphiQL Tool

In the GraphiQL tool in your workspace, you can explore the GraphQL schema and
interactively develop and test queries. To open the GraphiQL tool, on the help menu,
choose Developer Tools \> GraphQL
Editor.

By default, only admins have access to the GraphiQL tool. As an admin, you can grant
permission to access the GraphiQL tool to non-admin roles in the User
Roles and Permissions section of the administration area. For more
details, see [Role-Based Permissions](https://help.sap.com/docs/leanix/ea/user-roles-and-permissions?locale=en-US&state=PRODUCTION&version=CLOUD#loio275def827a4410149362f3672c614956__role-based_permissions).

In the GraphiQL tool, you can:

- Create and execute queries in the interactive Query Editor. To define
variables for a query, enter them in the Variables section in JSON
format.

- View the GraphQL schema. To open the schema, in the sidebar on the left, click
Show Documentation Explorer.

- View your request history and open your previous requests. To expand the
History section, in the sidebar, click Show History. You can
delete specific or all entries, add requests to favorites, and edit the request
labels.

- Interactively create queries and mutations in the Explorer section. To
expand the section, in the sidebar, click Show GraphiQL Explorer. Here,
you can:

  - Select queries and mutations that you want to add to the Query Editor

  - View and select available attributes for each query and mutation,
    without having to navigate to the GraphQL schema

  - Duplicate, rename, and delete queries and mutations

![Creating Queries Using the Explorer in the GraphiQL Tool](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2756cece7a4410149462e2a5d2f29d17_LowRes.png)

Creating Queries Using the Explorer in the GraphiQL Tool

## GraphQL Schema

A GraphQL schema defines the structure and capabilities
of a GraphQL API.

You can explore the GraphQL schema in the Docs section in the GraphiQL tool.
To expand the section, in the sidebar on the left, click Show Documentation Explorer.

![Documentation Explorer in the GraphiQL Tool](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274159067a441014b8becae7eb306b22_LowRes.png)

Documentation Explorer in the GraphiQL Tool

To reload the GraphQL schema, in the sidebar, click Re-fetch GraphQL schema.

In the Docs section, you can:

- View a list of available queries and mutations

- Search for specific queries, mutations, fields, arguments, and other API
elements

In the specification, required attributes are marked with an exclamation
mark.

## Retrieving the GraphQL Schema Metadata

To retrieve the GraphQL schema metadata, use the following query.

```graphql
query {
  __schema {
    types {
      name
      kind
      interfaces {
        kind
        name
      }
      fields {
        name
      }
      inputFields {
        name
        defaultValue
      }
    }
    queryType {
      name
    }
  }
}
```

## Authentication

To authenticate your requests to the GraphQL API, you need an access token. For more information,
see [Authentication to SAP LeanIX Services](https://help.sap.com/docs/leanix/ea/authentication-to-sap-leanix-services?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to authenticate to SAP LeanIX services.").

When using the GraphiQL tool in your workspace, you don't need to authenticate.

## GraphQL API Endpoints

Endpoint for standard GraphQL requests:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/graphql
```

Endpoint for GraphQL file uploads:

```
https://{SUBDOMAIN}.leanix.net/services/pathfinder/v1/graphql/upload
```

## Exporting Queries from the Inventory

You can export GraphQL queries from the inventory based on the current inventory
data, including any applied filters and sorting options. You can copy a JSON query
for external use or export it to the interactive GraphiQL tool in your workspace. By
using these export options, you can create queries more quickly and save time on
configuring complex filtering options.

To access query export options from the inventory, select the arrow icon on the
filter bar, then choose the option you need:

- Copy as JSON Query: Copy a JSON query based on the
current inventory data for external use. The query includes any filters and
sorting options you've applied.

- Open in GraphiQL: Generate a GraphQL query based on
the current inventory data and open it in the GraphiQL tool. The query
includes any filters and sorting options you've applied.

By default, only admins can access these export options in the inventory. As an
admin, you can grant permissions for one or both export options to non-admin roles
in the User Roles and Permissions section of the
administration area. For more details, see [Role-Based Permissions](https://help.sap.com/docs/leanix/ea/user-roles-and-permissions?locale=en-US&state=PRODUCTION&version=CLOUD#loio275def827a4410149362f3672c614956__role-based_permissions).

![Inventory screen showing export options: Copy as JSON Query and Open in GraphiQL.](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio775229cd70154486965c095850a2b519_LowRes.png)

Query Export Options in the Inventory

## Best Practices

Here are some best practices for using GraphQL:

- Focus on queries and mutations that are one-off in nature or for which you don't
need to regularly (such as monthly or weekly) get up-to-date information.

- Use queries to pull relatively simple information. While you can run complex
queries, there are other alternative tools that you can leverage. For example,
the [Integration API](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD "Overview of the Integration API.") may be an easier
and more flexible choice for some use cases. Due to a complexity limit in
GraphQL, long queries are denied to prevent possible Denial of Service (DOS)
attacks.

- When you query a large number of fact sheets, use pagination. To learn more, see [Pagination in GraphQL](https://help.sap.com/docs/leanix/ea/pagination-in-graphql?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how pagination in GraphQL works and how to paginate results in your queries.").

- Use GraphQL when building custom reports. GraphQL allows you to pull information
presented in charts and other visual formats from your workspace. To view
examples of using GraphQL with custom reports, see [Using GraphQL Queries with Custom Reports](https://help.sap.com/docs/leanix/ea/using-graphql-queries-with-custom-reports?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to use GraphQL queries when creating custom reports.").

## Scripts

You can find scripts that use GraphQL in our public SAP LeanIX GitHub
repository. Here are some examples:

- [Update Costs![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgithub.com%2Fleanix-public%2Fscripts%2Ftree%2Fmaster%2FimportCosts "https://github.com/leanix-public/scripts/tree/master/importCosts")

- [Import Metrics![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgithub.com%2Fleanix-public%2Fscripts%2Ftree%2Fmaster%2FimportMetrics "https://github.com/leanix-public/scripts/tree/master/importMetrics")

- [Create Resources![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgithub.com%2Fleanix-public%2Fscripts%2Ftree%2Fmaster%2FcreateDocuments "https://github.com/leanix-public/scripts/tree/master/createDocuments")
