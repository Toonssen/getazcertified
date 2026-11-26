---
question: |-
  You have a Microsoft Entra tenant that is linked to an Azure subscription named Sub-Dev. The tenant contains the objects shown in the following table.

  You need to assign the Virtual Machine Contributor role to a user named Admin2.

  At which objects can you assign the role?
documentation:
  - "https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview"
  - "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name       Type
MG-Prod    Management group
Sub-Dev    Subscription
RG-Web     Resource group
vm-web01   Virtual machine
AU-Sales   Administrative unit
```

- [x] MG-Prod, Sub-Dev, RG-Web, and vm-web01 only
  > Azure RBAC role assignments can be made at four scopes: management group, subscription, resource group and
  > resource. All four Azure objects in the table qualify.
- [ ] Sub-Dev and RG-Web only
  > Management groups and individual resources are valid scopes as well, so this list is too short.
- [ ] vm-web01 only
  > Assigning at the resource works, but it isn't the only scope that does: the role can also be assigned higher
  > up and is inherited.
- [ ] MG-Prod, Sub-Dev, RG-Web, vm-web01, and AU-Sales
  > An administrative unit scopes Microsoft Entra roles, not Azure RBAC roles such as Virtual Machine Contributor.
