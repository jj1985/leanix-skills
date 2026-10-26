<!-- Source: https://help.sap.com/docs/leanix/ea/authorization-model -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Authorization Model

## Overview

The SAP LeanIX
out-of-the-box Authorization model (part of the overall meta model) includes three
default roles, VIEWER, MEMBER, and ADMIN. In general, these roles govern access to read (view), create (add), update (edit), and delete information at the Fact Sheet TYPE level. This "information" includes but is not limited to attributes, relations, and tags. This means that the Authorization Model is set and
defined for the entire Fact Sheet TYPES, for example, IT Component. There are also
some capabilities surrounding Import, Export, Saved Searches, and more.

Please see the [meta model](https://help.sap.com/docs/leanix/ea/meta-model?locale=en-US&state=PRODUCTION&version=CLOUD "Get an overview of the SAP LeanIX meta model and its key concepts.") for basic information
on what a Fact Sheet TYPE is and what is the SAP LeanIX meta
model.

You can request that these settings be different per role, VIEWER, MEMBER, and or
ADMIN. In addition, you can also request that new roles be added to the
authorization model; they would exist in addition to the standard roles.

The ability to configure the Authorization model is contingent upon the SAP LeanIX
package that you have. As such, please discuss any authorization model changes that
you are considering with your CSM, and they can inform you if your package covers
authorization model changes. This document is not meant to be exhaustive in nature,
as such, having a conversation with your CSM regarding your use case, especially if
it's not covered in this document, could be very useful.

**Note**

Virtual Workspaces

If your organization is looking to control access at the level of
individual Fact Sheets, your Use Case may be be
accommodated by [Virtual Workspaces](https://help.sap.com/docs/leanix/ea/virtual-workspaces?locale=en-US&state=PRODUCTION&version=CLOUD "Manage access to fact sheets for custom user groups"). The standard authorization model cannot control access to
individual Fact Sheets.

**Restriction**

New Authorization Model roles can only be created and utilized when your
organization has your Identity Provider configured as external IdP. To learn
more about setting up single sign-on (SSO), see [Single Sign-On (SSO)](https://help.sap.com/docs/leanix/ea/single-sign-on-sso?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to configure single sign-on (SSO) with SAP LeanIX.").

Any customer can request that the out-of-the-Box roles be updated (no new roles
being created), this does not require a particular IP configuration (assuming
that your package allows Authorization model changes).

## Terminology

Please see the chart below for helpful terminology:

| Terminology | Definition |
| --- | --- |
| read | To be able to "see", to make visible. For example, this can be<br>defined for a particular attribute and or relation. |
| create | To be able to associate a response to an attribute, relation, etc<br>that is "null"/empty/not filled out. |
| delete | To be able to remove/delete information that has been entered AND<br>SAVED against a particular Fact Sheet within a particular attribute,<br>relation, etc. Such as a particular relation, e.g. the Data Objects<br>relation on the Application Fact Sheet type. |
| update | To be able to edit information that is already existing. For<br>example, the Description of a Fact Sheet reads, "A new version is<br>coming out in 2022". If a user is assigned to an authorization role<br>that has access to update this attribute, they would be able to<br>CHANGE the answer to anything else they wish, such as "A new version<br>is coming out in 2024" |

## Fact Sheet Attributes

The most commonly requested authorization model configuration changes pertain to controlling read
(view), create (add), update (edit), and delete access on attributes. As previously
explained, for the most part, the Authorization Model works on the level of Fact
Sheet types. If you need clarification on what an attribute or relation is, please
see [Meta Model](https://help.sap.com/docs/leanix/ea/meta-model?locale=en-US&state=PRODUCTION&version=CLOUD "Get an overview of the SAP LeanIX meta model and its key concepts.").

For each attribute and or "relation" on a Fact Sheet type, it is possible to define
whether a role has a view, edit, and or delete access to it. These properties can be
combined into several combinations, that is, as long as it is logical. For example,
you would not set the Description attribute to be write(edit) access, but NOT
read(access) for the MEMBER role or any role. After all, a user cannot edit what
they cannot see.

In the example below, the Description attribute has been set to be read-only (view
only) for any user assigned to the Member role. You can see that the attribute is
visible but greyed out, which indicates to the user that they do not have access to
edit this attribute.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2753f6f47a441014b47adec8e1c299a5_LowRes.png)

The same can be done for any attribute and or relation, whether it's an
out-of-the-box attribute such as a description or a custom attribute (an attribute
that was created by the customer using self-configuration).

The same logic applies when setting an attribute to write(edit), delete, and or
update properties. You can see in the screenshot above that any attribute that is
available to write (edit) has a textbox that is white instead of grey.

Below is an example where create (add) was restricted for Members on the Application
Fact Sheet type, Application to IT Component relation. You can see that there is a
lock symbol within that subsection indicating to the user that they cannot
"add"/create a new relation.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274233b27a441014bad29a2d6ec6def6_LowRes.png)

## Common Use Case: Hide Costs

A common use case is making cost and or
other financial information hidden from specific authorization roles. The "Total
Annual Cost" is an out-of-the-box attribute that can be found in several relations,
including the Application to IT Component relation. This can be done by removing
"read" (view) access for that particular attribute and or relation.

Below you can see that the Total Annual Cost is not visible to the user who
signed in under the MEMBER authorization role:

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio27526b937a441014b6b1cea278bdde9c_LowRes.png)

## Fact Sheet Type Level

Entire Fact Sheet types can be set to be read,
created, updated, and or deleted per role. In the example below, take a look at the
upper left-hand side. Notice that the Provider Fact Sheet type is no longer visible
to any users assigned to the Member role. This was done by removing read (view)
access.

Similarly, entire Fact Sheet types can be set to be read-only (view) by specific
roles. This means that those roles would only be able to view the information for
any Fact Sheets under that particular Fact Sheet TYPE, but they would not be able to
delete, update (edit), nor create any information. This is helpful for Fact Sheet
types that represent fixed models or taxonomies like Business Capabilities and or
Tech Category.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2742e7717a441014ab86b062f9821fa8_LowRes.png)

In addition, the Export, Import, and Inline Edit functionality can also be
restricted. In the below example, Import and Table Edit have been restricted for
MEMBERs for the Application Fact Sheet Type. As you can see, the user does
NOT have access to the Import functionality, which would normally be in the
highlighted area on the right-hand side.

Please see below, and notice that the Import button is not available for the
Application Fact Sheet type.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2741ce317a441014960b9b735711dd3c_LowRes.png)

Below is an example where the MEMBER role has been restricted from "Archiving" any
Application Fact Sheets:

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274443737a4410148d1f8d10e5aa4067_LowRes.png)

## Subscription Type Check

Any attribute or relation can have a
"subscription type check" against it. If you are not familiar with Subscription
Types, please see the [Manage Subscription Roles](https://help.sap.com/docs/leanix/ea/subscription-roles?locale=en-US&state=PRODUCTION&version=CLOUD "Learn how to create, edit, and delete subscription roles and manage settings like enabling the “Accountable” subscription type, limiting multiple subscriptions, and enforcing mandatory role selection.").

A subscription type check allows you to define read, create, delete, and or update
access based on that user's subscription type for that particular Fact Sheet
TYPE. The actual check occurs at the Fact Sheet level, this is because subscriptions
are assigned to the necessary users, on each Fact Sheet, via the Subscriptions tab
of that Fact Sheet.

In the example below the audimex Fact Sheet has one subscription type assigned, which
is the subscription type of Responsible. Please take note that it is not possible to complete a check by "Application Portfolio Owner". Application Portfolio
Owner is the Subscription Role, and the type is "Responsible".

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274dc58e7a4410149685dacfdac2f668_LowRes.png)

## Saved Searches

Saved Searches access can also be controlled, but these
changes apply to All Fact Sheet types. It is not possible to define access
differently for Saved Searches by Fact Sheet Type. The same options previously
described are available read (view), create (add), update (edit), and delete.

In the example below, as a Member I have read, create, update, and delete access.
This Saved Search is named "No responsible set". You can see in the upper right-hand
corner, along with the grey box, that I have access to Save As (UPDATE) and Save
(CREATE)

**Note**

Saved Searches Permission Settings

The Authorization model will respect the specific Saved Search settings, defined
at the time that the Saved Search is created and Saved. For example if "User B",
creates a search and sets it so that only they have access to edit it. I as
"User A", cannot update that Saved Search even if the role I have has access to
update Saved Searches.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio2753ab967a441014b2b0dfe21da9640d_LowRes.png)

## Granular Access

In addition, "change-owner", and "manage predefined" can be set. Change Owner is referring to the "Change Owner" button available
within "Manage Searches". In the default Authorization model, the only role that has
access to these two properties is ADMIN.

![](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/loio274ec4647a441014813c8ba59598e891_LowRes.png)

General Categories:

| Type | Details |
| --- | --- |
| Published |  |
| Private |  |
| Shared |  |
| System | This is referring to predefined Saved Searches, that all users<br>have set by default. |

Saved Searches can be defined at another level of granularity:

- Published\[own\]

- Private\[own\]

- Shared\[own\]

In the above examples, the functionality is restricted to the users "own" those Saved
Searches. Meaning the searches that they themselves created.

## Summary of Functionality

The Authorization Model allows for the
configuration of many different combinations of access both within Fact Sheet types,
and with other Fact Sheet related functionality such as Saved Searches.

Please see the tables in the following sections for a capabilities summary of the
Authorization model.

Please refer back to the table available in the "Terminology" section, which provides
details on the specific access properties that can be defined, they are read,
create, update, and delete.

## Routines

The table below focuses on executable programs, such as the
Export routine, that you as a user can trigger, as opposed to fields/attributes
within a Fact Sheet. As such, the normal CRUD operations (create, read, update, and
delete) don't quite apply here. In general, if a user can see a routine, then it
follows that they can run/execute that routine.

| Functionality/Area of Interest | Is it possible to configure | Details/Example |
| --- | --- | --- |
| Import | Yes | This is can be set by Fact Sheet TYPE. Meaning that this can be<br>set to be viewable and usable on all Fact Sheet Types except IT<br>Component (as an example). |
| Export | Yes | This is can be set by Fact Sheet TYPE. Meaning that this can be<br>set to be viewable and usable on all Fact Sheet Types except IT<br>Component (as an example). |
| Inline Edit | Yes | For detailed information on inline editing, see [Inline Editing](https://help.sap.com/docs/leanix/ea/bulk-updating-data-in-inventory-table-view?locale=en-US&state=PRODUCTION&version=CLOUD#loioc61816d6a4da4c5fbc9bc6365f2646c2__inline_editing).<br>Please note that Inline Edit DOES respect the Authorization model.<br>For example, the MEMBER role is only able to read but Not update or<br>create, the attribute Description for Application Fact Sheet types.<br>In addition, the MEMBER role does have access to Inline Edit. This<br>means that they will be able to click on Inline Edit and utilize it,<br>but they will only be able to "read" the Description for Application<br>Fact Sheet but not update, delete, or create. This can be set by<br>Fact Sheet TYPE. For example, for a specific role(s) this could be<br>set to be viewable and usable on all Fact Sheet Types except<br>Provider. |
| Archive | Yes | Please see the [Searching and Filtering in the Inventory](https://help.sap.com/docs/leanix/ea/searching-and-filtering-in-inventory?locale=en-US&state=PRODUCTION&version=CLOUD "Searching and filtering in the inventory helps efficiently manage your data. Learn how to quickly find fact sheets, apply filters, manage filters, and save search results for future access."), for<br>information on what Archiving is. This is set per Fact Sheet<br>TYPE. |
| Saved Searches (previously named bookmarks) | Yes | Example, "set the role NONMANAGER to be able to CREATE Saved<br>Searches, but NOT update (edit)". This would apply to any and all<br>Saved Searches for any user assigned to the NONMANAGER role.<br>However, it does respect, the specific settings defined on the Saved<br>Search. For example I can create a Saved Search and set it so that<br>only I have access to edit it, this is defined on the Saved Search<br>itself when I create and save it. The Authorization model will<br>respect this. In addition, "change-owner", and "manage predefined". Are also available as properties that can be set. In the default Authorization model, the only role that<br>has access to these two properties is ADMIN. Saved Searches can be<br>defined at a more granular level: General Categories: Published,<br>Shared, System(this is referring to predefined searches) Further<br>granularity: Published\[own\], Shared\[own\] |
| Invite | Yes, but not via the Authorization model | Please reach out to support at [SAP LeanIX Support![Information published on non-SAP site](https://help.sap.com/doc/72d375467c1e4dcb872dfa2998b6328d/CLOUD/en-US/themes/sap-light/img/3rd_link.png)](https://help.sap.com/docs/link-disclaimer?site=https%3A%2F%2Fwww.leanix.net%2Fsupport "https://www.leanix.net/support") or reach out to your CSM for more<br>details. |
| Cloning | No | For more information, see [Cloning a Fact Sheet](https://help.sap.com/docs/leanix/ea/creating-fact-sheets?locale=en-US&state=PRODUCTION&version=CLOUD#loio2759925e7a441014a7e9e6f502b4cd21__cloning_a_fact_sheet) |
| Printing | No |  |

## Fact Sheet Specific

| Functionality/Area of Interest | Is it possible to configure | Details/Example | Create | Read | Update | Delete |
| --- | --- | --- | --- | --- | --- | --- |
| Fact Sheet Types | Yes | This is referring to entire Fact Sheet Types e.g Application, IT<br>Component etc. Example set the "custom" role MANAGER to only READ<br>(view) Application Fact Sheet types. This means that this role would<br>not be able to create, update, or delete any Application Fact<br>Sheets. | X | X | X | X |
| Fact Sheets (as in individual Fact Sheets such as<br>Audimex) | No | No, access to individual Fact Sheets cannot be controlled via the<br>Authorization model. One example of such a request is : can the Fact<br>Sheet Audimex be completely hidden for MEMBERS. The answer is no.<br>However, this functionality is available within [Virtual<br>Workspaces](https://help.sap.com/docs/leanix/ea/virtual-workspaces?locale=en-US&state=PRODUCTION&version=CLOUD "Manage access to fact sheets for custom user groups"). |  |  |  |  |
| Tags (<referring to associating tags to individual Fact<br>Sheets>) | Yes | This is not referring to creating Tags in the Administration area, but rather associating tags to Fact Sheets.\* In<br>addition, this is referring to all tags. It is not possible to<br>define a particular set of tags that the role(s) should have access<br>to. |  | X | X |  |
| Tag Groups | No | Example, set user NONMANAGER to only be able to see, the tag<br>group "Cloud". This is not possible. You might find it beneficial to<br>remove some Tag Groups and instead set them as attributes. The<br>benefit to this is that attributes can be set to create, read,<br>update and or delete. This is a possibility that might be optimal<br>depending on your Use Case. As such please contact your CSM in order<br>to discuss this. |  |  |  |  |
| Attributes (also called fields) | Yes | Examples of out-of-the-box attributes are Description, Alias,<br>Release, and Name. Including attributes that are within relations<br>such as Total Annual Cost. Attributes also includes any customer<br>defined attributes. Depending on your SAP LeanIX package, you might have the ability via Self-Configuration or via<br>SAP LeanIX Support to create attributes that do not exist in the standard<br>meta model. If you have Virtual Workspaces, the "ACE" read and write can also be controlled in the same way as all other attributes. | X | X | X | X |
| Relations | Yes |  | X | X | X | X |
| Attributes that exist within a Relation | Yes | For example, the standard Application to IT Component relation,<br>includes a Total Annual Cost Attribute. This could be set to be READ<br>only for the MEMBER role. | X | X | X | X |
| Quality Seal | Yes | It is possible to define for the property "update" only, this is<br>due to the nature of the functionality. For more information on the<br>Quality Seal, please see the [Increase your Data<br>Quality](https://help.sap.com/docs/leanix/ea/increasing-your-data-quality?locale=en-US&state=PRODUCTION&version=CLOUD "Enhance data quality in SAP LeanIX with features like fact sheet completion scores, fact sheet subscriptions, mandatory fields, quality seals, and surveys. Use integrations and discovery tools for accurate, up-to-date data.") |  |  | X |  |
| Fact Sheet Tabs | No |  |  |  |  |  |

## Administration Area Functionality

The entire "Administration" area is
hardcoded to only be accessible to the ADMIN role. It is not possible for any other
role to have access to the Administration area. Furthermore, it is not possible to
define specific access to the Administration area even for the ADMIN role. Any user
with this role will automatically have access to everything under the Administration
area.

Please note that all users have access to Profile, Password, and Notifications. These
three options are available under "My Settings".

## Dashboards

At this time there aren't specific settings within the Authorization model that determine access
to Dashboards. However, when users create Dashboards, they can define some access
settings for the particular Dashboard that they are creating. For more information
on dashboards, see [Dashboard Modeling](https://help.sap.com/docs/leanix/ea/dashboard-modeling?locale=en-US&state=PRODUCTION&version=CLOUD "Best practices and examples for creating dashboards tailored to various use cases.").

**Note**

At this time, all roles are able to create Public Dashboards even those with the
role of VIEWER.
