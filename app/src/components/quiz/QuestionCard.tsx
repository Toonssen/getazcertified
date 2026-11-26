"use client";

import type { ReactNode } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { BookOpen, CircleAlert } from "lucide-react";

export interface QuestionCardProps {
  headerLabel: string;
  headerActions?: ReactNode;
  progressBar?: ReactNode;
  documentationHrefs?: string[];
  reportHref?: string;
  learnMoreLabel?: string;
  moreDocsLabel?: string;
  reportLabel?: string;
  reportTooltip?: string;
  children: ReactNode;
  footer: ReactNode;
}

/** Readable page name from a Learn URL: ".../azure/backup/backup-vault-overview" -> "backup vault overview". */
export function docPageTitle(href: string): string {
  const path = href.split(/[?#]/, 1)[0].replace(/\/+$/, "");
  const slug = path.slice(path.lastIndexOf("/") + 1);
  return decodeURIComponent(slug).replace(/[-_]+/g, " ").trim() || href;
}

export function QuestionCard({
  headerLabel,
  headerActions,
  progressBar,
  documentationHrefs = [],
  reportHref,
  learnMoreLabel,
  moreDocsLabel,
  reportLabel,
  reportTooltip,
  children,
  footer,
}: QuestionCardProps) {
  return (
    <Card className="overflow-hidden shadow-sm border-[1.5px] pt-0 gap-0">
      <CardHeader className="bg-foreground px-4 sm:px-7 pt-4 sm:pt-5 pb-3 sm:pb-4 flex flex-col gap-3 space-y-0">
        <div className="flex items-center justify-between gap-3 w-full">
          <span className="font-display text-[13px] font-bold text-card/50 tracking-wide">
            {headerLabel}
          </span>
          <div className="flex items-center gap-2.5 ml-auto">
            {headerActions}
            {learnMoreLabel &&
              documentationHrefs.slice(1).map((href) => (
                <a
                  key={href}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center rounded-md px-1.5 py-1 transition-colors text-card/50 hover:bg-card/10 hover:text-card/70"
                  title={`${moreDocsLabel ?? learnMoreLabel}: ${docPageTitle(href)}`}
                  aria-label={`${moreDocsLabel ?? learnMoreLabel}: ${docPageTitle(href)}`}
                >
                  <BookOpen className="size-3.5" />
                </a>
              ))}
            {documentationHrefs[0] && learnMoreLabel && (
              <a
                href={documentationHrefs[0]}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-[11px] font-semibold tracking-wide uppercase transition-colors text-card/50 hover:bg-card/10 hover:text-card/70"
                title={learnMoreLabel}
              >
                <BookOpen className="size-3.5" />
                <span className="hidden sm:inline">{learnMoreLabel}</span>
              </a>
            )}
            {reportHref && reportLabel && (
              <a
                href={reportHref}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-[11px] font-semibold tracking-wide uppercase transition-colors text-card/50 hover:bg-card/10 hover:text-card/70"
                title={reportTooltip}
              >
                <CircleAlert className="size-3.5" />
                <span className="hidden sm:inline">{reportLabel}</span>
              </a>
            )}
          </div>
        </div>
        {progressBar}
      </CardHeader>
      <CardContent className="p-4 sm:p-7 text-left">
        {children}
      </CardContent>
      <Separator />
      {footer}
    </Card>
  );
}
