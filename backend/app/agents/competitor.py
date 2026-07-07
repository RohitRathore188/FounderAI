from app.agents.base import BaseAgent
from app.schemas.responses import CompetitorData
from typing import Dict, Any

class CompetitorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="competitor_agent",
            response_schema=CompetitorData,
            prompt_file="competitor.txt"
        )

    def run(self, startup_info: Dict[str, Any], discovery_summary: str, market_summary: str) -> Dict[str, Any]:
        print(f"\n[COMPETITOR AGENT] startup_info received: {startup_info}")
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
            "market_summary": market_summary
        }
        
        data = self.invoke_llm(variables)
        
        comp_names = [c.name for c in data.real_competitors]
        summary = f"Competitors: {', '.join(comp_names[:2])}. Gap: {data.gap_analysis[:60]}."
        return self.create_response_payload(summary, data)
