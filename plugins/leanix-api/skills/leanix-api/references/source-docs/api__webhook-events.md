<!-- Source: https://help.sap.com/docs/leanix/ea/webhook-events -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Webhook Events

Available event types for webhook subscriptions.

## Fact Sheets

**Note**

For events related to fact sheets, you can optionally select a fact sheet type.
This allows you to receive event notifications only for this fact sheet type
without configuring a callback.

| Event | Description |
| --- | --- |
| `FACT_SHEET_CREATED` | A new fact sheet is created. |
| `FACT_SHEET_UPDATED` | A fact sheet is updated. This also includes updates to fact sheet<br>relations. |
| `FACT_SHEET_VIEWED` | A fact sheet is viewed by a workspace user. |
| `FACT_SHEET_ARCHIVED` | A fact sheet is archived. |
| `FACT_SHEET_DELETED` | A fact sheet is deleted. Deletion occurs when a fact sheet type<br>is deleted from the meta model configuration or the retention period<br>for an archived fact sheet ends. |
| `FACT_SHEET_RECOVERED` | A fact sheet is recovered. |

## Fact Sheet Relations

| Event | Description |
| --- | --- |
| `RELATION_CREATED` | A new relation between fact sheets is created. |
| `RELATION_UPDATED` | A relation between fact sheets is updated. |
| `RELATION_ARCHIVED` | A relation between fact sheets is archived. |
| `RELATION_DELETED` | A relation between fact sheets is deleted. Deletion occurs when a<br>fact sheet type is deleted from the meta model configuration or the<br>retention period for an archived fact sheet ends. |
| `RELATION_SWITCH` | Only the target fact sheet within a relation changed. |

## Fact Sheet Tags

| Event | Description |
| --- | --- |
| `FACT_SHEET_TAG_ADDED` | A tag is added to a fact sheet. |
| `FACT_SHEET_TAG_REMOVED` | A tag is removed from a fact sheet. |

## Fact Sheet Fields

| Event | Description |
| --- | --- |
| `FACT_SHEET_FIELD_UPDATED` | A field on a fact sheet is updated. |

## Fact Sheet Resources

| Event | Description |
| --- | --- |
| `DOCUMENT_CREATED` | A resource is added to a fact sheet. |
| `DOCUMENT_UPDATED` | A resource is updated on a fact sheet. |
| `DOCUMENT_DELETED` | A resource is deleted from a fact sheet. |

## Fact Sheet Subscriptions

| Event | Description |
| --- | --- |
| `SUBSCRIPTION_CREATED` | A subscription is added to a fact sheet. |
| `SUBSCRIPTION_UPDATED` | A subscription is updated on a fact sheet. |
| `SUBSCRIPTION_DELETED` | A subscription is deleted from a fact sheet. |

## Fact Sheet Comments

| Event | Description |
| --- | --- |
| `COMMENT_CREATED` | A comment is created on a fact sheet. |
| `COMMENT_REPLY_ADDED` | A reply is added to a comment on a fact sheet. |
| `COMMENT_DELETED` | A comment is deleted from a fact sheet. |

## Integration Runs

**Note**

For events related to integrations, you can optionally select a specific
integration. This allows you to receive event notifications only for this
integration without configuring a callback.

| Event | Description |
| --- | --- |
| `INTEGRATION_RUN_STARTED` | An integration run started. |
| `INTEGRATION_RUN_FINISHED` | An integration run finished. |
| `INTEGRATION_RUN_ABORTED` | An integration run is canceled. |

## Integration Configurations

| Event | Description |
| --- | --- |
| `CONFIGURATION_CREATED` | A configuration for an integration is created. |
| `CONFIGURATION_UPDATED` | A configuration for an integration is updated. |
| `CONFIGURATION_DELETED` | A configuration for an integration is deleted. |
| `CONFIGURATION_ACTIVATED` | A configuration for an integration is activated. |
| `CONFIGURATION_DEACTIVATED` | A configuration for an integration is deactivated. |

## Automations

| Event | Description |
| --- | --- |
| `AUTOMATION_TRIGGERED` | An automation is triggered. For more details, see [Creating an<br>Automation with a Webhook Action](https://help.sap.com/docs/leanix/ea/automations-webhooks?locale=en-US&state=PRODUCTION&version=CLOUD "Send webhooks from automations to trigger external workflows."). |

## Surveys

| Event | Description |
| --- | --- |
| `POLL_RESULT_CREATED` | A survey response is created. |
| `POLL_RESULT_UPDATED` | A survey response is updated. |
| `POLL_RESULT_FINALIZED` (within `POLL_RESULT_UPDATED`) | A survey response for a fact sheet is submitted. |

## To-Dos

| Event | Description |
| --- | --- |
| `TODO_CREATED` | A to-do is created. |
| `TODO_UPDATED` | A to-do is updated. |
| `TODO_DELETED` | A to-do is deleted. |
| `TODO_ASSIGNEE_CREATED` | An assignee is added to a to-do. |
| `TODO_ASSIGNEE_UPDATED` | A user claimed a to-do. |
| `TODO_ASSIGNEE_DELETED` | An assignee is removed from a to-do. |
