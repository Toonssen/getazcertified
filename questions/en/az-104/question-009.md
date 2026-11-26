---
question: |-
  You have an Azure subscription that contains a storage account named stqueue07. The storage account uses Microsoft Entra authorization for data access.

  You assign a user named User2 the following roles at the scope of stqueue07:

  - Reader
  - Storage Queue Data Contributor

  Which two actions can User2 perform?
documentation: "https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles"
skill_area: "access-azure-resources"
study_guide: "2026-04-17"
archetype: "choose-n"
---

- [x] View the configuration of stqueue07 in the Azure portal
  > Reader grants read access to the control plane: the account's properties and settings.
- [x] Add messages to queues in stqueue07
  > Storage Queue Data Contributor grants data-plane read, write and delete on queues and messages.
- [ ] Regenerate the access keys of stqueue07
  > Regenerating keys is a control-plane write (and listKeys is an action). Reader allows neither.
- [ ] Read blobs in stqueue07
  > Data roles are per service. A queue data role gives no access to blob data, and Reader can't list the keys.
- [ ] Add a firewall rule to stqueue07
  > Changing network rules is a control-plane write, which Reader doesn't allow.
