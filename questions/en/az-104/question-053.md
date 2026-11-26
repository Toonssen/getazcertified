---
question: |-
  You have an App Service plan named asp-shop that runs two instances. You configure autoscale as shown in the following exhibit.

  During the first hour after you save the setting, the average CPU percentage stays at 10 percent.

  How many instances are running at the end of the hour?
documentation:
  - title: "Autoscale settings in Azure Monitor"
    url: "https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-understanding-settings"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "calculate"
series: "asp-shop-autoscale"
---

```text
Autoscale setting for App Service plan asp-shop
  Instance limits:   Minimum 2   Maximum 6   Default 2
  Scale out rule:    Average CPU percentage > 75 over the last 10 minutes -> increase count by 1, cool down 5 minutes
  Scale in rule:     Average CPU percentage < 25 over the last 10 minutes -> decrease count by 1, cool down 5 minutes
```

- [x] 2
  > The scale-in rule would remove instances, but autoscale never goes below the minimum of 2, which is also the
  > current count.
- [ ] 1
  > Autoscale doesn't go below the instance limit minimum.
- [ ] 0
  > App Service autoscale can't scale to zero, and the minimum is 2.
- [ ] 6
  > Low CPU triggers scale-in, not scale-out.
