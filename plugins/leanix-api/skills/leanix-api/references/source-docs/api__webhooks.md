<!-- Source: https://help.sap.com/docs/leanix/ea/webhooks -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Webhooks

Listen to events in SAP LeanIX using
webhooks.

## Overview

Webhooks let you receive updates about events as they happen in near real time in SAP LeanIX. With
webhooks, you can set up event-driven triggers that initiate automated actions,
which allows you to automate workflows for your organization and eliminate manual
processes.

We support the following webhook types, based on the event delivery method:

- PUSH webhooks: As events occur in SAP LeanIX,
they're sent through HTTP POST requests to the specified target URL. This is the
recommended way to receive events from SAP LeanIX.

- PULL webhooks: A client requests events by polling a REST endpoint on the
SAP LeanIX API. This method of retrieving events is useful if your environment doesn't
allow exposing a public HTTP server to receive events, such as when your
application operates behind a firewall. Events are retained on the server for 30
days, but it's recommended to retrieve them more regularly.

The following image illustrates how PUSH and PULL webhooks work.

![Workflows for Data Retrieval Using PUSH and PULL Webhooks](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio27498a0a7a44101480d58f637ab18a2d_LowRes.png)

Workflows for Data Retrieval Using PUSH and PULL Webhooks

**Note**

Within the [Webhooks API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DWebhooks "https://app.leanix.net/openapi-explorer/?urls.primaryName=Webhooks"), webhooks are referred to
as subscriptions. This term is also used in the application UI and this
document.

## Creating a Webhook

Follow these steps:

1. In the administration area, navigate to the Webhooks
section.

2. Click New Webhook.

3. Optional: Enter a name and description for the webhook.

4. Configure the visibility of the webhook:

   - Private: Only you can access the webhook.

   - Workspace: Any admin in the workspace can view,
     modify, or delete the webhook.
5. Select the delivery type and configure relevant parameters:

   - PUSH: For more information, see [PUSH Webhooks](https://help.sap.com/docs/leanix/ea/push-webhooks?locale=en-US&state=PRODUCTION&version=CLOUD "Receive events to a target URL as they occur in your workspace.").

   - PULL: To learn how to fetch events, see [PULL Webhooks](https://help.sap.com/docs/leanix/ea/pull-webhooks?locale=en-US&state=PRODUCTION&version=CLOUD "Request events by polling an API endpoint.").

**Note**

Once you save a delivery type for a webhook,
you cannot change it.

6. The webhook is active by default. To deactivate the webhook, switch it off under
Status.

7. In the Triggering Events section, click Add
new set to add a triggering event for the webhook. For a full
list of events, see [Webhook Events](https://help.sap.com/docs/leanix/ea/webhook-events?locale=en-US&state=PRODUCTION&version=CLOUD "Available event types for webhook subscriptions.").

8. Click Save.

A webhook is created. You can update its configuration or delete it if needed.

![Webhook Configuration Page](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio9b07429b9b8d45e492653ee4b6408577_HiRes.png)

## Event Types and Payloads

For a full list of available event types, see
[Webhook Events](https://help.sap.com/docs/leanix/ea/webhook-events?locale=en-US&state=PRODUCTION&version=CLOUD "Available event types for webhook subscriptions.").

To view example payloads for selected event types, see [Webhook Payloads](https://help.sap.com/docs/leanix/ea/webhook-payloads?locale=en-US&state=PRODUCTION&version=CLOUD "Example payloads for selected webhook events.").

## PUSH Webhooks

With PUSH webhooks, each time an event occurs in SAP LeanIX, it's
sent to the specified target URL through an HTTP POST request. The request body
contains an event payload in JSON format. To learn how to use PUSH webhooks, visit
[PUSH Webhooks](https://help.sap.com/docs/leanix/ea/push-webhooks?locale=en-US&state=PRODUCTION&version=CLOUD "Receive events to a target URL as they occur in your workspace.").

## PULL Webhooks

With PULL webhooks, a client requests events by polling an endpoint on the SAP LeanIX
Webhooks API. To learn how to use PUSH webhooks, visit [PULL Webhooks](https://help.sap.com/docs/leanix/ea/pull-webhooks?locale=en-US&state=PRODUCTION&version=CLOUD "Request events by polling an API endpoint.").
