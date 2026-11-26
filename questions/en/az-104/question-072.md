---
question: |-
  You have a virtual machine scale set named vmss-front that uses Uniform orchestration.

  You need a scale set to which you can add standard Azure virtual machines that each have their own configuration.

  What should you do?
documentation: "https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes"
skill_area: "virtual-machines"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Create a new scale set that uses Flexible orchestration.
  > Flexible orchestration manages standard Azure VMs and lets you add VMs to the set. The orchestration mode is
  > fixed at creation, so vmss-front can't be switched.
- [ ] Change the orchestration mode of vmss-front to Flexible.
  > The mode can't be changed after the scale set is created.
- [ ] Change the upgrade policy of vmss-front to Manual.
  > The upgrade policy controls how model changes roll out, not whether VMs with their own configuration can join.
- [ ] Change the security type of vmss-front to Trusted launch.
  > Security type is unrelated to adding VMs with their own configuration.
