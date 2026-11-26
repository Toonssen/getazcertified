---
question: |-
  You have the storage accounts shown in the following table.

  You need to automatically tier and expire data by using lifecycle management.

  On which storage accounts can you configure lifecycle management?
documentation: "https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview"
skill_area: "files-blob"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name     Kind               Performance
st-gp2   StorageV2          Standard
st-blk   BlockBlobStorage   Premium
st-fil   FileStorage        Premium
st-gp1   Storage (v1)       Standard
```

- [x] st-gp2 and st-blk only
  > Lifecycle management works on general-purpose v2, premium block blob and legacy Blob Storage accounts.
  > FileStorage holds only file shares, and general-purpose v1 isn't supported (upgrade it to v2 first).
- [ ] st-gp2 only
  > Premium block blob accounts (BlockBlobStorage) support lifecycle management too, but only the actions premium
  > supports, such as delete.
- [ ] st-gp2, st-blk, and st-gp1 only
  > General-purpose v1 accounts don't support lifecycle management.
- [ ] st-gp2, st-blk, st-fil, and st-gp1
  > FileStorage accounts contain no blobs, and v1 isn't supported.
