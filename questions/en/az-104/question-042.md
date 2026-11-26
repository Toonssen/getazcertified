---
question: |-
  You have an Azure Storage account named stcontent03 that contains a blob container named media. stcontent03 is configured as shown in the following exhibit, and users have the access shown in the second exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "User4 can read blobs in media."
documentation:
  - "https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/storage"
  - "https://learn.microsoft.com/en-us/azure/storage/common/shared-key-authorization-prevent"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "shared-key-disabled"
---

```text
stcontent03 > Configuration
  Allow storage account key access:                Disabled
  Default to Microsoft Entra authorization in the Azure portal: Enabled
  Secure transfer required:                        Enabled
```

```text
User    Access to container media in stcontent03
User1   User delegation SAS (read, list)
User2   Service SAS signed with key1 (read, write, delete, list)
User3   Storage Account Contributor role on stcontent03
User4   Storage Blob Data Reader role on stcontent03
```

- [x] Yes
  > Storage Blob Data Reader grants read access to blob data through Microsoft Entra ID, which isn't affected by
  > disabling Shared Key.
- [ ] No
  > Disabling key access only blocks Shared Key and key-signed SAS. Microsoft Entra data roles still work.
