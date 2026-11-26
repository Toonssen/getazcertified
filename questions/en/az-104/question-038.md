---
question: |-
  You have an Azure Storage account named stexport02. You export stexport02 as an Azure Resource Manager template. The template contains the section shown in the following exhibit. stexport02 has no identity-based authentication configured for Azure Files.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "A user who has the Owner role for the subscription can mount the file shares in stexport02 by using their Microsoft Entra credentials."
documentation:
  - title: "Azure Files identity auth"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-active-directory-overview"
  - title: "Azure Files share permissions"
    url: "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "export-template"
---

```json
"properties": {
  "networkAcls": {
    "bypass": "AzureServices",
    "defaultAction": "Deny",
    "ipRules": [ { "value": "203.0.113.0/24", "action": "Allow" } ]
  },
  "accessTier": "Hot",
  "supportsHttpsTrafficOnly": true
},
"kind": "StorageV2"
```

- [ ] No
  > SMB access with user credentials needs an identity source for Azure Files plus a share-level data role.
  > Neither is configured, and Owner is a control-plane role that grants no file data access by itself.
- [x] Yes
  > Owner manages the account but has no SMB data permissions, and identity-based authentication isn't enabled.
