---
question: |-
  You have a subnet named snet-dmz that has a network security group with the following inbound rules:

  - Priority 100: allow TCP 22 from Any
  - Priority 200: deny TCP 1-1024 from Any
  - Priority 300: allow TCP 80, 443 from Internet
  - Priority 400: allow TCP 80, 443 from VirtualNetwork

  You need to allow HTTP and HTTPS traffic from the internet to snet-dmz without allowing any other new traffic.

  What should you change?
documentation: "https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview"
skill_area: "secure-vnet-access"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Change the priority of the 300 rule to 150.
  > Rules are processed in priority order and the first match wins. Today the 200 deny matches TCP 80 and 443
  > first. At 150, the internet allow for 80/443 is matched before the deny.
- [ ] Change the priority of the 400 rule to 150.
  > That rule only matches a VirtualNetwork source, so internet traffic would still hit the deny.
- [ ] Change the priority of the 200 rule to 450.
  > Internet HTTP/HTTPS would work, but so would the 400 rule: HTTP and HTTPS from the virtual network, which the
  > deny blocks today, is new traffic the requirements rule out.
- [ ] Delete the 100 rule.
  > The SSH rule has nothing to do with HTTP and HTTPS.
