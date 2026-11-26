---
question: |-
  You have an App Service plan named asp-shop that runs two instances. You configure autoscale as shown in the following exhibit.

  Select the answer that completes the following statement.

  "After the first scale-out action, the earliest that the scale-out rule can start another scale-out action is ____ later."
documentation:
  - title: "Autoscale settings in Azure Monitor"
    url: "https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-understanding-settings"
skill_area: "app-service"
study_guide: "2026-04-17"
archetype: "complete-statement"
series: "asp-shop-autoscale"
---

```text
Autoscale setting for App Service plan asp-shop
  Instance limits:   Minimum 2   Maximum 6   Default 2
  Scale out rule:    Average CPU percentage > 75 over the last 10 minutes -> increase count by 1, cool down 5 minutes
  Scale in rule:     Average CPU percentage < 25 over the last 10 minutes -> decrease count by 1, cool down 5 minutes
```

- [x] 5 minutes
  > The cool down is the time after a scale action before the rule may act again: 5 minutes here.
- [ ] 1 minute
  > Autoscale evaluates often, but the rule is blocked until its cool down ends.
- [ ] 10 minutes
  > 10 minutes is the metric window the rule evaluates, not the wait between actions.
- [ ] 15 minutes
  > This adds the window to the cool down. Only the cool down decides when the rule may act again.
