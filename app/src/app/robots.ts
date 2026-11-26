import type { MetadataRoute } from "next";
import { IS_PREVIEW, SITE_URL } from "@/lib/site";

export const dynamic = "force-static";

/**
 * Only the full production site may be indexed. Dev (any other SITE_URL) and the sneak-peek build disallow the app;
 * the sneak peek still allows "/" (the static landing page that replaces the root redirect on prod).
 */
const IS_PRODUCTION = SITE_URL === "https://getazcertified.com" && !IS_PREVIEW;

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        ...(IS_PRODUCTION
          ? { allow: "/" }
          : IS_PREVIEW
            ? { allow: "/$", disallow: "/" }
            : { disallow: "/" }),
      },
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
