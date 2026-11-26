---
question: |-
  You have an Azure subscription that contains a storage account named stfiles01. stfiles01 hosts an SMB Azure file share named projects.

  Users in your Microsoft Entra tenant are hybrid identities synchronized from on-premises Active Directory Domain Services (AD DS). No identity-based authentication is configured for stfiles01.

  You need users to mount projects by using their own identities, with access controlled by the Storage File Data SMB Share Contributor role.

  What should you do first?
documentation:
  - title: "Azure Files share permissions"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions"
  - title: "Azure Files identity auth"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-active-directory-overview"
  - title: "Authorize data access in Azure Storage"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/authorize-data-access"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Enable an identity source for Azure Files on stfiles01, such as Microsoft Entra Kerberos.
  > Share-level roles only take effect after an identity source (AD DS, Microsoft Entra Domain Services or
  > Microsoft Entra Kerberos) is enabled for the account. Assigning the role comes after that.
- [ ] Enable Default to Microsoft Entra authorization in the Azure portal.
  > This changes how the portal authorizes blob and queue browsing. SMB mounts don't use it.
- [ ] Generate a shared access signature (SAS) for projects.
  > SAS isn't an authorization option for Azure Files over SMB (only identity-based access or the account key),
  > and a SAS isn't the user's identity.
- [ ] Enable large file shares on stfiles01.
  > Large file shares raise capacity limits. They don't affect authentication.
