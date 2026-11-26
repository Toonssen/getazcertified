---
question: |-
  You have a virtual network named VNet-Shop.

  You plan to host a web app that must be deployed into VNet-Shop, so that the app runs inside a subnet of VNet-Shop and is reachable only on a private IP address. The solution must minimize costs.

  Which App Service pricing tier should you use?
documentation:
  - title: "App Service Environment overview"
    url: "https://learn.microsoft.com/en-us/azure/app-service/environment/overview"
  - title: "App Service VNet integration"
    url: "https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Isolated v2 (an App Service Environment v3)
  > Only an App Service Environment runs the app itself in a subnet of your virtual network, and ASE v3 uses the
  > Isolated v2 tier. The other tiers stay multitenant.
- [ ] Basic B1
  > Basic supports virtual network integration, but that only carries the app's outbound calls into the network.
  > The app isn't deployed into it.
- [ ] Premium v3 P0v3
  > Premium v3 adds integration and private endpoints, but the app still runs in the multitenant service, not in
  > VNet-Shop.
- [ ] Free F1
  > Free has no virtual network features at all.
