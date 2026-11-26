---
question: |-
  An Azure VM named vm-orders hosts a database that changes all day. The business accepts losing at most 6 hours of data if the VM must be restored.

  You plan to meet this recovery point objective with Azure Backup alone.

  Which kind of policy do you need?
documentation:
  - "https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-enhanced-policy"
  - "https://learn.microsoft.com/en-us/azure/backup/backup-vault-overview"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Enhanced, in a Recovery Services vault
  > VM backups use a Recovery Services vault, and only the Enhanced policy supports several backups a day (every
  > 4, 6, 8, 12 or 24 hours).
- [ ] Standard, in a Recovery Services vault
  > A standard policy schedules daily or weekly backups only.
- [ ] Any policy in a Backup vault
  > Backup vaults don't protect whole Azure VMs.
- [ ] An Azure Automation runbook that triggers on-demand backups
  > This works around the schedule instead of using the supported policy, and it adds automation to maintain.
