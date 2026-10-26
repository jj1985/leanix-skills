<!-- Source: https://help.sap.com/docs/leanix/ea/workspace-administration -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Workspace Administration

The workspace administration area is a centralized hub for managing and customizing
your workspace. As an admin, you can adjust workspace settings to best suit the needs of
your team.

## Navigating to the Administration Area

Once you've set up your account
with SAP LeanIX,
you can navigate to the workspace administration area by selecting
Administration in the user profile menu.

![Navigating to the Administration Area from the User Profile Menu](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274d8a7b7a4410148b66f1c79bd138bb_LowRes.png)

Navigating to the Administration Area from the User Profile Menu

## Configuring Workspace Settings

You can configure workspace settings by
navigating to the corresponding sections of the administration area. For an overview
of settings, see [Workspace Settings Overview](https://help.sap.com/docs/leanix/ea/workspace-settings-overview?locale=en-US&state=PRODUCTION&version=CLOUD "Overview of settings available in the workspace administration area.").

To get started, you can do the following:

- Customize branding settings: To align the workspace with your
organization's brand identity, navigate to the Branding section in the
administration area and make the necessary adjustments. To learn more, see [Branding](https://help.sap.com/docs/leanix/ea/branding-settings?locale=en-US&state=PRODUCTION&version=CLOUD "Personalize your workspace's appearance to reflect your brand identity or choose from one of the predefined workspace designs.").

- Set the default language: Navigate to the General section in the
administration area and select a language in the Default Language list.
This action sets the default language for new users and existing users who
haven't yet set their language preference. Users can change their workspace
language in the user profile.

- Configure notification settings: Configure default notification settings
for workspace users. For more information, see [Notifications Center](https://help.sap.com/docs/leanix/ea/notifications-center?locale=en-US&state=PRODUCTION&version=CLOUD "Configure notification settings for your workspace."). Users can then
adjust their notification preferences in the Notifications section.

- Adjust other basic settings: You can start by adjusting settings in the
General section and then proceed to customize other settings as per
your organization's requirements.

## Managing User Access and Permissions

Once you've configured basic
workspace settings, you can start inviting users. To streamline the process of user
access management, consider setting up single sign-on (SSO) for your organization.
This will allow users to access the workspace from your SSO identity provider,
enhancing security and convenience. To learn how to manage user access with and
without SSO, see [Managing Users](https://help.sap.com/docs/leanix/ea/managing-users?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to manage user access and roles with and without single sign-on (SSO).").

You can manage fact sheet permissions for non-admin user roles in the Meta
Model Configuration section of the administration area.
Additionally, you can configure role-based permissions that are not related to fact
sheets in the User Roles and Permissions section of the
administration area. For more details, see [Role-Based Permissions](https://help.sap.com/docs/leanix/ea/user-roles-and-permissions?locale=en-US&state=PRODUCTION&version=CLOUD#loio275def827a4410149362f3672c614956__role-based_permissions).

If needed, you can set up virtual workspaces to limit access to specific inventory
data. For more information, see [Virtual Workspaces](https://help.sap.com/docs/leanix/ea/virtual-workspaces?locale=en-US&state=PRODUCTION&version=CLOUD "Manage access to fact sheets for custom user groups").

## Switching Your User Role

As an admin, you can temporarily sign in to
the workspace under a different user role. This enables you to preview the workspace
as it appears to specific roles when you modify certain settings. Switching the user
role does not allow you to sign in under a specific user account and is not
associated with user impersonation.

To switch your user role, in the user profile menu, select Switch user
role, select a role, then click Login. If
activated, you can also switch between Access Control Entities (ACEs). For more
information, see [Virtual Workspaces](https://help.sap.com/docs/leanix/ea/virtual-workspaces?locale=en-US&state=PRODUCTION&version=CLOUD "Manage access to fact sheets for custom user groups").

To switch your user role back and sign in as admin, in the user profile menu, select
Switch user role, then click Re-login as Admin in the dialog that
appears.

## Enabling Maintenance Mode for a Workspace

When applying significant changes to your workspace, you can temporarily enable maintenance mode
to prevent non-admin users from accessing the workspace. To minimize disruption to
user workflows, consider conducting maintenance outside of regular business hours.
For more information, see [Maintenance Mode](https://help.sap.com/docs/leanix/ea/general-settings?locale=en-US&state=PRODUCTION&version=CLOUD#loio275959347a44101489cfee4fe45f7c0f__maintenance_mode).

## Finding the Workspace ID

When configuring integrations and working with
APIs, you may need the workspace ID. To find the workspace ID, navigate to the
API Tokens section in the administration area and locate the
`WorkspaceId` value.
