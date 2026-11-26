#!/usr/bin/env node
// Build step (npm run build): the public repo's contributors + their avatars, saved as static files so the site never
// loads anything from github.com at runtime (the prod CSP allows images from 'self' only).
//
//   public/contributors/<login>.<png|jpg>   avatar, 72 px
//   public/contributors/contributors.json   [{ login, avatar, contributions }]   (read by src/lib/contributors.ts)
//
// Never fails the build: on any error it writes an empty list and the home page hides the section.
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export const REPO = "Toonssen/getazcertified";
const OUT = join(process.cwd(), "public", "contributors");
const LOGIN_RE = /^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$/;
const MAX = 100;

/** Humans only, valid logins only, most contributions first. */
export function normalize(data) {
  if (!Array.isArray(data)) return [];
  return data
    .filter((c) => c && c.type === "User" && typeof c.login === "string" && LOGIN_RE.test(c.login) && !c.login.endsWith("[bot]"))
    .map((c) => ({ login: c.login, avatarUrl: String(c.avatar_url ?? ""), contributions: Number(c.contributions) || 0 }))
    .sort((a, b) => b.contributions - a.contributions)
    .slice(0, MAX);
}

async function main() {
  rmSync(OUT, { recursive: true, force: true });
  mkdirSync(OUT, { recursive: true });
  const list = [];
  try {
    const headers = { Accept: "application/vnd.github+json", "User-Agent": "getazcertified-build" };
    if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
    const res = await fetch(`https://api.github.com/repos/${REPO}/contributors?per_page=100`, { headers, signal: AbortSignal.timeout(15000) });
    if (!res.ok) throw new Error(`GitHub API ${res.status}`);
    for (const c of normalize(await res.json())) {
      const url = new URL(c.avatarUrl);
      if (url.protocol !== "https:" || !url.hostname.endsWith(".githubusercontent.com")) continue;
      url.searchParams.set("s", "72");
      const img = await fetch(url, { signal: AbortSignal.timeout(15000) });
      const type = img.headers.get("content-type") ?? "";
      const ext = type.includes("png") ? "png" : type.includes("jpeg") ? "jpg" : null;
      if (!img.ok || !ext) continue;
      const bytes = Buffer.from(await img.arrayBuffer());
      if (bytes.length > 200_000) continue;
      writeFileSync(join(OUT, `${c.login}.${ext}`), bytes);
      list.push({ login: c.login, avatar: `/contributors/${c.login}.${ext}`, contributions: c.contributions });
    }
  } catch (e) {
    console.warn(`fetch-contributors: ${e.message}; the contributors section will be hidden`);
    list.length = 0;
  }
  writeFileSync(join(OUT, "contributors.json"), JSON.stringify(list, null, 2) + "\n");
  console.log(`fetch-contributors: ${list.length} contributors of ${REPO}`);
}

if (import.meta.url === `file://${process.argv[1]}`) await main();
