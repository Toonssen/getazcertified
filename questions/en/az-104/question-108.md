---
question: |-
  You back up an Azure virtual machine named vm-file9 with Azure Backup. A user deletes a single folder on vm-file9.

  You need to recover only that folder from yesterday's recovery point, without restoring a disk or a VM.

  What should you do?
documentation:
  - title: "Recover files from a VM backup"
    url: "https://learn.microsoft.com/en-us/azure/backup/backup-azure-restore-files-from-vm"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Use File Recovery: download the script for the recovery point and run it to mount the recovery point as local drives.
  > File Recovery mounts the recovery point's disks on a machine through a script, so you can copy back just the
  > folder you need.
- [ ] Restore the virtual machine to a new VM.
  > This restores the whole VM, more than the requirement asks for.
- [ ] Restore the disks and attach them to vm-file9.
  > Restoring disks is a disk-level restore, which the requirements rule out.
- [ ] Use the instant restore snapshot in the restore point collection directly.
  > Snapshots back disk and VM restores. You don't browse them file by file.
