---
question: |-
  You have an Azure subscription.

  You are creating the custom role shown in the following exhibit. Members of the operations team must be able to start, stop, restart, and reconfigure virtual machines, but the role must not allow them to delete virtual machines.

  Which value should you use for <value>?
documentation:
  - title: "Azure role definitions"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "complete-code"
---

```json
{
  "Name": "VM Operator Plus",
  "Actions": [ "Microsoft.Compute/virtualMachines/*" ],
  "NotActions": [ "<value>" ],
  "AssignableScopes": [ "/subscriptions/00000000-0000-0000-0000-000000000000" ]
}
```

- [x] Microsoft.Compute/virtualMachines/delete
  > NotActions subtracts this action from the wildcard in Actions, so everything except delete remains. NotActions
  > isn't a deny: another role that grants delete would still allow it.
- [ ] Microsoft.Compute/virtualMachines/write
  > Removing write would stop the team from reconfiguring virtual machines, and delete would still be allowed.
- [ ] Microsoft.Compute/virtualMachines/*/read
  > Removing read actions breaks the portal experience and still leaves delete.
- [ ] Microsoft.Compute/virtualMachines/deallocate/action
  > This would stop the team from stopping (deallocating) virtual machines, which they need.
