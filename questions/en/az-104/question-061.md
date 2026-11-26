---
question: |-
  You have the virtual networks shown in the following table. All are in the same region and subscription.

  You plan to create an Azure Container Apps environment that uses the default workload profiles environment type. The environment must use a new, dedicated subnet in an existing virtual network, and the subnet must be the smallest size that is supported.

  In which virtual networks can you create the subnet?
documentation:
  - title: "Container Apps networking"
    url: "https://learn.microsoft.com/en-us/azure/container-apps/networking"
skill_area: "containers"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Virtual network   Address space    Existing subnets
VNet-A            10.1.0.0/26      10.1.0.0/27
VNet-B            10.2.0.0/28      (none)
VNet-C            10.3.0.0/24      10.3.0.0/25
```

- [x] VNet-A and VNet-C only
  > A workload profiles environment needs at least a /27. VNet-A has exactly one free /27 (10.1.0.32/27), and
  > VNet-C has room for one in 10.3.0.128/25. VNet-B's /28 is too small.
- [ ] VNet-C only
  > The /23 minimum applies to the legacy Consumption-only environment. Workload profiles need only a /27, which
  > VNet-A can hold.
- [ ] VNet-A, VNet-B, and VNet-C
  > A /28 is smaller than the /27 minimum.
- [ ] VNet-B only
  > VNet-B is empty, but its address space is too small for a /27.
