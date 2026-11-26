---
question: |-
  You have a Recovery Services vault named rsv-core that has soft delete enabled. rsv-core protects the items shown in the following table.

  Which items' backups does rsv-core's soft delete protect?
documentation:
  - title: "Soft delete for Azure Backup"
    url: "https://learn.microsoft.com/en-us/azure/backup/secure-by-default"
  - title: "Soft delete for Azure file shares"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-prevent-file-share-deletion"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Item           Workload                       Backup tier
vm-app5        Azure virtual machine          Vault
sql-app5       SQL Server in an Azure VM      Vault
share-docs     Azure file share               Snapshot (operational)
```

- [x] vm-app5 and sql-app5 only
  > Vault soft delete protects data stored in the vault. Snapshot-based Azure Files backups stay in the storage
  > account and are protected by the account's file share soft delete instead.
- [ ] vm-app5 only
  > SQL Server in Azure VM backups are vaulted data too, so they're covered.
- [ ] share-docs only
  > This is backwards: the snapshot-tier share is the one outside vault soft delete.
- [ ] vm-app5, sql-app5, and share-docs
  > Snapshots of the share aren't in the vault. A share on the vaulted Azure Files tier would be covered.
