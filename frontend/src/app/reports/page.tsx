"use client";

import { AppLayout } from "@/components/layout/AppLayout";

export default function ReportsPage() {
  return (
    <AppLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Reports</h1>
        <div className="card text-center py-12">
          <p className="text-gray-500">
            Reports will appear here after running analysis on your deals.
          </p>
        </div>
      </div>
    </AppLayout>
  );
}
