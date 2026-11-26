/**
 * Documentation links of a question: the Microsoft Learn pages that back its answer, with a short title for the
 * "Learn more in the docs" menu. Client-safe (no Node imports), shared by the loader and the QuestionCard.
 *
 * Frontmatter (see questions/README.md › Documentation links):
 *   documentation:
 *     - title: "Share-level permissions for Azure Files"
 *       url: "https://learn.microsoft.com/en-us/azure/storage/files/..."
 */

export interface DocLink {
  title: string;
  url: string;
}

/** Readable page name from a Learn URL: ".../azure/backup/backup-vault-overview" -> "backup vault overview". */
export function docPageTitle(href: string): string {
  const path = href.split(/[?#]/, 1)[0].replace(/\/+$/, "");
  const slug = path.slice(path.lastIndexOf("/") + 1);
  return decodeURIComponent(slug).replace(/[-_]+/g, " ").trim() || href;
}

/**
 * Normalise the frontmatter value to DocLink[]. The checker only allows `{ title, url }` entries; a bare URL string
 * (older files, or a single value) still works and gets a title derived from the URL, so a page never breaks.
 */
export function toDocLinks(value: unknown): DocLink[] {
  const list = Array.isArray(value) ? value : value ? [value] : [];
  const links: DocLink[] = [];
  for (const item of list) {
    if (typeof item === "string" && item.length > 0) {
      links.push({ title: docPageTitle(item), url: item });
    } else if (item && typeof item === "object") {
      const { title, url } = item as { title?: unknown; url?: unknown };
      if (typeof url === "string" && url.length > 0) {
        const t = typeof title === "string" ? title.trim() : "";
        links.push({ title: t || docPageTitle(url), url });
      }
    }
  }
  return links;
}
