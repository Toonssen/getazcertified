---
question: |-
  You have a storage account named stbilling01 that has a default access tier of Hot. stbilling01 has the lifecycle management rule and the blobs shown in the following exhibits. The blobs were never modified after May 1.

  After inv-02.pdf is rehydrated, no one modifies it.

  When will inv-02.pdf most likely be moved back to the Archive tier?
documentation:
  - "https://learn.microsoft.com/en-us/azure/storage/blobs/archive-rehydrate-overview"
  - "https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview"
skill_area: "files-blob"
study_guide: "2026-04-17"
archetype: "calculate"
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

- [x] At the next lifecycle policy run, within about a day of the rehydration
  > Rehydrating changes the tier but not Last modified, which is still May 1. The blob already meets the 5-day
  > condition, so the next daily run archives it again. Copying the blob, or a daysAfterLastTierChangeGreaterThan
  > condition, avoids this.
- [ ] On May 17, five days after the rehydration
  > The 5 days count from the last modification (May 1), not from the tier change.
- [ ] On May 21
  > May 21 is when Rule1 deletes the blob (20 days after May 1), not when it archives it.
- [ ] Never, because a rehydrated blob is excluded from lifecycle rules
  > Rehydrated blobs aren't excluded. They're evaluated like any other blob.
