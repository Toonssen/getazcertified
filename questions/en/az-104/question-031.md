---
question: |-
  You have a storage account named stbilling01 that has a default access tier of Hot. stbilling01 has the lifecycle management rule and the blobs shown in the following exhibits. The blobs were never modified after May 1.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "On May 10, inv-01.pdf can be read without delay."
documentation:
  - title: "Lifecycle management overview"
    url: "https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview"
  - title: "Rehydrate archived blobs"
    url: "https://learn.microsoft.com/en-us/azure/storage/blobs/archive-rehydrate-overview"
skill_area: "files-blob"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "lifecycle-invoices"
---

```text
Lifecycle rule   Filter (prefix)     Actions (days after last modification)
Rule1            invoices/           Move to archive: 5     Delete: 20
```

```text
Blob                 Container   Last modified   Notes
invoices/inv-01.pdf  invoices    May 1           -
invoices/inv-02.pdf  invoices    May 1           Rehydrated to Hot (standard priority) on May 12
```

- [ ] No
  > Five days after its last modification (May 6), Rule1 moved inv-01.pdf to Archive. An archived blob is offline
  > and must be rehydrated before it can be read.
- [x] Yes
  > Rule1 applies because the blob matches the invoices/ prefix, so it is already archived on May 10.
