import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'LUCA Network - Living Universal Cognition Array',
  description: 'Decentralized mesh network with evolutionary consciousness',
  keywords: ['mesh network', 'decentralized', 'AI', 'consciousness', 'blockchain'],
  authors: [{ name: 'LUCA Team' }],
  openGraph: {
    title: 'LUCA Network',
    description: 'Decentralized mesh network with evolutionary consciousness',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 text-gray-900 antialiased`}>
        <div className="min-h-screen flex flex-col">
          {children}
        </div>
      </body>
    </html>
  )
}
