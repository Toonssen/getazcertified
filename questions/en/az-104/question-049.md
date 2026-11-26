---
question: |-
  You have an Azure subscription. You run the following commands:

  - New-AzResourceGroup -Name RG-Diag -Location northeurope
  - New-AzResourceGroupDeployment -ResourceGroupName RG-Diag -TemplateFile ./diag.json

  diag.json contains the sections shown in the following exhibit.

  For the following statement, select Yes if the statement is true. Otherwise, select No.

  "The first storage account that the deployment creates is named stdiag01."
documentation:
  - title: "Deploy resource copies"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/copy-resources"
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

- [x] Yes
  > copyIndex() is zero-based, but copyIndex(1) adds an offset of 1, so the three accounts are stdiag01, stdiag02
  > and stdiag03.
- [ ] No
  > Without the offset the first name would be stdiag00. The argument 1 shifts the index.
