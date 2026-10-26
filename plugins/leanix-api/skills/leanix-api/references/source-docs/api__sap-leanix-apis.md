<!-- Source: https://help.sap.com/docs/leanix/ea/sap-leanix-apis -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# SAP LeanIX APIs

Explore SAP LeanIX
APIs and learn when to use each API.

## Overview

We provide a suite of powerful APIs that enable you to interact with and manipulate
data within SAP LeanIX. These
APIs offer flexible and efficient ways to integrate with other systems, manage your
workspace data, and create custom reports.

The following table provides an overview of available APIs.

| API | Description |
| --- | --- |
| REST APIs | REST APIs offer access to a wide range of resources, including the meta model, workspace<br>settings, users, metrics, surveys, and more. These APIs are ideal<br>for integration with systems that support RESTful interactions. You<br>can explore and experiment with REST APIs using the OpenAPI<br>explorer, accessible from your workspace. |
| GraphQL API | The GraphQL API enables you to retrieve and update fact sheets<br>and related data using GraphQL queries and mutations. You can use<br>the built-in GraphiQL tool in the administration area of your<br>workspace to interactively develop and test your queries and<br>mutations. |
| Integration API | The Integration API supports integrations with external<br>platforms. It uses our custom LeanIX Data Interchange Format (LDIF)<br>to process data, simplifying the integration process and reducing<br>complexity. This API is ideal for building integrations between SAP<br>LeanIX and other vendor systems. |

## REST APIs

SAP LeanIX REST
APIs offer a versatile interface for interacting with a wide range of resources,
including the meta model, workspace settings, users, metrics, surveys, and more.
These APIs are designed for seamless integration with systems that support RESTful
interactions.

To enhance your experience with SAP LeanIX REST
APIs, we provide the [OpenAPI explorer![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F "https://app.leanix.net/openapi-explorer/"). This tool enables you to explore APIs, send requests, and view
responses directly in your browser. To navigate to the OpenAPI explorer from your
workspace, on the help menu, choose Developer Tools >
OpenAPI Documentation.

For additional information, see [REST APIs](https://help.sap.com/docs/leanix/ea/rest-apis?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with SAP LeanIX REST APIs.").

## GraphQL API

SAP LeanIX chose
GraphQL for managing fact sheets and related data due to its adaptability and
efficiency in handling intricate data structures and relationships. Fact sheets in
SAP LeanIX
often encompass complex models and relationships, which can be difficult to handle
with traditional REST APIs. GraphQL presents a solution to this challenge.

Rather than dealing with fixed data structures, GraphQL enables clients to specify
the exact data they need, significantly reducing the volume of data transferred over
the network and enhancing performance. This is particularly beneficial when dealing
with complex fact sheets, as it allows for more precise and efficient data
retrieval.

Moreover, GraphQL's capability to fetch related data in a single request aids in
managing the relational complexity of fact sheets. With traditional REST APIs,
retrieving related data often necessitates multiple requests to the server. However,
with GraphQL, you can retrieve all related data in a single query, making it a
powerful tool for working with the interconnected data in fact sheets.

GraphQL enables you to query data on your fact sheets as well as mutate (create,
update, or delete) data. In addition, GraphQL is used to create custom reports,
specifically to pull data from the workspace and present it using charts and other
graphics.

We provide GraphiQL, an interactive tool that streamlines interaction with the
GraphQL API, providing an intuitive interface for workspace administrators to
explore the GraphQL schema, experiment with queries and mutations, and validate them
in real time. To navigate to the GraphiQL tool, on the help menu, choose
Developer Tools \> GraphQL
Editor.

For additional information, see [GraphQL API](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the SAP LeanIX GraphQL API.").

## Integration API

The Integration API is a powerful and flexible tool designed to streamline the integration
process between SAP LeanIX and
other vendor systems. One of the key features of the API is that it uses the generic
LeanIX Data Interchange Format (LDIF), which minimizes complexity and eliminates the
need to map logic within the code. This enables developers to effectively use the
API without needing an in-depth understanding of the SAP LeanIX meta
model. For more information, see [LeanIX Data Interchange Format (LDIF)](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a99087a441014a04fa6cda4e0ec2b__leanix_data_interchange_format_ldif).

The Integration API manages CRUD operations for any inbound data from other systems
within SAP LeanIX, significantly reducing complexity. It also allows for the definition of
variables and exceptions and the use of [JUEL expressions![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fjuel.sourceforge.net%2F "https://juel.sourceforge.net/") to extract or import only
specific values.

Additional benefits of the Integration API include the encapsulation of SAP LeanIX
configuration in every connector, the capability to integrate even when the external
system doesn't allow direct access, and flexible error handling. The API mitigates
failure due to single or multiple data issues by disregarding data that doesn't meet
the requirements.

The Integration API also supports the import and export of data from your workspace.
This feature is particularly beneficial when the built-in functionality for
importing or exporting doesn't align with your needs, such as when managing
attributes on relations. The API also excels in handling more complex scenarios, for
example, when the data from the source system is not in a clean state.

For additional information, see [Integration API](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD "Overview of the Integration API.").
