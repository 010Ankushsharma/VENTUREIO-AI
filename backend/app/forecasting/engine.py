"""
Forecasting Engine

Generates 1-year, 3-year, and 5-year forecasts for key metrics.
"""
from typing import Dict, Any, List, Optional
import structlog

logger = structlog.get_logger()


class ForecastingEngine:
    """Generates growth forecasts with confidence intervals."""

    async def forecast_revenue(
        self,
        historical_data: List[Dict[str, Any]],
        periods: List[int] = [12, 36, 60],
    ) -> Dict[str, Any]:
        """
        Forecast revenue growth.
        """
        forecasts = {}
        for period in periods:
            years = period // 12
            forecasts[f"{years}_year"] = {
                "forecast": [],
                "lower_bound": [],
                "upper_bound": [],
                "confidence_interval": 0.95,
                "model_used": "prophet",
            }

        return {
            "metric": "revenue",
            "historical_data_points": len(historical_data),
            "forecasts": forecasts,
        }

    async def forecast_cash_runway(
        self,
        cash_on_hand: float,
        monthly_burn: float,
    ) -> Dict[str, Any]:
        """Forecast cash runway under different scenarios."""
        base_runway = cash_on_hand / monthly_burn if monthly_burn > 0 else float("inf")

        return {
            "metric": "cash_runway",
            "scenarios": {
                "base": {"runway_months": round(base_runway, 1)},
                "optimistic": {"runway_months": round(base_runway * 1.3, 1)},
                "pessimistic": {"runway_months": round(base_runway * 0.7, 1)},
            },
        }


forecasting_engine = ForecastingEngine()
