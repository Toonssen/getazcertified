---
question: |-
  You deploy a virtual machine scale set named vmss-batch that has the autoscale configuration shown in the following exhibit. The cool down for both rules is 5 minutes.

  Select the answer that completes the following statement.

  "If CPU usage is 90 percent for the first seven minutes after deployment, vmss-batch will be running ____."
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

- [x] 6 virtual machines
  > After 5 minutes above 80 percent, the rule adds 3 instances (3 + 3 = 6). The cool down then runs until minute
  > 10, so nothing else happens by minute 7.
- [ ] 3 virtual machines
  > The 5-minute duration has passed, so the scale-out has already happened.
- [ ] 8 virtual machines
  > 8 is the maximum, but reaching it needs a second scale action, which the cool down blocks until minute 10.
- [ ] 9 virtual machines
  > Two scale-outs would give 9, but that's above the maximum, and only one action fits in seven minutes.
