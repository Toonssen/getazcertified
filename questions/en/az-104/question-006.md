---
question: |-
  You have a Microsoft Entra tenant.

  You need to create a dynamic security group that contains only the users who work in the Finance department and are based in Belgium.

  You are writing the membership rule shown in the following exhibit.

  Which value should you use for <operator>?
documentation:
  - title: "Dynamic membership group rules"
    url: "https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "complete-code"
series: "dynamic-finance-belgium"
---

```text
(user.department -eq "Finance") <operator> (user.country -eq "Belgium")
```

- [x] -and
  > Both conditions must be true for a user to be a member, so the expressions are joined with -and.
- [ ] -or
  > -or would add every Finance user anywhere plus every user in Belgium in any department.
- [ ] -not
  > -not negates one expression. It doesn't join two.
- [ ] -any
  > -any is for multi-valued properties such as assignedPlans, not for joining expressions.
