---
question: |-
  You have the availability set shown in the following exhibit.

  A rack (power and network) fails in the datacenter that hosts as-api-neu.

  What is the maximum number of virtual machines in as-api-neu that can be unavailable because of the failure?
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

- [x] 8
  > A fault domain is a rack with shared power and network. 23 VMs over 3 fault domains give 8, 8 and 7, so one
  > failed rack takes down at most 8.
- [ ] 3
  > 3 is the largest update domain, which applies to planned maintenance.
- [ ] 7
  > 7 is the smallest fault domain. The question asks for the maximum.
- [ ] 23
  > Spreading over fault domains exists to stop one rack failure from taking down every VM.
