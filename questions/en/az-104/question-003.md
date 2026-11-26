---
question: |-
  You have an Azure subscription that contains the resources shown in the following table.

  You assign an Azure Policy definition as shown in the following exhibit.

  After the assignment, you create a storage account named stsales02 in RG-Sales. You make no other changes.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "stsales02 has the CostCenter: 4100 tag."
documentation: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-policies"
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
  > Resources don't inherit tags from their resource group. stsales02 gets Owner: ops-team from the policy and
  > nothing else. Inheriting CostCenter would need a policy such as 'Inherit a tag from the resource group if
  > missing'.
- [x] Yes
  > Tags on a resource group are not passed down to the resources in it.
