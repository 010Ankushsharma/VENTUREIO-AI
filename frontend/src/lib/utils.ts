import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function getScoreColor(score: number): string {
  if (score >= 80) return "text-green-600";
  if (score >= 60) return "text-yellow-600";
  if (score >= 40) return "text-orange-600";
  return "text-red-600";
}

export function getRecommendationColor(rec: string): string {
  switch (rec) {
    case "INVEST": return "bg-green-100 text-green-800";
    case "CONDITIONAL_INVEST": return "bg-yellow-100 text-yellow-800";
    case "DO_NOT_INVEST": return "bg-red-100 text-red-800";
    default: return "bg-gray-100 text-gray-800";
  }
}
