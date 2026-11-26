---
question: |-
  You have an Azure App Service web app named app-tickets that runs in an App Service plan on the Standard S1 tier. app-tickets already uses five staging deployment slots.

  A user named Dev2 has the Contributor role for app-tickets.

  You need to ensure that Dev2 can create three more staging slots for app-tickets.

  What should you do?
documentation:
  - title: "Azure subscription limits"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits"
  - title: "App Service staging slots"
    url: "https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Scale up the App Service plan to a Premium tier.
  > Staging slots per app are a tier limit: Standard 5, Premium and Isolated 20. Moving the plan to Premium (scale
  > up) raises the limit.
- [ ] Scale out the App Service plan to three instances.
  > Scaling out adds instances of the same tier. The slot limit stays at 5.
- [ ] Assign Dev2 the Owner role for app-tickets.
  > Contributor can already create slots. The limit is the tier, not permissions.
- [ ] Assign Dev2 the Website Contributor role for app-tickets.
  > Another role doesn't change the tier's slot limit.
