---
question: |-
  You have an app that runs on two virtual machines named vm-a and vm-b behind a public Azure Standard Load Balancer. The load balancing rule and the health probe both use TCP port 8443.

  The effective inbound security rules for both virtual machines are shown in the following exhibit.

  Connections to the app from the partner address 203.0.113.20 fail. The load balancer configuration is correct.

  You need to ensure that the partner can connect to the app.

  Solution: You change the priority of the Allow-Partner rule from 100 to 90.

  Does this meet the goal?
documentation:
  - "https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-custom-probe-overview"
  - "https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview"
skill_area: "name-resolution-load-balancing"
study_guide: "2026-04-17"
archetype: "goal-solution"
series: "lb-probe-8443"
---

```text
Inbound security rules (NSG on the subnet of vm-a and vm-b)
Priority  Name               Source              Destination  Port  Protocol  Action
100       Allow-Partner      203.0.113.20        Any          8443  TCP       Allow
200       Deny-8443          Any                 Any          8443  TCP       Deny
65000     AllowVnetInBound   VirtualNetwork      VirtualNetwork Any Any       Allow
65001     AllowAzureLoadBalancerInBound AzureLoadBalancer Any Any Any       Allow
65500     DenyAllInBound     Any                 Any          Any   Any       Deny
```

- [ ] No
  > Allow-Partner already wins for the partner's traffic. The failure is the health probe, which Deny-8443 still
  > blocks, so the backends stay unhealthy.
- [x] Yes
  > Raising the partner rule's priority changes nothing: rule 200 still blocks the AzureLoadBalancer probe.
