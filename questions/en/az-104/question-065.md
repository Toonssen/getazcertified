---
question: |-
  You have an Azure App Service web app named app-catalog.

  You need to configure continuous deployment so that every push to the main branch of an Azure Repos repository is deployed to app-catalog.

  What should you use?
documentation:
  - title: "Continuous deployment for App Service"
    url: "https://learn.microsoft.com/en-us/azure/app-service/deploy-continuous-deployment"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Deployment Center
  > Deployment Center connects the app to a source repository (Azure Repos, GitHub, Bitbucket or local Git) and
  > sets up the build and deploy.
- [ ] Deployment slots
  > Slots are deployment targets (staging, swap), not a source connection.
- [ ] Service Connector
  > Service Connector configures connections from the app to other Azure services such as databases and storage.
- [ ] App Service Editor
  > The editor changes files in place. It doesn't connect a repository.
