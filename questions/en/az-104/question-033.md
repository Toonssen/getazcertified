---
question: |-
  You have a storage account named stbilling01 that has a default access tier of Hot. stbilling01 has the lifecycle management rule and the blobs shown in the following exhibits. The blobs were never modified after May 1.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "On May 23, inv-01.pdf still exists in stbilling01."
documentation:
  - title: "Lifecycle management overview"
    url: "https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview"
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
  > Rule1 deletes blobs 20 days after their last modification. inv-01.pdf was last modified on May 1, so it's
  > deleted around May 21, whatever tier it's in.
- [x] Yes
  > Being in Archive doesn't protect a blob from a delete action. Rule1 removes it after 20 days.
