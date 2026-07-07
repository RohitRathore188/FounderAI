from app.agents.base import BaseAgent
from app.schemas.responses import DiscoveryData
from typing import Dict, Any

class DiscoveryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="discovery_agent",
            response_schema=DiscoveryData,
            prompt_file="discovery.txt"
        )

    def run(self, startup_info: Dict[str, Any]) -> Dict[str, Any]:
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
            "problem_statement": startup_info.get("problem_statement", startup_info.get("idea", "")),
            "business_stage": startup_info.get("business_stage", startup_info.get("stage", ""))
        }
        
        data = self.invoke_llm(variables)
        
        summary = f"Startup summary problem: {data.problem[:60]}. Industry: {data.industry}."
        return self.create_response_payload(summary, data)
