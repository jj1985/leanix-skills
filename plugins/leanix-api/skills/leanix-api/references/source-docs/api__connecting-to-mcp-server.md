<!-- Source: https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Connecting to the MCP Server

Learn how to configure authentication settings and connect to the SAP LeanIX MCP
server.

## Overview

The MCP server is enabled by default for all SAP LeanIX
workspaces.

Admin users configure allowed authentication methods for the MCP server. Users then connect to
it through their AI client using the corresponding method.

## Configure Authentication Settings

1. Go to Administration \> MCP Server.

2. On the MCP server configuration page, choose your preferred authentication methods. Both
methods are enabled by default:

   - User-Based Authentication: Allows individual
     users to authenticate using OAuth.

   - Technical Users: Allows technical users
     (service accounts) to authenticate using API tokens.

**Note**

The MCP server is enabled by default. To disable it for a workspace, turn off the
corresponding toggle on the MCP server configuration page. When disabled, the
system rejects all connections regardless of allowed authentication methods.

## Permissions

When you connect to the MCP server, the tools available to you depend on the features
and permissions your administrator has enabled for your user role. Your role also
determines whether you have read or write access to workspace data through MCP. For
details, see [MCP Server Permissions](https://help.sap.com/docs/leanix/ea/mcp-server-permissions?locale=en-US&state=PRODUCTION&version=CLOUD "MCP server permissions are role-based controls that determine what actions users can perform in SAP LeanIX through an AI assistant. Administrators configure permissions in the workspace administration area.").

## Authentication Methods

The authentication method you use depends on whether you're connecting as an individual user
or as a technical user. Your workspace administrator configures the allowed
authentication methods. If an administrator disables an authentication method, the
system rejects the corresponding requests.

| Authentication Method | Description | Endpoint | Details |
| --- | --- | --- | --- |
| User-based authentication (OAuth) | Individual users authenticate through the OAuth 2.0 flow. They’re prompted to<br>authenticate from their browser. Authentication expires after 24<br>hours. | `https://mcp.leanix.net/services/mcp-server/v1/mcp`<br>Alternative endpoint for connecting to a specific workspace<br>without manually entering workspace details in the browser<br>during authentication:<br>`https://mcp.leanix.net/services/mcp-server/v1/mcp/instance/{SUBDOMAIN}/workspace/{WORKSPACE-NAME}` | [OAuth](https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server?locale=en-US&state=PRODUCTION&version=CLOUD#loio19c0723e588e43519756d8bebf163048__oauth) |
| Technical user authentication | Technical users (service accounts) authenticate using an API<br>token.<br>Technical users are intended for automated workflows,<br>integrations, and non-interactive access. For details on<br>generating an API token, see [Technical Users](https://help.sap.com/docs/leanix/ea/technical-users?locale=en-US&state=PRODUCTION&version=CLOUD "Get an API token by creating a technical user in SAP LeanIX."). | `https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp` | [Technical User Authentication](https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server?locale=en-US&state=PRODUCTION&version=CLOUD#loio19c0723e588e43519756d8bebf163048__section_hxk_th4_2hc) |

## OAuth

OAuth is the recommended method for user-based access to the MCP server. Users authenticate
through the OAuth 2.0 flow. No credentials are passed directly in the request
header.

Authentication expires after 24 hours. Re-authenticate when your session expires.

MCP server endpoint for OAuth:

```
https://mcp.leanix.net/services/mcp-server/v1/mcp
```

Use this URL in your AI client to authenticate. You're prompted to sign in to your workspace
from your browser. During the authentication process, enter the subdomain and
workspace name for the workspace you want to connect to. You can find these values
in the workspace URL:
`https://{SUBDOMAIN}.leanix.net/{WORKSPACE_NAME}/`.

**Example**

Example request for Claude
Code:

```
claude mcp add --transport http leanix https://mcp.leanix.net/services/mcp-server/v1/mcp
```

Alternatively, use the following endpoint to authenticate to a specific workspace
without manually entering workspace details in your browser. Replace
`{SUBDOMAIN}` and `{WORKSPACE_NAME}` with your
values.

```
https://mcp.leanix.net/services/mcp-server/v1/mcp/instance/{SUBDOMAIN}/workspace/{WORKSPACE-NAME}
```

## Technical User Authentication

Technical users (service accounts) authenticate using an API token. For details on
generating an API token, see [Technical Users](https://help.sap.com/docs/leanix/ea/technical-users?locale=en-US&state=PRODUCTION&version=CLOUD "Get an API token by creating a technical user in SAP LeanIX.").

MCP server endpoint for technical user authentication:

```
https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp
```

Replace `{SUBDOMAIN}` with your workspace subdomain. You can copy it from your
workspace URL:
`https://{SUBDOMAIN}.leanix.net/{WORKSPACE_NAME}/`.

**Note**

When configuring API token permissions, use the minimum permissions required for
the intended use case. Admin-level permissions can cause unintended actions,
such as sending surveys or creating duplicate architecture decisions.

### API Token Header

You can pass the API token directly in the Authorization header:

```
Authorization: Token {YOUR-API-TOKEN}
```

### Basic Authentication Header

If your client doesn’t support the Authorization token, you can use Basic
authentication. Set `apitoken` as the username and your API token
as the password, then encode both in Base64:

```
Authorization: Basic BASE64(apitoken:{YOUR-API-TOKEN})
```

### Bearer Token Authentication

If you want to use a JWT access token, authenticate using a Bearer token in the
Authorization header:

```
Authorization: Bearer {YOUR-JWT}
```

### Client Configuration

You can connect to the MCP server using any clients that support MCP connections. Use the
following example configurations for reference. For details on how to connect to
an MCP server, refer to the official documentation of your AI client.

Claude Code

Before you start, ensure that you have `npx` installed on your
Claude Desktop client.

**Example**

```json
{
  "mcpServers": {
    "LeanIX MCP Server Remote": {
        "command": "npx",
        "args": [
            "-y",
            "mcp-remote",
            "https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp",
            "--header", "Authorization: Token {YOUR-API-TOKEN}"
      ]
    }
  }
}
```

Cline

**Example**

```json
{
  "mcpServers": {
   "leanix-remote-http": {
      "type": "streamableHttp",
      "url": "https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp",
      "headers": {
        "Authorization": "Token {YOUR-API-TOKEN}"
      }
    }
  }
}
```

Cursor

**Example**

```json
{
  "mcpServers": {
    "lx-remote-basic": {
      "transport": "streamableHttp",
      "url": "https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp",
      "headers": {
        "Authorization": "Token {YOUR-API-TOKEN}"
      }
    }
  }
}
```
