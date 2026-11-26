---
question: |-
  You have an Azure subscription. You run the following commands:

  - New-AzResourceGroup -Name RG-Diag -Location northeurope
  - New-AzResourceGroupDeployment -ResourceGroupName RG-Diag -TemplateFile ./diag.json

  diag.json contains the sections shown in the following exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "The storage accounts are created in the West Europe region."
documentation:
  - title: "Deploy multiple resource instances"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/copy-resources"
  - title: "Template functions: resources"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-resource"
skill_area: "arm-bicep"
study_guide: "2026-04-17"
archetype: "exhibit-statement"
series: "diag-copy-loop"
---

```json
"parameters": {
  "location": { "type": "string", "defaultValue": "westeurope" }
},
"resources": [
  {
    "type": "Microsoft.Storage/storageAccounts",
    "apiVersion": "2023-05-01",
    "name": "[concat('stdiag0', copyIndex(1))]",
    "location": "[resourceGroup().location]",
    "sku": { "name": "Standard_LRS" },
    "kind": "StorageV2",
    "copy": { "name": "diagCopy", "count": 3 }
  }
]
```

- [ ] No
  > The resources use [resourceGroup().location], which is North Europe. The location parameter defaults to
  > westeurope, but nothing in the resource uses it.
- [x] Yes
  > A parameter only matters where the template references it, and this resource takes the resource group's
  > location.
