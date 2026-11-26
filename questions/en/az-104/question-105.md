---
question: |-
  You have 15 Azure Monitor alert rules across three subscriptions.

  When any of the alerts fires, the on-call team must get an SMS and a ticket must be created through a webhook. The solution must minimize administrative effort when the on-call phone numbers change.

  What should you configure?
documentation:
  - "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/action-groups"
  - "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-processing-rules"
skill_area: "monitor-resources"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] One action group with the SMS and webhook actions, used by all 15 alert rules
  > An action group is a reusable set of notifications and actions. Changing a phone number in the group updates
  > every rule that uses it.
- [ ] The SMS and webhook settings in each alert rule
  > Alert rules don't hold notification details. That's what action groups are for.
- [ ] One alert processing rule per subscription that sends SMS messages
  > Processing rules add or suppress action groups. They don't send notifications themselves.
- [ ] A Logic App per alert rule
  > This works but means 15 workflows to keep in sync.
