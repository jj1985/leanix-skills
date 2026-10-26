<!-- Source: https://help.sap.com/docs/leanix/ea/getting-started-with-integration-api -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Getting Started with the Integration API

## Overview

To get started with the Integration API, use the built-in user interface in the
Integration API section of the administration area. Here, you can:

- View, modify, and run preconfigured processors.

- Create and manage processors.

- Complete test runs without the risk of overwriting or deleting workspace
data.

- Run processors to import or export data to and from your workspace.

- Get the data model of your workspace in JSON format, which includes the keys of
meta model attributes.

![Integration API Page in the Administration Area](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio275516587a441014ae78f8daf95aeacd_LowRes.png)

Integration API Page in the Administration Area

## Key Concepts

- Processor: A processor defines an action to be executed on each content
object of the incoming LDIF.

- Connector: A connector is not an entity within the Integration API but a
middleware that creates an LDIF. It defines a set of meta properties the
Integration API uses to bind incoming LDIF to a processor configuration. These
properties are: `connectorType`, `connectorId`, and `connectorVersion`.

- Processing direction: The direction of data processing:

  - Inbound: Data is imported from an external system to SAP LeanIX in LDIF format. For more information, see [Inbound Processors](https://help.sap.com/docs/leanix/ea/inbound-processors?locale=en-US&state=PRODUCTION&version=CLOUD).

  - Outbound: Data is exported from SAP LeanIX to an external system in LDIF format. For more information, see [Outbound Processors](https://help.sap.com/docs/leanix/ea/outbound-processors?locale=en-US&state=PRODUCTION&version=CLOUD).
- Processing Modes: The mode of data processing:

  - Full: The connector expects the complete set of data. You can
    apply `deletionScope`, and any data not sent as part of the run
    can be archived from the workspace.

  - Partial: The connector expects a subset of data.
- Integrated Tool: The third-party system from which the data is imported
or to which it's exported.

**Note**

Even though you can use outbound processors, it's recommended to use the [writeToLdif](https://help.sap.com/docs/leanix/ea/inbound-processors?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a8a067a4410148b1fcfe89dcdedca__write_to_ldif) inbound processor to export data in LDIF format
instead.

## Preconfigured Processors

To get started, you can review the
configuration of preconfigured processors marked with the lock icon on the
Integration API page. These processors cover typical scenarios for
importing data into your workspace:

- Import Applications Example: This processor imports application fact
sheets with basic attributes, tags, subscriptions, and relations.

- Import Hierarchy Example: This processor imports business capability fact
sheets with basic attributes and relation hierarchy, including parent and child
fact sheets.

- CMDB Connector Example: This processor imports data from a CMDB to your
workspace, including:

  - IT component, provider, and application fact sheets

  - Relations from IT components to applications and providers

  - Links added as resources (documents) on fact sheets

You can perform test runs for these processors and preview the results in the
Output Log section. Use these examples as a basis to create your own
processors by copying the configuration and adjusting the scope to your needs.

![Preconfigured Processors](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2741aa4e7a44101499aed257d20dd735_LowRes.png)

Preconfigured Processors

## Configuring a Processor

Follow these steps:

1. In the administration area, go to the Integration API section.

2. Click New Processor Configuration.

3. Specify the processor details, then click Save. Once you save the
processor, you can add new versions and update the integrated tool. You
can't change any other details.

![Creating a Processor](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2756be227a441014b511ee2e57d981a3_LowRes.png)

Creating a Processor

4. On the left side of the configuration page, define the processor
configuration. You can add multiple processors.

5. In the Input section, enter the following depending on the processor
direction:

   - Inbound: Enter the data to be imported in LDIF format. For more details,
     see [LeanIX Data Interchange Format (LDIF)](https://help.sap.com/docs/leanix/ea/integration-api?locale=en-US&state=PRODUCTION&version=CLOUD#loio275a99087a441014a04fa6cda4e0ec2b__leanix_data_interchange_format_ldif).

   - Outbound: To define the scope of data to export in LDIF format,
     in the upper-right corner, click the three-dot icon > Define Scope, then select fact sheets using inventory filters. The
     `scope` in
     the processor configuration on the left side is populated
     accordingly.
6. Click Save.

After saving a processor, you can test and run it, as described in the following
sections.

![Processor Configuration Page](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio27540a997a4410149bb78ff47132e7ee_LowRes.png)

Processor Configuration Page

**Note**

Processor configuration and data are strictly separated in the Integration API to
ensure synchronization runs are reliable, repeatable, and auditable. Whenever
you save the configuration of processors, only the processors are stored. The
system does not store any LDIF data.

## Testing a Processor

To verify the processor configuration, you can
complete a test run. This doesn't apply any changes to your workspace.

To complete a test run, click Test Run at the bottom of the processor page.
The results of the test run appear in the Output Log section. Review the
output for possible errors and update the processor configuration or input as
needed.

![Output Log](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2743adc17a441014be9afd2d2c2f6e60_LowRes.png)

Testing a Processor and Previewing Results in the Output Log

## Running a Processor

After successfully testing a processor, you can run
it. This applies changes to your workspace, so always ensure to test your processors
first.

To run a processor, click Run at the bottom of the processor page. The results
appear in the Output Log section.

## Saving New Processor Versions

You can update the processor
configuration and save it as a new version without deleting the previous version.
This allows you to maintain a history of changes.

Always version processors using the `number.number.number` format,
such as `1.0.0`. This convention helps maintain the processor's
version history and supports versioning during configuration updates.

To save a configuration to a new version, in the upper-right corner of the processor
page, click the three-dot icon > Save New Version, then enter the version
details and click OK.

![Saving a New Processor Version](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio27580c767a441014b1f5f394c5c082cb_LowRes.png)

Saving a New Processor Version

You can switch between the processor versions by using the drop-down list at the top
of the processor page.

![Processor Versions](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio275104af7a44101489f3ff00a87f0bc2_LowRes.png)

Processor Versions

## Getting the Data Model of Your Workspace

The data model of your workspace provides the meta model attributes in JSON format. Each fact
sheet attribute is uniquely identified by an attribute key, also known as the
technical name. To learn more about attribute keys in the meta model configuration,
see [Attribute Key](https://help.sap.com/docs/leanix/ea/meta-model-configuration?locale=en-US&state=PRODUCTION&version=CLOUD#loio275955467a441014a5dce078bf2e383c__attribute_key).

To get the data model of your workspace, in the upper-right corner of the processor
page, click the three-dot icon > Get Data Model.

The data model in JSON format is returned in the Output Log section. You can
copy attribute keys from here and use them in your configurations.

![Getting the Data Model of a Workspace](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274d82bd7a441014b8d2f9c0c0874f99_LowRes.png)

Getting the Data Model of a Workspace

## Managing Processors

- Updating the configuration: To update the processor configuration, make
the necessary changes and then click Save. Note that the system doesn't
save input data.

- Updating the integrated tool: You can update the integrated tool
associated with the processor from the Integration API page.

- Deleting a processor: Be cautious with this action, as it cannot be
undone. To delete a processor, click the three-dot icon in the upper-right
corner of the processor page, then select Delete Configuration.
