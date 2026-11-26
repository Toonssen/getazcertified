---
question: |-
  You have an Azure virtual machine named vm-fin2 that runs Windows Server and an Azure key vault named kv-fin.

  You need to encrypt vm-fin2. The solution must meet the following requirements:

  - Use a key stored in kv-fin.
  - Encrypt the operating system disk and the data disks.
  - Keep the disk contents encrypted inside the guest operating system, so they remain unreadable if a VHD is copied out of Azure.

  Which encryption method should you use?
documentation:
  - title: "Disk encryption options"
    url: "https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview"
  - title: "Server-side encryption of managed disks"
    url: "https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption"
skill_area: "virtual-machines"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Azure Disk Encryption
  > Azure Disk Encryption runs BitLocker inside the VM, with keys in Key Vault, so the volumes themselves are
  > encrypted. Note: it retires on September 15, 2028, and encryption at host is the recommended choice for new
  > VMs that don't need guest-level encryption.
- [ ] Encryption at host
  > Encryption at host encrypts at the Azure host (disks, caches, temp disk). The guest sees plain data, so it
  > doesn't meet the guest-level requirement.
- [ ] Server-side encryption with a customer-managed key
  > Server-side encryption protects data at rest in the storage platform and decrypts it as it's read, so it isn't
  > guest-level encryption.
- [ ] Confidential disk encryption
  > This is only for confidential VM sizes and binds the keys to the VM's TPM. It isn't a general option for an
  > existing standard VM.
