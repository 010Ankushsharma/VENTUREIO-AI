"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { AppLayout } from "@/components/layout/AppLayout";
import { dealsAPI, documentsAPI, analysisAPI, reportsAPI } from "@/lib/api";
import { Deal, Document, Analysis } from "@/types";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { FileUpload } from "@/components/ui/FileUpload";

export default function DealDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [deal, setDeal] = useState<Deal | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    if (!id) return;
    dealsAPI.get(id).then((r) => setDeal(r.data));
    documentsAPI.list(id).then((r) => setDocuments(r.data));
    analysisAPI.list(id).then((r) => setAnalyses(r.data));
  }, [id]);

  const triggerAnalysis = async () => {
    await analysisAPI.trigger(id);
    // Poll for updates
    const interval = setInterval(async () => {
      const res = await analysisAPI.list(id);
      setAnalyses(res.data);
      const allDone = res.data.every((a: Analysis) => a.status !== "pending" && a.status !== "running");
      if (allDone) clearInterval(interval);
    }, 3000);
  };

  const generateReport = async () => {
    await reportsAPI.generate(id);
  };

  if (!deal) return <AppLayout><p>Loading...</p></AppLayout>;

  const tabs = ["overview", "documents", "analysis", "report"];

  return (
    <AppLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">{deal.name}</h1>
            <div className="flex gap-3 mt-1 text-sm text-gray-500">
              {deal.industry && <span>{deal.industry}</span>}
              {deal.stage && <span>• {deal.stage}</span>}
              <StatusBadge status={deal.status} />
            </div>
          </div>
          <div className="flex gap-3">
            <button onClick={triggerAnalysis} className="btn-primary">
              🤖 Run AI Analysis
            </button>
            <button onClick={generateReport} className="btn-secondary">
              📄 Generate Report
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 border-b">
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab
                  ? "border-brand-500 text-brand-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === "overview" && (
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="font-semibold mb-3">Company Info</h3>
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between"><dt className="text-gray-500">Industry</dt><dd>{deal.industry || "-"}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Stage</dt><dd>{deal.stage || "-"}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Business Model</dt><dd>{deal.business_model || "-"}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Country</dt><dd>{deal.country || "-"}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Website</dt><dd>{deal.website || "-"}</dd></div>
              </dl>
            </div>
            <div className="card">
              <h3 className="font-semibold mb-3">Investment Score</h3>
              <div className="text-center py-8">
                <span className="text-5xl font-bold">{deal.investment_score ?? "—"}</span>
                <span className="text-2xl text-gray-400"> / 100</span>
              </div>
              {deal.recommendation && (
                <div className="text-center">
                  <span className={`badge text-base px-4 py-1 ${
                    deal.recommendation === "INVEST" ? "bg-green-100 text-green-800" :
                    deal.recommendation === "CONDITIONAL_INVEST" ? "bg-yellow-100 text-yellow-800" :
                    "bg-red-100 text-red-800"
                  }`}>
                    {deal.recommendation.replace("_", " ")}
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "documents" && (
          <div className="space-y-6">
            <FileUpload dealId={id} onUploadComplete={() => documentsAPI.list(id).then((r) => setDocuments(r.data))} />
            <div className="card">
              <h3 className="font-semibold mb-3">Uploaded Documents ({documents.length})</h3>
              {documents.length === 0 ? (
                <p className="text-gray-500 text-sm">No documents uploaded yet.</p>
              ) : (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-500 border-b">
                      <th className="pb-2">File</th>
                      <th className="pb-2">Category</th>
                      <th className="pb-2">Type</th>
                      <th className="pb-2">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {documents.map((doc) => (
                      <tr key={doc.id} className="border-b last:border-0">
                        <td className="py-2">{doc.filename}</td>
                        <td className="py-2 text-gray-600">{doc.document_category}</td>
                        <td className="py-2 text-gray-600">.{doc.file_type}</td>
                        <td className="py-2"><StatusBadge status={doc.processing_status} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {activeTab === "analysis" && (
          <div className="space-y-4">
            {analyses.length === 0 ? (
              <div className="card text-center py-12">
                <p className="text-gray-500 mb-4">No analysis run yet.</p>
                <button onClick={triggerAnalysis} className="btn-primary">🤖 Run AI Analysis</button>
              </div>
            ) : (
              analyses.map((a) => (
                <div key={a.id} className="card">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">{a.agent_type.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}</h3>
                    <div className="flex items-center gap-3">
                      {a.score != null && <span className="text-lg font-bold">{a.score}/100</span>}
                      <StatusBadge status={a.status} />
                    </div>
                  </div>
                  {a.summary && <p className="text-sm text-gray-600 mt-2">{a.summary}</p>}
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === "report" && (
          <div className="card text-center py-12">
            <p className="text-gray-500 mb-4">Generate a full due diligence report after running analysis.</p>
            <button onClick={generateReport} className="btn-primary">📄 Generate Report</button>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
