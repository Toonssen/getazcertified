---
question: |-
  You have the vaults and resources shown in the following exhibits. All are in the same region.

  To which vaults can you back up the blob containers in stmedia07 by using Azure Backup?
documentation:
  - "https://learn.microsoft.com/en-us/azure/backup/backup-vault-overview"
  - "https://learn.microsoft.com/en-us/azure/backup/backup-overview"
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
  > Azure Blobs backup (operational and vaulted) is a Backup vault workload. Recovery Services vaults don't
  > protect blobs.
- [ ] rsv-data only
  > Recovery Services vaults handle VMs, SQL/SAP HANA in VMs and Azure Files, not blobs.
- [ ] bv-data or rsv-data
  > Each workload belongs to one vault type, and blobs belong to Backup vaults.
- [ ] Neither vault
  > Blobs are supported, through a Backup vault.
