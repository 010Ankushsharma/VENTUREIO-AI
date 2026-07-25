// ============================================================
// VentureIQ AI — TypeScript Type Definitions
// ============================================================

export interface User {
  id: string;
  email: string;
  full_name: string;
  organization?: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Deal {
  id: string;
  name: string;
  description?: string;
  industry?: string;
  stage?: string;
  business_model?: string;
  country?: string;
  website?: string;
  funding_ask?: number;
  status: "pending" | "in_progress" | "completed" | "archived";
  investment_score?: number;
  recommendation?: "INVEST" | "CONDITIONAL_INVEST" | "DO_NOT_INVEST";
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  deal_id: string;
  filename: string;
  file_type: string;
  document_category: string;
  storage_path: string;
  file_size?: number;
  processing_status: string;
  created_at: string;
}

export interface Analysis {
  id: string;
  deal_id: string;
  agent_type: string;
  status: string;
  result?: Record<string, any>;
  score?: number;
  confidence?: number;
  summary?: string;
  evidence?: Record<string, any>;
  created_at: string;
}

export interface Report {
  id: string;
  deal_id: string;
  report_type: string;
  title: string;
  content?: string;
  sections?: Record<string, any>;
  recommendation?: string;
  file_path?: string;
  created_at: string;
}

export interface DashboardStats {
  total_deals: number;
  active_deals: number;
  completed_deals: number;
  average_investment_score?: number;
}

export interface ScoringBreakdown {
  team: { score: number; weight: number; weighted_score: number };
  product: { score: number; weight: number; weighted_score: number };
  market: { score: number; weight: number; weighted_score: number };
  traction: { score: number; weight: number; weighted_score: number };
  financial_health: { score: number; weight: number; weighted_score: number };
  risk_profile: { score: number; weight: number; weighted_score: number };
}
