import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VentureIQ AI — Due Diligence Platform",
  description: "AI-powered investment due diligence platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
