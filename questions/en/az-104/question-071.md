---
question: |-
  You have an Azure virtual machine named vm-rpt3 that runs Windows Server. vm-rpt3 has the items shown in the following table.

  You resize vm-rpt3 to a larger size.

  Which items are still present after the resize?
documentation:
  - "https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/resize-vm"
  - "https://learn.microsoft.com/en-us/azure/virtual-machines/managed-disks-overview"
skill_area: "virtual-machines"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Item              Location
report.db         C:\ (operating system disk)
archive.zip       F:\ (managed data disk)
cache.tmp         D:\ (temporary disk)
ReportService     Running process
Admin session     Remote Desktop session in progress
```

- [x] report.db and archive.zip only
  > Resizing a running VM restarts it, and it may move to other hardware. Managed OS and data disks persist. The
  > temporary disk, running processes and open sessions don't survive.
- [ ] report.db only
  > Data disks are persistent managed disks, so archive.zip survives as well.
- [ ] report.db, archive.zip, and cache.tmp only
  > D: is the temporary disk. Its data might be lost during maintenance, a redeploy or a stop, and a resize can
  > move the VM to other hardware.
- [ ] All the items
  > The restart ends ReportService's running state and the Remote Desktop session.
