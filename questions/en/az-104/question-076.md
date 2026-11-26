---
question: |-
  You have the virtual networks, the Azure private DNS zone, and the DNS server shown in the following exhibits. vm-dns1 doesn't forward corp.example queries anywhere else.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "A VM in VNet-Hub resolves db1.corp.example to 10.30.0.5."
documentation: "https://learn.microsoft.com/en-us/azure/dns/private-dns-privatednszone"
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
  > VNet-Hub uses Azure-provided DNS and is linked to the private zone, so it gets 10.20.0.5. Hosting vm-dns1
  > doesn't make the network use it as its DNS server.
- [x] Yes
  > Only networks configured with 10.0.0.10 as their DNS server use vm-dns1.
