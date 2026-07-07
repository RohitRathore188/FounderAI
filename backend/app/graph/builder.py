from langgraph.graph import StateGraph, END
from app.graph.state import FounderState
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
from app.utils.engines import VerificationEngine

# Instantiate agents once
discovery_agent = DiscoveryAgent()
validation_agent = ValidationAgent()
market_agent = MarketAgent()
competitor_agent = CompetitorAgent()
business_model_agent = BusinessModelAgent()
financial_agent = FinancialPlanningAgent()
legal_agent = LegalAgent()
funding_agent = FundingAgent()
roadmap_agent = RoadmapAgent()
risk_agent = RiskAgent()

def run_discovery(state: FounderState) -> dict:
    startup = state["startup"]
    res = discovery_agent.run(startup)
    return {"discovery": res}

def run_validation(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    res = validation_agent.run(startup, discovery_summary)
    return {"validation": res}

def run_market(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    res = market_agent.run(startup, discovery_summary)
    return {"market": res}

def run_competitors(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    market = state["market"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    market_summary = market.get("summary", "") if market else ""
    res = competitor_agent.run(startup, discovery_summary, market_summary)
    return {"competitors": res}

def run_business_model(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    market = state["market"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    market_summary = market.get("summary", "") if market else ""
    res = business_model_agent.run(startup, discovery_summary, market_summary)
    return {"business_model": res}

def run_financial(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    business_model = state["business_model"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    bm_summary = business_model.get("summary", "") if business_model else ""
    res = financial_agent.run(startup, discovery_summary, bm_summary)
    return {"financial": res}

def run_legal(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    business_model = state["business_model"]
    financial = state["financial"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    bm_summary = business_model.get("summary", "") if business_model else ""
    fin_summary = financial.get("summary", "") if financial else ""
    res = legal_agent.run(startup, discovery_summary, bm_summary, fin_summary)
    return {"legal": res}

def run_funding(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    financial = state["financial"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    fin_summary = financial.get("summary", "") if financial else ""
    res = funding_agent.run(startup, discovery_summary, fin_summary)
    return {"funding": res}

def run_roadmap(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    financial = state["financial"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    fin_summary = financial.get("summary", "") if financial else ""
    res = roadmap_agent.run(startup, discovery_summary, fin_summary)
    return {"roadmap": res}

def run_risk(state: FounderState) -> dict:
    startup = state["startup"]
    discovery = state["discovery"]
    financial = state["financial"]
    legal = state["legal"]
    discovery_summary = discovery.get("summary", "") if discovery else ""
    fin_summary = financial.get("summary", "") if financial else ""
    legal_summary = legal.get("summary", "") if legal else ""
    res = risk_agent.run(startup, discovery_summary, fin_summary, legal_summary)
    return {"risk": res}

def run_verification(state: FounderState) -> dict:
    updated_state = VerificationEngine.audit_and_verify(state)
    return {
        "discovery": updated_state.get("discovery"),
        "validation": updated_state.get("validation"),
        "market": updated_state.get("market"),
        "competitors": updated_state.get("competitors"),
        "business_model": updated_state.get("business_model"),
        "financial": updated_state.get("financial"),
        "legal": updated_state.get("legal"),
        "funding": updated_state.get("funding"),
        "roadmap": updated_state.get("roadmap"),
        "risk": updated_state.get("risk")
    }

# Construct the 11-node LangGraph workflow (10 agents + 1 verification node)
workflow = StateGraph(FounderState)

workflow.add_node("discovery", run_discovery)
workflow.add_node("validation", run_validation)
workflow.add_node("market", run_market)
workflow.add_node("competitors", run_competitors)
workflow.add_node("business_model", run_business_model)
workflow.add_node("financial", run_financial)
workflow.add_node("legal", run_legal)
workflow.add_node("funding", run_funding)
workflow.add_node("roadmap", run_roadmap)
workflow.add_node("risk", run_risk)
workflow.add_node("verification", run_verification)

workflow.set_entry_point("discovery")

workflow.add_edge("discovery", "validation")
workflow.add_edge("validation", "market")
workflow.add_edge("market", "competitors")
workflow.add_edge("competitors", "business_model")
workflow.add_edge("business_model", "financial")
workflow.add_edge("financial", "legal")
workflow.add_edge("legal", "funding")
workflow.add_edge("funding", "roadmap")
workflow.add_edge("roadmap", "risk")
workflow.add_edge("risk", "verification")
workflow.add_edge("verification", END)

# Compile graph
graph = workflow.compile()
