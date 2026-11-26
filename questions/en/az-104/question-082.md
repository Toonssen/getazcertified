---
question: |-
  You have an app that runs on two virtual machines named vm-a and vm-b behind a public Azure Standard Load Balancer. The load balancing rule and the health probe both use TCP port 8443.

  The effective inbound security rules for both virtual machines are shown in the following exhibit.

  Connections to the app from the partner address 203.0.113.20 fail. The load balancer configuration is correct.

  You need to ensure that the partner can connect to the app.

  Solution: You create an inbound rule with priority 150 that allows TCP 8443 from the AzureLoadBalancer service tag.

  Does this meet the goal?
documentation:
  - title: "Load Balancer health probes"
    url: "https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-custom-probe-overview"
  - title: "Network security groups"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview"
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

- [x] Yes
  > Health probes come from the AzureLoadBalancer tag (168.63.129.16). Rule 200 denies them before the default
  > allow at 65001, so both VMs are marked unhealthy and get no traffic. An allow at 150 lets the probes through,
  > and rule 100 already admits the partner.
- [ ] No
  > The partner rule is fine. The problem is the probe, and allowing AzureLoadBalancer above priority 200 solves
  > it.
