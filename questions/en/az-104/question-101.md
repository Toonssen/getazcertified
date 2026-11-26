---
question: |-
  You have an Azure virtual machine named vm-iis4 that runs Windows Server. The Azure Monitor Agent collects vm-iis4's Application event log into a Log Analytics workspace named law-ops by using a data collection rule.

  You need an alert when an event with level Error from the source IIS appears in the Application log of vm-iis4.

  What should you use as the scope of the alert rule?
documentation:
  - title: "Types of Azure Monitor alerts"
    url: "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types"
  - title: "Data collection rules"
    url: "https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-overview"
skill_area: "monitor-resources"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] law-ops
  > The events are stored in the workspace. A log search alert scoped to law-ops runs a KQL query against the
  > Event table and fires on matches.
- [ ] vm-iis4
  > A VM scope suits metric alerts on platform metrics such as CPU. Event log entries aren't metrics.
- [ ] The data collection rule
  > The DCR defines what is collected. It doesn't hold the data an alert can query.
- [ ] The subscription
  > A subscription scope is for activity log or service health alerts, not guest event logs.
