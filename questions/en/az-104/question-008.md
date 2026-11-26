---
question: |-
  You have a Microsoft Entra tenant that has Microsoft Entra ID P1 licenses.

  You need to grant access to a resource for the Finance department's users and the Windows devices registered to them by using dynamic membership. The solution must minimize administrative effort.

  What should you do?
documentation:
  - title: "Dynamic membership group rules"
    url: "https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "best-choice"
series: "dynamic-finance-belgium"
---

- [x] Create two dynamic groups: one with a user rule and one with a device rule.
  > A dynamic membership rule can contain users or devices, never both. Two groups, each with its own rule, keep
  > membership automatic.
- [ ] Create one dynamic group whose rule combines user.department and device.deviceOSType.
  > You can't create a rule that mixes user and device properties.
- [ ] Create one assigned group and add the users and devices manually.
  > This works but isn't dynamic, and every change in Finance becomes a manual task.
- [ ] Create one dynamic Microsoft 365 group with a device rule.
  > Microsoft 365 groups can only contain users, so a device rule isn't available for them.
