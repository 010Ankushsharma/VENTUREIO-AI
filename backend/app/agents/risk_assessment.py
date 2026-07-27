"""
Agent 5: Risk Assessment Agent

Identifies operational, regulatory, market, founder, and financial risks.
"""
from typing import Any, Dict, Optional
from app.agents.base_agent import BaseAgent


class RiskAssessmentAgent(BaseAgent):
    @property
    def agent_name(self) -> str:
        return "Risk Assessment Agent"

    @property
    def description(self) -> str:
        return (
            "Identify and categorize all risks: operational, regulatory, market, "
            "founder, financial, and execution risks. Generate a risk matrix."
        )

    async def run(self, deal_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("running", deal_id=deal_id)

        risk_assessment = {
            "risk_matrix": [],  # [{category, risk, severity, likelihood, impact, mitigation}]
            "operational_risks": [],
            "regulatory_risks": [],
            "market_risks": [],
            "financial_risks": [],
            "founder_risks": [],
            "execution_risks": [],
            "technology_risks": [],
            "overall_risk_level": "",  # LOW, MEDIUM, HIGH, CRITICAL
            "risk_score": None,  # 0-100 (lower = less risky)
            "key_risk_factors": [],
            "risk_mitigants": [],
        }

        return self._format_output(
            result=risk_assessment,
            score=None,
            confidence=0.0,
            summary="Risk assessment completed.",
        )
