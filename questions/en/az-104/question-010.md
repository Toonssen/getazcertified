---
question: |-
  You have a Microsoft Entra tenant. The external collaboration settings have Guest invite settings set to "Only users assigned to specific admin roles can invite guest users".

  A user named Dev1 has no admin roles. Dev1 tries to invite a partner, ana@partner.example, and the invitation fails.

  You need to ensure that Dev1 can invite guest users. The solution must not change any tenant-wide setting and must follow the principle of least privilege.

  What should you do?
documentation: "https://learn.microsoft.com/en-us/entra/external-id/external-collaboration-settings-configure"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Assign the Guest Inviter role to Dev1.
  > With invitations restricted to specific admin roles, Guest Inviter is the narrowest role that is allowed to
  > invite guests, and no tenant setting changes.
- [ ] Assign the User Administrator role to Dev1.
  > User Administrator can invite guests too, but it also manages every user and group, which is far more than
  > needed.
- [ ] Add partner.example to the allowed domains under Collaboration restrictions.
  > Collaboration restrictions decide which domains can be invited, not who can send invitations. It's also a
  > tenant-wide change.
- [ ] Change Guest invite settings so that member users can invite.
  > This would work, but it changes a tenant-wide setting for every member, which the requirements rule out.
