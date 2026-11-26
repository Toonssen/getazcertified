---
question: |-
  Scheduled backups of vm-erp2, a Windows Server VM, succeed, but backups are only crash-consistent instead of application-consistent. The vault dashboard flags vm-erp2 with a Warning in its Backup Pre-Check column.

  Which issue is the most likely cause?
documentation: "https://learn.microsoft.com/en-us/azure/backup/backup-azure-manage-windows-server"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] The Azure VM Agent on vm-erp2 is outdated.
  > Backup prechecks look at the VM's configuration. An old or missing VM Agent is a typical warning, because the
  > backup extension depends on the agent.
- [ ] Soft delete is enabled on the vault.
  > Soft delete protects deleted backup data. It doesn't affect how consistent new backups are, and it isn't a
  > precheck finding.
- [ ] The vault uses geo-redundant storage.
  > Vault redundancy has nothing to do with VM configuration prechecks.
- [ ] vm-erp2 has more than one data disk.
  > Multiple data disks are normal and supported.
