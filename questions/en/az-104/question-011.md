---
question: |-
  You have a Microsoft Entra tenant that contains two security groups named HR-Staff and IT-Staff. Self-service password reset (SSPR) is set to None.

  You need to enable SSPR for the members of HR-Staff and IT-Staff only, by using the Microsoft Entra admin center.

  What should you do first?
documentation: "https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "best-choice"
---

- [x] Create a security group and add HR-Staff and IT-Staff to it as members.
  > In the admin center the Selected scope accepts a single group, and Microsoft Entra ID supports nested groups
  > in an SSPR deployment, so a parent group containing both groups covers both teams.
- [ ] Set SSPR to Selected and select HR-Staff and IT-Staff.
  > You can enable only one group for SSPR in the admin center, so two groups can't be selected.
- [ ] Set SSPR to All and exclude the other users.
  > There is no exclusion list for SSPR. All means every user.
- [ ] Configure the authentication methods policy for HR-Staff and IT-Staff.
  > The authentication methods policy controls which methods are available, not which users get SSPR.
