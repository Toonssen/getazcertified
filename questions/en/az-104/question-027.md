---
question: |-
  You are creating a general-purpose v2 storage account named starchive9 with Standard performance, Microsoft-managed keys, and infrastructure encryption disabled.

  Select the answer that completes the following statement.

  "After starchive9 is created, you can change the ____ setting."
documentation:
  - "https://learn.microsoft.com/en-us/azure/storage/common/infrastructure-encryption-enable"
  - "https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview"
skill_area: "storage-accounts"
study_guide: "2026-04-17"
archetype: "complete-statement"
---

- [x] encryption key type
  > You can switch between Microsoft-managed keys and customer-managed keys at any time after the account exists.
- [ ] infrastructure encryption
  > Infrastructure encryption can only be chosen when the account is created. You can't enable or disable it
  > later.
- [ ] performance
  > Standard and Premium are different account types. Changing means creating a new account and migrating the
  > data.
- [ ] storage account name
  > The account name is part of every endpoint and can't be renamed.
