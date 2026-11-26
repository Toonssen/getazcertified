/**
 * Shared certification metadata — icons, descriptions, and color classes.
 *
 * Single source of truth consumed by the homepage, practice-tests catalog,
 * and questions library. Keeps cert branding consistent and DRY.
 *
 * Icons are generic lucide-react glyphs: no Microsoft logos or certification badges (trademark).
 */

import { ServerCog } from "lucide-react";
import type { CertificationType } from "./questions";

export interface CertMeta {
  colorClass: string;
  borderClass: string;
  textClass: string;
  icon: React.ReactNode;
  beta?: boolean;
}

export const CERT_META: Record<CertificationType, CertMeta> = {
  "az-104": {
    colorClass: "bg-cert-az-104",
    borderClass: "border-cert-az-104",
    textClass: "text-cert-az-104",
    icon: <ServerCog size={24} className="text-primary-foreground" />,
  },
};
