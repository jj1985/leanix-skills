<!-- Source: https://help.sap.com/docs/leanix/ea/quick-start-guide-for-mcp-server -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Quick Start Guide for the MCP Server

Get started with the SAP LeanIX MCP server.
Install an MCP client, connect to the MCP server, and explore your workspace data using
plain language.

## Overview

The SAP LeanIX
MCP server connects external MCP clients to your workspace data through the Model
Context Protocol (MCP). Before you start building workflows or exploring use cases,
this page walks you through the key steps to get connected and understand how the
server works in practice.

## Before You Start

Keep the following in mind before you get started with the MCP server:

- Results may vary. Responses through the MCP server are
non-deterministic. This is expected. Results depend on the model, its
configuration, and the data in your workspace.

- Your workspace admin configures MCP server settings.
This configuration affects all MCP connections to the workspace from
individual users. If you have questions about the MCP server configuration,
contact your workspace administrator.

- Your permissions affect what you can do. The capabilities and actions
available to you depend on your user role and the permissions assigned to
this role. If a capability is missing or you can't perform specific
operations, clarify your permissions with the workspace administrator. Learn
more in [MCP Server Permissions](https://help.sap.com/docs/leanix/ea/mcp-server-permissions?locale=en-US&state=PRODUCTION&version=CLOUD "MCP server permissions are role-based controls that determine what actions users can perform in SAP LeanIX through an AI assistant. Administrators configure permissions in the workspace administration area.").

## Prerequisites

Workspace administrators configure basic settings for the MCP server that affect all
user connections to the workspace. Go to Administration >
MCP Server, then configure the following:

- Authentication methods: Configure the allowed
authentication methods for the workspace using the corresponding toggles.
Learn more in [Configure Authentication Settings](https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server?locale=en-US&state=PRODUCTION&version=CLOUD#loio19c0723e588e43519756d8bebf163048__configure-authentication-settings).

- Progressive tool discovery: This workspace-level setting
controls how the MCP server presents its tools to AI agents. We recommend
enabling this setting because it significantly reduces token consumption.
Learn more in [Progressive Tool Discovery](https://help.sap.com/docs/leanix/ea/progressive-tool-discovery?locale=en-US&state=PRODUCTION&version=CLOUD "Progressive tool discovery is a workspace-level setting that significantly reduces token consumption. Instead of loading the full tool catalog upfront, the MCP server exposes tools only when an agent searches for them.").

## Step 1: Install an MCP Client

An MCP client is an application that connects to the MCP server. MCP clients are also
referred to as AI clients, agentic clients, or AI coding assistants. Common clients
include Claude Code, Microsoft Copilot, GitHub Copilot, Cline, Cursor, and
Goose.

Install an MCP client that your organization has approved. Verify that the client
supports MCP interactions. If you're unsure which client to use, contact your IT
team or administrator.

## Step 2: Connect to the MCP Server

Connect your client to the MCP server using the appropriate endpoint. To determine which
authentication method is allowed and recommended for use within your organization,
contact your workspace administrator. For details, see [Connecting to the MCP Server](https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to configure authentication settings and connect to the SAP LeanIX MCP server.").

We recommend connecting to the MCP server using OAuth:

```
https://mcp.leanix.net/services/mcp-server/v1/mcp/instance/{SUBDOMAIN}/workspace/{WORKSPACE-NAME}
```

Replace `{SUBDOMAIN}` and `{WORKSPACE_NAME}` with your values.
You can copy them from the workspace URL:
`https://{SUBDOMAIN}.leanix.net/{WORKSPACE_NAME}/`.

**Tip**

You can find the MCP connection endpoint for your workspace in
Administration \> MCP
Server.

## Step 3: Ask Your First Question

After connecting to the MCP server, use plain language to explore your workspace
data. To get started, try prompts like the following:

- "How many fact sheets do we have in the workspace?"

- "Show me applications with a broken quality seal."

- "Which IT components have no owner assigned?"

- "List initiatives that are currently in progress."

- "What is the lifecycle status of our CRM application?"

Check results against your workspace to verify the connection is working as
expected.

## Step 4: Explore Available Capabilities

The MCP server exposes API capabilities as discoverable tools that AI applications
can invoke. Related tools are organized into toolsets—named collections that let you
control what an agent sees in a single session. To learn more about available
toolsets and how to use them, see [MCP Server Toolsets](https://help.sap.com/docs/leanix/ea/mcp-server-toolsets?locale=en-US&state=PRODUCTION&version=CLOUD "The SAP LeanIX MCP server exposes its capabilities as tools that AI agents can discover and invoke. Explore the available toolsets and learn how tools are loaded.").

To understand what operations are available, browse the tools exposed by the MCP server. You
can ask questions such as the following:

- "What can you do in my connected LeanIX workspace?"

- “What tools are available for LeanIX?”

- “What operations does the LeanIX MCP server support?”

The response contains the tools and actions available to you. If a tool is missing,
contact your workspace administrator to verify your permissions.

## Next Steps

Build skills and agents to automate workflows: Once you’ve
tested basic queries and explored what’s possible with the MCP server, you can
create skills to automate repetitive tasks. A skill is a pre-built, reusable prompt
or workflow that automates a specific task using the MCP server tools. Then you can
connect additional data sources and build custom agents tailored to your enterprise
architecture use cases. Start with the most common scenarios and then create more
agents based on your organization’s needs.
