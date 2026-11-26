---
question: |-
  You have an Azure subscription that contains the public IP resources shown in the following table. All are in West Europe and aren't associated with any resource.

  You plan to deploy an Azure Firewall instance named fw-hub in a virtual network in West Europe.

  Which resources can you associate with fw-hub?
documentation:
  - "https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/configure-public-ip-firewall"
  - "https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/public-ip-addresses"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "exhibit-select"
---

```text
Name        Type                       Details
pip-01      Public IP address          Standard, IPv4, static
pip-02      Public IP address          Standard, IPv4, static, allocated from ippre-01
pip-03      Public IP address          Standard, IPv4, static
ippre-01    Public IP address prefix   /30, Standard
```

- [x] pip-01, pip-02, and pip-03 only
  > Azure Firewall uses Standard SKU public IP addresses, up to 250 for a firewall in a virtual network. It can't
  > attach a public IP prefix itself, but it can use individual addresses allocated from one, such as pip-02.
- [ ] pip-01 and pip-03 only
  > An address allocated from a prefix is still a Standard public IP address, and the firewall can use it.
- [ ] pip-01, pip-02, pip-03, and ippre-01
  > Azure Firewall doesn't support attaching a public IP prefix. Use addresses allocated from the prefix instead.
- [ ] pip-01 only
  > A firewall isn't limited to one public IP address. It supports up to 250 in a virtual network.
