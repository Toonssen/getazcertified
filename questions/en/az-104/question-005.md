---
question: |-
  You have a Microsoft Entra tenant.

  You need to modify the user settings for the tenant to meet the following requirements:

  - Users who aren't administrators must be prevented from creating app registrations.
  - Users who aren't administrators must be prevented from creating new Microsoft Entra tenants.

  Which two settings should you modify?
documentation:
  - title: "Default user permissions"
    url: "https://learn.microsoft.com/en-us/entra/fundamentals/users-default-permissions"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "choose-n"
---

- [x] Users can register applications
  > Set to No: standard users can no longer create app registrations (and the service principals that come with
  > them).
- [x] Restrict non-admin users from creating tenants
  > Set to Yes: only admins with the Tenant Creator role (or higher) can create a new tenant.
- [ ] Restrict access to Microsoft Entra admin center
  > This only hides the admin center UI from non-admins. It does not block PowerShell or Microsoft Graph, and it
  > controls neither app registrations nor tenant creation.
- [ ] Guest user access restrictions
  > This limits what guest users can see in the directory, not what members can create.
- [ ] Users can create security groups
  > This controls group creation, not app registrations or tenants.
