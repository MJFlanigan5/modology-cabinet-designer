import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Terms of Service | KerfOS',
  description: 'KerfOS terms of service - Rules and guidelines for using our service.',
}

export default async function TermsPage() {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/gdpr/terms-of-service`, {
    cache: 'no-store',
  })
  const terms = await response.json()

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{terms.title}</h1>
          <p className="text-sm text-gray-500 mb-8">
            Last updated: {terms.last_updated} | Version {terms.version}
          </p>

          <div className="prose prose-blue max-w-none">
            {/* Sections */}
            {terms.sections?.map((section: { title: string; content: string }, index: number) => (
              <div key={index} className="mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">{section.title}</h2>
                <p className="text-gray-600 leading-relaxed">{section.content}</p>
              </div>
            ))}

            {/* Highlights */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-8">
              <div className="bg-green-50 rounded-lg p-6">
                <h3 className="font-semibold text-green-900 mb-2">✓ You Own Your Designs</h3>
                <p className="text-sm text-green-700">
                  All cabinet designs and projects you create in KerfOS are your intellectual property.
                </p>
              </div>
              <div className="bg-blue-50 rounded-lg p-6">
                <h3 className="font-semibold text-blue-900 mb-2">🔒 Your Data is Protected</h3>
                <p className="text-sm text-blue-700">
                  We use industry-standard security to protect your information.
                </p>
              </div>
              <div className="bg-purple-50 rounded-lg p-6">
                <h3 className="font-semibold text-purple-900 mb-2">💳 Cancel Anytime</h3>
                <p className="text-sm text-purple-700">
                  No long-term contracts. Cancel your subscription at any time.
                </p>
              </div>
              <div className="bg-orange-50 rounded-lg p-6">
                <h3 className="font-semibold text-orange-900 mb-2">📧 Contact Us</h3>
                <p className="text-sm text-orange-700">
                  Questions? Email us at support@kerfos.com
                </p>
              </div>
            </div>

            {/* Footer */}
            <div className="border-t pt-6">
              <p className="text-sm text-gray-500">
                By using KerfOS, you agree to these terms. If you do not agree, please do not use our service.
              </p>
              <div className="mt-4 flex gap-4 text-sm">
                <Link href="/privacy" className="text-blue-600 hover:underline">
                  Privacy Policy
                </Link>
                <Link href="/cookies" className="text-blue-600 hover:underline">
                  Cookie Policy
                </Link>
                <Link href="/gdpr" className="text-blue-600 hover:underline">
                  GDPR Rights
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
