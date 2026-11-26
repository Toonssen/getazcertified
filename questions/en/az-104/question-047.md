---
question: |-
  You have an Azure subscription.

  You create a Bicep file named landing.bicep that starts with the line targetScope = 'subscription' and contains a resource group and a policy assignment.

  You need to deploy landing.bicep by using the Azure CLI.

  Which command should you run?
documentation:
  - title: "Bicep deployments to a subscription"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-to-subscription"
skill_area: "arm-bicep"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] az deployment sub create
  > A file with targetScope 'subscription' (one that creates resource groups) is deployed at subscription scope.
- [ ] az deployment group create
  > Group deployments go into an existing resource group and can't create the resource group itself.
- [ ] az deployment mg create
  > Management group deployments are for files with targetScope 'managementGroup'.
- [ ] az deployment tenant create
  > Tenant deployments are for targetScope 'tenant', such as creating management groups.
