import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "VoiceCard - Master Phrasal Verbs with AI",
  description: "Learn phrasal verbs through AI-powered conversation practice. Master English fluency with spaced repetition and pronunciation feedback.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        <Toaster 
          position="top-center" 
          richColors 
          expand={true}
          visibleToasts={5}
          closeButton={true}
          toastOptions={{
            style: {
              marginBottom: '8px',
            }
          }}
        />
      </body>
    </html>
  );
}
