---
question: |-
  You have an Azure App Service web app named app-tickets that runs in an App Service plan named plan-tickets on a Premium tier. app-tickets has eight deployment slots.

  To reduce costs, you plan to move plan-tickets to the Standard tier.

  You need to ensure that you can scale plan-tickets down to the Standard tier.

  What should you do first?
documentation:
  - title: "App Service staging slots"
    url: "https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots"
  - title: "Azure subscription limits"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Delete deployment slots until app-tickets has no more than five.
  > The target tier must support the number of slots the app already uses. Standard supports only five, so an app
  > with more than five slots can't scale down to it.
- [ ] Swap each staging slot into production.
  > A swap exchanges the content of two slots. Every slot still exists afterwards, so the count stays at eight.
- [ ] Scale in plan-tickets to one instance.
  > The instance count doesn't change the slot limit. Standard allows five slots per app at any instance count.
- [ ] Stop every staging slot of app-tickets.
  > A stopped slot still counts as a slot. Only deleting slots brings the count down.
