"use client";

import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { useDeals } from "@/hooks/useDeals";
import { dealsAPI } from "@/lib/api";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { formatDate } from "@/lib/utils";
import Link from "next/link";

export default function DealsPage() {
  const { deals, total, loading, refetch } = useDeals();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: "", industry: "", stage: "", description: "" });

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await dealsAPI.create(form);
    setShowForm(false);
    setForm({ name: "", industry: "", stage: "", description: "" });
    refetch();
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Deals ({total})</h1>
          <button onClick={() => setShowForm(true)} className="btn-primary">
            + New Deal
          </button>
        </div>

        {/* Create Form */}
        {showForm && (
          <div className="card">
            <h2 className="text-lg font-semibold mb-4">Create New Deal</h2>
            <form onSubmit={handleCreate} className="grid md:grid-cols-2 gap-4">
              <input
                placeholder="Company Name *"
                className="input"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
              <select
                className="input"
                value={form.industry}
                onChange={(e) => setForm({ ...form, industry: e.target.value })}
              >
                <option value="">Select Industry</option>
                {["FinTech", "HealthTech", "EdTech", "SaaS", "E-Commerce", "AI/ML",
                  "CleanTech", "BioTech", "PropTech", "InsurTech", "Other"].map((i) => (
                  <option key={i} value={i}>{i}</option>
                ))}
              </select>
              <select
                className="input"
                value={form.stage}
                onChange={(e) => setForm({ ...form, stage: e.target.value })}
              >
                <option value="">Select Stage</option>
                {["Pre-Seed", "Seed", "Series A", "Series B", "Series C+", "Growth", "Pre-IPO"].map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
              <input
                placeholder="Description"
                className="input"
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
              />
              <div className="md:col-span-2 flex gap-3">
                <button type="submit" className="btn-primary">Create</button>
                <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
              </div>
            </form>
          </div>
        )}

        {/* Deals Table */}
        <div className="card">
          {loading ? (
            <p className="text-gray-500">Loading...</p>
          ) : deals.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No deals yet. Create your first deal above.</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2">Company</th>
                  <th className="pb-2">Industry</th>
                  <th className="pb-2">Stage</th>
                  <th className="pb-2">Status</th>
                  <th className="pb-2">Score</th>
                  <th className="pb-2">Recommendation</th>
                  <th className="pb-2">Created</th>
                </tr>
              </thead>
              <tbody>
                {deals.map((deal) => (
                  <tr key={deal.id} className="border-b last:border-0 hover:bg-gray-50">
                    <td className="py-3">
                      <Link href={`/deals/${deal.id}`} className="font-medium text-brand-600 hover:underline">
                        {deal.name}
                      </Link>
                    </td>
                    <td className="py-3 text-gray-600">{deal.industry || "-"}</td>
                    <td className="py-3 text-gray-600">{deal.stage || "-"}</td>
                    <td className="py-3"><StatusBadge status={deal.status} /></td>
                    <td className="py-3 font-bold">{deal.investment_score ?? "-"}</td>
                    <td className="py-3">
                      {deal.recommendation ? (
                        <span className={`badge ${
                          deal.recommendation === "INVEST" ? "bg-green-100 text-green-800" :
                          deal.recommendation === "CONDITIONAL_INVEST" ? "bg-yellow-100 text-yellow-800" :
                          "bg-red-100 text-red-800"
                        }`}>
                          {deal.recommendation.replace("_", " ")}
                        </span>
                      ) : "-"}
                    </td>
                    <td className="py-3 text-gray-500">{formatDate(deal.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
