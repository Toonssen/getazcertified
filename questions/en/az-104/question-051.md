---
question: |-
  You have an App Service plan named asp-shop that runs two instances. You configure autoscale as shown in the following exhibit.

  Right after you save the setting, the average CPU percentage stays at 90 percent.

  How many instances are running 22 minutes later?
documentation: "https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-understanding-settings"
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

- [x] 5
  > The first scale-out happens once the 10-minute window is breached (3 instances). Each later action waits for
  > the 5-minute cool down: 4 at minute 15, 5 at minute 20. The next one would be at minute 25.
- [ ] 3
  > This stops after the first scale action. The rule keeps firing every time the cool down ends.
- [ ] 4
  > This counts one action too few: at minute 20 the cool down has passed and CPU is still above 75 percent.
- [ ] 6
  > The maximum is reached at minute 25, not by minute 22.
