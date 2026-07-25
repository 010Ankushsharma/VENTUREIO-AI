import { useState, useEffect, useCallback } from "react";
import { dealsAPI } from "@/lib/api";
import { Deal } from "@/types";

export function useDeals() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDeals = useCallback(async (params?: { status?: string }) => {
    setLoading(true);
    try {
      const res = await dealsAPI.list(params);
      setDeals(res.data.deals);
      setTotal(res.data.total);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDeals();
  }, [fetchDeals]);

  return { deals, total, loading, error, refetch: fetchDeals };
}
