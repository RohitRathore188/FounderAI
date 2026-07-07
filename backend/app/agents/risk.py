from app.agents.base import BaseAgent
from app.schemas.responses import RiskData
from typing import Dict, Any

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="risk_agent",
            response_schema=RiskData,
            prompt_file="risk.txt"
        )

    def run(self, startup_info: Dict[str, Any], discovery_summary: str, financial_summary: str, legal_summary: str) -> Dict[str, Any]:
        variables = {
            "idea": startup_info.get("idea", ""),
            "industry": startup_info.get("industry", ""),
            "country": startup_info.get("country", ""),
            "state": startup_info.get("state", ""),
            "district": startup_info.get("district", ""),
            "location_context": startup_info.get("location_context", startup_info.get("country", "")),
            "budget": startup_info.get("budget", ""),
            "stage": startup_info.get("stage", ""),
            "founder_name": startup_info.get("founder_name", ""),
            "target_market": startup_info.get("target_market", ""),
            "team_size": startup_info.get("team_size", "1"),
            "customer_segment": startup_info.get("customer_segment", startup_info.get("target_market", "")),
            "discovery_summary": discovery_summary,
            "financial_summary": financial_summary,
            "legal_summary": legal_summary
        }
        
        data = self.invoke_llm(variables)
        
        summary = f"Risk assessment compiled. Mitigation strategy count: {len(data.mitigation)}."
        return self.create_response_payload(summary, data)
