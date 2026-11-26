---
question: |-
  A developer is building an internal app that downloads monthly reports from a storage account named stfin05. Anonymous access is disabled on stfin05, and the account's default settings are otherwise unchanged.

  The developer asks which ways the app can authorize its blob read requests.

  What should you tell the developer?
documentation: "https://learn.microsoft.com/en-us/azure/storage/common/authorize-data-access"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "fact-recall"
---

- [x] Microsoft Entra ID, Shared Key, or a shared access signature (SAS) only
  > Blob data requests can be authorized with Microsoft Entra ID, Shared Key (account key) or a SAS. Anonymous
  > access is the fourth option, and it's disabled here.
- [ ] Microsoft Entra ID only
  > Shared Key and SAS also work unless Shared Key access is disallowed.
- [ ] Microsoft Entra ID, a SAS, or a client certificate only
  > Azure Storage has no client-certificate authorization. A certificate can only be used to get a Microsoft Entra
  > token.
- [ ] Shared Key or a SAS only
  > Microsoft Entra ID is supported for blob data, and it's the recommended option.
