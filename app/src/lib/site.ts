/**
 * Site identity — one place for the name, canonical URL and source repo.
 *
 * NEXT_PUBLIC_SITE_URL is set per deployment (dev.getazcertified.com for the dev site); the default is production.
 */

export const SITE_NAME = "getazcertified";
export const SITE_TITLE = "Get Azure Certified — Practice Tests";
export const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL ?? "https://getazcertified.com").replace(/\/$/, "");
export const SITE_REPO = process.env.NEXT_PUBLIC_SITE_REPO ?? "Toonssen/getazcertified-dev";

/**
 * Preview ("sneak peek") build: NEXT_PUBLIC_SITE_MODE=preview. Practice tests and the question browser only; no
 * challenges, no contributor list, a sneak-peek banner, and nothing indexed. Unset = the full site (dev).
 */
export const IS_PREVIEW = process.env.NEXT_PUBLIC_SITE_MODE === "preview";
export const UPSTREAM_REPO_URL = "https://github.com/v-fidelusaleksander/ghcertified";
export const MS_LEARN_CERTS_URL = "https://learn.microsoft.com/credentials/browse/?credential_types=certification";
export const SITE_REPO_URL = `https://github.com/${SITE_REPO}`;
/**
 * Where contributions go, on every build: the public repo owns the questions and takes issues and pull requests
 * (CONTRIBUTING.md there). The dev site points here too, so a report always lands where it can be fixed.
 */
export const CONTRIBUTE_REPO_URL = "https://github.com/Toonssen/getazcertified";
