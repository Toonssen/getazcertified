---
question: |-
  You have two Azure subscriptions named Sub-Dev3 and Sub-Prod3 that contain the resource groups shown in the following exhibit.

  You create a custom role named Web Operator2. The AssignableScopes property of Web Operator2 contains only Sub-Dev3. You have the Owner role for both subscriptions.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "You can assign Web Operator2 to a user at the scope of rg-web6."
documentation:
  - title: "Azure role definitions"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions"
  - title: "Azure custom roles"
    url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
---

```text
Resource group  Subscription
rg-web5         Sub-Dev3
rg-api5         Sub-Dev3
rg-web6         Sub-Prod3
```

- [ ] Yes
  > AssignableScopes sets where a custom role can be assigned. Web Operator2 lists only Sub-Dev3, and rg-web6 is
  > in Sub-Prod3. Being Owner of Sub-Prod3 doesn't change where the role is available.
- [x] No
  > A custom role is available for assignment only in the scopes its AssignableScopes lists, plus the resource
  > groups and resources inside them. Sub-Prod3 isn't listed, so the role isn't available at rg-web6.
