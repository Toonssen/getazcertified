import { useTranslations } from "next-intl";
import { Sparkles } from "lucide-react";

/**
 * SneakPeekBanner — thin strip under the navbar on the preview ("sneak peek") build only (IS_PREVIEW).
 * Tells visitors the site is an early preview, without boxes: soft primary tint, one line.
 */
export function SneakPeekBanner() {
  const t = useTranslations("SneakPeek");
  return (
    <div role="note" className="bg-primary-soft border-b border-border" data-testid="sneak-peek-banner">
      <div className="max-w-[1200px] mx-auto px-4 sm:px-8 py-2 flex items-center justify-center gap-2 text-[13px] text-foreground text-center">
        <Sparkles className="size-3.5 text-primary shrink-0" aria-hidden="true" />
        <span>
          <span className="font-bold text-primary">{t("label")}:</span> {t("text")}
        </span>
      </div>
    </div>
  );
}
