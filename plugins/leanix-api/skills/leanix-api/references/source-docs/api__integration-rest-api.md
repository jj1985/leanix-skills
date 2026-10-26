<!-- Source: https://help.sap.com/docs/leanix/ea/integration-rest-api -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Integration REST API

How to connect to the Integration API from an external system.

## Overview

In the previous documents in this series the focus is on utilizing the Integration
API via the built-in UI. This is an excellent way to quickly get started, and to
test different scenarios. In addition, it can be used with real data in "one-off"
situations where you quickly need to get an answer to a question using the Outbound
Processor, or even doing a simple one time import via the Inbound Processors.
However, in other more complex cases such as when you need to connect an "other
vendor" system to SAP LeanIX, it
will eventually be necessary to build a REST API.

If you haven't done so already please see [Integration API](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD "Overview of the Integration API.") in order to familiarize yourself with the basics of the
Integration API.

To view reference documentation for the Integration REST API, navigate to the [OpenAPI Explorer![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DIntegration%2520API "https://app.leanix.net/openapi-explorer/?urls.primaryName=Integration%20API"). When you make API
requests, ensure that you use the right base URL. For more information, see [Base URL](https://help.sap.com/docs/leanix/ea/base-url?locale=en-US&state=PRODUCTION&version=CLOUD "Find your base URL to use in API requests or configurations.").

To learn how to authenticate to SAP LeanIX APIs,
see [Authentication to SAP LeanIX Services](https://help.sap.com/docs/leanix/ea/authentication-to-sap-leanix-services?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to authenticate to SAP LeanIX services.").

Integration runs in two steps and a minimum two calls are required to start a Sync
run. Please see below for the integration flow including calls.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio275772a17a441014b864cc70032ee6a4_LowRes.png)

## Creating a Processor

Create a Processor under Integration API, with the below details:

- Connector Type: importProjectsExample

- Connector Id: importProjectsExample

- Connector Version: 1.0.0

- Processing Direction: inbound

Place the below details in the processor :

```json
{
 "processors": [
  {
   "processorType": "inboundFactSheet",
   "processorName": "Projects from prj",
   "processorDescription": "Creates LeanIX Projects from external LDIF",
   "type": "Project",
   "filter": {
    "type": "prj|subp"
   },
   "identifier": {
    "external": {
     "id": {
      "expr": "${content.id}"
     },
     "type": {
      "expr": "externalId"
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
       "expr": "${data.displayName} (${content.id})"
      }
     ]
    },
    {
     "key": {
      "expr": "description"
     },
     "values": [
      {
       "expr": "${data.processDescription}"
      }
     ]
    },
    {
     "key": {
      "expr": "lifecycle.active"
     },
     "values": [
      {
       "expr": "${data.startActive}"
      }
     ]
    }
   ],
   "enabled": true,
   "variables": [],
   "logLevel": "warning"
  }
 ],
 "variables": {}
}
```

## Creating a Synchronization Run

To create a synchronization run, make a `POST` request to the
following endpoint and include the processor details in the request body:

```
https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns
```

Example request body:

```json
{
 "connectorType": "importProjectsExample",
 "connectorId": "importProjectsExample",
 "connectorVersion": "1.0.0",
 "lxVersion": "1.0.0",
 "processingDirection": "inbound",
 "description": "Imports Projects from default project connector",
 "content": [
  {
   "type": "prj",
   "id": "0123-459",
   "data": {
    "displayName": "Save the company",
    "processDescription": "Most important project of our 'Herkömmliche AG'",
    "startActive": "2019-12-12",
    "tags": [
     "Importance:High",
     "Some invalid Content to be ignored",
     "Effort:Medium"
    ]
   }
  }
 ]
}
```

In the response, the `id` of the synchronization run
is returned. The `id` is required to start a synchronization
run.

Example response:

```json
{
 "id": "xxxx523c-2c03-4b16-a1f1-xxxxc9dc6e6df"
}
```

## Starting a Synchronization Run

With the `id` of the synchronization run, you can start a
synchronization by making a `POST` request to the following
endpoint:

```
https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns/{id}/start
```

## Canceling a Synchronization Run

To cancel a synchronization run in progress, make a `POST` request to
the following endpoint:

```
https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns/runId/stop
```

## Retrieving the Status of a Synchronization Run

To get the status of the synchronization run that you
initiated, make a `GET` request to the following
endpoint:

```
https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns/{id}/status
```

Example response:

```json
{
 "id": "xxxx523c-2c03-4b16-a1f1-xxxxc9dc6e6df",
 "status": "FINISHED"
}
```

## Retrieving the Details of a Synchronisation Run

With the `id` of a synchronization run, you can get additional details
about it. To do that, use the following endpoints listed in the table.

| Method | Endpoint | Details |
| --- | --- | --- |
| `GET` | `https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns/runId/status` | Get the status of a synchronization run. |
| `GET` | `https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns/runId/results` | Get the results of a synchronization run in LDIF format. The LDIF<br>output includes all Fact Sheet data which is defined in the<br>corresponding processor declared in a workspace. |
| `GET` | `https://{SUBDOMAIN}.leanix.net/services/integration-api/v1/synchronizationRuns/runId/warnings` | Get warning messages for a synchronization run. For example, if<br>an attribute that is included in a processor does not exist in a<br>workspace, this information is returned in a warning<br>message. |

## Importing a Collection to Postman

To make API calls to the Integration REST API in Postman, you can import the
following file into it.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2750bb187a44101499e1f0f84e5627a1_LowRes.png)

```json
{
 "info": {
  "_postman_id": "d5fc07f1-cef1-4b28-b965-97f2c662eb4b",
  "name": "Connect Integration API with Sample Connector",
  "description": "Check documentation for more details :- https://docs-eam.leanix.net/reference/integration-api",
  "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
 },
 "item": [
  {
   "name": "Post LDIF to LeanIX",
   "request": {
    "method": "POST",
    "header": [
     {
      "key": "Content-Type",
      "name": "Content-Type",
      "type": "text",
      "value": "application/json"
     }
    ],
    "body": {
     "mode": "raw",
     "raw": ""
    },
    "url": {
     "raw": "https://{{base_url}}/services/integration-api/v1/synchronizationRuns",
     "protocol": "https",
     "host": [
      "{{base_url}}"
     ],
     "path": [
      "services",
      "integration-api",
      "v1",
      "synchronizationRuns"
     ]
    }
   },
   "response": []
  },
  {
   "name": "Start the Sync",
   "request": {
    "method": "POST",
    "header": [],
    "url": {
     "raw": "https://{{base_url}}/services/integration-api/v1/synchronizationRuns/:id/start",
     "protocol": "https",
     "host": [
      "{{base_url}}"
     ],
     "path": [
      "services",
      "integration-api",
      "v1",
      "synchronizationRuns",
      ":id",
      "start"
     ],
     "variable": [
      {
       "key": "id",
       "value": "e546e34b-cbe5-43f2-9f43-2cbcda4c5405"
      }
     ]
    }
   },
   "response": []
  },
  {
   "name": "Status of Sync",
   "request": {
    "auth": {
     "type": "oauth2",
     "oauth2": [
      {
       "key": "accessToken",
       "value": "",
       "type": "string"
      },
      {
       "key": "tokenType",
       "value": "bearer",
       "type": "string"
      },
      {
       "key": "addTokenTo",
       "value": "header",
       "type": "string"
      }
     ]
    },
    "method": "GET",
    "header": [],
    "url": {
     "raw": "https://{{base_url}}/services/integration-api/v1/synchronizationRuns/:id/status",
     "protocol": "https",
     "host": [
      "{{base_url}}"
     ],
     "path": [
      "services",
      "integration-api",
      "v1",
      "synchronizationRuns",
      ":id",
      "status"
     ],
     "variable": [
      {
       "key": "id",
       "value": "e546e34b-cbe5-43f2-9f43-2cbcda4c5405"
      }
     ]
    }
   },
   "response": []
  },
  {
   "name": "Results of Sync",
   "request": {
    "method": "GET",
    "header": [],
    "url": {
     "raw": "https://{{base_url}}/services/integration-api/v1/synchronizationRuns/:id/results",
     "protocol": "https",
     "host": [
      "{{base_url}}"
     ],
     "path": [
      "services",
      "integration-api",
      "v1",
      "synchronizationRuns",
      ":id",
      "results"
     ],
     "variable": [
      {
       "key": "id",
       "value": "e546e34b-cbe5-43f2-9f43-2cbcda4c5405"
      }
     ]
    }
   },
   "response": []
  },
  {
   "name": "Warnings of Sync",
   "request": {
    "method": "GET",
    "header": [],
    "url": {
     "raw": "https://{{base_url}}/services/integration-api/v1/synchronizationRuns/:id/warnings",
     "protocol": "https",
     "host": [
      "{{base_url}}"
     ],
     "path": [
      "services",
      "integration-api",
      "v1",
      "synchronizationRuns",
      ":id",
      "warnings"
     ],
     "variable": [
      {
       "key": "id",
       "value": "e546e34b-cbe5-43f2-9f43-2cbcda4c5405"
      }
     ]
    }
   },
   "response": []
  }
 ],
 "auth": {
  "type": "oauth2",
  "oauth2": [
   {
    "key": "accessToken",
    "value": "",
    "type": "string"
   },
   {
    "key": "tokenType",
    "value": "bearer",
    "type": "string"
   },
   {
    "key": "addTokenTo",
    "value": "header",
    "type": "string"
   }
  ]
 },
 "event": [
  {
   "listen": "prerequest",
   "script": {
    "id": "ec73502c-9e67-4cf0-85cf-cf8170200181",
    "type": "text/javascript",
    "exec": [
     ""
    ]
   }
  },
  {
   "listen": "test",
   "script": {
    "id": "74a45df7-6d1e-4161-9f91-cf050d515c92",
    "type": "text/javascript",
    "exec": [
     ""
    ]
   }
  }
 ],
 "variable": [
  {
   "id": "99861109-e4a2-4607-9ed3-75857900a6ab",
   "key": "base_url",
   "value": "app.leanix.net",
   "type": "string"
  }
 ],
 "protocolProfileBehavior": {}
}
```

Follow these steps:

1. Import the collection to Postman.

2. Within the Postman UI, edit the collection at the Parent level, updating the
Authorization by clicking Get New Access Token, and providing an API token
from your SAP LeanIX workspace.

3. Updated the raw body of the 'Post LDIF to LeanIX 'step to reflect the
identifiers of the Integration API connector you would like to
test.

4. Send the Post LDIF to LeanIX request, and notice that an id is returned in
the response { "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }

5. Pass this id to Start the Sync, and each subsequent step as a Path Variable,
id. Note: Start the Sync returns no Body, just a status 200 OK.
