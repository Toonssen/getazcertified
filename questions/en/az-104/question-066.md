---
question: |-
  You have the App Service web apps shown in the following table.

  You need to run a background script on a schedule by using WebJobs.

  Which apps support WebJobs?
documentation: "https://learn.microsoft.com/en-us/azure/app-service/overview-webjobs"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
App       Platform
app-w1    Windows, code (.NET 8)
app-w2    Windows, custom container
app-l1    Linux, code (Python 3.12)
app-l2    Linux, custom container based on Alpine Linux
```

- [x] app-w1, app-w2, and app-l1 only
  > WebJobs run on Windows code, Windows containers, Linux code and Linux containers. Custom Linux containers
  > based on Alpine Linux are the exception.
- [ ] app-w1 only
  > That was true years ago. Containers and Linux are supported now.
- [ ] app-w1 and app-w2 only
  > Linux code apps such as app-l1 support WebJobs too.
- [ ] app-w1, app-w2, app-l1, and app-l2
  > Alpine-based custom Linux containers don't support WebJobs.
