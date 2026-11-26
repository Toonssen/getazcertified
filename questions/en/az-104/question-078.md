---
question: |-
  You have the virtual networks, virtual machines, and Azure Bastion host shown in the following exhibits.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "You can connect to vm-win1 through bas-1 by using the Remote Desktop Connection client (mstsc) on your computer."
documentation:
  - title: "Bastion native client"
    url: "https://learn.microsoft.com/en-us/azure/bastion/native-client"
  - title: "Choose an Azure Bastion SKU"
    url: "https://learn.microsoft.com/en-us/azure/bastion/bastion-sku-comparison"
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

- [ ] No
  > Native client support (mstsc or a local SSH client) needs the Standard SKU or higher with Native client
  > support enabled. Basic only offers connections from the Azure portal.
- [x] Yes
  > On Basic you can still connect to vm-win1 over RDP, but only from the browser in the Azure portal.
