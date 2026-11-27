---
question: |-
  Your company plans to deploy a new Azure virtual machine named vm-pay4 that runs Ubuntu Server.

  The security team sets the following requirements for vm-pay4:

  - The operating system disk, the data disks, the temp disk, and the disk caches must be encrypted at rest.
  - The encryption method must not be one that Microsoft has scheduled for retirement.

  Which encryption method should you configure for vm-pay4?
documentation:
  - title: "Disk encryption options"
    url: "https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview"
skill_area: "virtual-machines"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Encryption at host
  > Encryption at host also encrypts the temp disk and the disk caches at rest, and it's the option Microsoft
  > recommends for new VMs.
- [ ] Azure Disk Encryption
  > Azure Disk Encryption encrypts the disks inside the VM, but it's scheduled for retirement on September 15,
  > 2028. New VMs should use encryption at host instead.
- [ ] Server-side encryption with a customer-managed key
  > Server-side encryption covers the OS and data disks, but it doesn't encrypt the temp disk or the disk caches.
- [ ] Confidential disk encryption
  > Confidential disk encryption protects only the OS disk, and it binds the keys to the TPM of a confidential VM.
