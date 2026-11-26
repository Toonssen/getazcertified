---
question: |-
  You have a Microsoft Entra tenant that contains the groups shown in the following table.

  You assign a Microsoft 365 E3 license to G-Staff by using group-based licensing.

  Which users receive the license from G-Staff?
documentation:
  - title: "Group-based licensing"
    url: "https://learn.microsoft.com/en-us/entra/fundamentals/concept-group-based-licensing"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Group      Type       Members
G-Staff    Security   UserA, UserB, G-Interns
G-Interns  Security   UserC, UserD
```

- [x] UserA and UserB only
  > Group-based licensing applies to the direct members of the group. Nested groups aren't supported, so the
  > members of G-Interns get nothing from G-Staff.
- [ ] UserA, UserB, UserC, and UserD
  > This assumes the license flows through the nested group G-Interns, which group-based licensing doesn't do.
- [ ] UserC and UserD only
  > These users are members of G-Interns, not direct members of G-Staff.
- [ ] No users, because a nested group blocks the assignment
  > The nested group is ignored. The direct members are still licensed.
