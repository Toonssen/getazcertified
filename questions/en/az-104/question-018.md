---
question: |-
  You have the Azure hierarchy and role assignments shown in the following exhibit. RG-1 contains a virtual machine named vm-app1.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "User3 can delete vm-app1."
documentation:
  - title: "Steps to assign an Azure role"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps"
  - title: "What is Azure RBAC?"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
---

```text
Tenant Root Group
  MG-Corp                 User3: Contributor
    Sub-A
      RG-1                User3: Reader
        vm-app1
```

- [x] Yes
  > Role assignments are inherited by child scopes, and Azure RBAC is additive. Contributor from MG-Corp applies
  > at RG-1, and the Reader assignment there doesn't take it away.
- [ ] No
  > A lower-scope Reader assignment doesn't override an inherited Contributor. Only a deny assignment would block
  > the delete.
