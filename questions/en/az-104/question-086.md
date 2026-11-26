---
question: |-
  You plan to add an inbound security rule named Allow-Mgmt to a network security group.

  Allow-Mgmt must be evaluated before every other custom rule in the network security group.

  Which priority should you assign?
documentation: "https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "fact-recall"
---

- [x] 100
  > Custom rule priorities range from 100 to 4096, and lower numbers are processed first. 100 is the lowest
  > allowed number.
- [ ] 0
  > 0 is outside the allowed range of 100 to 4096.
- [ ] 1
  > 1 is outside the allowed range.
- [ ] 4096
  > 4096 is the lowest priority (processed last), the opposite of what's needed.
