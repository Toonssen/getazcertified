---
question: |-
  You have an Azure subscription named Sub-Ops2 that contains a resource group named rg-data4. The resource group contains a storage account named stlogs04.

  A user named User6 has the role assignments shown in the following exhibit. Storage Operator1 and Storage Admin1 are custom roles. No other role assignments, deny assignments or resource locks apply to stlogs04.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "User6 can delete stlogs04."
documentation:
  - title: "Azure role definitions"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
---

```text
Principal  Role               Scope
User6      Storage Operator1  rg-data4
User6      Storage Admin1     rg-data4

Role               Actions                                         NotActions
Storage Operator1  Microsoft.Storage/storageAccounts/*             Microsoft.Storage/storageAccounts/delete
Storage Admin1     Microsoft.Storage/storageAccounts/delete        (none)
```

- [x] Yes
  > NotActions isn't a deny rule. It only removes the delete action from Storage Operator1's own set of allowed
  > actions. Storage Admin1 grants the same action, and a user who has a second role that grants an action
  > excluded by another role's NotActions is allowed to perform it.
- [ ] No
  > The exclusion in Storage Operator1 applies to that role only (Actions minus NotActions). A deny assignment would
  > block a granted action, and none applies here.
