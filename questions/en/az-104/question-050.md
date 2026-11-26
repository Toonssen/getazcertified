---
question: |-
  Your team publishes a template spec named ts-vm01. Its template defines the virtual machine's image, disk type, and network settings, and exposes only two parameters: vmName and adminUsername.

  You deploy ts-vm01 from the Azure portal.

  Which value can you choose during the deployment besides the parameters?
documentation:
  - title: "Template specs"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/template-specs"
skill_area: "arm-bicep"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] The target resource group
  > Every deployment needs a scope, so you always choose the subscription and resource group. Everything else is
  > fixed unless it's exposed as a parameter.
- [ ] The operating system image
  > The image is hard-coded in the template, so you can't change it at deployment time.
- [ ] The disk type
  > The disk type isn't a parameter, so it comes from the template.
- [ ] The virtual network address space
  > Network settings are fixed in the template.
