<!-- Source: https://help.sap.com/docs/leanix/ea/filtering-in-graphql -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Filtering in GraphQL

Learn how filtering in GraphQL works and how to apply filters to your
queries.

Data filtering is crucial for extracting relevant insights from your
organization's data. GraphQL allows you to filter data accurately based on specific
criteria, enhancing data retrieval and management efficiency.

This document offers an overview of data filtering in GraphQL, with a focus on its
implementation in the SAP LeanIX
GraphQL API. You'll learn how to fetch available filters and use them in your
GraphQL queries.

**Tip**

You can export GraphQL queries from the inventory based
on your inventory data, including any applied filters and sorting options. To learn more,
see [Exporting Queries from the Inventory](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__section_gym_cf3_jhc).

**Note**

Understanding which GraphQL operations support filtering is key to using filters
effectively. You can explore available filters by navigating through the GraphiQL
interface in your SAP LeanIX workspace.
This interface provides a comprehensive and interactive overview of the GraphQL schema. To
learn more about GraphiQL and how to navigate to it, see [GraphiQL Tool](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a6d497a4410149a8bffcc34da11b9__graphiql_tool).

## Filters

The SAP LeanIX
GraphQL API offers robust filtering capabilities to enhance your data retrieval
operations. These filters are particularly useful when managing large data volumes,
as they boost the accuracy and efficiency of your data management tasks.

The filtering capabilities are supported in specific operations through the
`filter` argument associated with the corresponding API
operation. This argument lets you define the criteria that data must meet to be
included in the operation's results.

For example, to retrieve fact sheets with a specific technical fit, use the
`filter` argument in your API operation. The system returns only
the fact sheets that meet this criterion.

## Logical Operators

Logical operators are essential tools for filtering
complex data sets in GraphQL. They let you combine or modify filter conditions,
enabling you to create more complex and precise data queries.

The table below provides an overview of the logical operators you can use in your
GraphQL queries:

| Logical Operator | Description |
| --- | --- |
| `AND` | Returns true if all specified conditions are met. It allows you<br>to narrow down results by requiring multiple criteria to be<br>satisfied. |
| `OR` | Returns true if at least one specified condition is met. It<br>allows you to broaden results by including data that satisfies any<br>of the given criteria. |
| `NOR` | Returns true if none of the specified conditions are met. It<br>allows you to exclude data that satisfies any of the given<br>criteria. |

## Facet Keys

**Note**

This document doesn't provide a comprehensive list of all available filter
options. You can view a full list of filters and facet keys in the GraphQL
schema, accessible through the GraphiQL tool in your SAP LeanIX
workspace. Explore filter options for each query in the Explorer section
of GraphiQL and apply them interactively to your operations.

Facets are a powerful feature that enhances the precision of data filtering
operations. They are the `keys` used to filter results in queries.
These keys can be based on various attributes, such as the fact sheet type, the
relation between fact sheets, and more.

Given the diverse nature of fact sheets in SAP LeanIX,
facets fall into two categories:

- [Global facet keys](https://help.sap.com/docs/leanix/ea/filtering-in-graphql?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a2edc7a441014bb70948cb326e764__global_facet_keys)

- [Facet keys specific to fact sheet types](https://help.sap.com/docs/leanix/ea/filtering-in-graphql?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a2edc7a441014bb70948cb326e764__facet_keys_specific_to_fact_sheet_types)

This categorization ensures you can apply the most appropriate and relevant filters
to your data.

## Global Facet Keys

Global facet keys apply to all fact sheet types. These facets are based on attributes
or relations common to all fact sheets, regardless of type. This consistency allows
you to apply uniform filters across different fact sheet types, ensuring uniformity
in your data retrieval operations. For example, `lxState` is a global
facet that lets you filter fact sheets by a specific quality seal state.

The table below lists the available global facet filters. Each entry includes the
facet key used in GraphQL queries and the corresponding filter name as it appears on
the left-side filter pane in the inventory.

| Facet Key | Filter Name in the Inventory |
| --- | --- |
| `FactSheetTypes` | Type |
| `hierarchyLevel` | Hierarchy Level |
| `Subscriptions` | Subscriptions |
| `DataQuality` | Data Quality |
| `lxState` | Quality Seal |
| `TrashBin` | Trash Bin |
| `_TAGS_` | Other Tags |

The following image shows filters on the left-side pane of the inventory. To learn
more about filtering data in the inventory, see [Searching and Filtering in the Inventory](https://help.sap.com/docs/leanix/ea/searching-and-filtering-in-inventory?locale=en-US&state=PRODUCTION&version=CLOUD "Searching and filtering in the inventory helps efficiently manage your data. Learn how to quickly find fact sheets, apply filters, manage filters, and save search results for future access.").

![Filters in the Inventory](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2754d9e77a441014945bfabcca56cfb5_LowRes.png)

Filters in the Inventory

## Facet Keys Specific to Fact Sheet Types

Facet keys specific to certain types of fact sheets rely on the specific attributes
or relations of a particular fact sheet type. For instance, the
`dataFlowDirection` facet, which indicates the data flow
direction of an interface, is available only for fact sheets of the
`Interface` type. This specificity helps narrow down results to a
particular fact sheet type.

In the GraphQL Explorer, you can switch between different fact sheet types. Each type
has its own unique set of facet filters, offering more granularity in data
filtering. As you switch between types, the available facet filters on the sidebar
change, allowing you to access and apply unique filters to your data.

Understanding the types of fact sheets you're working with and the filters they
support is key to effective data filtering. By leveraging this knowledge, you can
apply the most relevant and precise filters, ensuring your data management and
analysis tasks are efficient and accurate.

## Retrieving Facet Filters

You can retrieve the available filter options for specific fact sheet types. This feature
helps you understand the available facets, their keys, the possible operators you can use
with them, and the options for applying a specific filter.

The following GraphQL query retrieves the available facet filters for the
`Application` fact sheet type:

```
query availableFaceFilters {
  allFactSheets(factSheetType: Application) {
    filterOptions {
      facets {
        facetKey
        possibleOperators
        operator
        results {
          name
          key
        }
        dateFilter {
          from
          to
          type
          minDate
          maxDate
        }
        relationFieldsFilterOperator
        relationFieldsFilter {
          fieldName
          values {
            key
            selected
          }
        }
      }
    }
  }
}
```

The query returns a list of facets for the `Application` fact sheet type.
Each facet includes the following attributes:

- `facetKey`: The facet's
key.

- `possibleOperators`: A list of
logical operators you can use with the facet.

- `operator`: The logical
operator used with the facet.

- `results`: A list of available
options for using the facet. Each option has a `name` and a `key`.

- `dateFilter`: If the filter
supports date ranges, this attribute provides details and options, including the range
( `from` and `to`), `type`, and the minimum and maximum
dates ( `minDate` and `maxDate`).

- `relationFieldsFilterOperator`:
The operator used with the relational fields filter.

- `relationFieldsFilter`: Details
of the relational fields filter, including the field name ( `fieldName`) and a list of values. Each
value has a `key` and a `selected` status.

The following example response is shortened and doesn't include all available filter
options.

```json
{
  "data": {
    "allFactSheets": {
      "filterOptions": {
        "facets": [
          {
            "facetKey": "FactSheetTypes",
            "possibleOperators": [],
            "operator": "OR",
            "results": [
              {
                "name": "Objective",
                "key": "Objective"
              },
              {
                "name": "Platform",
                "key": "Platform"
              },
              {
                "name": "Initiative",
                "key": "Initiative"
              },
              {
                "name": "BusinessCapability",
                "key": "BusinessCapability"
              },
              {
                "name": "BusinessContext",
                "key": "BusinessContext"
              },
              {
                "name": "Organization",
                "key": "Organization"
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
            ],
            "dateFilter": null,
            "relationFieldsFilterOperator": null,
            "relationFieldsFilter": null
          },
          {
            "facetKey": "DataQuality",
            "possibleOperators": [
              "OR",
              "AND",
              "NOR"
            ],
            "operator": "OR",
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
            ],
            "dateFilter": null,
            "relationFieldsFilterOperator": null,
            "relationFieldsFilter": null
          },
          {
            "facetKey": "lxState",
            "possibleOperators": [
              "OR",
              "NOR"
            ],
            "operator": "OR",
            "results": [
              {
                "name": "BROKEN_QUALITY_SEAL",
                "key": "BROKEN_QUALITY_SEAL"
              },
              {
                "name": "DRAFT",
                "key": "DRAFT"
              },
              {
                "name": "REJECTED",
                "key": "REJECTED"
              },
              {
                "name": "APPROVED",
                "key": "APPROVED"
              }
            ],
            "dateFilter": null,
            "relationFieldsFilterOperator": null,
            "relationFieldsFilter": null
          },
          ...
        ]
      }
    }
  }
}
```

## Examples

To view example queries with filters, see [Filtering Fact Sheets](https://help.sap.com/docs/leanix/ea/filtering-fact-sheets?locale=en-US&state=PRODUCTION&version=CLOUD "Example queries for filtering fact sheets through the GraphQL API."). You can adapt
these examples to suit your needs based on the data you want to fetch.

In this section, we provide an example query with multiple facet filters and explain how
each filter works. We aim to filter fact sheets by these parameters:

- Fact sheet type: `Application`

- Technical fit: `unreasonable`

- Functional fit: Any value except `perfect` or `appropriate`

- Lifecycle phase: `phaseIn`, with the start date
between 2023 and 2029

The table below lists the facet filters to use in the query and specifies the operations
they perform.

| Facet Key | Facet Filter Object | Operation |
| --- | --- | --- |
| `FactSheetTypes` | <br>```json<br>{<br>  "facetKey": "FactSheetTypes",<br>  "operator": "OR",<br>  "keys": [<br>    "Application"<br>  ]<br>}<br>```<br><br> | Filters fact sheets of the `Application` type. |
| `technicalSuitability` | <br>```json<br>{<br>  "facetKey": "technicalSuitability",<br>  "operator": "OR",<br>  "keys": [<br>    "unreasonable"<br>  ]<br>}<br>```<br><br> | Filters fact sheets with the technical fit set to `unreasonable`. |
| `functionalSuitability` | <br>```json<br>{<br>  "facetKey": "functionalSuitability",<br>  "operator": "NOR",<br>  "keys": [<br>    "perfect",<br>    "appropriate"<br>  ]<br>}<br>```<br><br> | Excludes fact sheets with the functional fit set to `perfect` or `appropriate`. |
| `lifecycle` | <br>```json<br>{<br>  "facetKey": "lifecycle",<br>  "operator": "OR",<br>  "keys": [<br>    "phaseIn"<br>  ],<br>  "dateFilter": {<br>    "type": "RANGE",<br>    "from": "2023-01-01",<br>    "to": "2029-12-31"<br>  }<br>}<br>```<br><br> | Filters fact sheets in the `phaseIn` lifecycle phase with the start date between 2023 and<br>2029. |

Additionally, we sort items in the response in descending order by the
`updatedAt` field using the `sortings` variable.

Example query:

```graphql
query filterFactSheets($filter: FilterInput!, $sortings: [Sorting]) {
  allFactSheets(filter: $filter, sort: $sortings) {
    totalCount
    edges {
      node {
        id
        displayName
        type
        ... on Application {
          technicalSuitability
          functionalSuitability
          lifecycle {
            phases {
              phase
              startDate
            }
          }
          updatedAt
        }
      }
    }
  }
}
```

Variables:

```json
{
  "filter": {
    "facetFilters": [
      {
        "facetKey": "FactSheetTypes",
        "operator": "OR",
        "keys": [
          "Application"
        ]
      },
      {
        "facetKey": "technicalSuitability",
        "operator": "OR",
        "keys": [
          "unreasonable"
        ]
      },
      {
        "facetKey": "functionalSuitability",
        "operator": "NOR",
        "keys": [
          "perfect",
          "appropriate"
        ]
      },
      {
        "facetKey": "lifecycle",
        "operator": "OR",
        "keys": [
          "phaseIn"
        ],
        "dateFilter": {
          "type": "RANGE",
          "from": "2023-01-01",
          "to": "2029-12-31"
        }
      }
    ]
  },
  "sortings": [
    {
      "key": "updatedAt",
      "order": "desc"
    }
  ]
}
```

Example response:

```json
{
  "data": {
    "allFactSheets": {
      "totalCount": 2,
      "edges": [
        {
          "node": {
            "id": "01740698-1ffa-4729-94fa-da6194ebd7cd",
            "displayName": "AC Management",
            "type": "Application",
            "technicalSuitability": "unreasonable",
            "functionalSuitability": "unreasonable",
            "lifecycle": {
              "phases": [
                {
                  "phase": "phaseIn",
                  "startDate": "2024-02-01"
                }
              ]
            },
            "updatedAt": "2024-12-12T15:07:59.227127386Z"
          }
        },
        {
          "node": {
            "id": "2e50479c-fd64-4800-b398-3f34c653994b",
            "displayName": "Adobe Creative Cloud",
            "type": "Application",
            "technicalSuitability": "unreasonable",
            "functionalSuitability": "insufficient",
            "lifecycle": {
              "phases": [
                {
                  "phase": "phaseIn",
                  "startDate": "2024-02-05"
                }
              ]
            },
            "updatedAt": "2024-12-03T15:45:04.375449793Z"
          }
        }
      ]
    }
  }
}
```
