---
question: |-
  You have the virtual networks, virtual machines, and Azure Bastion host shown in the following exhibits.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "You can use the Azure portal to connect to vm-lin2 through bas-1 by using SSH."
documentation: "https://learn.microsoft.com/en-us/azure/bastion/vnet-peering"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "bas-1-basic"
---

```text
Virtual network   Peering                    VMs (private IPs only)
VNet1             VNet2                      vm-win1 (Windows)
VNet2             VNet1, VNet3               vm-lin2 (Linux)
VNet3             VNet2                      vm-lin3 (Linux)
```

```text
Bastion host   bas-1
SKU            Basic
Deployed to    VNet1 / AzureBastionSubnet
```

- [x] Yes
  > Bastion works across virtual network peering, and Basic supports portal-based SSH. VNet2 is peered directly
  > with VNet1.
- [ ] No
  > The Basic SKU's limit is native client support, not peering or SSH from the portal.
