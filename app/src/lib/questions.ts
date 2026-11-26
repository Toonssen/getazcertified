/**
 * Question data loaded from markdown files via the quizdown parser.
 *
 * This is the app-specific glue layer: it knows about certification types,
 * directory structure, and how to map parsed questions to our domain model.
 * Supports multiple locales — questions live in `questions/<locale>/<cert>/`.
 */

import { join } from "node:path";
import { toDocLinks, type DocLink } from "./doc-links";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { parseDirectory } from "mdquiz";

// ── App-specific types ──────────────────────────────────────────────

/** A certification id from questions/certs/<id>.json, e.g. "az-104". */
export type CertificationType = string;

/** questions/certs/<id>.json (validated by scripts/check_questions.py; see CONTRIBUTING.md). */
export interface CertDefinition {
  id: string;
  title: string;
  description: string;
  status: "draft" | "live";
  study_guide: string;
  study_guide_url?: string;
  color: number;
  icon: string;
  domains: { id: string; name: string; weight: [number, number]; skill_areas: string[] }[];
}

export interface Question {
  id: string;
  cert: CertificationType;
  question: string;
  answers: { id: string; text: string; isCorrect: boolean; explanation?: string }[];
  isMultiSelect: boolean;
  codeBlock?: string;
  /** Learn pages backing the answer: one to three, each with a short title; the first is the main page. */
  documentation?: DocLink[];
}

export interface CertInfo {
  cert: CertificationType;
  title: string;
  description: string;
  color: number;
  icon: string;
  status: "draft" | "live";
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

const QUESTIONS_ROOT = join(process.cwd(), "..", "questions");

/**
 * Certification registry: every questions/certs/*.json. Draft certs (new, still collecting questions) are built
 * only when SHOW_DRAFT_CERTS=1 (the dev site); the public site lists live ones.
 */
export function loadCertRegistry(
  root: string = QUESTIONS_ROOT,
  showDrafts: boolean = process.env.SHOW_DRAFT_CERTS === "1",
): CertDefinition[] {
  const dir = join(root, "certs");
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .sort()
    .map((f) => JSON.parse(readFileSync(join(dir, f), "utf8")) as CertDefinition)
    .filter((c) => c.status === "live" || (showDrafts && c.status === "draft"));
}

const CERTS: CertDefinition[] = loadCertRegistry();

export const CERT_TITLES: Record<CertificationType, string> = Object.fromEntries(
  CERTS.map((c) => [c.id, c.title]),
);

const VALID_CERTS: CertificationType[] = CERTS.map((c) => c.id);

export { VALID_CERTS };

function contentDir(locale: SupportedLocale): string {
  return join(QUESTIONS_ROOT, locale);
}

export { toDocLinks } from "./doc-links";
export type { DocLink } from "./doc-links";

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
  return CERTS.map((c) => ({
    cert: c.id,
    title: c.title,
    description: c.description,
    color: c.color,
    icon: c.icon,
    status: c.status,
    questionCount: all.filter((q) => q.cert === c.id).length,
  }));
}

export function getCertInfo(
  cert: CertificationType,
  locale: SupportedLocale = DEFAULT_LOCALE,
): CertInfo | undefined {
  return getCertCatalog(locale).find((c) => c.cert === cert);
}

