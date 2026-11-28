---
question: |-
  A build pipeline pushes an image named orders:2.4 to an Azure container registry named acrops01.

  You deploy a new Azure virtual machine named vm-ops01 that runs Ubuntu Server. No other software is installed on vm-ops01.

  You need to pull orders:2.4 from acrops01 and start it as a container on vm-ops01.

  Which software must you install on vm-ops01?
documentation:
  - title: "Push and pull images with ACR"
    url: "https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli"
skill_area: "containers"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] A container runtime such as Docker Engine
  > An image needs a container runtime to run. With Docker installed, you sign in to the registry (`docker login`
  > works), pull the image and run it.
- [ ] The Azure CLI
  > `az acr login` is the recommended way to sign in, but it isn't required, and the Azure CLI can't start a
  > container on the VM.
- [ ] The Azure Container Apps CLI extension
  > That extension manages Container Apps in Azure. It doesn't run containers on the VM.
- [ ] kubectl
  > kubectl sends commands to a Kubernetes cluster. On its own, it can't pull or run an image on the VM.
