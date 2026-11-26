---
question: |-
  You have a virtual network named VNet-Spoke that contains virtual machines, and an Azure Firewall named fw-hub in a peered virtual network.

  You need all internet-bound traffic from the virtual machines in VNet-Spoke to pass through fw-hub so that it can be filtered.

  What should you create first?
documentation:
  - "https://learn.microsoft.com/en-us/azure/firewall/tutorial-firewall-deploy-portal"
  - "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview"
skill_area: "virtual-networks"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A route table with a 0.0.0.0/0 route whose next hop is a virtual appliance at fw-hub's private IP address
  > Traffic goes straight to the internet by default. A user-defined route on the spoke subnets is what sends it
  > to the firewall.
- [ ] A network security group that denies outbound internet traffic
  > An NSG can block traffic but can't redirect it to the firewall.
- [ ] An Azure Network Watcher instance
  > Network Watcher diagnoses and monitors traffic. It doesn't change routing.
- [ ] A NAT gateway on the spoke subnets
  > A NAT gateway gives outbound internet access with its own IP. It bypasses the firewall instead.
