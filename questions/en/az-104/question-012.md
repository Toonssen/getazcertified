---
question: |-
  You have a Microsoft Entra tenant.

  You need to ensure that a user named Ops3 can perform the following tasks:

  - Create new user accounts.
  - Assign licenses to users.
  - Reset the passwords of users who aren't administrators.

  The solution must follow the principle of least privilege.

  Which Microsoft Entra role should you assign to Ops3?
documentation: "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] User Administrator
  > User Administrator creates and manages users and groups, assigns licenses, and resets passwords for non-admins
  > and limited admins. It is the smallest single role that covers all three tasks.
- [ ] Helpdesk Administrator
  > Helpdesk Administrator resets passwords for non-admins but can't create users or assign licenses.
- [ ] License Administrator
  > License Administrator manages license assignments but can't create users or reset passwords.
- [ ] Global Administrator
  > This covers everything, which breaks least privilege.
