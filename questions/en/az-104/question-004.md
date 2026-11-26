---
question: |-
  You have an Azure subscription that contains the resources shown in the following table.

  You assign an Azure Policy definition as shown in the following exhibit.

  After the assignment, you create a storage account named stsales02 in RG-Sales. You make no other changes.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "RG-Sales has the Owner: ops-team tag."
documentation:
  - title: "Policy definitions for tagging"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-policies"
skill_area: "subscriptions-governance"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "tag-policy-rg-sales"
---

```text
Name         Type             Resource group   Tags
RG-Sales     Resource group   -                CostCenter: 4100
vnet-sales   Virtual network  RG-Sales         Env: Prod
```

```text
Policy assignment
  Definition:          Add a tag to resources  (effect: Modify)
  Scope:               RG-Sales
  Parameters:          Tag name: Owner   Tag value: ops-team
  Remediation task:    none
```

- [ ] No
  > 'Add a tag to resources' evaluates resources only (indexed mode), not the resource group itself. Tagging
  > resource groups takes the separate 'Add a tag to resource groups' definition, assigned at a scope above the
  > group.
- [x] Yes
  > The resource group is the assignment scope, not a resource the definition targets.
