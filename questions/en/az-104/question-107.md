---
question: |-
  You have 30 Azure virtual machines that don't have any monitoring agents installed.

  You need to view CPU, memory, and disk performance trends for the VMs in VM insights.

  What must be deployed to each VM, and what defines what is collected?
documentation:
  - title: "Enable VM insights"
    url: "https://learn.microsoft.com/en-us/azure/azure-monitor/vm/vminsights-enable"
  - title: "Migrate from the Log Analytics agent"
    url: "https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-migration"
skill_area: "monitor-resources"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] The Azure Monitor Agent, with a data collection rule
  > VM insights uses the Azure Monitor Agent, and a data collection rule says which performance data goes to which
  > Log Analytics workspace.
- [ ] The Log Analytics agent, with workspace settings
  > The legacy Log Analytics agent is retired. VM insights uses the Azure Monitor Agent.
- [ ] The Network Watcher extension, with a flow log
  > That extension serves network diagnostics, not guest performance counters.
- [ ] Nothing, because platform metrics include guest memory
  > Host-level platform metrics don't include guest-level memory usage, which needs the agent.
