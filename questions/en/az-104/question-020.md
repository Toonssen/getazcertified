---
question: |-
  You have an Azure subscription that contains a resource group named RG-Data. RG-Data contains a storage account named stdata01.

  You apply the lock shown in the following exhibit.

  A user named Admin5 has the Owner role for the subscription.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "Admin5 can list the access keys of stdata01 in the Azure portal."
documentation: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources"
skill_area: "subscriptions-governance"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
---

```text
Lock name:   lock-data
Scope:       RG-Data
Lock type:   Read-only
```

- [ ] No
  > Locks apply to every user, Owners included, and are inherited by the resources in the group. Listing keys is a
  > POST operation (listKeys), which a Read-only lock blocks.
- [x] Yes
  > Owner doesn't bypass a lock. Admin5 would have to remove the lock first.
