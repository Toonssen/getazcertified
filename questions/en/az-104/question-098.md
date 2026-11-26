---
question: |-
  You have the vaults and resources shown in the following exhibits. All are in the same region.

  To which vaults can you back up disk-sql02 by using Azure Disk Backup?
documentation:
  - "https://learn.microsoft.com/en-us/azure/backup/backup-vault-overview"
  - "https://learn.microsoft.com/en-us/azure/backup/disk-backup-overview"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "exhibit-select"
series: "vault-types"
---

```text
Vault        Type
bv-data      Backup vault
rsv-data     Recovery Services vault
```

```text
Resource        Type
stmedia07       Storage account (blob containers and Azure file shares)
disk-sql02      Managed disk
```

- [x] bv-data only
  > Azure Disk Backup protects individual managed disks with snapshots, and it's configured in a Backup vault.
- [ ] rsv-data only
  > A Recovery Services vault backs up the whole VM, not a single managed disk through Azure Disk Backup.
- [ ] bv-data or rsv-data
  > Azure Disk Backup is only available with Backup vaults.
- [ ] Neither vault
  > Managed disks are a supported Backup vault workload.
