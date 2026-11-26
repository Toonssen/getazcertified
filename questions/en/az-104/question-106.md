---
question: |-
  You have an Azure virtual machine named vm-api3. Clients report that connections to vm-api3 on TCP port 8080 from 198.51.100.40 time out.

  You need to determine whether a network security group rule is blocking the traffic, and which rule it is.

  What should you use?
documentation:
  - "https://learn.microsoft.com/en-us/azure/network-watcher/ip-flow-verify-overview"
  - "https://learn.microsoft.com/en-us/azure/network-watcher/connection-monitor-overview"
skill_area: "monitor-resources"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] IP flow verify in Azure Network Watcher
  > IP flow verify tests a 5-tuple against the effective security rules and returns Allow or Deny with the name of
  > the matching rule.
- [ ] Connection monitor in Azure Network Watcher
  > Connection monitor tracks reachability and latency over time between endpoints, but it doesn't name the NSG
  > rule involved.
- [ ] Next hop in Azure Network Watcher
  > Next hop shows routing (where a packet goes), not security rule decisions.
- [ ] VM insights
  > VM insights shows performance and process dependencies, not NSG evaluation.
