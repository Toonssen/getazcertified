---
question: |-
  You have a general-purpose v2 storage account named stcorp22 that hosts blobs and SMB Azure file shares. Some clients still use HTTP and SMB 2.1.

  You need to ensure that requests over HTTP are rejected and that SMB mounts without encryption are rejected.

  Which two settings should you enable on stcorp22?
documentation:
  - title: "SMB file shares in Azure Files"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/files-smb-protocol"
  - title: "Require secure transfer"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/storage-require-secure-transfer"
  - title: "Enforce a minimum TLS version"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/transport-layer-security-configure-minimum-version"
skill_area: "storage-accounts"
study_guide: "2026-04-17"
archetype: "choose-n"
---

- [x] Secure transfer required
  > This rejects REST requests made over HTTP, so only HTTPS gets through.
- [x] Require Encryption in Transit for SMB
  > This allows only SMB 3.x mounts that use channel encryption, so SMB 2.1 clients are rejected. Secure transfer
  > required now covers REST/HTTPS only.
- [ ] Minimum TLS version 1.2
  > This rejects old TLS versions on HTTPS, but plain HTTP doesn't use TLS at all.
- [ ] Allow storage account key access: Disabled
  > This changes how requests are authorized, not whether they're encrypted.
- [ ] Cross-Origin Resource Sharing (CORS)
  > CORS controls which web origins can call the service from a browser.
