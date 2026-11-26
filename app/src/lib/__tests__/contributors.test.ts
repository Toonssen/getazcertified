import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { getContributors } from "@/lib/contributors";
// @ts-ignore plain ESM build script without types
import { normalize } from "../../../scripts/fetch-contributors.mjs";

describe("contributors", () => {
  it("keeps humans with valid logins, most contributions first", () => {
    const out = normalize([
      { login: "alice", type: "User", avatar_url: "https://avatars.githubusercontent.com/u/1?v=4", contributions: 2 },
      { login: "dependabot[bot]", type: "Bot", avatar_url: "x", contributions: 50 },
      { login: "../evil", type: "User", avatar_url: "x", contributions: 9 },
      { login: "bob", type: "User", avatar_url: "https://avatars.githubusercontent.com/u/2?v=4", contributions: 5 },
    ]);
    expect(out.map((c: { login: string }) => c.login)).toEqual(["bob", "alice"]);
  });

  it("reads the saved list with same-origin avatars only", () => {
    const dir = mkdtempSync(join(tmpdir(), "contrib-"));
    writeFileSync(
      join(dir, "contributors.json"),
      JSON.stringify([
        { login: "alice", avatar: "/contributors/alice.png", contributions: 3 },
        { login: "mallory", avatar: "https://evil.example/x.png", contributions: 1 },
      ]),
    );
    expect(getContributors(dir)).toEqual([
      { login: "alice", avatar: "/contributors/alice.png", profileUrl: "https://github.com/alice", contributions: 3 },
    ]);
    expect(getContributors(join(dir, "missing"))).toEqual([]);
  });
});
