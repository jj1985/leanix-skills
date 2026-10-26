<!-- Source: https://help.sap.com/docs/leanix/ea/rate-limiting -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Rate Limiting

Learn how our rate limiting in SAP LeanIX APIs
works.

## Overview

Rate limiting restricts the number of requests that a user or system can make to a
network interface within a specific timeframe. Rate limiting ensures the
following:

- Fair resource allocation: All customer workspaces
receive equitable access to API resources regardless of individual usage
patterns.

- System reliability: Prevents potential downtimes and
service degradation caused by excessive request volumes.

- Performance optimization: Maintains consistent response
times for all users by balancing load across the infrastructure.

Consider our rate limits when implementing high-frequency API calls.

## How Rate Limiting Works

If you reach a rate limit, you get the HTTP `429 Too Many Requests`
response status code.

The API response may contain a message showing the reason for reaching the rate
limit. For example, if you reach a user-based rate limit, you get a response like
the following: `HTTP 429 Too Many Requests.
USER_INTERVAL_REQUEST_LIMIT_EXCEEDED`.

In the event of rate limiting or temporary unavailability, the API response may
include a `Retry-After` header, indicating the recommended duration
the client should wait before initiating a new request. If this header is not
present, the client must determine an appropriate retry interval based on the
specific rate limits established by the API.

## Rate Limits for the Pathfinder API

The [Pathfinder API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DPathfinder "https://app.leanix.net/openapi-explorer/?urls.primaryName=Pathfinder") is the core service that
allows you to work with your fact sheets. The API powers data and capabilities
behind the fact sheets functionality.

**Note**

Rate limits apply to both your interactions with fact sheets in the application
UI and your backend API calls.

| Type | Rate Limit |
| --- | --- |
| User-based rate limit | 1800 requests per minute per user (including both human users and<br>technical users) |
| Rate limit for internal requests | 1200 requests per minute per workspace for requests from specific<br>internal services listed below. These services automatically<br>reschedule rate-limited requests for you. This applies to:<br>- [Import Export API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DImport%2520Export "https://app.leanix.net/openapi-explorer/?urls.primaryName=Import%20Export")<br>  <br>- [Integration API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DIntegration%2520API "https://app.leanix.net/openapi-explorer/?urls.primaryName=Integration%20API")<br>  <br>- [Integration ServiceNow API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DIntegration%2520ServiceNow "https://app.leanix.net/openapi-explorer/?urls.primaryName=Integration%20ServiceNow")<br>  <br>- [Integration Signavio API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DIntegration%2520Signavio "https://app.leanix.net/openapi-explorer/?urls.primaryName=Integration%20Signavio") |

Rate Limits for the Pathfinder API

## Rate Limits for the Self-Built Software Discovery API

The [Self-Built Software Discovery API![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fapp.leanix.net%2Fopenapi-explorer%2F%3Furls.primaryName%3DSelf-Built%2BSoftware%2BDiscovery "https://app.leanix.net/openapi-explorer/?urls.primaryName=Self-Built+Software+Discovery") applies
rate limits to the following endpoints:

| Endpoint | Description | Rate Limit |
| --- | --- | --- |
| `POST /factSheets/{factSheetId}/sboms` | Upload an SBOM file for a specific fact sheet | 300 requests per minute per workspace |
| `PUT /manifests` | Upload a manifest file | 300 requests per minute per workspace |
| `GET<br>/applications/{factSheetId}/components` | Retrieve discovered SBOM library components for a business<br>application | 300 requests per minute per workspace |
| `GET /components/search` | Search for SBOM library components by package URL | 300 requests per minute per workspace |

Rate-Limited Endpoints

If your integration exceeds these limits, the API returns an HTTP `429 Too
Many Requests` response. To handle rate limit responses gracefully,
build retry logic with exponential backoff into your integration.

**Sample Code**

```
import time
from requests.exceptions import HTTPError
def request_with_retry(request_func, max_retries=3, base_delay=1):
    """Execute request with exponential backoff on rate limit."""
    for attempt in range(max_retries):
        response = request_func()
        if response.status_code == 429:
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            continue
        response.raise_for_status()
        return response
    raise HTTPError("Max retries exceeded due to rate limiting")
```
