---
question: |-
  You have an Azure Storage account named stweb01 that contains Azure file shares. stweb01 and the virtual machines are configured as shown in the following exhibits.

  You plan to protect the file shares in stweb01 by using Azure Backup.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "Azure Backup can back up the file shares in stweb01 with the current network configuration."
documentation: "https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security"
skill_area: "storage-access"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
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

- [ ] No
  > With access limited to selected networks, Azure Backup needs the exception 'Allow Azure services on the
  > trusted services list to access this storage account'. It's cleared in the exhibit.
- [x] Yes
  > Azure Backup doesn't run from snet-web, so the virtual network rule doesn't cover it. The trusted services
  > exception does, but it's off.
