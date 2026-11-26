---
question: |-
  You plan to deploy six low-traffic internal web apps to Azure App Service. All the apps run on Linux in the same region and have similar resource needs.

  You need to identify what to create before you deploy the apps. The solution must minimize costs.

  What should you create?
documentation:
  - title: "App Service plans"
    url: "https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans"
  - title: "App Service Environment overview"
    url: "https://learn.microsoft.com/en-us/azure/app-service/environment/overview"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A single App Service plan shared by all six apps
  > Several apps can share one plan and its instances. You pay for the plan, not per app, so one plan is the
  > cheapest option.
- [ ] A separate App Service plan for each app
  > One plan per app multiplies the compute you pay for.
- [ ] An App Service Environment v3
  > An App Service Environment is single-tenant, Isolated-tier hosting, by far the most expensive option.
- [ ] An Azure Application Gateway in front of the apps
  > A gateway load-balances traffic to apps. It doesn't host them.
