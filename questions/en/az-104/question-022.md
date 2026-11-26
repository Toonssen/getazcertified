---
question: |-
  You have an Azure subscription that contains a resource group named RG-Test. RG-Test contains several virtual machines.

  You need to ensure that the virtual machines in RG-Test are shut down automatically when the month's costs for RG-Test reach 90 percent of EUR 200.

  What should you do?
documentation:
  - title: "Create and manage budgets"
    url: "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets"
  - title: "Azure spending limit"
    url: "https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/spending-limit"
skill_area: "subscriptions-governance"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Create a budget for RG-Test with an alert condition at 90 percent that triggers an action group that runs an automation runbook.
  > Budgets don't stop resources on their own. A budget alert can trigger an action group, and the action group
  > can run automation (a runbook or Logic App) that shuts the VMs down.
- [ ] Create a budget for RG-Test with an email alert at 90 percent.
  > An email alert only notifies. Nothing shuts the VMs down.
- [ ] Set a spending limit on the subscription.
  > A spending limit exists only on free accounts and offers with monthly credits (not pay-as-you-go), and when
  > it's reached all deployed services are disabled, not just specific VMs.
- [ ] Assign an Azure Policy definition that denies virtual machines in RG-Test.
  > Policy evaluates resource configuration, not cost, and deny doesn't shut down existing VMs.
