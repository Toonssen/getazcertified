/**
 * Certification visuals: palette slot + icon name from questions/certs/<cert>.json → classes and a lucide icon.
 * Client-safe (no Node imports). The allowed icon names and palette slots are mirrored in scripts/check_questions.py
 * (CERT_ICONS, CERT_COLORS), which rejects anything this file can't render.
 *
 * Icons are generic lucide-react glyphs: no Microsoft logos or certification badges (trademark).
 */

import {
  Boxes,
  Brain,
  ChartLine,
  Cloud,
  Code,
  Database,
  KeyRound,
  Lock,
  Network,
  ServerCog,
  ShieldCheck,
  Workflow,
  type LucideIcon,
} from "lucide-react";

export const CERT_ICONS: Record<string, LucideIcon> = {
  "server-cog": ServerCog,
  "shield-check": ShieldCheck,
  network: Network,
  database: Database,
  brain: Brain,
  cloud: Cloud,
  code: Code,
  lock: Lock,
  workflow: Workflow,
  "chart-line": ChartLine,
  "key-round": KeyRound,
  boxes: Boxes,
};

// Full class names (not built from strings) so Tailwind sees them; slots match --cert-1..8 in globals.css.
const COLOR_CLASSES: Record<number, { colorClass: string; borderClass: string; textClass: string }> = {
  1: { colorClass: "bg-cert-1", borderClass: "border-cert-1", textClass: "text-cert-1" },
  2: { colorClass: "bg-cert-2", borderClass: "border-cert-2", textClass: "text-cert-2" },
  3: { colorClass: "bg-cert-3", borderClass: "border-cert-3", textClass: "text-cert-3" },
  4: { colorClass: "bg-cert-4", borderClass: "border-cert-4", textClass: "text-cert-4" },
  5: { colorClass: "bg-cert-5", borderClass: "border-cert-5", textClass: "text-cert-5" },
  6: { colorClass: "bg-cert-6", borderClass: "border-cert-6", textClass: "text-cert-6" },
  7: { colorClass: "bg-cert-7", borderClass: "border-cert-7", textClass: "text-cert-7" },
  8: { colorClass: "bg-cert-8", borderClass: "border-cert-8", textClass: "text-cert-8" },
};

export interface CertMeta {
  colorClass: string;
  borderClass: string;
  textClass: string;
  icon: React.ReactNode;
  beta?: boolean;
}

/** Classes and icon for a cert; unknown values fall back to slot 1 and the server icon (the checker prevents them). */
export function certVisual(color: number, icon: string, beta = false): CertMeta {
  const Icon = CERT_ICONS[icon] ?? ServerCog;
  return {
    ...(COLOR_CLASSES[color] ?? COLOR_CLASSES[1]),
    icon: <Icon size={24} className="text-primary-foreground" />,
    beta,
  };
}
