---
question: |-
  You have a general-purpose v2 storage account named stsensor3 that contains a container named telemetry.

  You need a lifecycle management rule that moves the blobs in telemetry, 30 days after they were last modified, to the lowest-cost tier that still allows the blobs to be read immediately.

  You are writing the rule shown in the following exhibit.

  Which value should you use for <action>?
documentation:
  - "https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-policy-structure"
  - "https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview"
skill_area: "files-blob"
study_guide: "2026-04-17"
archetype: "complete-code"
---

```json
{
  "name": "telemetry-30d",
  "enabled": true,
  "type": "Lifecycle",
  "definition": {
    "filters": { "blobTypes": [ "blockBlob" ], "prefixMatch": [ "telemetry/" ] },
    "actions": {
      "baseBlob": {
        "<action>": { "daysAfterModificationGreaterThan": 30 }
      }
    }
  }
}
```

- [x] tierToCold
  > Cold is the cheapest online tier, so reads are still immediate.
- [ ] tierToArchive
  > Archive is cheaper but offline: a blob must be rehydrated (hours) before it can be read.
- [ ] tierToCool
  > Cool is online too but costs more to store than Cold, so it isn't the lowest-cost option.
- [ ] enableAutoTierToHotFromCool
  > This moves blobs back to Hot when they're accessed. It doesn't move them down a tier.
