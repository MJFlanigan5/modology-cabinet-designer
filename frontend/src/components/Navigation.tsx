'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { SignedIn, SignedOut, UserButton, SignInButton } from '@clerk/nextjs'

const navItems = [
  {
    label: 'Dashboard',
    href: '/',
    icon: '🏠',
  },
  {
    label: 'Design',
    href: '/design',
    icon: '📐',
    children: [
      { label: 'Cabinet Builder', href: '/design/builder' },
      { label: 'Style Presets', href: '/design/presets' },
      { label: 'Templates', href: '/design/templates' },
      { label: 'Sketch Import', href: '/design/sketch' },
      { label: 'AR Scanner', href: '/design/ar-scanner' },
    ],
  },
  {
    label: 'Materials',
    href: '/materials',
    icon: '🪵',
    children: [
      { label: 'Material Selector', href: '/materials/selector' },
      { label: 'Multi-Material Projects', href: '/materials/multi' },
      { label: 'Edge Banding', href: '/materials/edge-banding' },
    ],
  },
  {
    label: 'Hardware',
    href: '/hardware',
    icon: '🔧',
    children: [
      { label: 'Hardware Finder', href: '/hardware/finder' },
      { label: 'Recommendations', href: '/hardware/recommendations' },
    ],
  },
  {
    label: 'Optimize',
    href: '/optimize',
    icon: '⚡',
    children: [
      { label: 'Cut List Export', href: '/optimize/cutlist' },
      { label: 'Advanced Nesting', href: '/optimize/nesting' },
      { label: 'Scrap Tracker', href: '/optimize/scrap' },
      { label: 'Design Doctor', href: '/optimize/doctor' },
      { label: 'Cost Optimizer', href: '/optimize/cost' },
      { label: 'Board Yield', href: '/optimize/yield' },
    ],
  },
  {
    label: 'Export',
    href: '/export',
    icon: '📤',
    children: [
      { label: 'G-Code Export', href: '/export/gcode' },
      { label: '3D Export', href: '/export/3d' },
    ],
  },
  {
    label: 'Community',
    href: '/community',
    icon: '👥',
    children: [
      { label: 'Gallery', href: '/community/gallery' },
      { label: 'Brag Sheet', href: '/community/brag-sheet' },
    ],
  },
  {
    label: 'Tools',
    href: '/tools',
    icon: '🛠️',
    children: [
      { label: 'Local Suppliers', href: '/tools/localization' },
      { label: 'Store Integration', href: '/tools/stores' },
      { label: 'Scratch Build Calc', href: '/tools/scratch-build' },
      { label: 'Climate Adjustment', href: '/tools/climate' },
      { label: 'Version History', href: '/tools/history' },
    ],
  },
]

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null)
  const pathname = usePathname()

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-blue-600">Kerf</span>
              <span className="text-2xl font-light text-gray-600">OS</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <div
                key={item.href}
                className="relative"
                onMouseEnter={() => item.children && setActiveDropdown(item.label)}
                onMouseLeave={() => setActiveDropdown(null)}
              >
                <Link
                  href={item.href}
                  className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1 transition-colors ${
                    pathname === item.href || pathname.startsWith(item.href + '/')
                      ? 'text-blue-600 bg-blue-50'
                      : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                  {item.children && (
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  )}
                </Link>

                {/* Dropdown */}
                {item.children && activeDropdown === item.label && (
                  <div className="absolute left-0 mt-0 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50">
                    {item.children.map((child) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600"
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Right side - Auth */}
          <div className="hidden md:flex items-center space-x-4">
            <SignedIn>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
            <SignedOut>
              <SignInButton mode="modal">
                <button className="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700">
                  Sign In
                </button>
              </SignInButton>
              <Link
                href="/pricing"
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
              >
                Get Started
              </Link>
            </SignedOut>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navItems.map((item) => (
              <div key={item.href}>
                <Link
                  href={item.href}
                  className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.label}
                </Link>
                {item.children && (
                  <div className="ml-4 mt-1 space-y-1">
                    {item.children.map((child) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        className="block px-3 py-2 rounded-md text-sm text-gray-600 hover:text-blue-600 hover:bg-gray-50"
                        onClick={() => setMobileMenuOpen(false)}
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
            <div className="pt-4 border-t border-gray-200">
              <SignedIn>
                <div className="px-3 py-2">
                  <UserButton afterSignOutUrl="/" />
                </div>
              </SignedIn>
              <SignedOut>
                <SignInButton mode="modal">
                  <button className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50">
                    Sign In
                  </button>
                </SignInButton>
                <Link
                  href="/pricing"
                  className="block px-3 py-2 mt-2 text-center text-white bg-blue-600 rounded-md hover:bg-blue-700"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Get Started
                </Link>
              </SignedOut>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
