import type { Metadata } from "next";
import "./globals.css";
import "katex/dist/katex.min.css";
import { Providers } from "./providers";
import MixpanelInitializer from "./MixpanelInitializer";
import { Toaster } from "@/components/ui/sonner";
import TailwindBrowserRuntime from "@/components/runtime/TailwindBrowserRuntime";
export const metadata: Metadata = {
  metadataBase: new URL("https://sanrathi.com"),
  title: "Sanrathi Slide Maker",
  description:
    "Make classroom slides from a topic or a recorded lecture.",
  keywords: [
    "AI presentation generator",
    "data storytelling",
    "data visualization tool",
    "AI data presentation",
    "presentation generator",
    "data to presentation",
    "interactive presentations",
    "professional slides",
  ],
  openGraph: {
    title: "Sanrathi Slide Maker",
    description:
      "Make classroom slides from a topic or a recorded lecture.",
    url: "https://sanrathi.com",
    siteName: "Sanrathi",
    images: [
      {
        url: "/logo-with-bg.png",
        width: 1200,
        height: 630,
        alt: "Sanrathi logo",
      },
    ],
    type: "website",
    locale: "en_US",
  },
  alternates: {
    canonical: "https://sanrathi.com",
  },
  twitter: {
    card: "summary_large_image",
    title: "Sanrathi Slide Maker",
    description:
      "Make classroom slides from a topic or a recorded lecture.",
    images: ["/logo-with-bg.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="en">
      <body className="antialiased">
        <Providers>
          <MixpanelInitializer>

            {children}

          </MixpanelInitializer>
        </Providers>
        <TailwindBrowserRuntime />
        <Toaster position="top-center" />
      </body>
    </html>
  );
}
