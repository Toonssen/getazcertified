---
question: |-
  You have an Azure container registry that stores an image named orders:2.4, and an Azure virtual machine named vm-ops01 that runs Ubuntu Server.

  You need to run orders:2.4 on vm-ops01.

  What should you install on vm-ops01 first?
documentation:
  - title: "Push and pull images with ACR"
    url: "https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli"
skill_area: "containers"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A container runtime such as Docker Engine
  > An image needs a container runtime to run. With Docker installed, you sign in to the registry, pull the image
  > and run it.
- [ ] The Azure Container Apps CLI extension
  > That extension manages Container Apps in Azure. It doesn't run containers on the VM.
- [ ] Azure Storage Explorer
  > Storage Explorer browses storage accounts. Registries and containers are unrelated to it.
- [ ] The Hyper-V role
  > Hyper-V is a Windows feature and doesn't run Linux containers on its own.
