"""
Agent 1: Startup Understanding Agent

Extracts and structures the startup's profile from uploaded documents.
"""
from typing import Any, Dict, Optional

from app.agents.base_agent import BaseAgent


class StartupUnderstandingAgent(BaseAgent):
    @property
    def agent_name(self) -> str:
        return "Startup Understanding Agent"

    @property
    def description(self) -> str:
        return (
            "Analyze uploaded documents to build a comprehensive startup profile. "
            "Extract business model, value proposition, target market, revenue model, "
            "team info, traction metrics, and funding requirements."
        )

    async def run(self, deal_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info("running", deal_id=deal_id)

        # TODO: Fetch documents from DB/storage for this deal
        # TODO: Process pitch deck, website, etc.
        # TODO: Call LLM with structured extraction prompt

        # Placeholder structured output
        profile = {
            "company_name": "",
            "industry": "",
            "sub_industry": "",
            "business_model": "",  # B2B SaaS, B2C, Marketplace, etc.
            "revenue_model": "",  # Subscription, Transaction fee, etc.
            "stage": "",  # Pre-seed, Seed, Series A, etc.
            "target_market": "",
            "value_proposition": "",
            "founding_date": "",
            "headquarters": "",
            "team": {
                "founders": [],
                "team_size": 0,
                "key_hires": [],
            },
            "traction": {
                "revenue": None,
                "mrr": None,
                "arr": None,
                "users": None,
                "growth_rate": None,
                "customers": None,
            },
            "funding": {
                "total_raised": None,
                "current_round": None,
                "ask_amount": None,
                "valuation_cap": None,
            },
            "product": {
                "description": "",
                "key_features": [],
                "tech_stack": [],
                "ip_assets": [],
            },
        }

        return self._format_output(
            result=profile,
            confidence=0.0,
            summary="Startup profile extracted from uploaded documents.",
        )
