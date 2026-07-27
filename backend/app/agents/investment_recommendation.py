"""
Agent 8: Investment Recommendation Agent

Synthesizes all agent outputs into a final investment recommendation.
"""
from typing import Any, Dict, Optional
from app.agents.base_agent import BaseAgent


SCORING_WEIGHTS = {
    "team": 0.20,
    "product": 0.15,
    "market": 0.20,
    "traction": 0.20,
    "financial_health": 0.15,
    "risk_profile": 0.10,
}


class InvestmentRecommendationAgent(BaseAgent):
    @property
    def agent_name(self) -> str:
        return "Investment Recommendation Agent"

    @property
    def description(self) -> str:
        return (
            "Combine findings from all agents to produce a final investment "
            "recommendation with an investment score (0-100)."
        )

    async def run(self, deal_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("running", deal_id=deal_id)

        # TODO: Pull scores from all other agents in context
        # TODO: Apply weighted scoring framework
        # TODO: Generate final recommendation via LLM

        recommendation = {
            "investment_score": None,  # 0-100
            "recommendation": "",  # INVEST, CONDITIONAL_INVEST, DO_NOT_INVEST
            "scoring_breakdown": {
                "team": {"score": None, "weight": 0.20, "weighted_score": None},
                "product": {"score": None, "weight": 0.15, "weighted_score": None},
                "market": {"score": None, "weight": 0.20, "weighted_score": None},
                "traction": {"score": None, "weight": 0.20, "weighted_score": None},
                "financial_health": {"score": None, "weight": 0.15, "weighted_score": None},
                "risk_profile": {"score": None, "weight": 0.10, "weighted_score": None},
            },
            "key_strengths": [],
            "key_concerns": [],
            "conditions": [],  # conditions for CONDITIONAL_INVEST
            "deal_breakers": [],
            "executive_summary": "",
            "confidence": 0.0,
            "evidence_sources": [],
        }

        return self._format_output(
            result=recommendation,
            score=None,
            confidence=0.0,
            summary="Investment recommendation generated.",
        )
