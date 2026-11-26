---
question: |-
  You have three Azure subscriptions in a management group named MG-Apps.

  You need to apply the same 12 Azure Policy definitions to all three subscriptions, and to any subscription added to MG-Apps later. The solution must minimize administrative effort.

  What should you do?
documentation:
  - title: "Azure Policy overview"
    url: "https://learn.microsoft.com/en-us/azure/governance/policy/overview"
  - title: "Azure Blueprints retirement"
    url: "https://learn.microsoft.com/en-us/azure/governance/blueprints/blueprint-retirement"
skill_area: "subscriptions-governance"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Create an initiative that contains the 12 definitions and assign it to MG-Apps.
  > An initiative groups definitions into one assignable unit. Assigned at the management group, it's inherited by
  > every current and future subscription under it.
- [ ] Assign each of the 12 definitions to each subscription.
  > That's 36 assignments, and new subscriptions would need 12 more each.
- [ ] Create an Azure Blueprints definition and assign it to each subscription.
  > Azure Blueprints is being retired: new blueprint definitions can't be created since July 31, 2026, and new
  > assignments can't be created since October 31, 2026.
- [ ] Create a custom role that contains the definitions.
  > Roles grant permissions. They can't hold policy definitions.
