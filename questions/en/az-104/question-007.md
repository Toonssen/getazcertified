---
question: |-
  You have a Microsoft Entra tenant.

  You need to create a dynamic security group that contains only the users who work in the Finance department and are based in Belgium.

  You are writing the membership rule shown in the following exhibit.

  Which value should you use for <property>?
documentation:
  - title: "Dynamic membership group rules"
    url: "https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "complete-code"
series: "dynamic-finance-belgium"
---

```text
(user.department -eq "Finance") -and (<property> -eq "Belgium")
```

- [x] user.country
  > user.country holds the country as text, so it can be compared with "Belgium".
- [ ] user.usageLocation
  > usageLocation is a two-letter code used for license availability (BE), so it would never equal "Belgium". It
  > describes where services are used, not where the user is based.
- [ ] device.deviceOSType
  > Device properties can't be used in a rule for a group of users.
- [ ] user.physicalDeliveryOfficeName
  > This is the office name, such as 'Brussels HQ', not the country.
