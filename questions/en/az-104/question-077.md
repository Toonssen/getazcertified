---
question: |-
  You have an Azure Bastion host named bas-hub that uses the Basic SKU, and 40 Linux virtual machines in peered virtual networks.

  You need to ensure that bas-hub can handle 150 concurrent SSH sessions. The solution must minimize administrative effort.

  What should you do first?
documentation:
  - "https://learn.microsoft.com/en-us/azure/bastion/bastion-sku-comparison"
  - "https://learn.microsoft.com/en-us/azure/bastion/configuration-settings"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Upgrade bas-hub to the Standard SKU.
  > Basic has a fixed two instances. Host scaling (2 to 50 instances) is a Standard and Premium feature, so the
  > SKU upgrade comes first, then you raise the instance count.
- [ ] Increase the instance count of bas-hub.
  > The Basic SKU has no host scaling. The instance count is fixed at 2.
- [ ] Deploy a second Bastion host in each peered virtual network.
  > This adds hosts to manage and isn't needed: one Standard host scales out and reaches peered networks.
- [ ] Resize AzureBastionSubnet to /24.
  > A larger subnet makes room for instances but doesn't add any on a Basic host. A /26 already fits Standard
  > scaling.
