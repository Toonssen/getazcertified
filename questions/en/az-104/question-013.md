---
question: |-
  You have a Microsoft Entra tenant that contains a user named Kim.

  On March 1, you delete Kim's account. No one permanently deletes it afterwards.

  Until approximately which date can you restore Kim's account from Deleted users?
documentation: "https://learn.microsoft.com/en-us/entra/fundamentals/users-restore"
skill_area: "entra-users-groups"
study_guide: "2026-04-17"
archetype: "calculate"
---

- [x] March 31
  > A deleted user stays in Deleted users (soft-deleted) for 30 days and can be restored with its properties and
  > group memberships during that time.
- [ ] March 3
  > 48 hours isn't the retention period for deleted users.
- [ ] March 8
  > Seven days is too short. The retention period is 30 days.
- [ ] May 30
  > 90 days is longer than the 30 days Microsoft Entra ID keeps deleted users.
