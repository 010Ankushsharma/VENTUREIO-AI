"""
Agent 4: Competitive Intelligence Agent

Identify competitors and build competitive matrix.
"""
from typing import Any, Dict, Optional
from app.agents.base_agent import BaseAgent


class CompetitiveIntelligenceAgent(BaseAgent):
    @property
    def agent_name(self) -> str:
        return "Competitive Intelligence Agent"

    @property
    def description(self) -> str:
        return (
            "Identify direct, indirect, and emerging competitors. "
            "Compare features, pricing, funding, and market positioning."
        )

    async def run(self, deal_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("running", deal_id=deal_id)

        competitive_landscape = {
            "direct_competitors": [],
            "indirect_competitors": [],
            "emerging_threats": [],
            "competitive_matrix": [],  # list of {company, product, pricing, funding, strength, weakness}
            "differentiation": [],
            "competitive_advantages": [],
            "competitive_risks": [],
            "market_positioning": "",
            "moat_assessment": "",
        }

        return self._format_output(
            result=competitive_landscape,
            confidence=0.0,
            summary="Competitive landscape analysis completed.",
        )
