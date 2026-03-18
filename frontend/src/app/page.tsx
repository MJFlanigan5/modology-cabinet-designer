'use client'

import Link from 'next/link'
import { SignedIn, SignedOut } from '@clerk/nextjs'

const features = [
  {
    category: 'Design',
    icon: '📐',
    items: [
      { name: 'Cabinet Builder', href: '/design/builder', description: 'Create and customize cabinets', icon: '🏗️' },
      { name: 'Style Presets', href: '/design/presets', description: 'Shaker, flat-panel, raised-panel styles', icon: '🎨' },
      { name: 'Templates', href: '/design/templates', description: 'Kitchen layouts, vanity sets, bookshelves', icon: '📋' },
      { name: 'Sketch Import', href: '/design/sketch', description: 'Convert sketches to 3D models', icon: '✏️' },
      { name: 'AR Scanner', href: '/design/ar-scanner', description: 'Scan rooms with your phone', icon: '📱' },
    ],
  },
  {
    category: 'Materials & Hardware',
    icon: '🪵',
    items: [
      { name: 'Material Selector', href: '/materials/selector', description: 'Plywood, MDF, hardwood options', icon: '🪵' },
      { name: 'Multi-Material Projects', href: '/materials/multi', description: 'Mix materials in one project', icon: '🔀' },
      { name: 'Edge Banding', href: '/materials/edge-banding', description: 'Optimize edge banding calculations', icon: '📏' },
      { name: 'Hardware Finder', href: '/hardware/finder', description: 'Find hinges, slides, handles', icon: '🔧' },
      { name: 'Recommendations', href: '/hardware/recommendations', description: 'AI-powered hardware suggestions', icon: '💡' },
    ],
  },
  {
    category: 'Optimization',
    icon: '⚡',
    items: [
      { name: 'Cut List Export', href: '/optimize/cutlist', description: 'Optimized cut lists with waste reduction', icon: '📝' },
      { name: 'Advanced Nesting', href: '/optimize/nesting', description: 'Non-guillotine nesting algorithms', icon: '🧩' },
      { name: 'Scrap Tracker', href: '/optimize/scrap', description: 'Track and use leftover pieces', icon: '♻️' },
      { name: 'Design Doctor', href: '/optimize/doctor', description: 'Find design issues before building', icon: '🩺' },
      { name: 'Cost Optimizer', href: '/optimize/cost', description: '"Best bang for your buck" analysis', icon: '💰' },
      { name: 'Board Yield', href: '/optimize/yield', description: 'Maximize plywood sheet usage', icon: '📊' },
    ],
  },
  {
    category: 'Export & Share',
    icon: '📤',
    items: [
      { name: 'G-Code Export', href: '/export/gcode', description: 'CNC-ready code for GRBL, ShopBot', icon: '🤖' },
      { name: '3D Export', href: '/export/3d', description: 'OBJ, STL, 3MF, DXF formats', icon: '🎮' },
      { name: 'Community Gallery', href: '/community/gallery', description: 'Share and browse projects', icon: '🖼️' },
      { name: 'Brag Sheet', href: '/community/brag-sheet', description: 'Generate shareable project posts', icon: '🏆' },
    ],
  },
  {
    category: 'Tools',
    icon: '🛠️',
    items: [
      { name: 'Local Suppliers', href: '/tools/localization', description: 'Find suppliers near you', icon: '📍' },
      { name: 'Store Integration', href: '/tools/stores', description: 'Home Depot, Lowe\'s pricing', icon: '🏪' },
      { name: 'Scratch Build Calc', href: '/tools/scratch-build', description: 'Time and tool estimates', icon: '⏱️' },
      { name: 'Climate Adjustment', href: '/tools/climate', description: 'Humidity and wood movement', icon: '🌡️' },
      { name: 'Version History', href: '/tools/history', description: 'Track design changes', icon: '📜' },
    ],
  },
]

const stats = [
  { label: 'Active Users', value: '12,000+' },
  { label: 'Cabinets Designed', value: '250,000+' },
  { label: 'Wood Saved', value: '50,000 sheets' },
  { label: 'Money Saved', value: '$2M+' },
]

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-4">
              <span className="text-white">Kerf</span>
              <span className="font-light text-blue-200">OS</span>
            </h1>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Precision cabinet design for woodworkers and DIYers. Design smarter, cut efficiently, build with confidence.
            </p>
            <div className="flex justify-center gap-4">
              <SignedOut>
                <Link
                  href="/pricing"
                  className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
                >
                  Start Free Trial
                </Link>
              </SignedOut>
              <SignedIn>
                <Link
                  href="/design/builder"
                  className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
                >
                  Open Cabinet Builder
                </Link>
              </SignedIn>
              <Link
                href="/design/templates"
                className="px-8 py-3 border-2 border-white text-white rounded-lg font-semibold hover:bg-white/10 transition-colors"
              >
                Browse Templates
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white py-12 border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {stats.map((stat) => (
              <div key={stat.label}>
                <div className="text-3xl font-bold text-blue-600">{stat.value}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Everything You Need</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              From initial design to final cut, KerfOS helps you build better cabinets with less waste.
            </p>
          </div>

          <div className="space-y-12">
            {features.map((category) => (
              <div key={category.category}>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">{category.icon}</span>
                  <h3 className="text-xl font-semibold text-gray-900">{category.category}</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {category.items.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className="bg-white p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all group"
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-2xl group-hover:scale-110 transition-transform">{item.icon}</span>
                        <div>
                          <h4 className="font-medium text-gray-900 group-hover:text-blue-600">{item.name}</h4>
                          <p className="text-sm text-gray-500">{item.description}</p>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Build Smarter?</h2>
          <p className="text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of woodworkers and DIYers who trust KerfOS for their cabinet projects.
          </p>
          <div className="flex justify-center gap-4">
            <SignedOut>
              <Link
                href="/pricing"
                className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                Get Started Free
              </Link>
            </SignedOut>
            <SignedIn>
              <Link
                href="/design/builder"
                className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                Start Designing
              </Link>
            </SignedIn>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <span className="text-2xl font-bold text-white">Kerf</span>
              <span className="text-2xl font-light text-gray-400">OS</span>
            </div>
            <div className="flex gap-6 text-sm">
              <Link href="/privacy" className="hover:text-white">Privacy Policy</Link>
              <Link href="/terms" className="hover:text-white">Terms of Service</Link>
              <Link href="/gdpr" className="hover:text-white">GDPR</Link>
              <Link href="/pricing" className="hover:text-white">Pricing</Link>
            </div>
          </div>
          <div className="mt-8 text-center text-sm">
            © {new Date().getFullYear()} KerfOS. All rights reserved.
          </div>
        </div>
      </footer>
    </main>
  )
}

export const metadata = {
  title: "KerfOS - Precision Cabinet Design",
  description: "AI-powered cabinet design tool for woodworkers and DIYers. Design, optimize, and build with confidence.",
}
