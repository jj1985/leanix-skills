<!-- Source: https://help.sap.com/docs/leanix/ea/technical-users -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Technical Users

Get an API token by creating a technical user in SAP LeanIX.

## Overview

Admin users generate an API token by creating a technical user. Use API tokens in integrations or
to connect to APIs.

To learn how to authenticate to APIs, see [Authentication to SAP LeanIX Services](https://help.sap.com/docs/leanix/ea/authentication-to-sap-leanix-services?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to authenticate to SAP LeanIX services.").

## Usage Notes

With technical users, you get the following benefits:

- Integrations are no longer tied to a specific person, which allows you to avoid
problems such as the person being on vacation or otherwise unavailable.

- Users who don't have access to a workspace can still manage integrations and
access SAP LeanIX
APIs.

- Technical users can be subscribed to fact sheets for better integration
building.

- Technical users can be subscribed to notifications with a group email address,
which allows you to efficiently manage notifications in your organization.

## Creating a Technical User

1. Go to Administration \> Technical
Users.

2. Click New Technical User.

3. Enter the details for a technical user.

   - Username: Enter a username for the technical user.

   - (Optional) Description: Enter a description for the technical user.

   - Permission Role: Select a permission role: Admin, Viewer, or
     Member.

   - (Optional) Customer Roles: Select a role. Custom roles require that your
     workspace is SSO managed and that you configured the custom roles
     beforehand. The dropdown here also includes the default roles, Viewer,
     Member, Admin, in addition to any custom roles you defined. This is
     expected behavior. For more information, see [Managing User Roles with SSO](https://help.sap.com/docs/leanix/ea/single-sign-on-sso?locale=en-US&state=PRODUCTION&version=CLOUD#loio275cc8227a441014a371975e4b816f0a__managing-user-roles-with-sso).

   - (Optional) Access Control Entities: Use this parameter to map a technical
     user to Access Control Entities (ACEs) and Access Control Lists (ACLs)
     created with virtual workspaces. To learn more, see [Virtual      Workspaces](https://help.sap.com/docs/leanix/ea/virtual-workspaces?locale=en-US&state=PRODUCTION&version=CLOUD "Manage access to fact sheets for custom user groups").

   - Expiry Date: Set the expiration date for the API token associated
     with this user.
4. Click Save.

![Creating a Technical User](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2735786036494289bc5446a96fc1d37a_HiRes.png)

Creating a Technical User

A technical user is created, and an overlay with an API token is displayed.

**Caution**

Save the API token. It is shown only once.

## Managing Technical Users

- Replace the API token of a technical user: To do this, click Replace token on the technical user you need, then confirm your action. When you
replace an API token, the previous token is disabled. Any integrations or
scripts using the previous token will stop working.

- Update a technical user: To update the details associated with a
technical user, select a user on the Technical Users page, and update the
information you need. You can change the expiration date of the associated API
token, but this action doesn’t replace or delete the token.

- View the changelog of associated actions: To view the history of updates
for a technical user, click History on the technical user you need. You
can see the full changelog of actions associated with the user.

- Delete a technical user: To do this, click the trash bin icon on the
technical user you need, then confirm your action. When you delete a technical
user, the API token associated with the user is also deleted. Any integrations
or scripts using the token will stop working.

## Best Practices

Here are some best practices to securely use API tokens.
This list is non-exhaustive.

- Treat an API token like a password or other sensitive credentials.

- Don’t share API tokens with anyone who shouldn’t be using them.

- Delete unnecessary API tokens by deleting technical users.

- Replace API tokens periodically.

- Store API tokens securely, for example, by using secrets management tools.

- Securely use API tokens in your code.

- Transfer API tokens securely.

- Set up monitoring and auditing to detect and respond to any unauthorized
access.

For additional information, see [Integration Security](https://help.sap.com/docs/leanix/ea/security-best-practices?locale=en-US&state=PRODUCTION&version=CLOUD#loiofdd367014578453ba3fc2d82b5ad82fd__integration_security).
