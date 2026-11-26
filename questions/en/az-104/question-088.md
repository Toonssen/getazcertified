---
question: |-
  You have the resource groups and virtual networks shown in the following table.

  You need to deploy a virtual machine named vm-erp1 to RG-App in the North Europe region.

  To which virtual networks can you connect vm-erp1?
documentation:
  - "https://learn.microsoft.com/en-us/azure/virtual-network/network-overview"
  - "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-vnet-plan-design-arm"
skill_area: "virtual-networks"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name       Type              Resource group   Region
RG-Net     Resource group    -                West Europe
RG-App     Resource group    -                North Europe
VNet-A     Virtual network   RG-App           North Europe
VNet-B     Virtual network   RG-App           West Europe
VNet-C     Virtual network   RG-Net           North Europe
```

- [x] VNet-A and VNet-C only
  > A VM's network interface must be in the same region as the virtual network. The resource group doesn't matter:
  > VNet-C is in RG-Net but in North Europe.
- [ ] VNet-A only
  > Resources can use a virtual network in another resource group in the same region.
- [ ] VNet-A and VNet-B only
  > VNet-B is in West Europe, so a North Europe VM can't connect to it.
- [ ] VNet-A, VNet-B, and VNet-C
  > Region decides, and VNet-B is in the wrong one.
