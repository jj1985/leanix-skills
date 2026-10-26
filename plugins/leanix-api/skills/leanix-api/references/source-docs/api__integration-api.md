<!-- Source: https://help.sap.com/docs/leanix/ea/integration-api -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Integration API

Overview of the Integration API.

## Overview

The Integration API provides the ability to import and export data using a generic
LeanIX Data Interchange Format (LDIF). LDIF is a JSON format with a very simple
structure described in the following sections. All mapping and processing of the
incoming and outgoing data is done using "Data Processors" that are configured
behind the API. Configuration of the processors can be done using the UI, The
configurations can be managed using the Integration API as well.

To learn how to configure processors in the application UI, see [Getting Started with the Integration API](https://help.sap.com/docs/leanix/ea/getting-started-with-integration-api?locale=en-US&state=PRODUCTION&version=CLOUD).

## Advantages

- Complexity is minimized as developers no longer have to understand the SAP
LeanIX data model

- Configuration for SAP LeanIX is
contained in every connector

- No longer having to map logic inside of code

- Integration now possible even if the external system does not allow direct
access

- No need for a direct REST connection

- Flexible error handling, no failure due to a single or even multiple data
issues. Data that does not meet the requirements, is simply ignored

- Cross-cutting concerns are part of the API and in each connector

## Inbound and Outbound Data Processors

### Definitions

Inbound Data Processors read the incoming LDIF format, process and convert it into a
set of commands the Integration API can understand. Then it executes it against the
SAP LeanIX
backend database (Pathfinder) or in the case of inboundMetrics the Metrics API.

Outbound Data Processors read data from the workspace and export it to an
LDIF. The content of the produced LDIF will depend on the configured data
processors.

### General Attributes

There are attributes that can be set within the Processors, whether they be outbound
or inbound.

![838](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274d30ee7a441014a033861b5f137b8c_LowRes.png)

The flags are set at the end of the data processors

| Attribute | Allowed Values | Details |
| --- | --- | --- |
| `logLevel` | - `off` (default)<br>  <br>- `warning`<br>  <br>- `debug` | When writing Data Processors, the log level can be set to show detailed output<br>for all data objects processed by a data processor. In order to do this, a key<br>"logLevel" needs to be set to "debug" for the processor. debugInfo in addition to<br>the actual error information also contains the name of the processor and the<br>index. The "warning" logLevel also provides the processor name as well as the<br>index.<br>Default setting is "warning". In this setting detailed information will be<br>provided in case an issue happened processing the data. There may be cases (e.g.<br>incoming data is not consistent/of poor quality) where issues are expected and<br>must not flood the result report. In such cases, the "logLevel" can be set to<br>"off". No errors will be reported for the data processor. |
| `enabled` | - `true`<br>  <br>- `false` | Turns the whole processor on and off. This can be helpful to<br>analyze the impact of certain processors on the result without<br>having to completely remove and add back in them. |

The following example shows an output with warnings that contain the processor
`name` and `index`. These attributes are also
included when the `logLevel` is set to `debug`. In
this case, the debug information is included in the `debugInfo`
section of the output log.

![871](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2743bba67a441014b75bc1be7e2c45d3_LowRes.png)

Example Output of a Processor Run

## LeanIX Data Interchange Format (LDIF)

All data sent (inbound
Data Processor) to the SAP LeanIX
Integration API needs to be in a standard format, called LDIF. For synchronization
of data from SAP LeanIX to
other systems (outbound Data Processor), the Integration API will provide all data
in the same format as well.

The LDIF contains the following information:

- Data sent from the external system to SAP LeanIX.
Or in the case of outbound, data extracted from SAP LeanIX.

- Metadata information to identify the connector instance that wrote the LDIF. The
metadata is used to define ownership of entities in SAP LeanIX if
we need to ensure name spacing/deletion

- Identification of the target workspace and the target API version

- Allow customers adding some arbitrary description for any kind of grouping,
notification or any unstructured notes for display purposes that is not
processed by the API

## Mandatory Attributes

The following table lists mandatory attributes for data input in LDIF format.

| Attribute | Details |
| --- | --- |
| `connectorType` | Contains a string identifying a connector type in the workspace. A connector type<br>identifies code that can be deployed to multiple locations and is able to<br>communicate with a specific external program. In the above example, "lxKubernetes"<br>identifies a connector that was written to read data from a Kubernetes<br>installation and can be deployed into various Kubernetes clusters. In conjunction<br>with "connectorID", the Integration API will match configurations the<br>administrators created and stored in SAP LeanIX and<br>use it when processing incoming data.<br>Incoming data cannot be processed if the corresponding connectorType has not been<br>configured for the SAP LeanIX workspace. |
| `connectorVersion` (connector Version is not mandatory<br>for configurations where the version numbers follow the pattern<br>`number.number.number`) | In case the version number follows the pattern "number.number.number",<br>Integration API provides automatic grouping and handling of different versions of<br>a configuration.<br>The Admin UI will automatically group all configurations by their version numbers<br>and display the highest number on the overview page. In the details users can<br>select the specific version in a drop down.<br>Configurations that follow the pattern above can be executed without sending a<br>specific version number in the LDIF. The Integration API will always process with<br>the highest found version number if no version number was given in the input<br>LDIF.<br>In order to use a specific version for processing, the exact version can be<br>provided in the LDIF.<br>"connectorVersion" may contain any other string content. In such cases, automatic<br>detection of a version does not work and the exact string must be provided in the<br>LDIF |
| `connectorId` | Contains a string to identify a specific deployment of a connector type. As an<br>example: A Kubernetes connector might be deployed multiple times and collect<br>different data from the different Kubernetes clusters. In conjunction with<br>"connectorID", the Integration API will match configurations administrators<br>created and stored in SAP LeanIX and<br>use it when processing incoming data.<br>Administrators in SAP LeanIX can<br>manage each instance of a connector by creating and editing processing<br>configuration, monitor ongoing runs (progress, status) and interact (pause,<br>resume, cancel...). One data transfer for each instance can run at any point of<br>time.<br>Incoming data cannot be processed if the corresponding connectorId has not been<br>configured for the SAP LeanIX<br>workspace. |
| `lxVersion` | Defines the version of the Integration API the connector expects<br>to send data to and will be used to ensure that a component grabbing<br>LDIF files from a cloud storage will send it to the right<br>integration API version (in case no direct communication is<br>available). |
| `content` | The content section contains a list of Data Objects. This section<br>contains the data collected from the external system or the data to<br>be sent to the external system. Each Data Object is defined by an<br>"id", a type to group the source information and a map of data<br>elements (flat or hierarchical maps). Values of map entries may be<br>single string values or lists of string values. |

**Note**

Incoming data cannot be processed if the corresponding `connectorType` has
not been configured for the SAP LeanIX workspace.

## Content Array

The content section contains a list of Data Objects. This section contains the data collected from the external system or the data to be sent to the external system. Each Data Object is defined by an "id" (typically a UUID in the
source system), a type to group the source information and a map of data elements.
The keys "id", "type" and "data" are mandatory. The data map may be flat or
hierarchical maps. Values of map entries may be single string values, maps or
lists.

### Mandatory Attributes

The following table lists mandatory attributes for the `content` array
in the input data.

| Attribute | Description |
| --- | --- |
| `id` | Contains a string typically representing a unique identifier that<br>allows to track back the item in the source system and to ensure<br>updates in SAP LeanIX always go to the same Fact Sheet. SAP LeanIX Data processors will provide an efficient matching option to<br>allow configuration of specific mapping rules based on IDs or groups<br>of IDs that can be identified by patterns. |
| `type` | A string representing any required high level structuring of the<br>source data. Example content in case of Kubernetes are e.g.<br>"Cluster" (containing data that identifies the whole Kubernetes<br>instance) or "Deployment" (which can represent a type of application<br>in Kubernetes) Will typically be used to create different types or<br>subtypes of Fact Sheets or relations from. SAP LeanIX Data processors will provide an efficient matching option to<br>allow configuration of specific mapping rules based on Type or<br>groups of Type strings that can be identified by patterns. |
| `data` | The data extracted from the source system. The format is simple:<br>All data has to be in a Map. Each map can contain a single string as<br>a value for a key, a list of strings as a value or contain a map.<br>The map again has to follow the rules just described. |

### Optional Attributes

The following table lists optional attributes
for the `content` array in the input data.

| Attribute | Description |
| --- | --- |
| `processingMode` | May contain "PARTIAL" (default if not existing) or "FULL". Full<br>mode allows to automatically remove all Fact Sheets that match a<br>configured query and are not touched by the integration. |
| `chunkInformation` | If existing, it contains "firstDataObject", "lastDataObject" and<br>"maxDataObject". Each value is a number defining what is in this<br>potentially chunked LDIF. |
| `description` | The description can contain any string that may help to identify<br>source or type of data. Sometimes it is helpful to add some<br>information to analysis purposes or when setting up configuration on<br>SAP LeanIX side |
| `customFields` | This optional section may contain a map of fields and values<br>defined by the producer of the LDIF. All data can be referenced in<br>any data processor. It will be used for globally available custom<br>meta data. |
| `lxWorkspace` | Defines the SAP LeanIX<br>workspace the data is supposed to be sent to or received from. The content will<br>be used for additional validation by the integration API to check if data will<br>be sent to the right workspace. The content has to match the string visible in<br>the URL when accessing the workspace in a browser.<br>Users need to enter the UUID of the workspace in order to make use of this<br>additional security mechanism. The UUID can e.g. be read from the administration<br>page where API Tokens are created. Example "lxWorkspace":<br>"19fcafab-cb8a-4b7c-97fe-7c779345e20e" |

**Note**

- Additional fields in the LDIF that do not match the requirements of defined
here will be silently ignored.

- Each of the values listed above, except the values in the "content" section
must not be longer than 500 characters.

Example input data for importing fact sheets:

```json
{
  "connectorType": "cloudockit",
  "connectorId": "CDK",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "lxWorkspace": "workspace-id",
  "description": "Imports Cloudockit data into LeanIX",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "content": [
    {
      "type": "ITComponent",
      "id": "b6992b1d-4e4d",
      "data": {
        "name": "Gatsby.j",
        "description": "Gatsby is a free and open source framework based on React that helps developers build websites and apps.",
        "category": "sample_software",
        "provider": "gcp",
        "applicationId": "28db27b1-fc55-4e44"
      }
    },
    {
      "type": "ITComponent",
      "id": "cd4fab6c-4336",
      "data": {
        "name": "Contentful",
        "description": "Beyond headless CMS, Contentful is an API-first content management infrastructure to create, manage and distribute content to any platform or device.",
        "category": "cloud_service",
        "provider": "gcp",
        "applicationId": "28db27b1-fc55-4e44"
      }
    },
    {
      "type": "ITComponent",
      "id": "3eaaa629-5338-41f4",
      "data": {
        "name": "GitHub",
        "description": "GitHub is a tool that provides hosting for software development version control using Git.",
        "category": "cloud_service",
        "provider": "gcp",
        "applicationId": "28db27b1-fc55-4e44"
      }
    },
    {
      "type": "Application",
      "id": "28db27b1-fc55-4e44",
      "data": {
        "name": "Book a Room Internal",
        "description": "Web application that's used internal to book rooms for a meeting."
      }
    }
  ]
}
```

Example input data for importing lifecycle information:

```json
{
  "connectorType": "cloudockit",
  "connectorId": "CDK",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "lxWorkspace": "workspace-id",
  "description": "Imports Cloudockit data into LeanIX",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "content": [
    {
      "type": "Application",
      "id": "company_app_1",
      "data": {
        "name": "TurboTax",
        "plan": null,
        "phaseIn": "2016-12-29",
        "active": "2019-12-29",
        "phaseOut": "2020-06-29",
        "endOfLife": "2020-12-29"
      }
    },
    {
      "type": "Application",
      "id": "company_app_2",
      "data": {
        "name": "QuickBooks",
        "plan": null,
        "phaseIn": "2016-11-29",
        "active": "2019-11-29",
        "phaseOut": "2020-05-29",
        "endOfLife": "2020-11-29"
      }
    }
  ]
}
```

## Integration REST API

You can interact with the Integration API through
REST API endpoints. For more information, see [Integration REST API](https://help.sap.com/docs/leanix/ea/integration-rest-api?locale=en-US&state=PRODUCTION&version=CLOUD "How to connect to the Integration API from an external system.").

## Grouped Execution of Multiple Configurations

A new key "executionGroups" added to the main section now allows Integration API to
execute multiple Integration API configurations as if they were one. This is
advanced functionality, not available in the UI but only when using the REST API.
For details, navigate to the OpenAPI Explorer.

Example processor with grouped execution:

```json
{
  "processors": [
    {
      "processorType": "inboundTag",
      "processorName": "Set TIME tags",
      "processorDescription": "Sets the TIME tags based on existing Fact Sheet values",
      "filter": {
        "advanced": "${integration.contentIndex==0}"
      },
      "identifier": {
        "search": {
          "scope": {
            "ids": [],
            "facetFilters": [
              {
                "keys": [
                  "Application"
                ],
                "facetKey": "FactSheetTypes",
                "operator": "OR"
              }
            ]
          }
        }
      },
      "run": 0,
      "updates": [
        {
          "key": {
            "expr": "name"
          },
          "values": [
            {
              "expr": "${((lx.factsheet.functionalSuitability=='unreasonable' || lx.factsheet.functionalSuitability=='insufficient') && (lx.factsheet.technicalSuitability=='inappropriate' || lx.factsheet.technicalSuitability=='unreasonable'))?'Eliminate':null}"
            },
            {
              "expr": "${((lx.factsheet.functionalSuitability=='appropriate' || lx.factsheet.functionalSuitability=='perfect') && (lx.factsheet.technicalSuitability=='inappropriate' || lx.factsheet.technicalSuitability=='unreasonable'))?'Migrate':null}"
            },
            {
              "expr": "${((lx.factsheet.functionalSuitability=='unreasonable' || lx.factsheet.functionalSuitability=='insufficient') && (lx.factsheet.technicalSuitability=='adequate' || lx.factsheet.technicalSuitability=='fullyAppropriate'))?'Tolerate':null}"
            },
            {
              "expr": "${((lx.factsheet.functionalSuitability=='appropriate' || lx.factsheet.functionalSuitability=='perfect') && (lx.factsheet.technicalSuitability=='adequate' || lx.factsheet.technicalSuitability=='fullyAppropriate'))?'Invest':null}"
            },
            {
              "expr": "No Data"
            }
          ]
        },
        {
          "key": {
            "expr": "group.name"
          },
          "values": [
            {
              "expr": "Time Model"
            }
          ]
        }
      ],
      "logLevel": "warning",
      "read": {
        "fields": [
          "technicalSuitability",
          "name",
          "functionalSuitability"
        ]
      }
    }
  ],
  "executionGroups": [
    "customGroupA",
    "anotherGroup",
    "myGroup"
  ]
}
```

Calling
`/synchronizationRuns/createSynchronizationRunWithExecutionGroup`
with parameter `customGroupA` will run all configurations that
contain `customGroupA` in the list of
`executionGroups` defined.

**Caution**

Advanced functionality: use with careful management of
configurations.

The system will merge the configurations and use all processors from all configurations.
There will be no ordering applied. Processors from different configurations with same run
levels will run in parallel.

Conflicting settings like mixing inbound and outbound configurations will result in an
error. Other special logic like settings for e.g. a data consumer will be taken from any
configuration. If multiple ones are found, the run will be executed with the last found
configuration.

In order to detect the "last found configuration", Integration API configurations with a
matching tag will be sorted alphabetically and merged one by one. Sorting happens by type,
then id, then version.

## Comments in Processors

Integration API allows to solve simple mapping tasks as well solving highly complex
processing and aggregation use cases.

Documentation of more complex processing
is key for maintenance work in case of changes. Integration API allows to add
"description" keys in the locations listed in the below examples. The free text will
be stored with the configuration but not be used for any processing. It is just used
to document more complex expressions used.

Example inbound processor with descriptions:

```json
{
  "identifier": {
    "description": "We iterate over all Fact Sheets of type 'Application'"
  },
  "variables": [
    {
      "description": "Write a variable for each found child to copy description to that later",
      "key": "collectedChild_${integration.variables.valueOfForEach.target.id}",
      "value": "${lx.factsheet.description}",
      "forEach": {
        "elementOf": "${lx.relations}"
      }
    },
    {
      "description": "Write all children to one variable to iterate over in later processor",
      "key": "collectedChildren",
      "value": "${integration.variables.valueOfForEach.target.id}",
      "forEach": {
        "elementOf": "${lx.relations}"
      }
    }
  ],
  "updates": [
    {
      "description": "Values to writing the field Business Fit are taken from a variable",
      "values": [
        {
          "description": "The source variable is names Businessfit_[currentFactSheetId]"
        }
      ]
    }
  ]
}
```

Example outbound processor with descriptions:

```json
{
  "output": [
    {
      "description": "Example description",
      "key": {
        "expr": "content.id"
      },
      "values": [
        {
          "description": "Example description"
        }
      ]
    }
  ]
}
```
