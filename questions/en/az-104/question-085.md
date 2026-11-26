---
question: |-
  You have the resources shown in the following table.

  You create an application security group named asg-web.

  Which resources can use or contain asg-web?
documentation: "https://learn.microsoft.com/en-us/azure/virtual-network/application-security-groups"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name          Type
nsg-front     Network security group
nic-web01     Network interface of vm-web01
snet-front    Subnet
app-portal    App Service web app
```

- [x] nsg-front and nic-web01 only
  > An application security group is referenced as a source or destination in NSG security rules, and its members
  > are network interfaces.
- [ ] nsg-front only
  > Network interfaces are what you add to an ASG, so nic-web01 qualifies too.
- [ ] nsg-front, nic-web01, and snet-front only
  > You associate an NSG with a subnet, not an ASG.
- [ ] nic-web01 and app-portal only
  > An App Service app has no network interface to add, and the ASG is only used inside NSG rules.
