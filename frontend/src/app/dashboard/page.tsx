"use client";

import { useEffect, useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { dashboardAPI, dealsAPI } from "@/lib/api";
import { DashboardStats, Deal } from "@/types";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { formatDate } from "@/lib/utils";
import Link from "next/link";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentDeals, setRecentDeals] = useState<Deal[]>([]);

  useEffect(() => {
    dashboardAPI.stats().then((r) => setStats(r.data));
    dealsAPI.list({ limit: 5 }).then((r) => setRecentDeals(r.data.deals));
  }, []);

  return (
    <AppLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { label: "Total Deals", value: stats?.total_deals ?? "-" },
            { label: "Active", value: stats?.active_deals ?? "-" },
            { label: "Completed", value: stats?.completed_deals ?? "-" },
            { label: "Avg Score", value: stats?.average_investment_score ?? "-" },
          ].map((s, i) => (
            <div key={i} className="card">
              <p className="text-sm text-gray-500">{s.label}</p>
              <p className="text-3xl font-bold mt-1">{s.value}</p>
            </div>
          ))}
        </div>

        {/* Recent Deals */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Recent Deals</h2>
            <Link href="/deals" className="text-brand-500 text-sm font-medium hover:underline">
              View All →
            </Link>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b">
                <th className="pb-2">Name</th>
                <th className="pb-2">Industry</th>
                <th className="pb-2">Stage</th>
                <th className="pb-2">Status</th>
                <th className="pb-2">Score</th>
                <th className="pb-2">Date</th>
              </tr>
            </thead>
            <tbody>
              {recentDeals.map((deal) => (
                <tr key={deal.id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="py-3">
                    <Link href={`/deals/${deal.id}`} className="font-medium text-brand-600 hover:underline">
                      {deal.name}
                    </Link>
                  </td>
                  <td className="py-3 text-gray-600">{deal.industry || "-"}</td>
                  <td className="py-3 text-gray-600">{deal.stage || "-"}</td>
                  <td className="py-3"><StatusBadge status={deal.status} /></td>
                  <td className="py-3 font-semibold">{deal.investment_score ?? "-"}</td>
                  <td className="py-3 text-gray-500">{formatDate(deal.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppLayout>
  );
}
