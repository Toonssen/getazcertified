/**
 * Tests that every question file across all certifications and locales
 * parses correctly through the mdquiz parser — the same pipeline the app uses.
 */

import { describe, it, expect } from "vitest";
import { join } from "node:path";
import { readdirSync, existsSync } from "node:fs";
import { parseDirectory } from "mdquiz";

const QUESTIONS_ROOT = join(__dirname, "../../../../questions");

import { VALID_CERTS as CERTS } from "../questions";

const locales = readdirSync(QUESTIONS_ROOT).filter(
  (entry) =>
    !entry.startsWith(".") &&
    !entry.endsWith(".md") &&
    existsSync(join(QUESTIONS_ROOT, entry)),
);

describe("question parsing", () => {
  for (const locale of locales) {
    describe(`locale: ${locale}`, () => {
      for (const cert of CERTS) {
        const dir = join(QUESTIONS_ROOT, locale, cert);
        if (!existsSync(dir)) continue;

        it(`parses all ${cert} questions`, () => {
          const questions = parseDirectory(dir, { filePrefix: "question-", strict: true });

          expect(questions.length).toBeGreaterThan(0);

          for (const q of questions) {
            // Every question must have question text
            expect(q.question, `${cert}/${q.id} missing question text`).toBeTruthy();

            // Every question must have at least 2 answers
            expect(
              q.answers.length,
              `${cert}/${q.id} has fewer than 2 answers`,
            ).toBeGreaterThanOrEqual(2);

            // Every question must have at least 1 correct answer
            const correctCount = q.answers.filter((a: { isCorrect: boolean }) => a.isCorrect).length;
            expect(
              correctCount,
              `${cert}/${q.id} has no correct answer`,
            ).toBeGreaterThanOrEqual(1);

            // Each answer must have text
            for (const a of q.answers) {
              expect(
                (a as { text: string }).text,
                `${cert}/${q.id} has answer with empty text`,
              ).toBeTruthy();
            }
          }
        });
      }
    });
  }
});

describe("documentation links", () => {
  it("every question has 1–3 titled Learn links (title + url frontmatter)", async () => {
    const { getQuestionsByCert } = await import("../questions");
    const questions = getQuestionsByCert("az-104");
    expect(questions.length).toBeGreaterThan(0);
    for (const q of questions) {
      const docs = q.documentation ?? [];
      expect(docs.length, q.id).toBeGreaterThanOrEqual(1);
      expect(docs.length, q.id).toBeLessThanOrEqual(3);
      for (const d of docs) {
        expect(d.url, q.id).toMatch(/^https:\/\/learn\.microsoft\.com\//);
        expect(d.title.length, `${q.id} ${d.title}`).toBeLessThanOrEqual(40);
        expect(d.title, q.id).not.toMatch(/^[a-z0-9 ]+$/); // a real title, not the slug fallback
      }
    }
    const q25 = questions.find((q) => q.id === "az-104-025");
    expect(q25?.documentation?.map((d) => d.title)).toEqual([
      "Azure Files share permissions",
      "Azure Files identity auth",
      "Authorize data access in Azure Storage",
    ]);
  });
});
