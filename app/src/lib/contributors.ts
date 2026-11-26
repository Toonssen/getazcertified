import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

export interface Contributor {
  login: string;
  /** Same-origin path of the saved avatar, e.g. /contributors/octocat.png */
  avatar: string;
  profileUrl: string;
  contributions: number;
}

/**
 * Contributors of the public repo, saved at build time by scripts/fetch-contributors.mjs (avatars included, so nothing
 * loads from github.com in the browser). Empty when the file is missing or broken: the home page then hides the section.
 */
export function getContributors(dir = join(process.cwd(), "public", "contributors")): Contributor[] {
  const file = join(dir, "contributors.json");
  if (!existsSync(file)) return [];
  try {
    const data = JSON.parse(readFileSync(file, "utf-8"));
    if (!Array.isArray(data)) return [];
    return data
      .filter((c) => typeof c?.login === "string" && /^\/contributors\/[A-Za-z0-9-]+\.(png|jpg)$/.test(c?.avatar ?? ""))
      .map((c) => ({
        login: c.login,
        avatar: c.avatar,
        profileUrl: `https://github.com/${c.login}`,
        contributions: Number(c.contributions) || 0,
      }));
  } catch {
    return [];
  }
}
