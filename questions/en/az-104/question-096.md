---
question: |-
  You have a resource group named RG-Ops that contains a virtual machine named vm-ops1. You create the activity log alert rules shown in the following exhibit, and then two users perform the actions shown in the second exhibit.

  Which alert rules does UserB's action trigger?
documentation: "https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log-schema"
skill_area: "monitor-resources"
study_guide: "2026-04-17"
archetype: "exhibit-select"
series: "ops-activity-alerts"
---

```text
Alert rule   Scope      Condition (activity log)
Alert-RG     RG-Ops     Category: Administrative, all operations
Alert-VM     vm-ops1    Category: Administrative, all operations
```

```text
User    Action
UserA   Creates a managed disk in RG-Ops and attaches it to vm-ops1
UserB   Signs in to vm-ops1 over RDP and installs an application
```

- [x] No alert rules
  > Signing in and installing software happen inside the guest OS. They aren't Azure Resource Manager operations,
  > so nothing reaches the activity log.
- [ ] Alert-VM only
  > The activity log records control-plane operations on vm-ops1, not what happens inside it.
- [ ] Alert-RG and Alert-VM
  > Neither action is an operation on an Azure resource.
- [ ] Alert-RG only
  > No resource in RG-Ops is created, changed or deleted.
