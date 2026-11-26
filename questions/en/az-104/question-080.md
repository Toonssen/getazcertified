---
question: |-
  You have the virtual networks, virtual machines, and Azure Bastion host shown in the following exhibits.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "You can use the Azure portal to connect to vm-lin3 through bas-1."
documentation:
  - title: "VNet peering and Azure Bastion"
    url: "https://learn.microsoft.com/en-us/azure/bastion/vnet-peering"
  - title: "Secure hub-spoke network design"
    url: "https://learn.microsoft.com/en-us/azure/networking/cross-service-scenarios/design-secure-hub-spoke-network"
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
  > Peering isn't transitive. VNet3 is peered with VNet2, not with VNet1, so bas-1 can't reach vm-lin3. Peering
  > VNet1 and VNet3 directly would fix it.
- [x] Yes
  > Being peered with a network that's peered with VNet1 isn't enough. Bastion needs a direct peering (or a hub
  > design with routing).
