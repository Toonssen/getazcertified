---
question: |-
  You have a Microsoft Entra tenant that contains users in the Amsterdam and Lisbon offices.

  You need to ensure that the helpdesk staff in Amsterdam can reset the passwords of Amsterdam users only.

  What should you do?
documentation:
  - title: "Administrative units"
    url: "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Create an administrative unit for the Amsterdam users and assign the Helpdesk Administrator role scoped to it.
  > Administrative units restrict a Microsoft Entra role assignment to the users and devices in the unit, so
  > password reset is limited to Amsterdam.
- [ ] Create a management group for Amsterdam and assign the Helpdesk Administrator role to it.
  > Management groups organize Azure subscriptions. They can't scope Microsoft Entra directory roles.
- [ ] Assign the Helpdesk Administrator role at the tenant scope.
  > A tenant-wide assignment lets the staff reset passwords for Lisbon users too.
- [ ] Create a custom Azure RBAC role with password-reset permissions.
  > Password reset is a Microsoft Entra permission. Azure RBAC roles cover Azure resources, not directory users.
