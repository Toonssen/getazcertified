---
question: |-
  You have an Azure SQL database named sqldb01 and an on-premises network connected to a virtual network named VNet-Core by ExpressRoute private peering.

  You need on-premises servers to reach sqldb01 over a private IP address, with no traffic over its public endpoint.

  What should you configure?
documentation:
  - title: "What is a private endpoint?"
    url: "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview"
  - title: "Virtual network service endpoints"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A private endpoint for the logical server of sqldb01 in VNet-Core
  > A private endpoint gives the service a private IP address in your virtual network, and that IP is reachable
  > from on-premises over the private peering.
- [ ] A virtual network service endpoint for Microsoft.Sql on a VNet-Core subnet
  > Service endpoints keep the public endpoint and only work for traffic from that subnet, not from on-premises.
- [ ] A server-level firewall rule that allows the on-premises public IP addresses
  > This still uses the public endpoint.
- [ ] A NAT gateway on VNet-Core
  > A NAT gateway handles outbound internet traffic. It doesn't give a service a private IP.
