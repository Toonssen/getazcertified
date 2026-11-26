import { test, expect, type Page } from "@playwright/test";

/**
 * Sneak-peek (preview) build only: E2E_PREVIEW=1, run against the built static export served with the production
 * headers (prod repo CI), so the Content-Security-Policy is enforced. Any CSP violation or console error fails.
 */
test.skip(!process.env.E2E_PREVIEW, "preview build only");

const APP_PAGES = ["/en/", "/en/practice-tests/", "/en/practice-tests/az-104", "/en/questions/az-104"];

function collectProblems(page: Page): string[] {
  const problems: string[] = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") problems.push(`console: ${msg.text()}`);
  });
  page.on("pageerror", (err) => problems.push(`pageerror: ${err.message}`));
  page.on("request", (req) => {
    const url = new URL(req.url());
    if (!["localhost", "127.0.0.1"].includes(url.hostname) && url.protocol !== "data:") {
      problems.push(`third-party request: ${req.url()}`);
    }
  });
  return problems;
}

for (const path of APP_PAGES) {
  test(`${path}: banner, no challenges, no CSP violations`, async ({ page }) => {
    const problems = collectProblems(page);
    await page.goto(path);
    await page.waitForLoadState("networkidle");
    await expect(page.getByTestId("sneak-peek-banner")).toBeVisible();
    await expect(page.getByRole("link", { name: /challenge/i })).toHaveCount(0);
    // Contributions and issue reports open at the full launch; no links to them yet.
    await expect(page.getByRole("link", { name: /contribute|write a question|report/i })).toHaveCount(0);
    expect(problems).toEqual([]);
  });
}

test("AZ-104 practice test runs to a score", async ({ page }) => {
  const problems = collectProblems(page);
  await page.goto("/en/practice-tests/az-104?questions=3");
  const group = () =>
    page.getByRole("radiogroup", { name: /answer options/i }).or(
      page.getByRole("group", { name: /answer options/i }),
    ).first();
  await group().waitFor({ timeout: 15_000 });

  for (let i = 0; i < 3; i++) {
    const checkboxes = group().getByRole("checkbox");
    if ((await checkboxes.count()) > 0) await checkboxes.first().click();
    else await group().getByRole("radio").first().click();
    if (i < 2) {
      await page.getByRole("button", { name: "Next question", exact: true }).click();
      await expect(page.getByText(new RegExp(`question ${i + 2} of 3`, "i"))).toBeVisible();
    }
  }
  await page.getByRole("button", { name: /submit exam/i }).first().click();
  const dialog = page.getByRole("dialog");
  await dialog.getByRole("button", { name: /submit exam/i }).click();
  await expect(page.getByText(/\d+ of 3 correct/i)).toBeVisible();
  expect(problems).toEqual([]);
});

test("question browser lists the AZ-104 questions", async ({ page }) => {
  const problems = collectProblems(page);
  await page.goto("/en/questions/az-104");
  await expect(page.getByText(/\d{2,} questions/i).first()).toBeVisible();
  expect(problems).toEqual([]);
});

test("challenges are not part of the sneak peek", async ({ page }) => {
  const res = await page.goto("/en/challenges/");
  expect(res?.status()).toBe(404);
});
