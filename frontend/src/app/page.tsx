import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-brand-900 to-gray-900 text-white">
      {/* Nav */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="text-2xl font-bold tracking-tight">
          Venture<span className="text-brand-500">IQ</span> AI
        </div>
        <div className="flex gap-4">
          <Link href="/auth" className="btn-secondary !text-white !bg-white/10 hover:!bg-white/20">
            Login
          </Link>
          <Link href="/auth" className="btn-primary">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-4xl mx-auto text-center py-24 px-4">
        <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
          AI-Powered <br />
          <span className="text-brand-500">Due Diligence</span> Platform
        </h1>
        <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
          Evaluate startups in hours, not weeks. Comprehensive investment analysis
          powered by 8 specialized AI agents.
        </p>
        <Link href="/auth" className="btn-primary text-lg px-8 py-3">
          Start Analyzing →
        </Link>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-4 pb-24 grid md:grid-cols-3 gap-8">
        {[
          { title: "Document Intelligence", desc: "Upload pitch decks, financials, cap tables — AI extracts everything." },
          { title: "8 AI Agents", desc: "Financial, market, competitive, risk, fraud, valuation analysis in parallel." },
          { title: "Investment Memos", desc: "Auto-generated institutional-grade due diligence reports." },
        ].map((f, i) => (
          <div key={i} className="card !bg-white/5 !border-white/10">
            <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
            <p className="text-gray-400 text-sm">{f.desc}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
