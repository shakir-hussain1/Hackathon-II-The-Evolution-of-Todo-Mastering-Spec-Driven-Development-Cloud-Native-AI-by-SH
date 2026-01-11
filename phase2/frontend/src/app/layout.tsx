/**
 * Root Layout
 *
 * Global layout for the Next.js application.
 * Includes global styles and providers.
 */

import type { Metadata } from "next";
import './globals.css';

export const metadata: Metadata = {
  title: "Phase II Todo - Task Management",
  description: "Full-stack todo application with user authentication",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        {children}
      </body>
    </html>
  );
}
