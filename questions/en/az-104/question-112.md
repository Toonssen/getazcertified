---
question: |-
  You have an Azure subscription that contains a storage acount named st1.

  You need to ensure that blobs in st1 can be restored to any point in the last 7 days.

  What should you enable first?
documentation:
  - title: "Point-in-time restore for block blobs"
    url: "https://learn.microsoft.com/en-us/azure/storage/blobs/point-in-time-restore-overview"
skill_area: "storage-acess"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Blob soft delete, versioning and change feed
  > Point-in-time restore needs soft delete, versioning and the change feed to be enabled on the account.
- [ ] Geo-redundant storage
  > Geo-redundancy copies data to another region; it doesn't let you restore earlier states.
- [ ] A resource lock on st1
