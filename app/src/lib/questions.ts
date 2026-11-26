/**
 * Question data loaded from markdown files via the quizdown parser.
 *
 * This is the app-specific glue layer: it knows about certification types,
 * directory structure, and how to map parsed questions to our domain model.
 * Supports multiple locales — questions live in `questions/<locale>/<cert>/`.
 */

import { join } from "node:path";
import { existsSync } from "node:fs";
import { parseDirectory } from "mdquiz";

// ── App-specific types ──────────────────────────────────────────────

export type CertificationType = "az-104";

export interface Question {
  id: string;
  cert: CertificationType;
  question: string;
  answers: { id: string; text: string; isCorrect: boolean; explanation?: string }[];
  isMultiSelect: boolean;
  codeBlock?: string;
  /** Learn pages backing the answer: one or more, first one is the main page. */
  documentation?: string[];
}

export interface CertInfo {
  cert: CertificationType;
  title: string;
  questionCount: number;
}

// ── Locales ─────────────────────────────────────────────────────────

export {
  SUPPORTED_LOCALES,
  DEFAULT_LOCALE,
  isValidLocale,
} from "./locales";
export type { SupportedLocale } from "./locales";
export { parseSupportedLocale } from "./locales";

import { DEFAULT_LOCALE } from "./locales";
import type { SupportedLocale } from "./locales";

// ── Constants ───────────────────────────────────────────────────────

export const CERT_TITLES: Record<CertificationType, string> = {
  "az-104": "Azure Administrator (AZ-104)",
};

const VALID_CERTS: CertificationType[] = ["az-104"];

export { VALID_CERTS };

function contentDir(locale: SupportedLocale): string {
  return join(process.cwd(), "..", "questions", locale);
}

/** Frontmatter `documentation` is a single URL or a YAML list of URLs. */
export function toDocLinks(value: unknown): string[] {
  const list = Array.isArray(value) ? value : value ? [value] : [];
  return list.filter((v): v is string => typeof v === "string" && v.length > 0);
}

// ── Loader (cached per locale) ──────────────────────────────────────

const _cache = new Map<SupportedLocale, Question[]>();

function loadAll(locale: SupportedLocale): Question[] {
  const cached = _cache.get(locale);
  if (cached) return cached;

  const base = contentDir(locale);
  const all: Question[] = [];
  for (const cert of VALID_CERTS) {
    const dir = join(base, cert);
    if (!existsSync(dir)) continue;

    const raw = parseDirectory(dir, { filePrefix: "question-" });
    for (const q of raw) {
      all.push({
        id: `${cert}-${q.id.replace("question-", "")}`,
        cert,
        question: q.question,
        answers: q.answers,
        isMultiSelect: q.isMultiSelect,
        codeBlock: q.codeBlock,
        documentation: toDocLinks(q.frontmatter.documentation),
      });
    }
  }

  _cache.set(locale, all);
  return all;
}

// ── Public API ──────────────────────────────────────────────────────

export function getAllQuestions(
  locale: SupportedLocale = DEFAULT_LOCALE,
): Question[] {
  return loadAll(locale);
}

export function getQuestionsByCert(
  cert: CertificationType,
  locale: SupportedLocale = DEFAULT_LOCALE,
): Question[] {
  return loadAll(locale).filter((q) => q.cert === cert);
}

export function getCertCatalog(
  locale: SupportedLocale = DEFAULT_LOCALE,
): CertInfo[] {
  const all = loadAll(locale);
  return VALID_CERTS.map((cert) => ({
    cert,
    title: CERT_TITLES[cert],
    questionCount: all.filter((q) => q.cert === cert).length,
  }));
}

export function getCertInfo(
  cert: CertificationType,
  locale: SupportedLocale = DEFAULT_LOCALE,
): CertInfo | undefined {
  return getCertCatalog(locale).find((c) => c.cert === cert);
}

