---
question: |-
  You have the resources shown in the following exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "app-orders can connect to vm-sql."
documentation:
  - title: "App Service VNet integration"
    url: "https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "app-orders-vnet"
---

```text
Name         Type              Details
VNet-Core    Virtual network   Subnets: snet-integration (delegated to Microsoft.Web/serverFarms), snet-mgmt
VNet-Data    Virtual network   Peered with VNet-Core. Subnet snet-sql contains vm-sql
app-orders   Web app           Premium v3 plan, virtual network integration with VNet-Core/snet-integration
NSG-Integration    NSG               Associated to snet-integration. Inbound rule: deny all traffic from Internet
```

- [x] Yes
  > Virtual network integration routes the app's outbound calls into VNet-Core, and from there to peered virtual
  > networks such as VNet-Data, unless an NSG or route blocks it.
- [ ] No
  > Integration isn't limited to the integration subnet's own virtual network: peered networks, globally peered
  > ones included, are reachable.
