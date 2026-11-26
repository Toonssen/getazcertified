---
question: |-
  You have a virtual network named VNet-Ops in the North Europe region.

  You plan to deploy the container groups shown in the following table.

  Which container groups can you deploy to VNet-Ops?
documentation:
  - "https://learn.microsoft.com/en-us/azure/container-instances/container-instances-virtual-network-concepts"
  - "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-vnet-plan-design-arm"
skill_area: "containers"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Container group   OS        Region
cg-1              Linux     North Europe
cg-2              Windows   North Europe
cg-3              Linux     West Europe
```

- [x] cg-1 and cg-2 only
  > A resource can only join a virtual network in its own region, so cg-3 is out. Virtual network deployment is
  > generally available for both Linux and Windows container groups.
- [ ] cg-1 only
  > The old Linux-only limitation is gone. Windows container groups can be deployed to a virtual network too.
- [ ] cg-1 and cg-3 only
  > cg-3 is in West Europe and can't join a North Europe virtual network.
- [ ] cg-1, cg-2, and cg-3
  > Region still matters: cg-3 would need a West Europe virtual network.
