---
question: |-
  You have a Microsoft Entra tenant.

  You receive a CSV file that lists 350 new employees.

  You need to create a user account for each employee in the Microsoft Entra admin center. The solution must minimize administrative effort.

  What should you use?
documentation:
  - title: "Bulk create users"
    url: "https://learn.microsoft.com/en-us/entra/identity/users/users-bulk-add"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Bulk create
  > Bulk create in the admin center takes a CSV template and creates the user accounts in one operation.
- [ ] Bulk invite
  > Bulk invite sends B2B invitations to external guests. It doesn't create member accounts.
- [ ] New user, once per employee
  > This works, but it means 350 separate tasks.
- [ ] Microsoft Entra Connect Sync
  > Connect Sync synchronizes accounts from on-premises AD DS. These employees exist only in a CSV file.
