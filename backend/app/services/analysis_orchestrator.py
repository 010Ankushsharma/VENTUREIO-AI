"""
Analysis Orchestrator — Runs the multi-agent due diligence pipeline.

Uses LangGraph to orchestrate 8 specialized agents in a DAG:

    ┌─────────────────────────┐
    │  Document Processing    │
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────┐
    │ Startup Understanding   │  (Agent 1)
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────────────────────────────┐
    │            Parallel Execution                    │
    │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
    │  │Financial │ │ Market   │ │ Competitive      │ │
    │  │ Agent 2  │ │ Agent 3  │ │ Agent 4          │ │
    │  └──────────┘ └──────────┘ └──────────────────┘ │
    └────────────┬────────────────────────────────────┘
                 │
    ┌────────────▼────────────────────────┐
    │        Parallel Execution           │
    │  ┌──────────┐ ┌──────────────────┐  │
    │  │  Risk    │ │ Fraud Detection  │  │
    │  │ Agent 5  │ │ Agent 6          │  │
    │  └──────────┘ └──────────────────┘  │
    └────────────┬────────────────────────┘
                 │
    ┌────────────▼────────────┐
    │ Valuation Agent 7       │
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────┐
    │ Investment Rec Agent 8  │
    └─────────────────────────┘
"""
import asyncio
import structlog
from typing import List

from app.agents.startup_understanding import StartupUnderstandingAgent
from app.agents.financial_analysis import FinancialAnalysisAgent
from app.agents.market_intelligence import MarketIntelligenceAgent
from app.agents.competitive_intelligence import CompetitiveIntelligenceAgent
from app.agents.risk_assessment import RiskAssessmentAgent
from app.agents.fraud_detection import FraudDetectionAgent
from app.agents.valuation import ValuationAgent
from app.agents.investment_recommendation import InvestmentRecommendationAgent

logger = structlog.get_logger()

AGENT_MAP = {
    "startup_understanding": StartupUnderstandingAgent,
    "financial": FinancialAnalysisAgent,
    "market_intelligence": MarketIntelligenceAgent,
    "competitive_intelligence": CompetitiveIntelligenceAgent,
    "risk_assessment": RiskAssessmentAgent,
    "fraud_detection": FraudDetectionAgent,
    "valuation": ValuationAgent,
    "investment_recommendation": InvestmentRecommendationAgent,
}


async def run_due_diligence(deal_id: str, agent_types: List[str]):
    """
    Execute the full due-diligence pipeline for a deal.
    """
    logger.info("due_diligence_started", deal_id=deal_id, agents=agent_types)

    context = {"deal_id": deal_id, "results": {}}

    try:
        # Phase 1: Startup Understanding
        if "startup_understanding" in agent_types:
            agent = StartupUnderstandingAgent()
            context["results"]["startup_understanding"] = await agent.run(deal_id)

        # Phase 2: Parallel — Financial, Market, Competitive
        phase2 = []
        if "financial" in agent_types:
            phase2.append(("financial", FinancialAnalysisAgent().run(deal_id, context)))
        if "market_intelligence" in agent_types:
            phase2.append(("market_intelligence", MarketIntelligenceAgent().run(deal_id, context)))
        if "competitive_intelligence" in agent_types:
            phase2.append(("competitive_intelligence", CompetitiveIntelligenceAgent().run(deal_id, context)))

        if phase2:
            results = await asyncio.gather(*[t[1] for t in phase2], return_exceptions=True)
            for (name, _), result in zip(phase2, results):
                if isinstance(result, Exception):
                    logger.error("agent_failed", agent=name, error=str(result))
                    context["results"][name] = {"error": str(result)}
                else:
                    context["results"][name] = result

        # Phase 3: Risk + Fraud
        phase3 = []
        if "risk_assessment" in agent_types:
            phase3.append(("risk_assessment", RiskAssessmentAgent().run(deal_id, context)))
        if "fraud_detection" in agent_types:
            phase3.append(("fraud_detection", FraudDetectionAgent().run(deal_id, context)))

        if phase3:
            results = await asyncio.gather(*[t[1] for t in phase3], return_exceptions=True)
            for (name, _), result in zip(phase3, results):
                if isinstance(result, Exception):
                    logger.error("agent_failed", agent=name, error=str(result))
                    context["results"][name] = {"error": str(result)}
                else:
                    context["results"][name] = result

        # Phase 4: Valuation
        if "valuation" in agent_types:
            agent = ValuationAgent()
            context["results"]["valuation"] = await agent.run(deal_id, context)

        # Phase 5: Final Recommendation
        if "investment_recommendation" in agent_types:
            agent = InvestmentRecommendationAgent()
            context["results"]["investment_recommendation"] = await agent.run(deal_id, context)

        logger.info("due_diligence_completed", deal_id=deal_id)

        # TODO: persist results back to DB
        return context

    except Exception as e:
        logger.error("due_diligence_failed", deal_id=deal_id, error=str(e))
        raise
