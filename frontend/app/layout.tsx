import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CustomerOps Agent — Ticket Workspace",
  description: "Multi-agent ticket processing workspace for after-sales customer service",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
