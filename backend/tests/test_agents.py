import pytest
from pydantic import BaseModel
from app.agents.base import BaseAgent
from app.agents import (
    DiscoveryAgent,
    ValidationAgent,
    MarketAgent,
    CompetitorAgent,
    BusinessModelAgent,
    FinancialPlanningAgent,
    LegalAgent,
    FundingAgent,
    RoadmapAgent,
    RiskAgent
)

class DummyResponse(BaseModel):
    answer: str

class DummyAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="dummy_agent", response_schema=DummyResponse, prompt_file="discovery.txt")


def test_prompt_build_includes_full_context_instruction():
    agent = DummyAgent()
    prompt = agent.build_prompt({
        "idea": "A climate fintech app",
        "industry": "Fintech",
        "country": "India",
        "state": "Karnataka",
        "district": "Bengaluru",
        "budget": "$10000",
        "stage": "MVP",
        "founder_name": "Asha",
        "target_market": "Freelancers"
    })

    assert "every supplied field" in prompt.lower()
    assert "must materially influence" in prompt.lower()

@pytest.fixture
def startup_info():
    return {
        "idea": "An AI-powered automated code reviews SaaS utility for developers",
        "industry": "Software / AI",
        "country": "India",
        "budget": "INR 50,000",
        "stage": "MVP",
        "founder_name": "Devin",
        "target_market": "Independent Developers and Tech Teams",
        "state": "Karnataka",
        "team_size": "2"
    }

def test_discovery_agent(startup_info):
    agent = DiscoveryAgent()
    res = agent.run(startup_info)
    
    assert res["status"] == "success"
    assert res["agent"] == "discovery_agent"
    assert "data" in res
    data = res["data"]
    assert "problem" in data
    assert "solution" in data
    assert "customer" in data
    assert "pain_points" in data
    assert "industry" in data
    assert "business_model" in data
    assert "confidence" in data

def test_market_agent(startup_info):
    discovery_res = DiscoveryAgent().run(startup_info)
    agent = MarketAgent()
    res = agent.run(startup_info, discovery_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "market_agent"
    assert "data" in res
    data = res["data"]
    assert "industry_specific_market" in data
    assert "TAM" in data
    assert "SAM" in data
    assert "SOM" in data
    assert "market_trends" in data
    assert "sources" in data

def test_competitor_agent(startup_info):
    discovery_res = DiscoveryAgent().run(startup_info)
    market_res = MarketAgent().run(startup_info, discovery_res.get("summary", ""))
    
    agent = CompetitorAgent()
    res = agent.run(startup_info, discovery_res.get("summary", ""), market_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "competitor_agent"
    assert "data" in res
    data = res["data"]
    assert "real_competitors" in data
    assert "pricing" in data
    assert "strengths" in data
    assert "weaknesses" in data
    assert "gap_analysis" in data

def test_business_model_agent(startup_info):
    discovery_res = DiscoveryAgent().run(startup_info)
    market_res = MarketAgent().run(startup_info, discovery_res.get("summary", ""))
    
    agent = BusinessModelAgent()
    res = agent.run(startup_info, discovery_res.get("summary", ""), market_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "business_model_agent"
    assert "data" in res
    data = res["data"]
    assert "customer_segments" in data
    assert "channels" in data
    assert "key_partners" in data
    assert "key_resources" in data
    assert "activities" in data
    assert "value_proposition" in data
    assert "revenue_model" in data
    assert "pricing_strategy" in data

def test_financial_planning_agent(startup_info):
    d_res = DiscoveryAgent().run(startup_info)
    bm_res = BusinessModelAgent().run(startup_info, d_res.get("summary", ""), MarketAgent().run(startup_info, d_res.get("summary", "")).get("summary", ""))
    
    agent = FinancialPlanningAgent()
    res = agent.run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "financial_planning_agent"
    assert "data" in res
    data = res["data"]
    assert "monthly_burn" in data
    assert "runway" in data
    assert "cash_flow" in data
    assert "expenses" in data
    assert "revenue_projection" in data
    assert "break_even" in data

def test_legal_agent(startup_info):
    d_res = DiscoveryAgent().run(startup_info)
    m_res = MarketAgent().run(startup_info, d_res.get("summary", ""))
    bm_res = BusinessModelAgent().run(startup_info, d_res.get("summary", ""), m_res.get("summary", ""))
    fin_res = FinancialPlanningAgent().run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""))
    
    agent = LegalAgent()
    res = agent.run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""), fin_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "legal_agent"
    assert "data" in res
    data = res["data"]
    assert "country_specific_requirements" in data
    assert "licenses" in data
    assert "taxes" in data
    assert "entity_type" in data
    assert "compliance" in data

def test_funding_agent(startup_info):
    d_res = DiscoveryAgent().run(startup_info)
    m_res = MarketAgent().run(startup_info, d_res.get("summary", ""))
    bm_res = BusinessModelAgent().run(startup_info, d_res.get("summary", ""), m_res.get("summary", ""))
    fin_res = FinancialPlanningAgent().run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""))
    
    agent = FundingAgent()
    res = agent.run(startup_info, d_res.get("summary", ""), fin_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "funding_agent"
    assert "data" in res
    data = res["data"]
    assert "recommended_funding" in data
    assert "recommended_investors" in data
    assert "bootstrap_strategy" in data

def test_roadmap_agent(startup_info):
    d_res = DiscoveryAgent().run(startup_info)
    m_res = MarketAgent().run(startup_info, d_res.get("summary", ""))
    bm_res = BusinessModelAgent().run(startup_info, d_res.get("summary", ""), m_res.get("summary", ""))
    fin_res = FinancialPlanningAgent().run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""))
    
    agent = RoadmapAgent()
    res = agent.run(startup_info, d_res.get("summary", ""), fin_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "roadmap_agent"
    assert "data" in res
    data = res["data"]
    assert "30_day_plan" in data or "thirty_day_plan" in data
    assert "60_day_plan" in data or "sixty_day_plan" in data
    assert "90_day_plan" in data or "ninety_day_plan" in data

def test_validation_agent(startup_info):
    discovery_res = DiscoveryAgent().run(startup_info)
    agent = ValidationAgent()
    res = agent.run(startup_info, discovery_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "validation_agent"
    assert "data" in res
    data = res["data"]
    assert "validation_score" in data
    assert "feasibility" in data
    assert "innovation" in data
    assert "risk" in data
    assert "reasoning" in data

def test_risk_agent(startup_info):
    d_res = DiscoveryAgent().run(startup_info)
    m_res = MarketAgent().run(startup_info, d_res.get("summary", ""))
    bm_res = BusinessModelAgent().run(startup_info, d_res.get("summary", ""), m_res.get("summary", ""))
    fin_res = FinancialPlanningAgent().run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""))
    leg_res = LegalAgent().run(startup_info, d_res.get("summary", ""), bm_res.get("summary", ""), fin_res.get("summary", ""))
    
    agent = RiskAgent()
    res = agent.run(startup_info, d_res.get("summary", ""), fin_res.get("summary", ""), leg_res.get("summary", ""))
    
    assert res["status"] == "success"
    assert res["agent"] == "risk_agent"
    assert "data" in res
    data = res["data"]
    assert "technical_risk" in data
    assert "market_risk" in data
    assert "financial_risk" in data
    assert "legal_risk" in data
    assert "mitigation" in data
