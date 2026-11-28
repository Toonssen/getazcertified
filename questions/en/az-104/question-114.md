---
question: |-
  You have an ARM template named main.json that deploys the resources for an app named app9.

  You need to convert main.json into a Bicep file so that your team can maintain the deployment in Bicep from now on.

  You plan to run the Azure CLI command shown in the following exhibit.

  Which value should you use for `<blank>`?
documentation:
  - title: "Decompile JSON to Bicep"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/decompile"
  - title: "Bicep CLI commands"
    url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/bicep-cli"
skill_area: "arm-bicep"
study_guide: "2026-04-17"
archetype: "complete-code"
---

```text
az bicep <blank> --file main.json
```

- [x] decompile
  > `decompile` turns the JSON template into Bicep and writes main.bicep next to main.json. The conversion isn't
  > guaranteed to be exact, so check the new file for warnings and errors.
- [ ] build
  > The `build` command goes the other way: it converts a Bicep file to a JSON ARM template.
- [ ] convert
  > There's no `convert` command in the Bicep CLI command list. Converting JSON to Bicep is done by `decompile`.
- [ ] decompile-params
  > `decompile-params` converts a JSON parameters file, not a template. main.json is a template.
