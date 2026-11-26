---
question: |-
  You plan to deploy a storage account named stlog01 by using the Bicep file shown in the following exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "The data in stlog01 is stored as three copies within the North Europe region."
documentation: "https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy"
skill_area: "storage-accounts"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "bicep-stlog01"
---

```bicep
resource stlog01 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'stlog01'
  location: 'northeurope'
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

resource blobs 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: stlog01
  name: 'default'
  properties: {
    isVersioningEnabled: true
    changeFeed: { enabled: true }
    deleteRetentionPolicy: { enabled: true, days: 14 }
    restorePolicy: { enabled: true, days: 10 }
  }
}
```

- [x] Yes
  > Standard_LRS keeps three copies of the data within the primary region (North Europe), with no copy in a
  > secondary region.
- [ ] No
  > LRS still means three copies; it's the geo-redundant options that add a secondary region.
