// @vitest-environment jsdom
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { QuestionCard, docPageTitle } from "@/components/quiz/QuestionCard";
import { toDocLinks, type DocLink } from "@/lib/doc-links";

const A = "https://learn.microsoft.com/en-us/azure/backup/backup-vault-overview";
const B = "https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-enhanced-policy";
const C = "https://learn.microsoft.com/en-us/azure/backup/backup-overview";
const DOCS: DocLink[] = [
  { title: "Backup vaults overview", url: A },
  { title: "Back up VMs with the Enhanced policy", url: B },
  { title: "What is Azure Backup?", url: C },
];

function renderCard(docs: DocLink[]) {
  return render(
    <QuestionCard
      headerLabel="Question 1 of 1"
      documentation={docs}
      learnMoreLabel="Learn more in the docs"
      mainDocLabel="Main page"
      footer={null}
    >
      body
    </QuestionCard>,
  );
}

describe("QuestionCard documentation menu", () => {
  it("shows one trigger, whatever the number of links, and no loose doc links", () => {
    for (const docs of [DOCS.slice(0, 1), DOCS]) {
      const { container, unmount } = renderCard(docs);
      expect(screen.getAllByTestId("docs-menu-trigger")).toHaveLength(1);
      expect(container.querySelectorAll('a[href^="https://learn.microsoft.com"]')).toHaveLength(0);
      unmount();
    }
  });

  it("lists every link by title when opened, opening in a new tab", async () => {
    renderCard(DOCS);
    fireEvent.click(screen.getByTestId("docs-menu-trigger"));
    const items = await screen.findAllByRole("menuitem");
    expect(items.map((el) => el.getAttribute("href"))).toEqual([A, B, C]);
    expect(items.map((el) => el.textContent)).toEqual([
      "Backup vaults overviewMain page",
      "Back up VMs with the Enhanced policy",
      "What is Azure Backup?",
    ]);
    for (const el of items) {
      expect(el.getAttribute("target")).toBe("_blank");
      expect(el.getAttribute("rel")).toBe("noopener noreferrer");
    }
  });

  it("says how many pages the menu holds", () => {
    renderCard(DOCS);
    expect(screen.getByTestId("docs-menu-trigger").getAttribute("aria-label")).toBe("Learn more in the docs (3)");
  });

  it("renders no menu when there are no links", () => {
    renderCard([]);
    expect(screen.queryByTestId("docs-menu-trigger")).toBeNull();
  });

  it("names a page from its slug", () => {
    expect(docPageTitle(`${B}#policy`)).toBe("backup azure vms enhanced policy");
  });
});

describe("toDocLinks", () => {
  it("reads title + url entries", () => {
    expect(toDocLinks([{ title: "Backup vaults overview", url: A }])).toEqual([DOCS[0]]);
  });

  it("falls back to a title from the URL for a bare string or a missing title", () => {
    expect(toDocLinks(A)).toEqual([{ title: "backup vault overview", url: A }]);
    expect(toDocLinks([{ url: A }, { title: "  ", url: B }])).toEqual([
      { title: "backup vault overview", url: A },
      { title: "backup azure vms enhanced policy", url: B },
    ]);
  });

  it("drops entries without a url", () => {
    expect(toDocLinks([{ title: "No url" }, null, ""])).toEqual([]);
    expect(toDocLinks(undefined)).toEqual([]);
  });
});
