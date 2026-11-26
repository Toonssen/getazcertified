// @vitest-environment jsdom
import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { QuestionCard, docPageTitle } from "@/components/quiz/QuestionCard";
import { toDocLinks } from "@/lib/questions";

const A = "https://learn.microsoft.com/en-us/azure/backup/backup-vault-overview";
const B = "https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-enhanced-policy";

function links(hrefs: string[]) {
  const { container } = render(
    <QuestionCard
      headerLabel="Question 1 of 1"
      documentationHrefs={hrefs}
      learnMoreLabel="Learn more in the docs"
      moreDocsLabel="More in the docs"
      footer={null}
    >
      body
    </QuestionCard>,
  );
  return Array.from(container.querySelectorAll("a")).map((a) => a.getAttribute("href"));
}

describe("QuestionCard documentation links", () => {
  it("renders one link for a single page", () => {
    expect(links([A])).toEqual([A]);
  });

  it("renders every page when there are several", () => {
    expect(links([A, B]).sort()).toEqual([A, B].sort());
  });

  it("renders no link when there are none", () => {
    expect(links([])).toEqual([]);
  });

  it("names a page from its slug", () => {
    expect(docPageTitle(`${B}#policy`)).toBe("backup azure vms enhanced policy");
  });
});

describe("toDocLinks", () => {
  it("accepts a string or a list", () => {
    expect(toDocLinks(A)).toEqual([A]);
    expect(toDocLinks([A, B])).toEqual([A, B]);
    expect(toDocLinks(undefined)).toEqual([]);
  });
});
