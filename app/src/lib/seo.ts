/**
 * Shared SEO helpers for generating per-page metadata.
 *
 * Centralises hreflang alternate generation, canonical URLs,
 * and OG defaults so every page stays consistent.
 */

import type { Metadata } from "next";
import { SUPPORTED_LOCALES } from "@/lib/locales";
import { SITE_URL as BASE_URL } from "@/lib/site";

/**
 * Build hreflang alternates + canonical for a given path.
 * @param locale  Current page locale
 * @param path    Path WITHOUT locale prefix (e.g. "/practice-tests/actions")
 */
export function buildAlternates(
  locale: string,
  path: string,
): Metadata["alternates"] {
  const clean = path.startsWith("/") ? path : `/${path}`;
  const languages: Record<string, string> = {};

  for (const loc of SUPPORTED_LOCALES) {
    languages[loc] = `${BASE_URL}/${loc}${clean}`;
  }
  // x-default points to English variant
  languages["x-default"] = `${BASE_URL}/en${clean}`;

  return {
    canonical: `${BASE_URL}/${locale}${clean}`,
    languages,
  };
}

/**
 * Open Graph images for social previews. Empty until getazcertified has its own artwork (Phase 3, before going
 * public): the upstream images were ghcertified-branded and were removed.
 */
export const OG_IMAGES: { url: string; width: number; height: number }[] = [];
