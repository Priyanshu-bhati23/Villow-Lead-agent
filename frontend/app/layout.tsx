import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Villow Lead Generation Agent Dashboard',
  description: 'AI-Powered Lead Generation Agent for Villow Founding Publisher Program',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
