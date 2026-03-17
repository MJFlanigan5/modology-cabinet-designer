export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-center font-mono text-sm">
        <h1 className="text-6xl font-bold mb-4 text-modology-600">
          Modology Cabinet Designer
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered cabinet design tool with cut list generation and hardware sourcing.
        </p>
        <div className="flex gap-4">
          <button className="px-6 py-3 bg-modology-500 text-white rounded-lg hover:bg-modology-600 transition-colors">
            Start Designing
          </button>
          <button className="px-6 py-3 border-2 border-modology-500 text-modology-500 rounded-lg hover:bg-modology-50 transition-colors">
            View Demo
          </button>
        </div>
      </div>
    </main>
  )
}