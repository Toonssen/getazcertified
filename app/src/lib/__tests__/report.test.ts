import { describe, expect, it } from "vitest";
import { questionFileUrl, questionReportUrl } from "@/lib/report";

describe("question report link", () => {
  it("opens the public repo's issue form with id, file and title prefilled", () => {
    const url = new URL(questionReportUrl("az-104", "az-104-025", "[az-104] Issue with az-104-025"));
    expect(url.origin + url.pathname).toBe("https://github.com/Toonssen/getazcertified/issues/new");
    expect(url.searchParams.get("template")).toBe("question-problem.yml");
    expect(url.searchParams.get("question-id")).toBe("az-104-025");
    expect(url.searchParams.get("title")).toBe("[az-104] Issue with az-104-025");
    expect(url.searchParams.get("question-file")).toBe(
      "https://github.com/Toonssen/getazcertified/blob/main/questions/en/az-104/question-025.md",
    );
  });

  it("maps a question id to its file", () => {
    expect(questionFileUrl("sc-500", "sc-500-003")).toMatch(/questions\/en\/sc-500\/question-003\.md$/);
  });
});

describe("question improve link", () => {
  it("opens GitHub's web editor for the question's file in the public repo", async () => {
    const { questionEditUrl } = await import("@/lib/report");
    expect(questionEditUrl("az-104", "az-104-025")).toBe(
      "https://github.com/Toonssen/getazcertified/edit/main/questions/en/az-104/question-025.md",
    );
  });
});
