---
question: |-
  You have the availability set shown in the following exhibit.

  Microsoft performs planned maintenance on the hosts in North Europe.

  What is the maximum number of virtual machines in as-api-neu that can be unavailable at the same time because of the maintenance?
documentation:
  - title: "Availability sets"
    url: "https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview"
skill_area: "virtual-machines"
study_guide: "2026-04-17"
archetype: "calculate"
series: "as-api-neu"
---

```text
Availability set   as-api-neu
Location           North Europe
Fault domains      3
Update domains     10
Virtual machines   23
```

- [x] 3
  > VMs are placed round-robin over 10 update domains, so 23 VMs give three domains with 3 VMs and seven with 2.
  > Planned maintenance reboots one update domain at a time, so at most 3 are down.
- [ ] 2
  > This divides 23 by 10 and rounds down. Three update domains hold a third VM.
- [ ] 8
  > 8 is the size of the biggest fault domain, which matters for rack failures, not planned maintenance.
- [ ] 10
  > 10 is the number of update domains, not the number of VMs in one.
