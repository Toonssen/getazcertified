---
question: |-
  You have an Azure virtual network named vnet-app7 that has an address space of 10.40.0.0/16.

  You add a subnet named snet-batch7 that has an address range of 10.40.8.0/28.

  snet-batch7 already contains the frontend IP configuration of an internal load balancer named lbi-batch7. The frontend uses one static private IP address from snet-batch7.

  You plan to deploy virtual machines to snet-batch7. Each virtual machine has one network interface with one private IP address.

  What is the maximum number of virtual machines that you can deploy to snet-batch7?
documentation:
  - title: "Azure Virtual Network FAQ"
    url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq"
  - title: "Load Balancer portal settings"
    url: "https://learn.microsoft.com/en-us/azure/load-balancer/manage"
skill_area: "virtual-networks"
study_guide: "2026-04-17"
archetype: "calculate"
---

- [x] 10
  > A /28 range holds 16 addresses. Azure reserves five in every subnet (the first four and the last), which leaves
  > 11, and the load balancer frontend already uses one of them, so 10 are left for the virtual machines.
- [ ] 11
  > 11 is what a /28 subnet offers after the five reserved addresses, but the internal load balancer's frontend
  > takes one of those 11 from snet-batch7.
- [ ] 13
  > 13 comes from removing the network, default gateway and broadcast addresses, but forgetting both the two
  > Azure DNS addresses and the load balancer frontend.
- [ ] 14
  > Subtracting only the network and broadcast addresses gives 14. Azure reserves five addresses per subnet, and
  > the load balancer frontend uses one more.
