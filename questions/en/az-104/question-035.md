---
question: |-
  You have an Azure Storage account named stweb01 that contains Azure file shares. stweb01 and the virtual machines are configured as shown in the following exhibits.

  Select the answer that completes the following statement.

  "Over the public endpoint of stweb01, vm-db1 ____ connect to the file shares."
documentation: "https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "complete-statement"
series: "stweb01-firewall"
---

```text
stweb01 > Networking
  Public network access:  Enabled from selected virtual networks and IP addresses
  Virtual networks:       VNet-App / snet-web (10.40.1.0/24)   Endpoint status: Enabled
  Firewall address range: (none)
  Exceptions:             [ ] Allow Azure services on the trusted services list to access this storage account
```

```text
VM        Virtual network   Subnet     IP address
vm-web1   VNet-App          snet-web   10.40.1.4
vm-db1    VNet-App          snet-db    10.40.2.4
```

- [x] can never
  > Only snet-web is allowed. Listing a subnet doesn't open the rest of the virtual network, and snet-db has no
  > rule (or service endpoint) on stweb01.
- [ ] can always
  > VNet-App isn't allowed as a whole. Each subnet needs its own virtual network rule.
- [ ] can only by using a shared access signature (SAS)
  > Network rules apply whatever the request's authorization, so a SAS doesn't get a request through from a
  > network that isn't allowed.
