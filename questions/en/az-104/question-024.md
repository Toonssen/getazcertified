---
question: |-
  You have an Azure subscription that contains the resource groups shown in the following table. RG-A contains a virtual machine named vm1 that is deployed to North Europe.

  You move vm1 and its dependent resources from RG-A to RG-B.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "After the move, vm1 runs in West Europe."
documentation:
  - title: "Move resources to a new group"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/move-resource-group-and-subscription"
  - title: "What is Azure Resource Mover?"
    url: "https://learn.microsoft.com/en-us/azure/resource-mover/overview"
skill_area: "subscriptions-governance"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
---

```text
Name   Location
RG-A   North Europe
RG-B   West Europe
```

- [ ] No
  > Moving a resource to another resource group changes only the group it belongs to. The resource keeps its
  > region; the resource group's location only stores the group's metadata.
- [x] Yes
  > A resource group's location doesn't decide where its resources run. Changing regions takes a redeployment, for
  > example with Azure Resource Mover.
