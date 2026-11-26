---
question: |-
  You have an Azure container registry named crshop42 that has default settings.

  A tester needs to push a test image to crshop42 from a laptop by running docker login with a username and password. The solution must minimize administrative effort.

  What should you do?
documentation:
  - title: "Container Registry authentication"
    url: "https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication"
skill_area: "containers"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Enable the admin user on the Access keys page of crshop42, and give the tester the username and one of the two passwords.
  > The admin user is disabled by default. Once enabled under Access keys, the page shows its username and two
  > passwords, and the account can always push and pull. It's meant for a single user and testing.
- [ ] Use the admin user's credentials without changing any setting.
  > Each registry has an admin user, but it's disabled by default, so it must be enabled first.
- [ ] Enable the admin user, and assign it the AcrPush role.
  > The admin user doesn't use Azure RBAC roles. It always has pull and push access.
- [ ] Create a second admin user for the tester on the Access keys page.
  > There's a single admin account per registry. For several people, use individual identities instead.
