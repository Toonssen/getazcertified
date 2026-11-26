"use client";

import type { ReactNode } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { BookOpen, ChevronDown, CircleAlert, ExternalLink, Pencil } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { DocLink } from "@/lib/doc-links";

export { docPageTitle } from "@/lib/doc-links";

export interface QuestionCardProps {
  headerLabel: string;
  headerActions?: ReactNode;
  progressBar?: ReactNode;
  /** Learn pages for this question, main page first; shown as one "Learn more in the docs" menu. */
  documentation?: DocLink[];
  reportHref?: string;
  learnMoreLabel?: string;
  /** Small tag on the first (main) page in the menu, e.g. "Main page". */
  mainDocLabel?: string;
  reportLabel?: string;
  reportTooltip?: string;
  /** "Improve" link: GitHub's web editor for the question's file (only where answers are visible anyway). */
  editHref?: string;
  editLabel?: string;
  editTooltip?: string;
  children: ReactNode;
  footer: ReactNode;
}

const headerButton =
  "inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-[11px] font-semibold tracking-wide uppercase transition-colors text-card/50 hover:bg-card/10 hover:text-card/70 focus-visible:ring-2 focus-visible:ring-card/40 focus-visible:outline-none";

/** One button in the card header; opens a menu with every Learn page of the question, by title. */
function DocsMenu({ docs, label, mainLabel }: { docs: DocLink[]; label: string; mainLabel?: string }) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        render={<button type="button" className={headerButton} aria-label={`${label} (${docs.length})`} />}
        data-testid="docs-menu-trigger"
      >
        <BookOpen className="size-3.5" />
        <span className="hidden sm:inline">{label}</span>
        <ChevronDown className="size-3" aria-hidden="true" />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-auto min-w-[240px] max-w-[min(340px,calc(100vw-2rem))] p-1.5">
        {docs.map((doc, i) => (
          <DropdownMenuItem
            key={doc.url}
            render={<a href={doc.url} target="_blank" rel="noopener noreferrer" />}
            className="cursor-pointer gap-1.5 px-2 py-2 text-[13px] font-medium"
            title={doc.url}
          >
            <BookOpen className="size-3.5 text-primary" />
            <span className="flex-1 min-w-0">{doc.title}</span>
            {i === 0 && docs.length > 1 && mainLabel && (
              <span className="shrink-0 text-[10px] font-semibold uppercase text-muted-foreground">{mainLabel}</span>
            )}
            <ExternalLink className="size-3 text-muted-foreground" aria-hidden="true" />
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export function QuestionCard({
  headerLabel,
  headerActions,
  progressBar,
  documentation = [],
  reportHref,
  learnMoreLabel,
  mainDocLabel,
  reportLabel,
  reportTooltip,
  editHref,
  editLabel,
  editTooltip,
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
            {learnMoreLabel && documentation.length > 0 && (
              <DocsMenu docs={documentation} label={learnMoreLabel} mainLabel={mainDocLabel} />
            )}
            {reportHref && reportLabel && (
              <a
                href={reportHref}
                target="_blank"
                rel="noopener noreferrer"
                className={headerButton}
                title={reportTooltip}
                aria-label={reportLabel}
              >
                <CircleAlert className="size-3.5" />
                <span className="hidden sm:inline">{reportLabel}</span>
              </a>
            )}
            {editHref && editLabel && (
              <a
                href={editHref}
                target="_blank"
                rel="noopener noreferrer"
                className={headerButton}
                title={editTooltip}
                aria-label={editLabel}
                data-testid="improve-link"
              >
                <Pencil className="size-3.5" />
                <span className="hidden sm:inline">{editLabel}</span>
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
