<!-- Source: https://help.sap.com/docs/leanix/ea/user-roles-and-permissions -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# User Roles and Permissions

Adjust role-based permissions and define custom roles.

In the User Roles and Permissions section of the
administration area, you can:

- Create custom user roles — if you’re managing roles within your single sign-on
(SSO) identity provider (IdP)

- Edit translations for user roles

- Modify role-based permissions unrelated to fact sheets

## User Roles

In SAP LeanIX,
the following standard user roles are available by default: Viewer, Member, and
Admin. If SSO is enabled for your organization and you're managing roles within your
IdP, you can create custom roles in addition to standard ones.

## Standard User Roles

The following table lists standard user roles available in SAP LeanIX.

| User Role | Default Fact Sheet Permissions |
| --- | --- |
| Viewer | Can view, subscribe to, and comment on all fact sheets. |
| Member | Can view, create, and modify all fact sheets. |
| Admin | Has all permissions of a member user as well as administrator<br>permissions for a workspace. |

As an admin, you can adjust permissions for non-admin roles. For more information,
see [Role-Based Permissions](https://help.sap.com/docs/leanix/ea/user-roles-and-permissions?locale=en-US&state=PRODUCTION&version=CLOUD#loio275def827a4410149362f3672c614956__role-based_permissions).

**Note**

You cannot delete standard user roles.

## Custom User Roles

When configuring SSO for SAP LeanIX, you
choose how you want to manage user roles: internally within SAP LeanIX or
externally within your IdP. For more information, see [Managing User Roles with SSO](https://help.sap.com/docs/leanix/ea/single-sign-on-sso?locale=en-US&state=PRODUCTION&version=CLOUD#loio275cc8227a441014a371975e4b816f0a__managing-user-roles-with-sso).

The possibility to create custom user roles depends on how you manage roles:

- Managing user roles internally within SAP LeanIX: Only
standard roles are available: Viewer, Member, and Admin. You can not create
custom user roles.

- Managing user roles externally within your IdP: You can
create custom user roles in addition to standard ones. This lets you assign
permissions that are more granular than those provided by standard roles.

**Note**

- A standard role is still required for access, but the custom role takes
precedence.

- If a user is assigned multiple custom roles, their permissions are
aggregated.

## Creating Custom User Roles

Follow these steps:

1. In your IdP, add claims `role` and
`customer_roles`, then create the corresponding
roles.

   - `role`: Create
     the following roles using uppercase letters: `VIEWER`, `MEMBER`, and
     `ADMIN`.

   - `customer_roles`: Create custom user roles using
     uppercase letters, for example, `AUDITOR`.

     To learn more about attribute mapping, see [SSO Attribute Overview](https://help.sap.com/docs/leanix/ea/sso-attribute-overview?locale=en-US&state=PRODUCTION&version=CLOUD "Reference the SAML 2.0 attribute overview for required authentication attributes and optional authorization attributes for roles and access control entities.").
2. In SAP LeanIX, create the corresponding user roles in the User
Roles section of the administration area.

1. Click New User Role. You land on the role
      configuration page.

2. In the Technical Name field, enter the role
      name using uppercase letters as specified in your IdP, for example,
      `AUDITOR`. The name serves as the unique role
      ID.

3. Optional: Clone permissions for the custom role from an existing
      role. This is a one-time snapshot, not a dynamic relation that is
      actively maintained. If you skip this option, the new custom role
      gets a set of default permissions, ensuring that the workspace
      functions as expected.

4. Optional: Add translations for the technical name to provide a more
      user-friendly format for the role label. Translations appear in
      various areas of the application. Select languages, then enter a
      translation and description for each language.

5. Click Add.

6. Create more custom roles to match the role matrix in your IdP.

      ![Creating a Custom User Role](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio275036e07a441014ae15fcf078b15228_LowRes.png)

      Creating a Custom User Role
3. In SAP LeanIX, configure permissions for each custom role. To learn more about
permissions, see [Role-Based Permissions](https://help.sap.com/docs/leanix/ea/user-roles-and-permissions?locale=en-US&state=PRODUCTION&version=CLOUD#loio275def827a4410149362f3672c614956__role-based_permissions).

After you’ve configured custom roles, you can assign these roles to users in your
IdP. Users get access to SAP LeanIX with
the permissions that you configured.

With this configuration, you can’t assign custom roles to users in your SAP LeanIX
workspace. You can only do it in your IdP.

## Role-Based Permissions

In SAP LeanIX,
user permissions are based on their assigned roles. As an admin, you can configure
permissions for non-admin user roles as needed. Permissions fall into two main
categories:

- Fact sheet permissions: Configure these in the
Meta Model Configuration section of the
administration area. For more details, see [Fact Sheet Permissions](https://help.sap.com/docs/leanix/ea/fact-sheet-permissions?locale=en-US&state=PRODUCTION&version=CLOUD "Configure fact sheet permissions for non-admin user roles.").

- Permissions unrelated to fact sheets: Configure these in
the User Roles and Permissions section of the
administration area. For an overview of permissions, refer to the following
table. Permissions for the admin role are read-only to ensure all workspace
admins can view and modify items.

The table below lists permissions unrelated to fact sheets.

| Feature | Permissions | Related Information |
| --- | --- | --- |
| Architecture executive dashboard | - Read: View the architecture executive<br>  dashboard.<br>  <br>- Update: Update the architecture<br>  executive dashboard. | [Architecture Executive Dashboard](https://help.sap.com/docs/leanix/ea/architecture-executive-dashboard?locale=en-US&state=PRODUCTION&version=CLOUD "Gain business insight by monitoring, analyzing, and customizing the architecture executive dashboard with both predefined and custom KPIs.") |
| Portals | Open, delete, create, and update portals | [Portals](https://help.sap.com/docs/leanix/ea/portals?locale=en-US&state=PRODUCTION&version=CLOUD "Create customizable, secure entry points that provide non-IT users with curated enterprise architecture information, resources, and visual assets outside the main application.") |
| Collections | Manage collections and content within collections | [Collections](https://help.sap.com/docs/leanix/ea/collections?locale=en-US&state=PRODUCTION&version=CLOUD "Use collections to arrange dashboards, reports, and diagrams into custom groups.") |
| Surveys | Create and manage surveys | [Surveys](https://help.sap.com/docs/leanix/ea/creating-survey?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to create surveys, from defining the scope and designing questions to using advanced fields and templates. Learn how to make questions mandatory, add links and descriptions, and import/export surveys.") |
| Diagram templates | - Read, create, update, delete, unlock, and change the owner<br>  for diagram templates<br>  <br>- Generate diagrams from templates | [Diagram Templates](https://help.sap.com/docs/leanix/ea/diagram-templates?locale=en-US&state=PRODUCTION&version=CLOUD "Diagram templates provide reusable, standardized rules for visualizing live inventory data, enabling dynamic exploration and consistent documentation of your landscape. Use them to efficiently create, manage, and share up-to-date diagrams for analysis, stakeholder communication, and audits.") |
| Fact sheet shape templates | Manage fact sheet shape templates in diagrams: view, delete,<br>create, update, change the owner, change default settings, and<br>unlock custom templates | [Fact Sheet<br>Shape Templates](https://help.sap.com/docs/leanix/ea/fact-sheet-shape-templates?locale=en-US&state=PRODUCTION&version=CLOUD "Templates define shapes and colors for fact sheets in diagrams. Use them to maintain visual consistency across your organization's architecture documentation or apply industry-standard notations like SAP LeanIX and ArchiMate 3.2.") |
| Presentations | Manage presentations | [Presentations](https://help.sap.com/docs/leanix/ea/presentations?locale=en-US&state=PRODUCTION&version=CLOUD "Use presentations to share enterprise architecture insights from reports and diagrams with your organization, without the need to export data to external presentation tools.") |
| Discovery inbox | Access to discovery inboxes: SAP discovery, SaaS discovery, and<br>AI agent discovery | - [SAP Discovery Inbox](https://help.sap.com/docs/leanix/ea/sap-discovery-inbox?locale=en-US&state=PRODUCTION&version=CLOUD "Discovered products, services, and extensions from your SAP landscape appear in the SAP discovery inbox. Learn how to create, link, and reject fact sheets related to discovered items.")<br>  <br>- [SaaS<br>  Discovery Inbox](https://help.sap.com/docs/leanix/ea/saas-discovery?locale=en-US&state=PRODUCTION&version=CLOUD "SaaS discovery identifies your organization's SaaS applications by integrating with SSO, SASE, and CASB solutions. It then updates and enriches fact sheets using the reference catalog.")<br>  <br>- [AI Agent Discovery Inbox](https://help.sap.com/docs/leanix/ea/ai-agent-discovery-inbox?locale=en-US&state=PRODUCTION&version=CLOUD "AI agents, MCP servers, and AI models discovered across your enterprise landscape appear in the AI agent discovery inbox. Learn how to review, link, and reject fact sheets related to discovered items.") |
| Architecture decisions | - View, create, update, and delete architecture decisions<br>  <br>- Manage architecture decision templates | [Architecture<br>Decisions](https://help.sap.com/docs/leanix/ea/architecture-decisions?locale=en-US&state=PRODUCTION&version=CLOUD "Document, review, and track decisions about your enterprise architecture, and link each decision directly to the affected architecture components in your inventory.") |
| Architecture guidance | - Read: View architecture insights and<br>  perform the recommended steps<br>  <br>- Manage: Change the status of<br>  architecture insights and reset or archive insights | [AI-Assisted Architecture Guidance](https://help.sap.com/docs/leanix/ea/ai-assisted-architecture-guidance?locale=en-US&state=PRODUCTION&version=CLOUD "AI-assisted architecture guidance analyzes your IT landscape, offering personalized insights and actionable steps that use AI to help you optimize your enterprise architecture.") |
| Software bill of materials (SBOM) | - Read: View SBOM explorer and SBOM<br>  fact sheet widget<br>  <br>- Upload: Upload SBOM files | [Software Bill of Materials (SBOM)](https://help.sap.com/docs/leanix/ea/software-bill-of-materials-sbom?locale=en-US&state=PRODUCTION&version=CLOUD "To understand and manage dependencies among your microservices, generate SBOM files and ingest them into SAP LeanIX using our API.") |
| Tech stack discovery | - View tech stack discovery<br>  <br>- Create and update tech stacks | [Tech Stack Discovery from SBOMs](https://help.sap.com/docs/leanix/ea/tech-stack-discovery-from-sboms?locale=en-US&state=PRODUCTION&version=CLOUD "Automatically discover tech stacks from ingested SBOMs. Add custom tech stacks manually to complete your technology portfolio.") |
| Transformations | Read, create, update, delete, and execute transformations | [Transformations](https://help.sap.com/docs/leanix/ea/transformations?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to define and manage Transformations in the Initiative Fact Sheet.") |
| Developer tools | - Access the GraphQL editor.<br>  <br>- Enable the Copy as JSON Query option<br>  in the filter bar in the inventory to copy the current<br>  query. | [GraphQL API](https://help.sap.com/docs/leanix/ea/graphql-api?locale=en-US&state=PRODUCTION&version=CLOUD "Get started with the SAP LeanIX GraphQL API.") |

**Tip**

As a best practice, grant full permissions sparingly and avoid assigning all
available permissions to every role. By ensuring that only users with the
appropriate roles have the ability to modify data, you can maintain its quality
and prevent unintended changes.

## Configuring Role-Based Permissions

**Tip**

Configure fact sheet permissions for non-admin roles in the Meta Model
Configuration section of the administration area. For more
information, see [Fact Sheet Permissions](https://help.sap.com/docs/leanix/ea/fact-sheet-permissions?locale=en-US&state=PRODUCTION&version=CLOUD "Configure fact sheet permissions for non-admin user roles.").

To configure role-based permissions unrelated to fact sheets, follow these steps:

1. In the administration area, navigate to the User Roles and
Permissions section.

2. Select a role for which you want to configure permissions.

3. On the role editing page, navigate to the Permissions
tab.

4. Adjust permissions as needed using relevant checkboxes.

5. Save the changes.

![Adjusting Non-Fact-Sheet Permissions for the Viewer Role](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274d0c5a7a4410148c49c83a28791f66_LowRes.png)

Adjusting Permissions Unrelated to Fact Sheets for the Viewer
Role
