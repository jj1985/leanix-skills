<!-- Source: https://help.sap.com/docs/leanix/ea/inbound-processors -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Inbound Processors

## Overview

The integration API reads provided [LDIF](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a99087a441014a04fa6cda4e0ec2b__leanix_data_interchange_format_ldif) and for each data object, it walks over all the configured Data Processors
and checks if the filter configured for each Data Processor matches. In case of a match, the
Processor executes the transformation of data and writes to an SAP LeanIX entity.

For each data object in the content section of the LDIF, inbound Data Processors, depending
on the type of Data Processor, create Fact Sheets, Relations, Subscriptions, Metrics and
Links (Resources tab of Fact Sheets formerly known as Documents). This includes setting and
updating values in fields from certain data keys and values in the data object.

Extended to fully support various sources and keep the connector code simple. SAP LeanIX
provides a powerful mapping component that allows to (partly) map, add and combine
information from multiple metadata elements and/or type or id. Creation of a relation that
depends on certain key value pairs or keys (in case of simple tags), as well as combining
input from different tags is supported. The configuration even allows to set fix values in
certain fields to cover cases where not all data points in the source system have
values.

Each Data Object will potentially be processed by multiple Data Processors (in case filters
of multiple Data Processors match). To prevent data inconsistency in the processing run like
creating a relation to a not yet existing object it is possible to order the execution by
assigning each Data Processor a numeric run key, e.g `run : 0` when creating
a Fact Sheet, `run: 1` when creating a relation to the new Fact Sheet.

**Note**

The processor name should not include any reserved characters which are as operators e.g.
+,\*,>,= …

## Types of Inbound Data Processors

| Inbound Data Processor Type | General | Details |
| --- | --- | --- |
| `inboundFactSheet` | Is used to manage fact sheets (create, update, delete). Example configuration can be found in<br>the Admin UI. | The configuration contains an additional "type" key to define the target Fact<br>Sheet Type to create/update.<br>The configuration needs to provide the name of the Fact Sheet to create and the<br>external ID in case of updating a Fact Sheet.<br>The following field types in Fact Sheet fields can be updated (using the update<br>section): STRING, SINGLE\_SELECT, MULTIPLE\_SELECT, DOUBLE, INTEGER, LOCATION,<br>LIFECYCLE, EXTERNALID, PROJECT,MILESTONE,FACTSHEETSTATE<br>Changing the Data Processor mode to "delete" will mark the Fact Sheet "archived",<br>so behave the same way as if users selected "Delete" from the UI. |
| `inboundRelation` | Is used to manage relations between Fact Sheets (create, update, delete).<br>Example configuration can be found in the Admin UI. | The configuration needs to provide an external or internal ID of the two Fact<br>Sheets that need to be connected.<br>The type of the relation needs to be provided.<br>Fields configured for the relation can be updated. Supported types are the same<br>as for the inboundFactSheet data processor. ActiveFrom and activeUntil can as well<br>be updated. The expected date format is following the ISO 8601 format (e.g.<br>"2019-08-02T09:03:49+00:00"). |
| `inboundSubscription` | Is used to create, update, or delete subscriptions on fact sheets. | The processor adds a new subscription to a fact sheet. This doesn't apply to<br>subscriptions of the Accountable type, for which the processor doesn't replace the<br>current subscription. To add a new subscription of the Accountable type, delete<br>the existing subscription first. You can delete subscriptions in one of the<br>following ways:<br>- Using the Integration API: See [Deletion of Subscriptions](https://help.sap.com/docs/leanix/ea/advanced-use-cases-for-integration-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio27587cd97a4410148028aef3419a720f__deletion_of_subscriptions).<br>  <br>- Using the GraphQL API: See [Delete a Fact Sheet Subscription](https://help.sap.com/docs/leanix/ea/managing-fact-sheet-subscriptions?locale=en-US&state=PRODUCTION&version=CLOUD#loio275af7677a4410148931efc16c6b337e__deleting_a_fact_sheet_subscription).<br>  <br>- In the application UI: Navigate to the Subscriptions<br>  tab on a fact sheet and delete the subscriptions that you need. Variables to be<br>  set in the output section: "user" (mandatory), "subscriptionType" (mandatory),<br>  "subscriptionRoles" (optional, depending on workspace configuration), "comment"<br>  (optional, will be ignored if no role given). |
| `inboundDocument` | Is used to create, update or delete documents linked to Fact Sheets (create,<br>update, delete). The structure is the same as for the inboundFactSheet data<br>processor. Same matching logic for Fact Sheets applies. The found Fact Sheet will<br>not be modified but a linked document changed according to mode (default is<br>"createOrUpdate"). | The updates section must contain a key "name" or the processor will fail. Other<br>potential keys to be set are "description", "url", "origin" to complete the<br>information for a document that is linked to a Fact Sheet. |
| `inboundTag` | Is used to manage Tag Groups (create, update), Tags (create, update, delete)<br>and assignments from Tags to Fact Sheets (create). Example configuration can be<br>found in the Admin UI. | Tags can only be removed completely currently. There is no way to remove tags for given Fact<br>Sheets only. If removal of flags is wanted, a Fact Sheet processor in run 0 needs to<br>be created to delete the tags. In run 1 a processor can then add them back in. If no<br>Tag Group is provided, the processor assumes the default Tag Group ("Other tags").<br>The processor automatically removes all Fast Sheet assignments if a Tag is<br>deleted. |
| `inboundMetrics` | Is used to write a single new point to a configured metrics endpoint. | Metrics can store time series data in SAP LeanIX and<br>become interactive charts to display data. In addition the data can be linked to<br>Fact Sheets, presented to the Dashboard or be displayed within the "Reports"<br>area. |
| `inboundImpact` | Is used to write BPM impacts using integration API. | All standard integration API functionality is available. A processor always<br>writes a single impact. In case a list of input data is given where "forEach" can<br>iterate over, multiple impacts can be written by a single processor. Different types<br>of impacts should be split into different processors in order to keep a<br>configuration readable as different impacts have different parameters. |
| `inboundToDo` | Is used to write To-do using integration API. |  |

## Execution of the Started iAPI Runs

When triggering the start of an iAPI run via API call, the Integration API scheduled the
run to be executed next when an available processing slot becomes available. While the
Integration API service is able to scape on demand, there may be heavy load where the
underlying system needs to be protected to be still available for standard user
operations.

Integration API tries to add as much robustness to the process as possible. Most temporary
outages of underlying infrastructure is covered and in case of issues, iAPI continues at the
last "save point". Save points are generated behind the scenes and ensure, not all work has
to be done again in case of a temporary failure.

When the customer calls a specific iAPI configuration multiple times, the order of
execution is not guaranteed. The second call might be processed first and in case of a
failure, a newer execution might be picked up first before the retry of the older one
starts.

### Configuring the Order of Runs

For cases where the order of execution is important, administrators can add a key/value
pair to the root path of the iAPI configuration to ensure that there is only one run for
the same configuration executed at a time, and in case of failures, the first triggered
run is always picked up first.

While this might be mandatory if an external system sends updates to same information
shortly after each other, it may lead to small updates having to wait for big ones.

In case you want to ensure sequential processing in order of starting time of a run,
please specify the below key value pair in your configuration

Example of using the `sequentialExecution` attribute for a sequential execution of runs:

```json
{
  "processors": [...],
  "sequentialExecution": true
}
```

## General Structure

### Filters

Filter section is where you define if the Data Processor should
work on the found data object.

**Note**

Data Processors provide
filter capabilities to configure on which Data Object the data processor will work on
(match the filter) and what Data Objects to skip (not match the filter)

Types
of filters that can be configured:

| Filter Type | Details |
| --- | --- |
| `exactType` ( `type`) | The `exactType` and<br>`type` filters work<br>differently when comparing strings with the `type` field of a data<br>object.<br>The `exactType` filter<br>requires an exact match between the string and the `type` field. This means the<br>entire string must match the `type` field for the filter to be applied. We recommend using this<br>filter type to ensure accurate matching.<br>The `type` filter<br>performs a comparison based on the first characters of the string, following the<br>logic of a regular expression. This means the filter is applied if the initial<br>characters of the string match the `type` field of the data<br>object, without considering the remaining characters. |
| `id` | If configured, the string is interpreted as a regular expression and matched<br>against the "id" field of the Data Object |
| `advanced` | If configured, the field contains a JUEL expression that may evaluate to "true"<br>for a match or "false". This filter allows to filter even for combinations of<br>certain key and values in the Data Object |
| `onRead` | Behaves like the advanced filter but uses results of eventually configured read<br>sections to filter based on existence of a Fact Sheet or based on specific values on<br>an existing Fact Sheet. You can find an example of how to use this filter in [Advanced Use Cases for the Integration API](https://help.sap.com/docs/leanix/ea/advanced-use-cases-for-integration-api?locale=en-US&state=PRODUCTION&version=CLOUD "Explore advanced scenarios and examples for the Integration API."). |
| `writeToLdif` | Using this processor, Administrators can configure an inbound Integration API<br>run to write a new LDIF file. The resulting LDIF will be available using the<br>/results and the /resultsUrl endpoints same as with outbound Integration API<br>runs |
| `updatedInDuration` | Used to filter on items that have changed recently. Integration API can target<br>Fact Sheets that have been changed recently. Only Fact Sheets that pass this<br>criteria will be processed. The feature is most helpful to generate proper output<br>with the "writeToLdif" processor that only contains e.g. Fact Sheets changed since<br>last export. It is used the following way: "updatedInDuration": "P3D". You can find<br>an example in [Outbound<br>Processors](https://help.sap.com/docs/leanix/ea/outbound-processors?locale=en-US&state=PRODUCTION&version=CLOUD). |

**Note**

All configured filters need to match in order to start the Data Processor on the Data
Object (AND logic).

Example of combining multiple filters:

```json
{
  "filters": {
    "exactType": "ITComponent",
    "updatedInDuration": "P3D"
  }
}
```

### Identifier Section

Identifier section defines the pathfinder entity in scope of the
processor. Depending on the processor it can be called "identifier" (all processors with one
Fact Sheet in scope) or "from" and "to" for the inboundRelation
processor.

Identification of the target Fact Sheet happens by defining the internal
ID, the external ID or a "search scope".

Only one field must be filled as a value of
key "identifier":

- `internalId`: JUEL expression,
replace RegEx

Example of identification by an internal ID:

```json
{
  "identifier": {
    "internal": "${content.id}"
  }
}
```

- `externalId`: JUEL expression,
replace RegEx (id/name of Fact Sheet or other entity)

Example of Identification by an external ID:

```json
{
  "identifier": {
    "external": {
      "id": {
        "expr": "${content.id}"
      },
      "type": {
        "expr": "externalId"
      }
    }
  }
}
```

Using the external key, it is possible to create an object in case it is
not found. This happens transparently without any need to distinguish between create or
update when configuring the processor.

When using the "search" based identification of
the Fact Sheet that are supposed to be updated by the incoming data object, then the section
may contain a section to limit the scope of searched Fact Sheets and an expression filtering
the Fact Sheets that should be updated. Details can be found on the "Advanced" page of this
documentation.

The below processor will update all descriptions of Application Fact
Sheets that have a tag "AsiaPacific" in the tag group "Region". The full example can be
found on the "Advanced" page.

Example processor for identifying Fact Sheets using search and updating them with incoming data:

```json
{
  "processors": [
    {
      "processorType": "inboundFactSheet",
      "processorName": "Update all Cloud Apps",
      "processorDescription": "Updates all Apps with tag 'Cloud'",
      "type": "Application",
      "filter": {
        "exactType": "AppUpdate"
      },
      "identifier": {
        "search": {
          "scope": {
            "facetFilters": [
              {
                "facetKey": "FactSheetTypes",
                "operator": "OR",
                "keys": [
                  "Application"
                ]
              },
              {
                "facetKey": "${integration.tags.getTagGroupId('Region')}",
                "operator": "OR",
                "keys": [
                  "${integration.tags.getTagId('Region','AsiaPacific')}"
                ]
              }
            ],
            "ids": []
          },
          "filter": "${true}",
          "multipleMatchesAllowed": true
        }
      },
      "logLevel": "debug",
      "updates": [
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "External sync executed ${data.dateTime}"
            }
          ]
        }
      ]
    }
  ]
}
```

### Update Section

The Update Section provides the ability to write to fields or further
metadata to the targeted entity (depending on the processor).

Multiple values can be
written. Each value consists of a JUEL and a RegEx for building the name of the target key
to be written and a list of potential values to be written.

Some keys might be
mandatory depending on the processor (see the processor description for details).

The
following field types in Fact Sheet fields can be updated (using the update
section):

| Attribute | Description |
| --- | --- |
| STRING | Is a basic text field with no functionality. This field has no configurable<br>formatting like displaying clickable links or bold formatting |
| SINGLE\_SELECT | Allows for the selection of one value from a dropdown list. This list of values<br>can be changed at any point in time without data loss. This attribute can be<br>filtered in the inventory and used as a view in the reports |
| MULTIPLE\_SELECT | Allows for the selection of multiple values from a predefined list. Once<br>defined this list cannot be changed again without incurring data loss |
| DOUBLE | There is no explicit currency field in SAP LeanIX, but<br>this type can display a currency icon |
| INTEGER | Represents a numeric value without decimal places |
| LOCATION | Will be sent to the location service to resolve a valid location from the given<br>input string. Setting the location will fail if the given data is not specific and<br>results in multiple possible locations. In case a "#" is found as the first one, the<br>API will pick the first result returned by the location service and use this. This<br>is helpful if comma separated coordinates are being provided |
| LIFECYCLE | Content needs to follow the date format specifications "yyyy-mm-dd". Each field<br>in the life cycle can be addressed with "."-syntax like e.g.<br>lifecycle.active |
| EXTERNALID | External Ids can only be written if they are not marked readonly in the data<br>model. The following fields can be written using "."-syntax: externalId.externalId,<br>externalId.externalUrl, externalId.comment, externalId.status,<br>externalId.externalVersion. The "externalId" left of the "." may be changed with the<br>name of the external id field. |
| PROJECT | Project status values will always written as a full set that replaces the currently set<br>project status values. In order to add to existing values, you need to add the<br>field to the read section. This returns an object you would then iterate over<br>using inner forEach (see advanced section for usage). While iterating a filter<br>could be applied to not write back all found status values but selected only. In<br>addition by defining more values new values can be added in the same step. The<br>structure of the required map can be copied from a read result (e.g. output to a<br>description field for testing): <br><br>```json<br>{<br>  "updates": [<br>    {<br>      "key": {<br>        "expr": "projectStatus"<br>      },<br>      "values": [<br>        {<br>          "map": [<br>            {<br>              "key": "id",<br>              "value": "myId"<br>            },<br>            {<br>              "key": "date",<br>              "value": "2020-07-25"<br>            },<br>            {<br>              "key": "status",<br>              "value": "green"<br>            },<br>            {<br>              "key": "progress",<br>              "value": "20"<br>            }<br>          ]<br>        }<br>      ]<br>    }<br>  ]<br>}<br>```<br><br> |
| FACTSHEETSTATE | Integration API reads and writes the content of a FactSheetState field as a<br>String, which makes it easy to handle. Please be aware to only send allowed values<br>into a state field. |
| MILESTONE | Milestones can be written following the same logic as "project" data is written by the<br>Integration API. All content will just replace the current content by default.<br>iAPI takes care to ensure the final state in Pathfinder reflects what was sent in<br>the processor. There is no need to decide if items need to be deleted or modified<br>or added new. The data sent by iAPI will always reflect the full state after<br>writing. This allows to process without knowledge of the current state and does<br>not interfere with potential other operations happening in parallel.<br><br>```json<br>{<br>  "key": {<br>    "expr": "lxMilestones"<br>  },<br>  "values": [<br>    {<br>      "forEach": {<br>        "elementOf": "${data.milestones}",<br>        "filter": "${true}"<br>      },<br>      "map": [<br>        {<br>          "key": "name",<br>          "value": "${integration.output.valueOfForEach.n}"<br>        },<br>        {<br>          "key": "date",<br>          "value": "${integration.output.valueOfForEach.d}"<br>        },<br>        {<br>          "key": "description",<br>          "value": "${integration.output.valueOfForEach.type}"<br>        }<br>      ]<br>    }<br>  ]<br>}<br>```<br><br> |

Example `updates` section for an inbound
data processor:

```json
{
  "updates": [
    {
      "key": {
        "expr": "name",
        "regexReplace": {
          "match": "",
          "replace": ""
        }
      },
      "values": [
        {
          "expr": "${data.app}"
        }
      ]
    },
    {
      "key": {
        "expr": "description"
      },
      "values": [
        {
          "expr": "${header.processingMode}",
          "regexMatch": "abc"
        },
        {
          "expr": "${header.processingMode}_2"
        }
      ],
      "optional": true
    }
  ]
}
```

### Modes

Changing the Data Processor mode to "delete" will mark the Fact
Sheet "archived", so behave the same way as if users selected "Delete" from the
UI.

Delete mode:

```json
{
  "mode": "delete"
}
```

Example connector and input data using the delete mode:

```json
{
  "processors": [
    {
      "processorType": "inboundFactSheet",
      "processorName": "Delete Data sent in the Input",
      "processorDescription": "",
      "type": "Application",
      "filter": {
        "exactType": "Deployment"
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
      "updates": [],
      "mode": "delete"
    }
  ],
  "variables": {}
}
```

Example input:

```json
{
  "connectorType": "example",
  "connectorId": "deleteMode",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "description": "Delete Data using mode",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {},
  "content": [
    {
      "type": "Deployment",
      "id": "634c16bf-198c-1129-9d08-92630b573fbf",
      "data": {
        "app": "HR Service",
        "version": "1.8.4",
        "maturity": "3",
        "clusterName": "westeurope",
        "tags": []
      }
    }
  ]
}
```

In case a Fact Sheet is updated with a standard mode that has been set to
"archived", there are two potential behaviors:

- In case the Fact Sheet was matched using the external ID, then a new Fact Sheet will be
created

- In case the reference was done by using the internal ID, then the old Fact Sheet will be
used and set back to "active"

## Inbound Fact Sheet

Example `inboundFactSheet`
processor:

```json
{
  "processors": [
    {
      "processorType": "inboundFactSheet",
      "processorName": "Create IT Components",
      "processorDescription": "One Processor for IT Components",
      "enabled": true,
      "type": "ITComponent",
      "identifier": {
        "external": {
          "id": {
            "expr": "${content.id.replaceAll('/','_')}"
          },
          "type": {
            "expr": "externalId"
          }
        }
      },
      "filter": {
        "exactType": "ITComponent"
      },
      "updates": [
        {
          "key": {
            "expr": "name"
          },
          "values": [
            {
              "expr": "${data.name}"
            }
          ]
        },
        {
          "key": {
            "expr": "cloudProvider"
          },
          "values": [
            {
              "expr": "${data.provider}"
            }
          ]
        },
        {
          "key": {
            "expr": "category"
          },
          "values": [
            {
              "expr": "${data.category}",
              "regexMatch": "(cloud_service)",
              "regexReplace": {
                "match": "^.*$",
                "replace": "cloudService"
              }
            },
            {
              "expr": "${data.category}",
              "regexMatch": "(sample_software)",
              "regexReplace": {
                "match": "^.*$",
                "replace": "software"
              }
            }
          ]
        }
      ],
      "vars": []
    }
  ]
}
```

## Lifecycle Management

Writing to fields of type lifecycle needs to be split
into different write operations (lines in the data processor. The value of the "key" field
has to use the "." syntax. E.g. "lifecycle.plan", "lifecycle.phaseIn". Other default values
are "phaseOut" and "endOfLife".

Example `inboundFactSheet` processor
with life cycle data:

```json
{
 "processorType": "inboundFactSheet",
 "processorName": "Lifecycle Example",
 "processorDescription": "Creates an Application with lifecycle information",
 "type": "Application",
 "filter": {
  "exactType": "Application"
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
     "expr": "${data.name}"
    }
   ]
  },
  {
   "key": {
    "expr": "description"
   },
   "values": [
    {
     "expr": "${data.name} is an application that carries lifecycle information"
    }
   ]
  },
  {
   "key": {
    "expr": "lifecycle.plan"
   },
   "values": [
    {
     "expr": "${data.plan == null ? '2014-01-01' : data.plan}"
    }
   ]
  },
  {
   "key": {
    "expr": "lifecycle.phaseIn"
   },
   "values": [
    {
     "expr": "${data.phaseIn}"
    }
   ]
  },
  {
   "key": {
    "expr": "lifecycle.active"
   },
   "values": [
    {
     "expr": "${data.active}"
    }
   ]
  },
  {
   "key": {
    "expr": "lifecycle.phaseOut"
   },
   "values": [
    {
     "expr": "${data.phaseOut}"
    }
   ]
  },
  {
   "key": {
    "expr": "lifecycle.endOfLife"
   },
   "values": [
    {
     "expr": "${data.endOfLife}"
    }
   ]
  }
 ]
}
```

## Location Management

Writing to fields of type "location" will require a single string as input. The string will
be sent to the location service (open street map). In case a single result was returned, the
location will be written to the field with all meta data returned by "open street map".
Providing latitudes and longitude works by simply passing the coordinates in that order,
separated by comma: "50.11, 8.682".

In case of no or multiple locations returned, the field will not be populated and an error
shown in the log for this field. Other updates by the data processor may still be valid and
pass.

**Note**

When writing locations, the used open street map service may return multiple results.
Default behaviour is to not set any location. In case the value provided to the Location
starts with a # character, the first result from open street map will be used (same logic
as we see when providing coordinates)

## Inbound Subscription

Variables to be set in the output section:

| Variable | Required | Notes |
| --- | --- | --- |
| `user` | Required | Users' email (either user or newUser" needs to be present. |
| `newUser` | Required | Works like "user" but creates a new user if not existing |
| `subscriptionType` | Required |  |
| `subscriptionRoles` | Optional | It may or may not be required because it is based on the specific configuration<br>set in each workspace |
| `addSubscriptionRoles` | Optional | Same as "subscriptionRoles" but adds to existing roles instead of completely<br>replacing all existing roles |
| `optional` | Optional | Boolean(Disables warnings related to new user creation in case<br>inboundSubscription only works for existing users) |
| `comment` | Optional |  |

Example `inboundSubscription`
processor:

```json
{
  "processorType": "inboundSubscription",
  "processorName": "Subscription creation",
  "processorDescription": "Creates subscriptions",
  "filter": {
    "exactType": "ITComponent"
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
  "updates": [
    {
      "key": {
        "expr": "user"
      },
      "values": [
        {
          "expr": "jane.doe@leanix.net"
        }
      ]
    },
    {
      "key": {
        "expr": "subscriptionType"
      },
      "values": [
        {
          "expr": "RESPONSIBLE"
        }
      ]
    },
    {
      "key": {
        "expr": "subscriptionRoles"
      },
      "values": [
        {
          "map": [
            {
              "key": "roleName",
              "value": "Business Owner"
            },
            {
              "key": "comment",
              "value": "This person is the business owner"
            }
          ]
        }
      ]
    },
    {
      "key": {
        "expr": "newUser.userName"
      },
      "values": [
        {
          "expr": "jane.doe@leanix.net"
        }
      ]
    },
    {
      "key": {
        "expr": "newUser.email"
      },
      "values": [
        {
          "expr": "jane.doe@leanix.net"
        }
      ]
    },
    {
      "key": {
        "expr": "newUser.firstName"
      },
      "values": [
        {
          "expr": "Jane"
        }
      ]
    },
    {
      "key": {
        "expr": "newUser.lastName"
      },
      "values": [
        {
          "expr": "Doe"
        }
      ]
    }
  ]
}
```

## Inbound Relation

The "inboundRelation" processor requires identification of two Fact Sheets. In this
processor the "identifier" is replaced by two fields named "from" and "to". The potential
values of the "from" and the "to" fields are identical with the "identifier" values and can
handle internal and external ids as well.

Allowed values: JUEL expression plus
optional replace RegEx map (available for each expression, for internal external and from
and to in case of the inboundRelation processor).

Example RegEx in ID mapping:

```json
{
  "identifier": {
    "external": {
      "id": {
        "expr": "${content.id}",
        "regexReplace": {
          "match": "",
          "replace": ""
        }
      },
      "type": {
        "expr": "externalId"
      }
    }
  }
}
```

Please replace the type "relApplicationToITComponent" with the name of the
relation that needs to be created or updated (e.g. "relToParent").

Example `inboundRelation` processor:

```json
{
  "processors": [
    {
      "processorType": "inboundRelation",
      "processorName": "Rel from Apps to ITComponent",
      "processorDescription": "Creates LeanIX Relations between the created or updated Applications and ITComponents",
      "type": "relApplicationToITComponent",
      "filter": {
        "exactType": "Deployment"
      },
      "from": {
        "external": {
          "id": {
            "expr": "${content.id}"
          },
          "type": {
            "expr": "externalId"
          }
        }
      },
      "to": {
        "external": {
          "id": {
            "expr": "${data.clusterName}"
          },
          "type": {
            "expr": "externalId"
          }
        }
      },
      "run": 1,
      "updates": [
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "Relationship Description"
            }
          ]
        },
        {
          "key": {
            "expr": "activeFrom"
          },
          "values": [
            {
              "expr": "2019-08-02T09:03:49+00:00"
            }
          ]
        },
        {
          "key": {
            "expr": "activeUntil"
          },
          "values": [
            {
              "expr": "2020-08-02T09:03:49+00:00"
            }
          ]
        }
      ],
      "logLevel": "debug"
    }
  ]
}
```

**Note**

Referencing "from" and "to" fact sheets for relations by internal IDs.

The
inboundRelation processor as well supports referencing source and target Fact Sheets by
their internal id as well. The syntax is the same we see for the identifier for
inboundFactsheet processor: "internal": "${content.id}"

**Note**

To create a Fact Sheet using the inboundFactsheet processor, providing an externalId is
mandatory.

## Inbound Relations Constraints

The relation processor allows to set constraining relations as well. In order to do so, a
target key "constrainingRelations" needs to be defined (in the output section similar to the
example target key "description in the example above"). All values of the resulting values
list will be written as constraints. Existing ones will be removed. Alternatively the key
"addConstrainingRelations" may be used to add constraints to existing ones.

Example configuration to read information of constraining relations from an LDIF input:

```json
{
  "key": {
    "expr": "constrainingRelations"
  },
  "values": [
    {
      "forEach": {
        "elementOf": "${integration.valueOfForEach.rels.constrainingRelations.relations}"
      },
      "map": [
        {
          "key": "type",
          "value": "${integration.output.valueOfForEach.type}"
        },
        {
          "key": "targetExternalIdType",
          "value": "externalId"
        },
        {
          "key": "targetExternalIdValue",
          "value": "${integration.output.valueOfForEach.target.externalId}"
        }
      ]
    }
  ]
}
```

Example configuration to generate an LDIF output with information about constraining relations:

```json
{
  "scope": {
    "ids": [
      "7750c7ba-5d24-4849-a1b4-564bc6c874a0"
    ],
    "facetFilters": [
      {
        "keys": [
          "Application"
        ],
        "facetKey": "FactSheetTypes",
        "operator": "OR"
      }
    ]
  },
  "processors": [
    {
      "processorType": "outboundFactSheet",
      "processorName": "Export to LDIF",
      "processorDescription": "This is an example how to use the outboundFactSheet processor",
      "enabled": true,
      "fields": [
        "lifecycle",
        "name",
        "location",
        "createdAt",
        "technicalSuitabilityDescription",
        "description"
      ],
      "relations": {
        "filter": [
          "relApplicationToProcess"
        ],
        "fields": [
          "description"
        ],
        "targetFields": [
          "displayName",
          "externalId"
        ],
        "constrainingRelations": true
      },
      "output": [
        {
          "key": {
            "expr": "content.id"
          },
          "mode": "selectFirst",
          "values": [
            {
              "expr": "${lx.factsheet.id}"
            }
          ]
        },
        {
          "key": {
            "expr": "content.type"
          },
          "mode": "selectFirst",
          "values": [
            {
              "expr": "${lx.factsheet.type}"
            }
          ]
        },
        {
          "key": {
            "expr": "Name"
          },
          "values": [
            {
              "expr": "${lx.factsheet.name}"
            }
          ],
          "optional": true
        },
        {
          "key": {
            "expr": "relations"
          },
          "mode": "list",
          "values": [
            {
              "forEach": {
                "elementOf": "${lx.relations}",
                "filter": "${true}"
              },
              "map": [
                {
                  "key": "relationName",
                  "value": "${integration.output.valueOfForEach.type}"
                },
                {
                  "key": "object",
                  "value": "${integration.output.valueOfForEach}"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Inbound Metrics

The `inboundMetrics` processor is used to write a single new point to a
configured metrics endpoint.

The `update` section of the processor must
contain the following keys with values:

| Required Attribute | Description |
| --- | --- |
| `measurement` | Name of the configured metrics measurement a points needs to be added<br>to |
| `time` | The date and time of the point in ISO formatting (e.g.<br>2019-09-09T08:00:00.000000Z) |
| `fieldKey` | Name of the field to store the point value in |
| `fieldValueNumber` | The value you want to store for that field and point of time |
| `tagKey` | Name of the tag |
| `tagValue` | Value of the tag. You may want to write the internal ID of a specific Fact<br>Sheet here to allow assignment of the data to a specific Fact Sheet as a rule in the<br>created chart for the measurement (go to admin/metrics to configure) |

The output section of the inboundMetrics data processor should be configured the
same as other inbound processors. The keys will be written to the corresponding
variables.

Example `inboundMetrics` processor:

```json
{
  "processorType": "inboundMetrics",
  "processorName": "Metrics data for measurement",
  "processorDescription": "Metrics processor configuration",
  "filter": {
    "exactType": "Metrics",
    "advanced": "${data.measurement.equals('measurement')}"
  },
  "run": 1,
  "updates": [
    {
      "key": {
        "expr": "measurement"
      },
      "values": [
        {
          "expr": "${data.measurement}"
        }
      ]
    },
    {
      "key": {
        "expr": "time"
      },
      "values": [
        {
          "expr": "${data.time}"
        }
      ]
    },
    {
      "key": {
        "expr": "fieldKey"
      },
      "values": [
        {
          "expr": "${data.fieldKey}"
        }
      ]
    },
    {
      "key": {
        "expr": "fieldValueNumber"
      },
      "values": [
        {
          "expr": "${data.fieldValueNumber}"
        }
      ]
    },
    {
      "key": {
        "expr": "tagKey"
      },
      "values": [
        {
          "expr": "${data.tagKey}"
        }
      ]
    },
    {
      "key": {
        "expr": "tagValue"
      },
      "values": [
        {
          "expr": "${data.tagValue}"
        }
      ]
    },
    {
      "key": {
        "expr": "tags"
      },
      "values": [
        {
          "map": [
            {
              "key": "key",
              "value": "${data.tagKey}_1"
            },
            {
              "key": "value",
              "value": "${data.tagValue}_1"
            }
          ]
        },
        {
          "map": [
            {
              "key": "key",
              "value": "${data.tagKey}_2"
            },
            {
              "key": "value",
              "value": "${data.tagValue}_2"
            }
          ]
        }
      ]
    }
  ],
  "logLevel": "debug"
}
```

## Inbound Document

The `inboundDocument` processor is used to create, update, or delete
documents linked to Fact Sheets.

The structure is the same as for the
`inboundFactSheet` data processor. Same matching logic for Fact Sheets
applies. The found Fact Sheet will not be modified but a linked document changed according
to mode (default is "createOrUpdate")

| Keys Specific to the `inboundDocument` Processor | Details |
| --- | --- |
| `description` | Description of the document |
| `origin` | From what department or person does this originate from |
| `url` | Link to the document |
| `documentType` | A string containing information how to display the link on the Resource tab. Values are<br>dynamic. It is suggested to first read the links for an item, then copy the values<br>for writing similar links. Some examples of the value but this can change based on<br>your specific configuration: `policy, decision, jira, documentation, website,<br>support_ticket, faq, additional_help, task, roadmap` |
| `metadata` | A string containing information how to display the link on the Resource tab.<br>Values are dynamic. It is suggested to first read the links for an item, then copy<br>the values for writing similar links |

**Caution**

The `updates` section must contain the key
`name`, otherwise the run will fail.

Example `inboundDocument` processor:

```json
{
  "processorType": "inboundDocument",
  "processorName": "My link to Integration API docs",
  "processorDescription": "Contains the link that will point to the documentation for the Integration API",
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
  "filter": {
    "exactType": "ITComponent"
  },
  "run": 1,
  "updates": [
    {
      "key": {
        "expr": "name"
      },
      "values": [
        {
          "expr": "Integration API Document"
        }
      ]
    },
    {
      "key": {
        "expr": "documentType"
      },
      "values": [
        {
          "expr": "website"
        }
      ]
    },
    {
      "key": {
        "expr": "origin"
      },
      "values": [
        {
          "expr": "CUSTOM_LINK"
        }
      ]
    },
    {
      "key": {
        "expr": "url"
      },
      "values": [
        {
          "expr": "https://docs-eam.leanix.net/reference/integration-api"
        }
      ]
    }
  ]
}
```

## Inbound Tag

### Tag Sent as an Array

In the below example if you just specify the name of the tag without
other attributes the Tag by the name specified will be created under "Other Tags" and
attached to the Fact Sheet.

Example `inboundTag` processor:

```json
{
  "processorType": "inboundTag",
  "processorName": "Tag creation",
  "processorDescription": "Creates tags and tag groups",
  "factSheets": {
    "external": {
      "ids": "${content.id}",
      "type": {
        "expr": "externalId"
      }
    }
  },
  "run": 1,
  "updates": [
    {
      "key": {
        "expr": "name"
      },
      "values": [
        {
          "expr": "${integration.valueOfForEach}"
        }
      ]
    },
    {
      "key": {
        "expr": "description"
      },
      "values": [
        {
          "expr": "${integration.valueOfForEach}"
        }
      ]
    },
    {
      "key": {
        "expr": "color"
      },
      "values": [
        {
          "expr": "#123456"
        }
      ]
    },
    {
      "key": {
        "expr": "group.name"
      },
      "values": [
        {
          "expr": "Kubernetes Tags"
        }
      ]
    },
    {
      "key": {
        "expr": "group.shortName"
      },
      "values": [
        {
          "expr": "k8s"
        }
      ]
    },
    {
      "key": {
        "expr": "group.description"
      },
      "values": [
        {
          "expr": "Tags relevant for Kubernetes"
        }
      ]
    },
    {
      "key": {
        "expr": "group.mode"
      },
      "values": [
        {
          "expr": "MULTIPLE"
        }
      ]
    },
    {
      "key": {
        "expr": "group.restrictToFactSheetTypes"
      },
      "values": [
        {
          "expr": "Application"
        },
        {
          "expr": "ITComponent"
        }
      ]
    }
  ],
  "forEach": "${data.tags}",
  "logLevel": "debug"
}
```

Example input in LDIF format for importing tags:

```json
{
  "connectorType": "ee",
  "connectorId": "Kub Dev-001",
  "connectorVersion": "1.2.0",
  "lxVersion": "1.0.0",
  "description": "Imports kubernetes data into LeanIX",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {},
  "content": [
    {
      "type": "Deployment",
      "id": "784616bf-198c-11f9-9da8-9263b0573fbe",
      "data": {
        "app": "Finance Service",
        "version": "10.5",
        "maturity": "5",
        "clusterName": "westeurope",
        "tags": [
          "Important"
        ]
      }
    }
  ]
}
```

Example input in LDIF format for importing tag groups and tags:

```json
{
  "connectorType": "Report Technology Radar",
  "connectorId": "Technology Radar Tags",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {},
  "content": [
    {
      "type": "Deployment",
      "id": "1",
      "data": {
        "taggroups": [
          {
            "name": "Technology radar - Quadrant",
            "shortname": "TRQ",
            "description": "Beschreibung Quadrant",
            "mode": "SINGLE",
            "factsheettype": "ITComponent"
          },
          {
            "name": "Technology radar - Ring",
            "shortname": "TRR",
            "description": "Beschreibung Ring",
            "mode": "SINGLE",
            "factsheettype": "ITComponent"
          }
        ],
        "tags": [
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Architecture Concepts",
            "description": "Beschreibung Architecture Concepts",
            "color": "#ff0000"
          },
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Platforms",
            "description": "Beschreibung Platforms",
            "color": "#00ff00"
          },
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Techniques",
            "description": "Beschreibung Techniques",
            "color": "#0000ff"
          },
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Tools & Infrastructure",
            "description": "Beschreibung Tools & Infrastructure",
            "color": "#000000"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Hold",
            "description": "Beschreibung Hold",
            "color": "#ff0000"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Incubating",
            "description": "Beschreibung Incubating",
            "color": "#00ff00"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Emerging",
            "description": "Beschreibung Emerging",
            "color": "#0000ff"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Mature",
            "description": "Beschreibung Mature",
            "color": "#000000"
          }
        ]
      }
    }
  ]
}
```

### Tag Groups

Processor and sample LDIF for Tag Groups and Tags.

Example `inboundTag` processor for tag
groups and tags:

```json
{
  "processors": [
    {
      "processorType": "inboundTag",
      "processorName": "Tag group creation",
      "processorDescription": "Creates tag groups",
      "run": 0,
      "forEach": "${data.taggroups}",
      "updates": [
        {
          "key": {
            "expr": "group.name"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.name}"
            }
          ]
        },
        {
          "key": {
            "expr": "group.shortName"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.shortname}"
            }
          ]
        },
        {
          "key": {
            "expr": "group.description"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.description}"
            }
          ]
        },
        {
          "key": {
            "expr": "group.mode"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.mode}"
            }
          ]
        },
        {
          "key": {
            "expr": "group.restrictToFactSheetTypes"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.factsheettype}"
            }
          ]
        }
      ],
      "logLevel": "warning",
      "enabled": true
    },
    {
      "processorType": "inboundTag",
      "processorName": "Tag creation",
      "processorDescription": "Creates tags",
      "run": 1,
      "forEach": "${data.tags}",
      "updates": [
        {
          "key": {
            "expr": "group.name"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.groupname}"
            }
          ]
        },
        {
          "key": {
            "expr": "name"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.name}"
            }
          ]
        },
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.description}"
            }
          ]
        },
        {
          "key": {
            "expr": "color"
          },
          "values": [
            {
              "expr": "${integration.valueOfForEach.color}"
            }
          ]
        }
      ],
      "logLevel": "warning",
      "enabled": true
    }
  ]
}
```

Example input in LDIF format for tag groups and tags:

```json
{
  "connectorType": "Report Technology Radar",
  "connectorId": "Technology Radar Tags",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {},
  "content": [
    {
      "type": "Deployment",
      "id": "1",
      "data": {
        "taggroups": [
          {
            "name": "Technology radar - Quadrant",
            "shortname": "TRQ",
            "description": "Beschreibung Quadrant",
            "mode": "SINGLE",
            "factsheettype": "ITComponent"
          },
          {
            "name": "Technology radar - Ring",
            "shortname": "TRR",
            "description": "Beschreibung Ring",
            "mode": "SINGLE",
            "factsheettype": "ITComponent"
          }
        ],
        "tags": [
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Architecture Concepts",
            "description": "Beschreibung Architecture Concepts",
            "color": "#ff0000"
          },
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Platforms",
            "description": "Beschreibung Platforms",
            "color": "#00ff00"
          },
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Techniques",
            "description": "Beschreibung Techniques",
            "color": "#0000ff"
          },
          {
            "groupname": "Technology radar - Quadrant",
            "name": "Tools & Infrastructure",
            "description": "Beschreibung Tools & Infrastructure",
            "color": "#000000"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Hold",
            "description": "Beschreibung Hold",
            "color": "#ff0000"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Incubating",
            "description": "Beschreibung Incubating",
            "color": "#00ff00"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Emerging",
            "description": "Beschreibung Emerging",
            "color": "#0000ff"
          },
          {
            "groupname": "Technology radar - Ring",
            "name": "Mature",
            "description": "Beschreibung Mature",
            "color": "#000000"
          }
        ]
      }
    }
  ]
}
```

### Tag Sent as a Comma-Separated List

Data in the tags looks like
"Important,Mature". Helper function(toList) below will convert the comma-separated string to
an Array and the Output of the below processor will be "Other Tags" : Important and Mature
attached to Deployment "Finance Service".

Example `inboundTag` processor:

```json
{
  "processorType": "inboundTag",
  "processorName": "Tag creation",
  "processorDescription": "Creates tags and tag groups",
  "factSheets": {
    "external": {
      "ids": "${content.id}",
      "type": {
        "expr": "externalId"
      }
    }
  },
  "run": 1,
  "updates": [
    {
      "key": {
        "expr": "name"
      },
      "values": [
        {
          "expr": "${integration.valueOfForEach.trim()}"
        }
      ]
    }
  ],
  "forEach": "${helper:toList(data.tags.split(','))}",
  "logLevel": "debug"
}
```

Example LDIF input for tags:

```json
{
  "connectorType": "ee",
  "connectorId": "Kub Dev-001",
  "connectorVersion": "1.2.0",
  "lxVersion": "1.0.0",
  "description": "Imports kubernetes data into LeanIX",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {},
  "content": [
    {
      "type": "Deployment",
      "id": "784616bf-198c-11f9-9da8-9263b0573fbe",
      "data": {
        "app": "Finance Service",
        "version": "10.5",
        "maturity": "5",
        "clusterName": "westeurope",
        "tags": "Important,Mature"
      }
    }
  ]
}
```

The inboundTag processor does automatically creates tags that do not exist
for a tag group (the tag processor does not create new tag groups).

The inbound
tagProcessor can be configured to not create any tags nor change metadata of existing tags
but only to assign Fact Sheets to existing tags. To use this functionality, an additional
key "tagsReadOnly" needs to be configured in the updates section as shown in the
example:

Example of enabling the "read only" mode for the `inboundTag` processor:

```json
{
  "updates": [
    {
      "key": {
        "expr": "tagsReadOnly"
      },
      "values": [
        {
          "expr": "${true}"
        }
      ]
    },
    {
      "key": {
        "expr": "name"
      },
      "values": [
        {
          "expr": "${data.myTagName}"
        }
      ]
    }
  ]
}
```

**Note**

The "optional" flag avoids warning messages if the
input data may not contain values for all fields and this is expected.

**Note**

Is used to only write values to internal
variables. This will be used for aggregation use cases where the LDIF content needs to be
used to only collect values without directly writing anything to SAP LeanIX.

## Write to LDIF

The processor allows Administrators to configure an inbound Integration API run to write a
new LDIF file. The resulting LDIF will be available using the /results and the /resultsUrl
endpoints same as with outbound Integration API runs.

With this functionality, inbound
runs can be used in all combinations to read, process, update Pathfinder entities and even
write a new LDIF in one step. Integrations that write to SAP LeanIX and read data
from SAP LeanIX can be
written and managed in one Integration API configuration executed with a single call.

The new processor can even be used to only export data or just transform an LDIF into
another LDIF.

In a configuration, all defined processors will write to a single,
globally defined LDIF. This allows to collect all kinds of data objects to the target LDIF
from multiple processors including content from aggregations and other processing (e.g.
variables).

The LDIF header definition needs to be set as a global key in the
Integration API congifuration. All fields can be freely configured and will be evaluated to
a String using JUEL. Exception is the "customFields" key. If defined, the value will be
interpreted as an object and passed to the target LDIF. Please ensure the expression always
results in a map object to not break the LDIF format.

Example `writeToLdif` processor:

```json
{
  "processors": [
    {
      "processorType": "writeToLdif",
      "updates": [
        {
          "key": {
            "expr": "content.id"
          },
          "values": [
            {
              "expr": "${content.id}"
            }
          ]
        },
        {
          "key": {
            "expr": "content.type"
          },
          "values": [
            {
              "expr": "${content.type}"
            }
          ]
        },
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "Just a test. Could be any read content or JUEL calculation"
            }
          ]
        }
      ]
    }
  ],
  "targetLdif": {
    "dataConsumer": {
      "type": "leanixStorage"
    },
    "ldifKeys": [
      {
        "key": "connectorType",
        "value": "myNewLdif"
      },
      {
        "key": "connectorId",
        "value": "mycreatedId"
      },
      {
        "key": "customFields",
        "value": "${integration.toObject('{\"anyKey\":\"anyValue\"}')}"
      }
    ]
  }
}
```

A more advanced example shows how to read content from Pathfinder and write
it to an LDIF using the processor. It requires an input LDIF with at lease one data object
but content is not relevant. The data object is only used to
trigger.

`writeToLdif` can write variables as well (run levels are
supported and variables are available one run after creation). You may even define multiple
writeToLdif processors. All content will be collected and written to one resulting
LDIF.

Please ensure to adjust the search scope to your workspace and change the id to
an existing one.

Advanced example of the `writeToLdif`
processor:

```json
{
  "processors": [
    {
      "processorType": "writeToLdif",
      "filter": {
        "advanced": "${integration.contentIndex==0}",
        "onRead": "${lx.factsheet.description!=''}"
      },
      "identifier": {
        "search": {
          "scope": {
            "ids": [
              "8de51ff7-6f13-47df-8af8-9132ada2e74d"
            ],
            "facetFilters": []
          },
          "filter": "${true}",
          "multipleMatchesAllowed": true
        }
      },
      "run": 0,
      "updates": [
        {
          "key": {
            "expr": "content.id"
          },
          "values": [
            {
              "expr": "${lx.factsheet.id}"
            }
          ]
        },
        {
          "key": {
            "expr": "content.type"
          },
          "values": [
            {
              "expr": "${lx.factsheet.name}"
            }
          ]
        },
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "${lx.factsheet.description}"
            }
          ]
        }
      ],
      "logLevel": "warning",
      "read": {
        "fields": [
          "description"
        ]
      }
    }
  ],
  "targetLdif": {
    "dataConsumer": {
      "type": "leanixStorage"
    },
    "ldifKeys": [
      {
        "key": "connectorType",
        "value": "${header.connectorType}_export"
      },
      {
        "key": "connectorId",
        "value": "${header.connectorId}_export"
      },
      {
        "key": "description",
        "value": "Enriched imporeted LDIF for Applications"
      }
    ]
  }
}
```

Example input in LDIF format:

```json
{
  "connectorType": "example",
  "connectorId": "example",
  "lxVersion": "1.0.0",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "content": [
    {
      "type": "",
      "id": "",
      "data": {}
    }
  ]
}
```

## Inbound Impact

The processor is used to write impacts to the SAP LeanIX backend.

A
processor always writes a single impact. In case a list of input data is given where
"forEach" can iterate over, multiple impacts can be written by a single processor. Different
types of impacts should be split into different processors in order to keep a configuration
readable as different impacts have different parameters.

The example below shows how
to define Impacts. Please be aware that each type of impacts may require a different set of
keys to be configured.

**Tip**

To find out about the different keys required for each Impact type, create the needed
types of impacts in the UI, then export using an outbound processor or by using the "read"
section in an inbound processor and either export to LDIF or write to a field like
"description"

Example `inboundImpact` processor:

```json
{
  "processors": [
    {
      "processorType": "inboundImpact",
      "updates": [
        {
          "key": {
            "expr": "groupName"
          },
          "values": [
            {
              "expr": "G1"
            }
          ]
        },
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "Group Description 2"
            }
          ]
        },
        {
          "key": {
            "expr": "impacts"
          },
          "values": [
            {
              "map": [
                {
                  "key": "type",
                  "value": "FACTSHEET_SET"
                },
                {
                  "key": "factSheetId",
                  "value": "28fe4aa2-6e46-41a1-a131-72afb3acf256"
                },
                {
                  "key": "fieldName",
                  "value": "functionalSuitabilityDescription"
                },
                {
                  "key": "fieldValue",
                  "value": "${data.value}"
                }
              ]
            }
          ]
        }
      ],
      "identifier": {
        "internal": "6d8acf0c-fa4e-40ed-9986-97da860f3414"
      },
      "logLevel": "warning"
    }
  ]
}
```

## Inbound To-dos

This processor can be used import to-dos into the workspace.

| Keys specific to the `inboundToDo` Processor | Details |
| --- | --- |
| `title` | Title of the To-do |
| `category` | Category of the To-do (Sample values: ANSWER,ACTION\_ITEM) |
| `description` | Description of the To-do |
| `status` | Status of the To-do (OPEN, CLOSED) |
| `resolution` | When closing you also have an option to provide the<br>resolution(ACCEPTED,REJECTED,REVERTED) |

Below example will need to be adapted as per specific type of
To-dos.

Example `inboundToDo` processor:

```json
{
  "processors": [
    {
      "processorType": "inboundToDo",
      "processorName": "Create toDos",
      "processorDescription": "Creates toDos from incoming data",
      "filter": {
        "exactType": "ActionItem"
      },
      "identifier": {
        "external": "${content.id}"
      },
      "run": 1,
      "updates": [
        {
          "key": {
            "expr": "factSheetId"
          },
          "values": [
            {
              "expr": "${data.factSheetId}"
            }
          ]
        },
        {
          "key": {
            "expr": "title"
          },
          "values": [
            {
              "expr": "${data.title}"
            }
          ]
        },
        {
          "key": {
            "expr": "description"
          },
          "values": [
            {
              "expr": "${data.description}"
            }
          ]
        },
        {
          "key": {
            "expr": "category"
          },
          "values": [
            {
              "expr": "${data.category}"
            }
          ]
        },
        {
          "key": {
            "expr": "dueDate"
          },
          "values": [
            {
              "expr": "${data.dueDate}"
            }
          ]
        }
      ],
      "variables": [
        {
          "key": "category",
          "value": "${lx.todo.id}_${lx.todo.category}"
        },
        {
          "key": "state",
          "value": "${lx.todo.state}"
        }
      ],
      "logLevel": "debug"
    }
  ],
  "variables": {}
}
```

Example input in LDIF format:

```json
{
  "connectorType": "todoReadType",
  "connectorId": "todoReadId",
  "connectorVersion": "1.0.0",
  "lxVersion": "1.0.0",
  "description": "",
  "processingDirection": "inbound",
  "processingMode": "partial",
  "customFields": {},
  "content": [
    {
      "type": "ActionItem",
      "id": "E-100",
      "data": {
        "title": "test abc",
        "description": "Updated by iAPI",
        "todoId": "ec25a364-66df-4313-9127-44e429df81ad",
        "dueDate": "2021-08-19",
        "category": "ACTION_ITEM",
        "varValue": "value1",
        "creatorId": "275617d6-2538-466c-b210-961ef2cb554a",
        "factSheetId": "28fe4aa2-6e46-41a1-a131-72afb3acf256"
      }
    }
  ]
}
```
