---
question: |-
  You have a virtual network that contains the subnets shown in the following table.

  You plan to deploy a new Azure Container Instances container group into the virtual network.

  To which subnets can you deploy the container group?
documentation:
  - title: "Container Instances in a virtual network"
    url: "https://learn.microsoft.com/en-us/azure/container-instances/container-instances-virtual-network-concepts"
skill_area: "containers"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Subnet   Delegation                                  Contents
snet-a   none                                        Two virtual machines
snet-b   Microsoft.Web/serverFarms                   App Service virtual network integration
snet-c   Microsoft.ContainerInstance/containerGroups Three container groups
snet-d   none                                        Empty
```

- [x] snet-c and snet-d only
  > A container group subnet must be delegated to container groups and contain only container groups. snet-c
  > already qualifies. snet-d is empty and can be delegated before (or during) the deployment.
- [ ] snet-c only
  > An empty subnet without a delegation can be delegated to container groups, so snet-d works too.
- [ ] snet-a, snet-c, and snet-d only
  > snet-a contains virtual machines, and a container group subnet can contain only container groups.
- [ ] snet-a, snet-b, snet-c, and snet-d
  > snet-b is delegated to App Service, and a subnet has one delegation.
