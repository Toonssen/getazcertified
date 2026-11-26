---
question: |-
  You deploy a virtual machine scale set named vmss-batch that has the autoscale configuration shown in the following exhibit. The cool down for both rules is 5 minutes.

  Select the answer that completes the following statement.

  "If CPU usage is 20 percent for the first seven minutes after deployment and then 50 percent for the next seven minutes, vmss-batch will be running ____."
documentation: "https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-autoscale-overview"
skill_area: "virtual-machines"
study_guide: "2026-04-17"
archetype: "complete-statement"
series: "vmss-batch-autoscale"
---

```text
Scale set vmss-batch
  Initial instance count:  3
  Instance limits:         Minimum 2   Maximum 8
  Scale out:               CPU threshold 80%, duration 5 minutes, increase instance count by 3
  Scale in:                CPU threshold 30%, duration 5 minutes, decrease instance count by 2
```

- [x] 2 virtual machines
  > The scale-in rule fires after 5 minutes and would remove 2 (3 - 2 = 1), but the count can't go below the
  > minimum of 2. At 50 percent, neither rule applies.
- [ ] 1 virtual machine
  > Autoscale stops at the instance minimum, which is 2.
- [ ] 3 virtual machines
  > The scale-in did happen, because CPU stayed under 30 percent for longer than the 5-minute duration.
- [ ] 6 virtual machines
  > 50 percent is below the 80 percent scale-out threshold.
