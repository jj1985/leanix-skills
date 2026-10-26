<!-- Source: https://help.sap.com/docs/leanix/ea/webhook-payloads -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Webhook Payloads

Example payloads for selected webhook events.

**Note**

This document provides example payloads for selected webhook events. To view a full list of
event types, see [Webhook Events](https://help.sap.com/docs/leanix/ea/webhook-events?locale=en-US&state=PRODUCTION&version=CLOUD "Available event types for webhook subscriptions.").

The data provided in a webhook payload is specific to each event type. In general, a payload
contains the following information:

- Event details

- User who triggered the event

- Metadata, such as the fact sheet type, fields, and relations

The maximum supported payload size is 20 MB.

## FACT\_SHEET\_CREATED

```json
{
  "id": 42834,
  "type": "FactSheetCreatedEvent",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "createdAt": "2024-02-16T13:12:27.032622Z",
  "factSheet": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 0,
    "name": "AC Management",
    "type": "Application",
    "level": 1,
    "fields": [],
    "status": "ACTIVE",
    "lxState": "BROKEN_QUALITY_SEAL",
    "fullName": "AC Management",
    "naFields": [],
    "createdAt": "2024-02-16T13:12:26.995583770Z",
    "documents": [],
    "relations": [],
    "updatedAt": "2024-02-16T13:12:26.999252278Z",
    "completion": {
      "type": "SectionCompletion",
      "completion": 0.005952380952380952,
      "percentage": 1,
      "totalWeight": 7,
      "weightedSum": 0.041666666666666664,
      "subCompletions": {
        "section.projects": {
          "type": "SectionCompletion",
          "completion": 0,
          "percentage": 0,
          "totalWeight": 1,
          "weightedSum": 0,
          "subCompletions": {
            "subsection.factSheetsAffecting.label": {
              "type": "ConcreteCompletion",
              "completion": 0,
              "percentage": 0,
              "totalWeight": 1,
              "weightedSum": 0
            }
          }
        },
        "section.sourcing": {...},
        "section.information": {...},
        "section.dependencies": {...},
        "section.dataManagement": {...},
        "section.businessSupport": {...},
        "section.lxPortfolioStrategy": {...}
      }
    },
    "milestones": [],
    "displayName": "AC Management",
    "subscriptions": [],
    "permittedReadACL": [],
    "permittedWriteACL": [],
    "lxExcludeFromQuota": false
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "clonedFactSheet": false,
  "transactionSequenceNumber": 75086
}
```

## FACT\_SHEET\_UPDATED

```json
{
  "id": 42844,
  "type": "FactSheetUpdatedEvent",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "createdAt": "2024-02-16T13:15:23.702272Z",
  "factSheet": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 3,
    "name": "AC Management",
    "tags": [...],
    "type": "Application",
    "level": 1,
    "fields": [],
    "status": "ACTIVE",
    "lxState": "BROKEN_QUALITY_SEAL",
    "fullName": "AC Management",
    "naFields": [],
    "createdAt": "2024-02-16T13:12:26.995584Z",
    "documents": [],
    "relations": [],
    "updatedAt": "2024-02-16T13:15:23.678693644Z",
    "completion": {...},
    "milestones": [],
    "description": "AC Management app",
    "displayName": "AC Management",
    "subscriptions": [],
    "permittedReadACL": [],
    "permittedWriteACL": [],
    "lxExcludeFromQuota": false
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "transactionSequenceNumber": 75088
}
```

## FACT\_SHEET\_VIEWED

```json
{
  "id": 118540,
  "type": "FactSheetViewedEvent",
  "userId": "e84a8c18-a374-4ccd-b783-5a8050787614",
  "createdAt": "2024-07-05T11:13:11.834105Z",
  "factSheetId": "3921ec8c-a81a-470e-89de-b26b972bca59",
  "workspaceId": "95ed41a8-1856-4372-96b7-f3117fbc9675",
  "transactionSequenceNumber": null
}
```

## FACT\_SHEET\_ARCHIVED

```json
{
  "id": 42914,
  "type": "FactSheetArchivedEvent",
  "fsType": "Application",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "comment": "Duplicate application",
  "createdAt": "2024-02-16T13:49:42.181834Z",
  "fsIdAndRev": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 11
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "affectedFactSheetIdAndRev": [
    {
      "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
      "rev": 11
    },
    {
      "id": "2efa37b5-18aa-48d8-9d70-1328c0d856d7",
      "rev": 27
    }
  ],
  "transactionSequenceNumber": 75126
}
```

## RELATION\_CREATED

```json
{
  "id": 42846,
  "type": "RelationCreatedEvent",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "relation": {
    "id": "675aacdd-cfdf-4702-8084-0646e74533b9",
    "toId": "2efa37b5-18aa-48d8-9d70-1328c0d856d7",
    "type": "relToChild",
    "fields": [],
    "fromId": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "status": "ACTIVE",
    "naFields": [],
    "typeToFS": "Application",
    "typeFromFS": "Application",
    "displayNameToFS": "AC Management / AC Management Cloud",
    "permittedReadACL": [],
    "constrainingRelations": []
  },
  "createdAt": "2024-02-16T13:17:20.965779Z",
  "toDetails": {
    "factSheetInfos": {
      "type": "Application",
      "idAndRev": {
        "id": "2efa37b5-18aa-48d8-9d70-1328c0d856d7",
        "rev": 25
      },
      "displayName": "AC Management / AC Management Cloud"
    },
    "effectiveRelationName": "relToParent"
  },
  "relationId": "675aacdd-cfdf-4702-8084-0646e74533b9",
  "fromDetails": {
    "factSheetInfos": {
      "type": "Application",
      "idAndRev": {
        "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
        "rev": 3
      },
      "displayName": "AC Management"
    },
    "effectiveRelationName": "relToChild"
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "transactionSequenceNumber": 75089
}
```

## FACT\_SHEET\_TAG\_ADDED

```json
{
  "id": 42840,
  "type": "FactSheetTagAddedEvent",
  "tagId": "5ab3558a-580b-422d-8a95-12f7f075dfd7",
  "fsType": "Application",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "tagName": "Public Cloud",
  "createdAt": "2024-02-16T13:14:08.732070Z",
  "fsIdAndRev": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 1
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "tagGroupName": "Cloud Transformation",
  "transactionSequenceNumber": 75087
}
```

## FACT\_SHEET\_FIELD\_UPDATED

```json
{
  "id": 42860,
  "path": "/externalId",
  "type": "FactSheetFieldUpdatedEvent",
  "fsType": "Application",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "newValue": {
    "type": "ExternalId",
    "status": "ACTIVE",
    "comment": null,
    "externalId": "123456",
    "externalUrl": null
  },
  "oldValue": {
    "type": "ExternalId",
    "status": "ACTIVE",
    "comment": null,
    "externalId": "123456789",
    "externalUrl": null
  },
  "createdAt": "2024-02-16T13:23:03.697933Z",
  "fsIdAndRev": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 7
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "transactionSequenceNumber": 75093
}
```

## DOCUMENT\_CREATED

```json
{
  "id": 42851,
  "type": "DocumentCreatedEvent",
  "refId": null,
  "fsType": "Application",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "createdAt": "2024-02-16T13:19:09.116531Z",
  "documentId": "d2421a7c-b4db-485f-873a-71a354eb7209",
  "fsIdAndRev": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 4
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "documentName": "Link to SAP LeanIX website",
  "documentType": null,
  "documentOrigin": "CUSTOM_LINK",
  "transactionSequenceNumber": 75090
}
```

## SUBSCRIPTION\_CREATED

```json
{
  "id": 42854,
  "type": "SubscriptionCreatedEvent",
  "fsType": "Application",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "createdAt": "2024-02-16T13:20:23.769518Z",
  "roleInfos": [],
  "fsIdAndRev": {
    "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
    "rev": 6
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "subscriptionId": "39aae878-6ded-40de-aa01-9524ce3ee6d0",
  "subscribedUserId": "8393b7a8-8bfb-4989-a348-6cb31d56745f",
  "subscriptionType": "RESPONSIBLE",
  "transactionSequenceNumber": 75091
}
```

## COMMENT\_CREATED

```json
{
  "id": 118533,
  "type": "CommentCreatedEvent",
  "fsType": "Application",
  "userId": "e84a8c18-a374-4ccd-b783-5a8050787614",
  "message": "This is a comment",
  "commentId": "e8182dd9-586b-4a5d-82f2-cfbec02cb118",
  "createdAt": "2024-07-05T11:02:00.129002Z",
  "fsIdAndRev": { "id": "3921ec8c-a81a-470e-89de-b26b972bca59", "rev": 35 },
  "workspaceId": "95ed41a8-1856-4372-96b7-f3117fbc9675",
  "transactionSequenceNumber": 106302
}
```

## COMMENT\_REPLY\_ADDED

```json
{
  "id": 118537,
  "type": "CommentReplyAddedEvent",
  "userId": "e84a8c18-a374-4ccd-b783-5a8050787614",
  "replyId": "847f58e0-8298-4f71-b541-71a38fccc0df",
  "commentId": "e8182dd9-586b-4a5d-82f2-cfbec02cb118",
  "createdAt": "2024-07-05T11:02:03.980262Z",
  "workspaceId": "95ed41a8-1856-4372-96b7-f3117fbc9675",
  "transactionSequenceNumber": 106303
}
```

## COMMENT\_DELETED

```json
{
  "id": 118542,
  "type": "CommentDeletedEvent",
  "fsType": "Application",
  "userId": "e84a8c18-a374-4ccd-b783-5a8050787614",
  "comment": {
    "id": "e8182dd9-586b-4a5d-82f2-cfbec02cb118",
    "status": "ACTIVE",
    "userId": "e84a8c18-a374-4ccd-b783-5a8050787614",
    "message": "This is a comment",
    "replies": [
      {
        "id": "847f58e0-8298-4f71-b541-71a38fccc0df",
        "userId": "e84a8c18-a374-4ccd-b783-5a8050787614",
        "message": "This is a reply to a comment",
        "createdAt": "2024-07-05T11:02:03.939396098Z"
      }
    ],
    "createdAt": "2024-07-05T11:02:00.017209Z",
    "replaySequence": 0
  },
  "commentId": "e8182dd9-586b-4a5d-82f2-cfbec02cb118",
  "createdAt": "2024-07-05T11:15:06.301588Z",
  "fsIdAndRev": { "id": "3921ec8c-a81a-470e-89de-b26b972bca59", "rev": 35 },
  "workspaceId": "95ed41a8-1856-4372-96b7-f3117fbc9675",
  "transactionSequenceNumber": 106304
}
```

## INTEGRATION\_RUN\_FINISHED (Integration API)

```json
{
  "type": "INTEGRATION-API",
  "scope": "PARTIAL",
  "version": "1.0.0",
  "duration": 3.924405624,
  "progress": "FINISHED",
  "direction": "INBOUND",
  "errorCount": 0,
  "connectorId": "inbound-document-connector",
  "warningCount": 0,
  "connectorType": "inboundDocument",
  "integratedTool": "",
  "processedCount": 2,
  "synchronizationId": "865b71a1-e66f-49c0-89de-5bc5fb42401b"
}
```

## INTEGRATION\_RUN\_STARTED (ServiceNow Integration)

```json
{
  "version": "?",
  "type": "SERVICENOW",
  "scope": "PARTIAL",
  "errorCount": 1,
  "warningCount": 2,
  "processedCount": 3,
  "duration": "PT0.123S",
  "progress": "RUNNING",
  "synchronizationId": "18886403-3edb-483d-a13f-cac5f4b34802"
}
```

## INTEGRATION\_RUN\_FINISHED (ServiceNow Integration)

```json
{
  "version": "?",
  "type": "SERVICENOW",
  "scope": "PARTIAL",
  "errorCount": 1,
  "warningCount": 2,
  "processedCount": 3,
  "duration": "PT0.123S",
  "progress": "FINISHED",
  "synchronizationId": "18886403-3edb-483d-a13f-cac5f4b34802"
}
```

## INTEGRATION\_RUN\_ABORTED (ServiceNow Integration)

```json
{
  "version": "?",
  "type": "SERVICENOW",
  "scope": "PARTIAL",
  "errorCount": 1,
  "warningCount": 2,
  "processedCount": 3,
  "duration": "PT0.123S",
  "progress": "ABORTED",
  "synchronizationId": "18886403-3edb-483d-a13f-cac5f4b34802"
}
```

## CONFIGURATION\_CREATED

```json
{
  "type": "CONFIGURATION_CREATED",
  "userId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
  "connectorId": "inbound-document-connector",
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "connectorType": "inboundDocument",
  "processingMode": "partial",
  "integrationType": "Integration API",
  "connectorVersion": "1.0.0",
  "processingDirection": "inbound"
}
```

## AUTOMATION\_TRIGGERED

```json
{
  "tag": "AUTOMATION_WEBHOOK_TAG",
  "userId": "6ef78c21-98a2-4377-acaa-fc66ff2b78gf",
  "factSheet": {
    "id": "7a5bace3-4f7c-4682-b511-aecc9a6927d0",
    "type": "Application",
    "displayName": "Test Application Fact Sheet"
  },
  "automation": {
    "id": "3c72aa45-457a-4c10-9fac-40146121167c",
    "sourceUrl": "https://app.leanix.net/workspace-name/admin/automations/edit/3c72aa45-457a-4c10-9fac-40146121167c"
  },
  "workspaceId": "b7d655f1-4aa0-4132-92c6-a390a60cb8gh"
}
```

## POLL\_RESULT\_CREATED

```json
{
  "type": "POLL_RESULT_CREATED",
  "pollRun": {
    "id": "0b38d423-7b15-4ecd-ae3e-175c9fb8134a",
    "poll": {
      "id": "3754281a-f8f2-43b5-8ec5-b78465f48be6",
      "title": "Update Life Cycle Dates",
      "status": "ACTIVE",
      "language": "en",
      "creatorId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
      "timeFrame": 0,
      "userQuery": {
        "roles": [
          {
            "roleDetails": [],
            "subscriptionType": "RESPONSIBLE"
          },
          {
            "roleDetails": [],
            "subscriptionType": "OBSERVER"
          }
        ]
      },
      "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
      "creationDate": "2024-02-16T13:31:19.391993Z",
      "factSheetType": "Application",
      "questionnaire": {
        "id": "5af9a9b9-6da1-465a-bc95-8344b9ec2fb2",
        "questions": [
          {
            "id": "9de72fa1-d999-bff3-eabb-ba3315bb479b",
            "type": "factsheetelement",
            "label": "Update life cycle",
            "deleted": false,
            "disabled": false,
            "powerfeature": true,
            "factSheetElement": {
              "type": "FACT_SHEET_FIELD",
              "factSheetFieldName": "lifecycle",
              "factSheetFieldType": "LIFECYCLE"
            }
          }
        ]
      },
      "factSheetQuery": {
        "ids": ["95fbeddd-abdf-4552-a82b-ce37c287735c"],
        "filter": {
          "facetFilter": [
            {
              "keys": ["Application"],
              "facetKey": "FactSheetTypes",
              "operator": "OR"
            }
          ]
        }
      },
      "repeatIntervall": 0,
      "introductionText": "...",
      "introductionSubject": "...",
      "additionalFactSheetText": "...",
      "allowedPermissionStatus": "ACTIVE_ONLY",
      "sendChangeNotifications": true,
      "additionalFactSheetSubject": "A Fact Sheet has been added to a Survey you are participating in",
      "additionalFactSheetCheckEnabled": true
    },
    "status": "PREPARING",
    "language": "en",
    "pollCopy": {
      "id": "3754281a-f8f2-43b5-8ec5-b78465f48be6",
      "title": "Update Life Cycle Dates",
      "status": "ACTIVE",
      "language": "en",
      "creatorId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
      "timeFrame": 0,
      "userQuery": {
        "roles": [
          {
            "roleDetails": [],
            "subscriptionType": "RESPONSIBLE"
          },
          {
            "roleDetails": [],
            "subscriptionType": "OBSERVER"
          }
        ]
      },
      "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
      "creationDate": "2024-02-16T13:31:19.391993Z",
      "factSheetType": "Application",
      "questionnaire": {
        "id": "5af9a9b9-6da1-465a-bc95-8344b9ec2fb2",
        "questions": [
          {
            "id": "9de72fa1-d999-bff3-eabb-ba3315bb479b",
            "type": "factsheetelement",
            "label": "Update life cycle",
            "deleted": false,
            "disabled": false,
            "powerfeature": true,
            "factSheetElement": {
              "type": "FACT_SHEET_FIELD",
              "factSheetFieldName": "lifecycle",
              "factSheetFieldType": "LIFECYCLE"
            }
          }
        ]
      },
      "factSheetQuery": {
        "ids": ["95fbeddd-abdf-4552-a82b-ce37c287735c"],
        "filter": {
          "facetFilter": [
            {
              "keys": ["Application"],
              "facetKey": "FactSheetTypes",
              "operator": "OR"
            }
          ]
        }
      },
      "repeatIntervall": 0,
      "introductionText": "...",
      "introductionSubject": "...",
      "additionalFactSheetText": "...",
      "allowedPermissionStatus": "ACTIVE_ONLY",
      "sendChangeNotifications": true,
      "additionalFactSheetSubject": "A Fact Sheet has been added to a Survey you are participating in",
      "additionalFactSheetCheckEnabled": true
    },
    "senderId": "3et65c21-98f2-5376-acaa-fchf654b9c22",
    "startTime": "2024-02-16T13:40:56.246318Z",
    "resultView": "NEW",
    "pollRunType": "LIVE",
    "pollResultType": "PER_FACTSHEET",
    "factsheetsTotal": 1,
    "recipientsTotal": 2,
    "factsheetsProgress": 0,
    "factsheetsSelected": 1,
    "recipientsProgress": 0,
    "factsheetsCompleted": 0,
    "recipientsCompleted": 0,
    "sendChangeNotifications": true,
    "additionalFactSheetCheckEnabled": true
  },
  "createdAt": 1708090856819,
  "pollResult": {
    "id": "1eda2425-2d33-4c5e-a3e3-7f767770b778",
    "users": [
      {
        "id": "8393b7a8-8bfb-4989-a348-6cb31d56745f",
        "email": "john.smith@organization.com",
        "fullName": "John Smith",
        "lastName": "Smith",
        "firstName": "John"
      },
      {
        "id": "3et65c21-98f2-5376-acaa-fchf654b9c22",
        "email": "john.doe@organization.com",
        "fullName": "John Doe",
        "lastName": "Doe",
        "firstName": "John"
      }
    ],
    "sender": {
      "id": "3et65c21-98f2-5376-acaa-fchf654b9c22",
      "email": "john.doe@organization.com",
      "fullName": "John Doe",
      "lastName": "Doe",
      "firstName": "John"
    },
    "status": "NEW",
    "answers": [
      {
        "questionId": "9de72fa1-d999-bff3-eabb-ba3315bb479b"
      }
    ],
    "factSheet": {
      "id": "95fbeddd-abdf-4552-a82b-ce37c287735c",
      "name": "AC Management",
      "type": "Application",
      "displayName": "AC Management App"
    },
    "pollRunId": "0b38d423-7b15-4ecd-ae3e-175c9fb8134a"
  },
  "workspaceId": "ae6756f1-4aag-4356-92c6-a390a60cb8fg",
  "pollResultEventType": "POLL_RESULT_CREATED"
}
```

## TODO\_CREATED

```json
{
"createdAt": "2026-03-26T14:00:00+01:00",
"type": "TODO_CREATED",
"sourceName": "todo",
"sourceId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"sourceUrl": "https://app.leanix.net/services/todo/v1/to-do?todoIds=a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"workspaceId": "11111111-2222-3333-4444-555555555555",
"userId": "aaaa1111-bbbb-2222-cccc-333333333333",
"tags": ["TODO", "TODO_CREATED"],
"payload": {
"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"title": "Review architecture decision",
"description": "Review the ADR for the new auth middleware",
"factSheetId": "ff000000-1111-2222-3333-444444444444",
"category": "ACTION_ITEM",
"state": "OPEN",
"dueDate": "2026-04-15",
"creatorId": "aaaa1111-bbbb-2222-cccc-333333333333",
"creationTime": "2026-03-26T13:00:00Z"
}
}
```

## TODO\_UPDATED

```json
{
"createdAt": "2026-03-26T14:05:00+01:00",
"type": "TODO_UPDATED",
"sourceName": "todo",
"sourceId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"sourceUrl": "https://app.leanix.net/services/todo/v1/to-do?todoIds=a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"workspaceId": "11111111-2222-3333-4444-555555555555",
"userId": null,
"tags": ["TODO", "TODO_UPDATED"],
"payload": {
"changes": {
"title": "Review architecture decision (updated)",
"state": "DONE"
},
"state": {
"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"title": "Review architecture decision (updated)",
"description": "Review the ADR for the new auth middleware",
"factSheetId": "ff000000-1111-2222-3333-444444444444",
"category": "ACTION_ITEM",
"state": "DONE",
"dueDate": "2026-04-15",
"creatorId": "aaaa1111-bbbb-2222-cccc-333333333333",
"creationTime": "2026-03-26T13:00:00Z"
}
}
}
```

## TODO\_DELETED

```json
{
"createdAt": "2026-03-26T14:10:00+01:00",
"type": "TODO_DELETED",
"sourceName": "todo",
"sourceId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"sourceUrl": "https://app.leanix.net/services/todo/v1/to-do?todoIds=a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"workspaceId": "11111111-2222-3333-4444-555555555555",
"userId": "bbbb2222-cccc-3333-dddd-444444444444",
"tags": ["TODO", "TODO_DELETED"],
"payload": {
"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
}
```

## TODO\_ASSIGNEE\_CREATED

```json
{
"createdAt": "2026-03-26T14:15:00+01:00",
"type": "TODO_ASSIGNEE_CREATED",
"sourceName": "todo",
"sourceId": "d4e5f6a7-b8c9-3210-fedc-ba9876543210",
"sourceUrl": "https://app.leanix.net/services/todo/v1/to-do?todoIds=a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"workspaceId": "11111111-2222-3333-4444-555555555555",
"userId": "bbbb2222-cccc-3333-dddd-444444444444",
"tags": ["TODO", "TODO_ASSIGNEE_CREATED"],
"payload": {
"userId": "cccc3333-dddd-4444-eeee-555555555555",
"todoId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
"isOwner": true,
"changedBy": "bbbb2222-cccc-3333-dddd-444444444444",
"id": "d4e5f6a7-b8c9-3210-fedc-ba9876543210"
}
}
```

## TODO\_ASSIGNEE\_UPDATED

```json
{
"createdAt": "2026-03-26T14:20:00+01:00",
"type": "TODO_ASSIGNEE_UPDATED",
"sourceName": "todo",
"sourceId": "d4e5f6a7-b8c9-3210-fedc-ba9876543210",
"sourceUrl": "https://app.leanix.net/services/todo/v1/to-do",
"workspaceId": "11111111-2222-3333-4444-555555555555",
"userId": "bbbb2222-cccc-3333-dddd-444444444444",
"tags": ["TODO", "TODO_ASSIGNEE_UPDATED"],
"payload": {
"isOwner": false,
"changedBy": "bbbb2222-cccc-3333-dddd-444444444444"
}
}
```

## TODO\_ASSIGNEE\_DELETED

```json
{
"createdAt": "2026-03-26T14:25:00+01:00",
"type": "TODO_ASSIGNEE_DELETED",
"sourceName": "todo",
"sourceId": "d4e5f6a7-b8c9-3210-fedc-ba9876543210",
"sourceUrl": "https://app.leanix.net/services/todo/v1/to-do",
"workspaceId": "11111111-2222-3333-4444-555555555555",
"userId": "bbbb2222-cccc-3333-dddd-444444444444",
"tags": ["TODO", "TODO_ASSIGNEE_DELETED"],
"payload": {
"changedBy": "bbbb2222-cccc-3333-dddd-444444444444"
}
}
```
