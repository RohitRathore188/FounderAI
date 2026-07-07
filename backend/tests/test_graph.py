import pytest
from app.graph.builder import graph

def test_full_langgraph_workflow():
    startup_input = {
        "idea": "An automated e-commerce inventory planner software",
        "industry": "RetailTech / SaaS",
        "country": "United States",
        "budget": "$10,000",
        "stage": "Idea",
        "founder_name": "Sarah",
        "target_market": "E-commerce Shopify Sellers",
        "state": "Delaware",
        "team_size": "2"
    }

    # Initialize Graph state (matching FounderState)
    initial_state = {
        "startup": startup_input,
        "discovery": None,
        "validation": None,
        "market": None,
        "competitors": None,
        "business_model": None,
        "financial": None,
        "legal": None,
        "funding": None,
        "roadmap": None,
        "risk": None,
        "metadata": {
            "run_id": "test_run_123",
            "status": "processing"
        }
    }

    # Run compiled workflow
    final_state = graph.invoke(initial_state)

    # Assert all keys are populated successfully by respective agents
    assert final_state["discovery"] is not None
    assert final_state["discovery"]["status"] == "success"
    assert final_state["discovery"]["agent"] == "discovery_agent"

    assert final_state["validation"] is not None
    assert final_state["validation"]["status"] == "success"
    assert final_state["validation"]["agent"] == "validation_agent"

    assert final_state["market"] is not None
    assert final_state["market"]["status"] == "success"
    assert final_state["market"]["agent"] == "market_agent"

    assert final_state["competitors"] is not None
    assert final_state["competitors"]["status"] == "success"
    assert final_state["competitors"]["agent"] == "competitor_agent"

    assert final_state["business_model"] is not None
    assert final_state["business_model"]["status"] == "success"
    assert final_state["business_model"]["agent"] == "business_model_agent"

    assert final_state["financial"] is not None
    assert final_state["financial"]["status"] == "success"
    assert final_state["financial"]["agent"] == "financial_planning_agent"

    assert final_state["legal"] is not None
    assert final_state["legal"]["status"] == "success"
    assert final_state["legal"]["agent"] == "legal_agent"

    assert final_state["funding"] is not None
    assert final_state["funding"]["status"] == "success"
    assert final_state["funding"]["agent"] == "funding_agent"

    assert final_state["roadmap"] is not None
    assert final_state["roadmap"]["status"] == "success"
    assert final_state["roadmap"]["agent"] == "roadmap_agent"

    assert final_state["risk"] is not None
    assert final_state["risk"]["status"] == "success"
    assert final_state["risk"]["agent"] == "risk_agent"
