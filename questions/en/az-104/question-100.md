---
question: |-
  You have an Azure key vault named kv-pay.

  You need to analyze who accessed kv-pay's secrets over the last 30 days by running Kusto Query Language (KQL) queries.

  To which destination should you send kv-pay's resource logs in a diagnostic setting?
documentation: "https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings"
skill_area: "monitor-resources"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A Log Analytics workspace
  > Resource logs in a Log Analytics workspace can be queried with KQL, for investigations, workbooks and log
  > alerts.
- [ ] A storage account
  > A storage account is cheap long-term archive, but you can't run KQL on it directly.
- [ ] An event hub
  > An event hub streams logs to other systems, such as a third-party SIEM. It isn't a query store.
- [ ] A partner solution
  > Partner integrations send logs to third-party tools, not to Azure Monitor Logs.
