import type { Metadata } from "next";
import { JetBrains_Mono, Nunito } from "next/font/google";
import "./globals.css";

import { IS_PREVIEW, SITE_NAME, SITE_TITLE, SITE_URL } from "@/lib/site";

/**
 * Nunito (variable, 200–1000) for all text: ExtraBold/Black for headings, buttons and the wordmark, Regular/SemiBold
 * for question and answer text. next/font self-hosts it at build time (no runtime request to Google).
 */
const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

const DESCRIPTION =
  "Free practice questions for Microsoft Azure certification exams, written from the Microsoft Learn documentation.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  ...(IS_PREVIEW ? { robots: { index: false, follow: false } } : {}),
  title: {
    default: SITE_TITLE,
    template: `%s — ${SITE_NAME}`,
  },
  description:
    DESCRIPTION,
  openGraph: {
    title: SITE_TITLE,
    description:
      DESCRIPTION,
    siteName: SITE_NAME,
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_TITLE,
    description:
      DESCRIPTION,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${nunito.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        {children}
      </body>
    </html>
  );
}
