import { afterEach, describe, expect, it, vi } from "vitest";

async function loadSite() {
  vi.resetModules();
  return import("@/lib/site");
}

describe("site identity", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it("is the full site by default", async () => {
    // Unset, not empty: CI environments (the prod repo's) may define these for the whole workflow.
    vi.stubEnv("NEXT_PUBLIC_SITE_MODE", undefined);
    vi.stubEnv("NEXT_PUBLIC_SITE_REPO", undefined);
    const site = await loadSite();
    expect(site.IS_PREVIEW).toBe(false);
    expect(site.SITE_REPO).toBe("Toonssen/getazcertified-dev");
  });

  it("switches to the sneak peek with NEXT_PUBLIC_SITE_MODE=preview", async () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_MODE", "preview");
    vi.stubEnv("NEXT_PUBLIC_SITE_REPO", "Toonssen/getazcertified");
    const site = await loadSite();
    expect(site.IS_PREVIEW).toBe(true);
    expect(site.SITE_REPO).toBe("Toonssen/getazcertified");
  });

  it("ignores other mode values", async () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_MODE", "Preview ");
    const site = await loadSite();
    expect(site.IS_PREVIEW).toBe(false);
  });
});
