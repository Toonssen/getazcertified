---
question: |-
  You have an Azure virtual machine named vm-crm1 and a Recovery Services vault named rsv-crm.

  On March 1, you protect vm-crm1 with a standard backup policy that has the following settings:

  - Backup frequency: daily at 22:00 UTC
  - Retain instant recovery snapshots for: 3 days
  - Retain daily backup points for: 14 days
  - Instant restore resource group: rg-crm-restore

  How many instant recovery snapshots of vm-crm1 are kept in rg-crm-restore on March 20?
documentation:
  - title: "Instant Restore for VM backups"
    url: "https://learn.microsoft.com/en-us/azure/backup/backup-instant-restore-capability"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "calculate"
---

- [x] 3
  > rg-crm-restore holds the restore point collection with the instant recovery snapshots, which are kept for 3
  > days. The 14 daily recovery points live in the vault, not in the resource group.
- [ ] 14
  > 14 is the number of daily recovery points in the vault.
- [ ] 17
  > Snapshots and vault recovery points are stored separately and aren't added together.
- [ ] 19
  > Snapshots older than the 3-day retention are deleted.
