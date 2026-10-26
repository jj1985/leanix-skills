<!-- Source: https://help.sap.com/docs/leanix/ea/mcp-server -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# MCP Server

Connect external AI applications to SAP LeanIX using the
Model Context Protocol (MCP) server to securely access enterprise architecture
data.

**Note**

The MCP server is not an AI capability and doesn't require AI units. It's available
in all workspaces with SAP LeanIX Application Portfolio Management without requiring
additional licenses.

## Overview

The Model Context Protocol (MCP) is an emerging open standard that defines how AI
applications can discover and interact with tools, such as APIs or functions, by
receiving structured context. Instead of merely connecting systems, MCP helps AI
tools understand available capabilities, how to use them, and the data they operate
on.

MCP enables AI agents to securely and consistently connect to external data, such as
enterprise architecture data in SAP LeanIX,
which is presented as tools. These agents can understand and interact with external
data, enabling developers to build their own AI-driven solutions or workflows.

For comprehensive details on MCP, refer to the [MCP specification![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fmodelcontextprotocol.io%2F "https://modelcontextprotocol.io/").

![Diagram showing MCP server connecting AI clients to SAP LeanIX data and APIs.](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio525a7a61eb1e46ce91624ac5027d6e41_LowRes.png)

MCP Server

## Benefits

- Standard gateway to connect AI agents to enterprise architecture data

- Secure connection between AI agents and your SAP LeanIX instance

- Acceleration of adoption and value realization for agentic AI applications in
enterprise architecture

## How the MCP Server Works

SAP LeanIX uses
MCP to expose selected APIs as AI tools, making them understandable and invokable by
AI applications. These tools are described in a structured, standardized format that
includes descriptions, inputs, and output types. This setup enables large language
models (LLMs) to facilitate the exposed APIs by using the structured metadata
provided by MCP.

Here's an example scenario:

1. An AI assistant asks, "What tools can I use?"

2. The MCP server returns a list of capabilities in SAP LeanIX.

3. The assistant can then invoke tools like "Get application by ID" or "List
fact sheets with low completeness score" as part of its workflow.

This process aligns with current LLM architectures.

## Connecting to the MCP Server

To learn how to connect to the MCP server from your AI client, visit [Connecting to the MCP Server](https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to configure authentication settings and connect to the SAP LeanIX MCP server.").

## Interacting with the MCP Server

After you connect to the MCP server in your AI client, use natural language to
interact with it. Ask questions about your workspace and retrieve the data you need,
such as "How many IT components do I have in the inventory?" or "Return applications
with the broken quality seal."

The MCP server returns responses in text form. When available, you can navigate to
your workspace directly from the chat using the provided links.

## MCP Tools

The MCP server exposes API capabilities as discoverable tools that AI applications
can invoke. Each tool includes structured metadata that describes inputs, outputs,
and usage so that an AI agent can discover what the tool does and how to call it.
Related tools are organized into toolsets — named collections that let you control
what an agent sees in a single session.

For detailed information, see [MCP Server Toolsets](https://help.sap.com/docs/leanix/ea/mcp-server-toolsets?locale=en-US&state=PRODUCTION&version=CLOUD "The SAP LeanIX MCP server exposes its capabilities as tools that AI agents can discover and invoke. Explore the available toolsets and learn how tools are loaded.").

## MCP Apps

MCP apps are interactive user interfaces that display your workspace data directly
within your AI chat conversation. If your AI client supports MCP apps, the MCP
server automatically renders data as visual components within the chat. This allows
you to interact with your workspace data visually without leaving the
conversation.

For detailed information, see [MCP Apps](https://help.sap.com/docs/leanix/ea/mcp-apps?locale=en-US&state=PRODUCTION&version=CLOUD "MCP apps are interactive user interfaces provided by the SAP LeanIX MCP server that render your workspace data as visual components directly within a supported AI client.").

## Streaming Mechanism

The MCP server supports the HTTP streaming mechanism for delivering responses as
they're generated. This means AI applications don't have to wait for the full result
when calling a tool. They can start receiving partial updates immediately. This
enhances responsiveness and the user experience.

## Related Information

- [Connecting to the MCP Server](https://help.sap.com/docs/leanix/ea/connecting-to-mcp-server?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to configure authentication settings and connect to the SAP LeanIX MCP server.")

- [MCP Server Toolsets](https://help.sap.com/docs/leanix/ea/mcp-server-toolsets?locale=en-US&state=PRODUCTION&version=CLOUD "The SAP LeanIX MCP server exposes its capabilities as tools that AI agents can discover and invoke. Explore the available toolsets and learn how tools are loaded.")

- [MCP Apps](https://help.sap.com/docs/leanix/ea/mcp-apps?locale=en-US&state=PRODUCTION&version=CLOUD "MCP apps are interactive user interfaces provided by the SAP LeanIX MCP server that render your workspace data as visual components directly within a supported AI client.")
