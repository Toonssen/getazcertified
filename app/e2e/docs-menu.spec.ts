import { test, expect } from "@playwright/test";

/**
 * Every question's "Learn more in the docs" menu at phone width: one trigger, 1–3 Learn links, and every title on one
 * line. Titles are limited by characters in scripts/check_questions.py (40, or 30 for the main page next to its
 * "Main page" tag); this checks the real rendering, so a wide title or a style change can't slip through.
 */
test.use({ viewport: { width: 390, height: 844 } });

test("every docs menu title fits on one line at 390px", async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto("/en/questions/az-104");
  const header = page.getByText(/question 1 of \d+/i).first();
  await expect(header).toBeVisible({ timeout: 15_000 });
  const total = Number((await header.innerText()).match(/of (\d+)/i)![1]);
  expect(total).toBeGreaterThan(0);

  const wrapped: string[] = [];
  for (let i = 1; i <= total; i++) {
    await expect(page.getByText(new RegExp(`question ${i} of ${total}`, "i")).first()).toBeVisible();
    await expect(page.getByTestId("docs-menu-trigger")).toHaveCount(1);
    await page.getByTestId("docs-menu-trigger").click();
    const items = page.getByRole("menuitem");
    await expect(items.first()).toBeVisible();
    const rows = await items.evaluateAll((els) =>
      els.map((el) => {
        const title = el.querySelector("span") as HTMLElement;
        const fontSize = parseFloat(getComputedStyle(title).fontSize);
        return {
          text: title.textContent ?? "",
          href: el.getAttribute("href") ?? "",
          oneLine: title.getBoundingClientRect().height < fontSize * 2,
        };
      }),
    );
    expect(rows.length, `question ${i}`).toBeGreaterThanOrEqual(1);
    expect(rows.length, `question ${i}`).toBeLessThanOrEqual(3);
    for (const r of rows) {
      expect(r.href, `question ${i}`).toMatch(/^https:\/\/learn\.microsoft\.com\//);
      if (!r.oneLine) wrapped.push(`question ${i}: "${r.text}"`);
    }
    await page.keyboard.press("Escape");
    await expect(items).toHaveCount(0);
    if (i < total) await page.getByRole("button", { name: "Next question", exact: true }).click();
  }
  expect(wrapped, "titles that wrap; shorten them in the question files").toEqual([]);
});
