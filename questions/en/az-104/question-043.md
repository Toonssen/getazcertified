---
question: |-
  You plan to encrypt an Azure Storage account by using a customer-managed key stored in Azure Key Vault Premium.

  Which keys can you use?
documentation:
  - title: "Customer-managed keys"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview"
skill_area: "storage-accounts"
study_guide: "2026-04-17"
archetype: "fact-recall"
---

- [x] RSA or RSA-HSM keys of 2048, 3072, or 4096 bits
  > Azure Storage encryption with customer-managed keys supports RSA and RSA-HSM keys of these three sizes.
- [ ] RSA keys of 4096 bits only
  > 4096 works, but so do 2048 and 3072.
- [ ] EC keys on the P-256 or P-384 curve
  > Elliptic-curve keys aren't supported for Azure Storage encryption.
- [ ] AES-256 symmetric keys
  > Storage wraps its account encryption key with an asymmetric RSA key, not a symmetric one.
