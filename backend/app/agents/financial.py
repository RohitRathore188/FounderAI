from app.agents.base import BaseAgent
from app.schemas.responses import FinancialData
from typing import Dict, Any

class FinancialPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="financial_planning_agent",
            response_schema=FinancialData,
            prompt_file="financial.txt"
        )

    def run(self, startup_info: Dict[str, Any], discovery_summary: str, business_model_summary: str) -> Dict[str, Any]:
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
            "business_model_summary": business_model_summary
        }
        
        data = self.invoke_llm(variables)
        
        summary = f"Monthly Burn: {data.monthly_burn}. Runway: {data.runway}. Break-even: {data.break_even}."
        return self.create_response_payload(summary, data)
