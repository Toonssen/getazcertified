---
question: |-
  You have the resources shown in the following exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "NSG-Integration blocks requests from the internet to app-orders."
documentation: "https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration"
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

- [ ] No
  > Virtual network integration is outbound only. Inbound NSG rules on the integration subnet don't apply to the
  > app. To restrict inbound traffic, use access restrictions or a private endpoint.
- [x] Yes
  > The app still receives traffic on its public endpoint. The subnet's NSG only affects the outbound traffic the
  > app sends through the integration.
