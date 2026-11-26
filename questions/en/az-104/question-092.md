---
question: |-
  Your company owns the domain tailspin.example, registered with a third-party registrar.

  You create a public DNS zone named tailspin.example in Azure DNS and add the records you need.

  You need the internet to resolve tailspin.example by using Azure DNS.

  What should you do next?
documentation:
  - "https://learn.microsoft.com/en-us/azure/dns/dns-delegate-domain-azure-dns"
  - "https://learn.microsoft.com/en-us/azure/dns/dns-zones-records"
skill_area: "name-resolution-load-balancing"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] At the registrar, set the domain's name servers to the four Azure DNS name servers listed in the zone's NS record.
  > Delegation happens at the parent: the registrar has to point the domain to the Azure DNS name servers assigned
  > to your zone.
- [ ] Add a CNAME record for tailspin.example in the Azure DNS zone.
  > A CNAME isn't allowed at the zone apex, and records in the zone don't delegate it.
- [ ] Link the zone to a virtual network.
  > Virtual network links are for private DNS zones, not public ones.
- [ ] Create an SOA record with the registrar's name server.
  > Azure DNS creates the SOA record itself. The parent delegation is what's missing.
