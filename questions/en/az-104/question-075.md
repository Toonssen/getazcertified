---
question: |-
  You have the virtual networks, the Azure private DNS zone, and the DNS server shown in the following exhibits. vm-dns1 doesn't forward corp.example queries anywhere else.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "A VM in VNet-App2 resolves db1.corp.example to 10.20.0.5."
documentation:
  - title: "Azure Private DNS zones"
    url: "https://learn.microsoft.com/en-us/azure/dns/private-dns-privatednszone"
  - title: "Name resolution for VMs"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances"
skill_area: "name-resolution-load-balancing"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "corp-dns"
---

```text
Virtual network   DNS servers                    Peered with
VNet-Hub          Azure-provided (default)       VNet-App1, VNet-App2
VNet-App1         Azure-provided (default)       VNet-Hub
VNet-App2         Custom: 10.0.0.10 (vm-dns1)    VNet-Hub
```

```text
Private DNS zone corp.example (linked to VNet-Hub and VNet-App1)
  db1    A    10.20.0.5

DNS server vm-dns1 (in VNet-Hub, authoritative for corp.example)
  db1    A    10.30.0.5
```

- [ ] No
  > VNet-App2 uses a custom DNS server, so its VMs ask vm-dns1, which answers 10.30.0.5 from its own zone. With
  > custom DNS set, linked private zones aren't consulted automatically, and VNet-App2 isn't linked anyway.
- [x] Yes
  > Peering doesn't share DNS settings. The custom server on VNet-App2 decides the answer.
