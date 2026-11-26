---
question: |-
  You have a resource group named RG-Ops that contains a virtual machine named vm-ops1. You create the activity log alert rules shown in the following exhibit, and then two users perform the actions shown in the second exhibit.

  Which alert rules does UserA's action trigger?
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

- [x] Alert-RG and Alert-VM
  > Creating the disk is an administrative write in RG-Ops. Attaching it updates vm-ops1, another administrative
  > write, and it also falls under RG-Ops.
- [ ] Alert-RG only
  > Attaching a disk changes the VM resource itself, which Alert-VM watches.
- [ ] Alert-VM only
  > The disk is created in RG-Ops, which Alert-RG covers.
- [ ] No alert rules
  > Every create, update and delete through Azure Resource Manager is logged in the Administrative category.
