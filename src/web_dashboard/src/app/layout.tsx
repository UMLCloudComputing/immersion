import type { Metadata } from "next";
import "./globals.css";
import SessionProvider from "@/components/SessionProvider";
import { NavBar } from "@/components/NavBar";
import { Provider } from "@/components/ui/provider"
import { Suspense } from "react";
import { Toaster } from "@/components/ui/toaster";

export const metadata: Metadata = {
  title: "Immersion",
  description: "Seamlessly integrate Discord with Engage",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <link rel="icon" href="immersion_logo_g.svg" type="img/svg+xml"></link>
      <body className="bg-neutral-300" suppressHydrationWarning>
        <Provider>
          <SessionProvider>
            <NavBar />

            <div className="min-h-[calc(100vh-3rem)] pt-12 bg-neutral-300">
              {children}
            </div>

            <Toaster />
          </SessionProvider>
        </Provider>
      </body>

    </html >
  );
}
