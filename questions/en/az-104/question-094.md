---
question: |-
  You have a Recovery Services vault named rsv-prod that protects production virtual machines. A single backup administrator manages rsv-prod.

  You need to ensure that if the backup administrator's account is compromised, it can't disable soft delete or reduce the retention on rsv-prod without permission from a security administrator.

  What should you create first?
documentation:
  - "https://learn.microsoft.com/en-us/azure/backup/multi-user-authorization-concept"
  - "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A Resource Guard managed by the security administrator
  > Multi-user authorization for a vault relies on a Resource Guard. Critical operations on rsv-prod then also
  > need permission on the guard, which the backup admin doesn't have.
- [ ] A custom Azure role that excludes the soft delete actions
  > Whoever manages the vault can manage role assignments around it, and a role doesn't add a second approver.
- [ ] An administrative unit for the backup administrator
  > Administrative units scope Microsoft Entra roles. They don't protect vault operations.
- [ ] A CanNotDelete lock on rsv-prod
  > A lock stops the vault from being deleted. It doesn't protect settings such as soft delete or retention, and
  > the admin could remove it.
