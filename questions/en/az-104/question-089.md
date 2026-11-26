---
question: |-
  You have a hub virtual network named VNet-Hub that contains a VPN gateway connected to your on-premises network. A spoke virtual network named VNet-Spoke1 is peered with VNet-Hub.

  You need virtual machines in VNet-Spoke1 to reach the on-premises network through the VPN gateway in VNet-Hub, without deploying another gateway.

  Which two settings should you enable?
documentation:
  - "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview"
  - "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-peering-gateway-transit"
skill_area: "virtual-networks"
study_guide: "2026-04-17"
archetype: "choose-n"
---

- [x] On the VNet-Hub to VNet-Spoke1 peering: allow gateway transit
  > Gateway transit lets the hub's gateway forward traffic for the peered network.
- [x] On the VNet-Spoke1 to VNet-Hub peering: use the remote virtual network's gateway
  > The spoke uses the hub's gateway, and the on-premises routes are learned through it.
- [ ] On the VNet-Spoke1 to VNet-Hub peering: allow gateway transit
  > Transit is set on the side that owns the gateway. The spoke has none.
- [ ] On both peerings: allow forwarded traffic only
  > Forwarded traffic covers traffic from an appliance in the peer. It doesn't share a VPN gateway.
- [ ] A peering between VNet-Spoke1 and the on-premises network
  > Peering connects Azure virtual networks. On-premises networks connect through gateways.
