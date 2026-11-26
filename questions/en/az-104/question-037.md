---
question: |-
  You have an Azure Storage account named stexport02. You export stexport02 as an Azure Resource Manager template. The template contains the section shown in the following exhibit. stexport02 has no identity-based authentication configured for Azure Files.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "A client that has the public IP address 198.51.100.7 can read blobs in stexport02 by using the account access key."
documentation:
  - title: "Storage firewall and network access"
    url: "https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "export-template"
---

```json
"properties": {
  "networkAcls": {
    "bypass": "AzureServices",
    "defaultAction": "Deny",
    "ipRules": [ { "value": "203.0.113.0/24", "action": "Allow" } ]
  },
  "accessTier": "Hot",
  "supportsHttpsTrafficOnly": true
},
"kind": "StorageV2"
```

- [ ] No
  > defaultAction is Deny, and 198.51.100.7 isn't in the 203.0.113.0/24 IP rule. A valid key doesn't change that:
  > the request comes from a network that isn't allowed, so it's rejected.
- [x] Yes
  > A valid key doesn't bypass the firewall. Only allowed networks (and trusted services, through bypass) get in.
