---
question: |-
  You have the Standard public IP addresses shown in the following table. None of them is associated with a resource.

  Your company runs regional load balancers for a web app in West Europe and East US. You add a cross-region load balancer named lbg-web in front of them so users reach the closest healthy region.

  Which public IP addresses can you use for the frontend of lbg-web?
documentation:
  - title: "Public IPs on Load Balancer"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/configure-public-ip-load-balancer"
  - title: "Global (cross-region) load balancer"
    url: "https://learn.microsoft.com/en-us/azure/load-balancer/cross-region-overview"
  - title: "Create a public IP address"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/create-public-ip-portal"
skill_area: "name-resolution-load-balancing"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name       SKU        Tier       Availability
pip-lb1    Standard   Regional   Zone-redundant
pip-lb2    Standard   Global     -
pip-lb3    Standard   Regional   No zone
pip-lb4    Standard   Global     -
```

- [x] pip-lb2 and pip-lb4 only
  > The frontend of a cross-region load balancer can only use the global tier of Standard public IPs. A global
  > address spans regions, while a regional address is tied to one region.
- [ ] pip-lb1 only
  > Zone redundancy protects against a zone failure inside one region, but pip-lb1 is still a regional-tier
  > address.
- [ ] pip-lb1 and pip-lb3 only
  > Regional-tier addresses are for regional load balancers, such as the ones behind lbg-web.
- [ ] pip-lb1, pip-lb2, pip-lb3, and pip-lb4
  > The tier matters: only global-tier addresses can be a cross-region frontend.
