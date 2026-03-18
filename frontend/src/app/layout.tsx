import './globals.css'
import { ClerkProvider } from '@clerk/nextjs'
import Navigation from '@/components/Navigation'

export const metadata = {
  title: 'KerfOS - Precision Cabinet Design',
  description: 'AI-powered cabinet design tool for woodworkers and DIYers. Design, optimize, and build with confidence.',
  keywords: 'cabinet design, woodworking, cut list, CNC, G-code, DIY, furniture design',
  authors: [{ name: 'KerfOS' }],
  openGraph: {
    title: 'KerfOS - Precision Cabinet Design',
    description: 'AI-powered cabinet design tool for woodworkers and DIYers.',
    type: 'website',
    url: 'https://kerfos.com',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="bg-gray-50">
          <Navigation />
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
