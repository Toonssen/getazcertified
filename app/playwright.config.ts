import { defineConfig } from "@playwright/test";

/**
 * Default: `npm run dev` on :3000 (dev repo CI). With E2E_BASE_URL set (prod repo CI), the tests run against an already
 * served static build instead; E2E_PREVIEW=1 marks the sneak-peek build, where the challenge specs don't apply.
 */
const BASE_URL = process.env.E2E_BASE_URL ?? "http://localhost:3000";
const PREVIEW = !!process.env.E2E_PREVIEW;

export default defineConfig({
  testDir: "./e2e",
  ...(PREVIEW ? { testIgnore: ["**/challenge-flow.spec.ts"], grepInvert: /challenge hub|leaderboard/i } : {}),
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
  },
  ...(process.env.E2E_BASE_URL
    ? {}
    : {
        webServer: {
          command: "npm run dev",
          url: "http://localhost:3000",
          reuseExistingServer: !process.env.CI,
        },
      }),
});
