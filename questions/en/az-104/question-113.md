---
question: |-
  You have two general-purpose v2 storage accounts named stsrc08 and stdst08. Both accounts store block blobs only. Hierarchical namespace is disabled on both accounts.

  Blob versioning is already enabled on stdst08.

  You need to configure object replication from a container in stsrc08 to a container in stdst08.

  Each correct answer presents part of the solution.

  Which two features should you enable on stsrc08 before you create the replication policy?
documentation:
  - title: "Object replication overview"
    url: "https://learn.microsoft.com/en-us/azure/storage/blobs/object-replication-overview"
skill_area: "files-blob"
study_guide: "2026-04-17"
archetype: "choose-n"
---

- [x] Change feed
  > Object replication requires change feed on the source account, and stsrc08 is the source.
- [x] Blob versioning
  > Object replication requires blob versioning on both the source and the destination accounts. It's already
  > on for stdst08, so stsrc08 still needs it.
- [ ] Hierarchical namespace
  > An account with a hierarchical namespace can't take part in object replication. Turning it on for stsrc08
  > would block the policy instead of enabling it.
- [ ] Soft delete for blobs
  > Soft delete isn't in the list of features that object replication requires: change feed on the source and
  > blob versioning on both accounts.
