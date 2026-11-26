---
question: |-
  You replicate production virtual machines from West Europe to North Europe by using Azure Site Recovery.

  You need to validate the disaster recovery plan without affecting production workloads or ongoing replication.

  What should you do?
documentation:
  - title: "Run a Site Recovery test failover"
    url: "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-test-failover-to-azure"
skill_area: "backup-recovery"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Run a test failover to an isolated virtual network in North Europe.
  > A test failover creates VMs from the replicated data in a network you choose. Replication keeps running, and
  > an isolated network keeps the test VMs away from production.
- [ ] Run a planned failover to North Europe.
  > A planned failover shuts down the source VMs and moves production to the target region.
- [ ] Run an unplanned failover and then fail back.
  > An unplanned failover is for real outages and moves production.
- [ ] Disable replication and restore the VMs from Azure Backup.
  > This breaks the replication you want to test.
