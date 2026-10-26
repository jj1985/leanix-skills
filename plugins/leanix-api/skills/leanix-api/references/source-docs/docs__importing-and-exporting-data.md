<!-- Source: https://help.sap.com/docs/leanix/ea/importing-and-exporting-data -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Importing and Exporting Data

Learn how to import and export data between your organization's system and SAP LeanIX.

Importing and exporting data is an essential step to ensure consistency of information
between your organization's system and SAP LeanIX.

To import and export your organization’s data, you can leverage the following
integrations:

- [Out-of-the-box integrations](https://help.sap.com/docs/leanix/ea/discovery-and-integrations?locale=en-US&state=PRODUCTION&version=CLOUD "SAP LeanIX offers a range of integrations that let you import data from external systems and export data to other platforms. Learn about the available integrations and how to get started.")
with third-party systems, such as SAP Signavio or ServiceNow.

- Integrations through commonly used file formats such as XLS. To learn more, refer
to:

  - [Importing Fact Sheet Data Through Excel File](https://help.sap.com/docs/leanix/ea/importing-fact-sheet-data-through-excel-file?locale=en-US&state=PRODUCTION&version=CLOUD "SAP LeanIX’s import feature enables efficient bulk updates, including adding, updating, and archiving fact sheets. This guide provides formatting rules, error handling, and step-by-step guidance for importing data through an Excel file.")

  - [Exporting Fact Sheet Data as Excel File](https://help.sap.com/docs/leanix/ea/exporting-fact-sheet-data-as-excel-file?locale=en-US&state=PRODUCTION&version=CLOUD "SAP LeanIX’s export feature allows you to export fact sheet data as an Excel file for bulk updates, easy data manipulation, and offline analysis. The exported file also serves as a template for importing data back into SAP LeanIX.")
- Custom integrations leveraging SAP LeanIX [REST APIs](https://help.sap.com/docs/leanix/ea/rest-apis?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with SAP LeanIX REST APIs.") and [GraphQL APIs](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the SAP LeanIX GraphQL API.").

- Custom integrations that you can set up on top of our [Integration API](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD "Overview of the Integration API.").

As a developer, you can streamline the process of importing and exporting data for your
organization. The technology that you should choose depends on the data type.

Here are some examples of technologies for specific data types:

- Fact Sheets and related data: [GraphQL API](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the SAP LeanIX GraphQL API.")
or [Integration API](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD "Overview of the Integration API.")

- Users: [MTM REST API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DMTM "https://app.leanix.net/openapi-explorer/?urls.primaryName=MTM")

- Metrics: [Metrics REST API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DMetrics "https://app.leanix.net/openapi-explorer/?urls.primaryName=Metrics")

- To-dos: [To-do REST API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DTo-Do "https://app.leanix.net/openapi-explorer/?urls.primaryName=To-Do")

- Surveys: [Poll REST API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DPoll "https://app.leanix.net/openapi-explorer/?urls.primaryName=Poll")
