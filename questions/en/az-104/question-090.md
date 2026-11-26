---
question: |-
  You have a subnet named snet-quarantine that hosts virtual machines under investigation.

  You need to drop all traffic from snet-quarantine to the internet, without deploying another resource.

  Select the answer that completes the following statement.

  "In a route table associated with snet-quarantine, add a route for 0.0.0.0/0 that has a next hop type of ____."
documentation:
  - title: "Virtual network traffic routing"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview"
skill_area: "virtual-networks"
study_guide: "2026-04-17"
archetype: "complete-statement"
---

- [x] None
  > Next hop type None drops matching traffic. A 0.0.0.0/0 route to None stops all internet-bound traffic without
  > another resource.
- [ ] Internet
  > That's the default behavior: it sends the traffic to the internet.
- [ ] Virtual appliance
  > This needs an appliance IP address to forward to, which means deploying one.
- [ ] Virtual network gateway
  > This sends the traffic to a gateway (to on-premises) instead of dropping it.
