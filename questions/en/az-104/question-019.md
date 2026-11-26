---
question: |-
  You have an Azure subscription that contains a resource group named RG-App.

  You need to ensure that a user named User4 can assign Azure roles to other users for RG-App. User4 must not be able to create, modify, or delete resources in RG-App.

  Which role should you assign to User4 for RG-App?
documentation:
  - title: "Azure built-in roles"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] User Access Administrator
  > User Access Administrator manages access (role assignments) without granting rights over the resources
  > themselves.
- [ ] Owner
  > Owner can assign roles, but it also has full control of every resource in RG-App.
- [ ] Contributor
  > Contributor manages resources but can't assign roles, so it fails on both counts.
- [ ] Reader
  > Reader can view role assignments but can't create them.
