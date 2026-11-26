---
question: |-
  You have two pools of web servers in the West Europe region: one serves /images/* and the other serves /api/*. Both are reached through one public hostname.

  You need to send requests to the right pool based on the URL path and terminate TLS centrally. The solution must use a regional service.

  Which service should you use?
documentation:
  - "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview"
  - "https://learn.microsoft.com/en-us/azure/application-gateway/overview"
skill_area: "name-resolution-load-balancing"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Azure Application Gateway
  > Application Gateway is a regional layer 7 load balancer: it supports URL path-based routing and TLS
  > termination.
- [ ] Azure Load Balancer
  > Load Balancer works at layer 4 (TCP/UDP) and can't see URL paths.
- [ ] Azure Traffic Manager
  > Traffic Manager is DNS-based and global. It never sees the URL path of a request.
- [ ] Azure Front Door
  > Front Door does path routing too, but it's a global service, and the requirement is regional.
