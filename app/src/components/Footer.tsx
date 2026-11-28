"use client";

/**
 * Footer — site footer with the Microsoft disclaimer, a link to our public repo and the ghcertified (GPL-3.0) credit.
 * Client component because it renders in the root layout (outside [locale]),
 * where setRequestLocale hasn't been called yet.
 */

import { useTranslations } from "next-intl";
import { Separator } from "@/components/ui/separator";
import { CONTRIBUTE_REPO_URL, MS_LEARN_CERTS_URL, UPSTREAM_REPO_URL } from "@/lib/site";

const linkClass = "text-primary no-underline hover:underline";

export function Footer() {
  const t = useTranslations("Footer");
  return (
    <footer className="mt-12">
      <Separator />
      <div className="py-6 sm:py-8 px-4 sm:px-8 text-center text-[13px] text-muted-foreground flex flex-col gap-2 max-w-[760px] mx-auto">
        <p>
          {t.rich("tagline", {
            link: (chunks) => (
              <a href={MS_LEARN_CERTS_URL} target="_blank" rel="noopener noreferrer" className={linkClass}>
                {chunks}
              </a>
            ),
          })}
        </p>
        <p>{t("disclaimer")}</p>
        <p>
          {t.rich("source", {
            repo: (chunks) => (
              <a href={CONTRIBUTE_REPO_URL} target="_blank" rel="noopener noreferrer" className={linkClass}>
                {chunks}
              </a>
            ),
          })}
        </p>
        <p>
          {t.rich("credit", {
            link: (chunks) => (
              <a href={UPSTREAM_REPO_URL} target="_blank" rel="noopener noreferrer" className={linkClass}>
                {chunks}
              </a>
            ),
          })}
        </p>
      </div>
    </footer>
  );
}
