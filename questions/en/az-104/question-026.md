---
question: |-
  You have an Azure Storage account named stmedia04 that serves video files to customers over the internet. The account is configured as shown in the following exhibit.

  Select the answer that completes the following statement.

  "To minimize the network costs of the traffic between stmedia04 and its internet clients, modify the ____ setting."
documentation: "https://learn.microsoft.com/en-us/azure/storage/common/network-routing-preference"
skill_area: "storage-accounts"
study_guide: "2026-04-17"
archetype: "complete-statement"
---

```text
Basics       Region: West Europe   Performance: Standard   Redundancy: ZRS
Networking   Public network access: Enabled from all networks
             Routing preference:    Microsoft network routing
Data         Default blob access tier: Hot
```

- [x] Routing preference
  > Internet routing hands traffic to the internet at the point closest to the Azure region, which is cheaper than
  > carrying it over the Microsoft global network (the default).
- [ ] Redundancy
  > Redundancy changes how data is replicated and what storage costs. It doesn't change the cost of internet
  > egress.
- [ ] Default blob access tier
  > The access tier changes storage and access charges, not network routing costs.
- [ ] Public network access
  > This controls which networks may connect, not how the traffic is routed or billed.
