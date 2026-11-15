import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SupeRR Selector — Pressure Performance Rankings",
  description:
    "Explore validated IPL and T20I pressure-performance rankings by role and national team.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
