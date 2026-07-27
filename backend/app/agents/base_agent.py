"""
Base agent class — all agents inherit from this.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import structlog

from app.core.config import settings


class BaseAgent(ABC):
    """Base class for all due diligence agents."""

    def __init__(self):
        self.logger = structlog.get_logger(agent=self.agent_name)

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Unique name for this agent."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """What this agent does."""
        pass

    @abstractmethod
    async def run(self, deal_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the agent's analysis."""
        pass

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the LLM."""
        return f"""You are {self.agent_name}, a specialized AI analyst for investment due diligence.

Your role: {self.description}

Guidelines:
- Provide evidence-based analysis with source references.
- Assign confidence scores (0.0 to 1.0) to every conclusion.
- Flag uncertainties explicitly.
- Use structured JSON output.
- Never fabricate data — state when information is missing.
"""

    def _format_output(
        self,
        result: Dict[str, Any],
        score: Optional[float] = None,
        confidence: Optional[float] = None,
        summary: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "agent": self.agent_name,
            "result": result,
            "score": score,
            "confidence": confidence,
            "summary": summary,
        }
