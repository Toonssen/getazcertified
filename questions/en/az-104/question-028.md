---
question: |-
  You plan to deploy a storage account named stlog01 by using the Bicep file shown in the following exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "After deployment, a block blob that was overwritten 12 days ago can be returned to its earlier state by using point-in-time restore."
documentation:
  - title: "Point-in-time restore for block blobs"
    url: "https://learn.microsoft.com/en-us/azure/storage/blobs/point-in-time-restore-overview"
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

- [ ] No
  > restorePolicy.days is 10, so point-in-time restore reaches back 10 days only. The 14-day soft-delete retention
  > must be longer than the restore window, but it doesn't extend it.
- [x] Yes
  > The restore window is set by restorePolicy (10 days), not by the soft-delete retention.
