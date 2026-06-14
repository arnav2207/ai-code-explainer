import type { Metadata } from "next";
import Link from "next/link";
import { Code2 } from "lucide-react";
import { ClerkProvider } from "@clerk/nextjs";

import "./globals.css";
import { Button } from "@/components/ui/button";
import { AuthButtons } from "@/components/auth/auth-buttons";

export const metadata: Metadata = {
  title: "AI Code Explainer",
  description: "Understand unfamiliar code with concise AI-powered explanations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,hsl(196_68%_91%),transparent_32rem),linear-gradient(180deg,hsl(210_24%_98%),hsl(0_0%_100%))]">
            <header className="sticky top-0 z-40 border-b bg-background/85 backdrop-blur">
              <div className="container flex h-16 items-center justify-between gap-4">
                <Link href="/" className="flex items-center gap-2 font-semibold">
                  <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
                    <Code2 className="h-5 w-5" />
                  </span>
                  <span>AI Code Explainer</span>
                </Link>
                <nav className="flex items-center gap-2">
                  <Button asChild variant="ghost" size="sm">
                    <Link href="/">Home</Link>
                  </Button>
                  <Button asChild size="sm">
                    <Link href="/explainer">Explainer</Link>
                  </Button>
                  <AuthButtons />
                </nav>
              </div>
            </header>
            {children}
          </div>
        </body>
      </html>
    </ClerkProvider>
  );
}
