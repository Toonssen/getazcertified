---
question: |-
  You have an Azure subscription that contains a resource group named RG-Web.

  From Azure Cloud Shell, you need to deploy an ARM template named webapp.json to RG-Web by using the command shown in the following exhibit.

  Which value should you use for <cmdlet>?
documentation:
  - title: "Deploy templates (PowerShell)"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-powershell"
  - title: "Template specs"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/template-specs"
skill_area: "arm-bicep"
study_guide: "2026-04-17"
archetype: "complete-code"
---

```powershell
<cmdlet> -ResourceGroupName RG-Web -TemplateFile ./webapp.json
```

- [x] New-AzResourceGroupDeployment
  > A template that targets an existing resource group is deployed at resource group scope, and this cmdlet takes
  > -ResourceGroupName and -TemplateFile.
- [ ] New-AzDeployment
  > New-AzDeployment deploys at subscription scope. It takes -Location, not -ResourceGroupName.
- [ ] New-AzTemplateSpec
  > This publishes a template as a template spec. It doesn't deploy it.
- [ ] New-AzResource
  > New-AzResource creates a single resource from properties, not from a template file.
