<!-- Source: https://help.sap.com/docs/leanix/ea/reporting-framework-and-cli -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Reporting Library and Custom Report Tools

Build custom reports using the SAP LeanIX Reporting
Library and Custom Report Tools.

## Overview

SAP LeanIX offers
a wide range of standard out-of-the-box reports. However, standard reports may be
insufficient for your organization. For more details on out-of-the-box reports, see
[Reports](https://help.sap.com/docs/leanix/ea/reports?locale=en-US&state=PRODUCTION&version=CLOUD "Reports transform fact sheet and meta model data into structured visualizations and analytical views that help you analyze your IT landscape, assess key metrics, identify trends, and monitor changes over time.")

As a developer, you can build custom reports using the reporting toolset, which
consists of two components:

- [SAP LeanIX Reporting Library![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgithub.com%2Fleanix%2Fleanix-reporting "https://github.com/leanix/leanix-reporting"): The library provides a connection to the
SAP LeanIX app, allowing you to create custom reports using workspace data and
functionality.

- [SAP LeanIX Custom Report Tools![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fwww.npmjs.com%2Fpackage%2F%40sap%2Fcreate-leanix-custom-report "https://www.npmjs.com/package/@sap/create-leanix-custom-report"): Create, develop,
build, and upload custom reports to your workspaces and the SAP LeanIX
Store.

## Reporting Library

The SAP LeanIX
Reporting Library is built into SAP LeanIX. It
exposes the `lx` API. Your custom report uses this API to connect to
the workspace, query data, and integrate with the SAP LeanIX user
interface.

The reporting library provides these features:

- Filtering of fact sheet information

- View selection

- Tabular view of report data

- Export to PDF and PNG files

- Choice of visualization options

Links to the reporting library:

- Library: [GitHub - leanix/leanix-reporting: Library to develop custom reports for LeanIX.![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgithub.com%2Fleanix%2Fleanix-reporting "https://github.com/leanix/leanix-reporting")

- API Documentation: [Reporting Library documentation![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fleanix.github.io%2Fleanix-reporting%2Findex.html%3Flocale%3Den-US "https://leanix.github.io/leanix-reporting/index.html?locale=en-US")

The documentation provides a comprehensive reference for enumerations,
classes, interfaces, type aliases, variables, and more.

## Custom Report Tools

The SAP LeanIX
custom report tools scaffold a new project with a React/TypeScript template and a
pre-configured Vite build setup. The Vite build setup handles the development
server, production build, and workspace upload.

### Report Tools Options

To see all available options, run:

```
npm create @sap/leanix-custom-report@latest -- --help
```

### Create a New Report

Use the CLI to bootstrap a new project:

```
npm create
                  @sap/leanix-custom-report@latest
```

Follow the interactive prompts to configure the report ID, title, author, and
workspace credentials. The tool generates a ready-to-use template-report with
React and TypeScript. To learn more, see [Creating Your Custom Report Project](https://help.sap.com/docs/leanix/ea/setting-up-your-custom-reports-project?locale=en-US "https://help.sap.com/docs/leanix/ea/setting-up-your-custom-reports-project?locale=en-US").

### Develop, Build, and Upload

Once your project is created, the following npm scripts are available:

|     |     |
| --- | --- |
| Command | Description |
| `npm run build` | Build the report for production |
| `npm run dev` | Start the local development server with hot module<br>replacement. Code edits will be automatically reflected once<br>saved. |
| `npm run upload` | Build and upload the report to your SAP LeanIX<br>workspace |

**Tip**

Before you start developing, initialize a git repository in your project
directory.

Run: `git init && git add . && git commit -m "Initial
commit"`

Use `add` and `commit` regularly to create a
log of your changes. This gives you recovery points if you need to undo
changes.

For more information, refer to the [Git documentation![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgit-scm.com%2Fdoc "https://git-scm.com/doc").

Links to custom report tools:

- Package including documentation: [GitHub - SAP/leanix-custom-report-tools: SAP LeanIX custom report tools![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fgithub.com%2FSAP%2Fleanix-custom-report-tools "https://github.com/SAP/leanix-custom-report-tools")

- npm scaffolding tool: [https://www.npmjs.com/package/@sap/create-leanix-custom-report![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fwww.npmjs.com%2Fpackage%2F%40sap%2Fcreate-leanix-custom-report "https://www.npmjs.com/package/@sap/create-leanix-custom-report")

## Required Knowledge

To work with the Reporting Library and Custom Report Tools, you should have a working
knowledge of the following:

- Command-line interface

- React/TypeScript

Depending on the use case, you may need knowledge and skills in other areas.

## Tutorials

To learn how to build custom reports using the reporting toolset, see our tutorials
in [Custom Reports](https://help.sap.com/docs/leanix/ea/custom-reports?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to build custom reports tailored to your organization's needs.").
