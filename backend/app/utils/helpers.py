from typing import Dict, Any, List
import re


def _clean_number(value: Any) -> int:
    clean = re.sub(r"[^\d]", "", str(value))
    return int(clean) if clean else 0


def _currency_for_country(country: str) -> str:
    c_lower = country.lower()
    if "india" in c_lower:
        return "₹"
    if "uk" in c_lower or "united kingdom" in c_lower:
        return "£"
    if any(k in c_lower for k in ["germany", "france", "italy", "spain", "netherlands"]):
        return "€"
    if "japan" in c_lower:
        return "¥"
    return "$"


def _sector_profile(idea: str, industry: str) -> Dict[str, Any]:
    combined = f"{idea} {industry}".lower()
    if re.search(r"health|med|doctor|clinic|fit|bio|pharm", combined):
        return {
            "name": "Healthcare",
            "business_model": "Compliance-first service platform",
            "market_label": "care delivery",
            "launch_prefix": "care and compliance",
        }
    if re.search(r"finance|pay|bank|wealth|money|fintech|crypto", combined):
        return {
            "name": "Fintech",
            "business_model": "Secure transaction platform",
            "market_label": "financial operations",
            "launch_prefix": "trust and payments",
        }
    if re.search(r"food|delivery|restaurant|eat|cook|meal|logistics", combined):
        return {
            "name": "Food & Logistics",
            "business_model": "On-demand operations platform",
            "market_label": "delivery coordination",
            "launch_prefix": "speed and reliability",
        }
    if re.search(r"tutor|teach|school|education|student|learn|edtech", combined):
        return {
            "name": "EdTech",
            "business_model": "Learning experience platform",
            "market_label": "learner engagement",
            "launch_prefix": "accessible learning",
        }
    if re.search(r"shop|e-commerce|store|sell|retail|marketplace|bamboo|wear|activewear|d2c", combined):
        return {
            "name": "Retail",
            "business_model": "Direct-to-consumer commerce",
            "market_label": "consumer demand",
            "launch_prefix": "product-led growth",
        }
    return {
        "name": "Software",
        "business_model": "B2B software platform",
        "market_label": "workflow automation",
        "launch_prefix": "digital operations",
    }


def _location_phrase(country: str, state: str, district: str, fallback: str) -> str:
    parts = [p for p in [district, state, country] if p]
    if parts:
        return ", ".join(parts)
    return fallback


def _build_context_sentence(idea: str, industry: str, country: str, state: str, district: str, target_market: str, founder: str, budget_str: str, stage: str, team_size_str: str) -> str:
    location = _location_phrase(country, state, district, country)
    budget_value = _clean_number(budget_str)
    team_size = _clean_number(team_size_str) or 1
    budget_phrase = f"with a {budget_str} budget" if budget_str else "with a lean budget"
    stage_phrase = f"at the {stage} stage" if stage else "at an early stage"
    team_phrase = f"for a team of {team_size}" if team_size > 1 else "for a solo founder"
    return (
        f"{founder} is shaping {idea} for the {industry} sector in {location}. "
        f"The launch plan focuses on {target_market} and is designed {budget_phrase} {stage_phrase}, {team_phrase}."
    )


def _build_pain_points(idea: str, industry: str, target_market: str) -> List[str]:
    tokens = f"{idea} {industry} {target_market}".lower()
    if re.search(r"custom|document|paper|compliance|regulation", tokens):
        return [
            f"Manual {target_market.lower()} paperwork is slowing approvals and raising error rates",
            f"Teams lose time switching between fragmented tools and spreadsheets for {industry.lower()}",
            "The cost of rework compounds as work volumes rise",
        ]
    if re.search(r"delivery|logistics|route|courier|restaurant", tokens):
        return [
            "Dispatch coordination is reactive and causes missed windows",
            f"Operators struggle to keep {target_market} promises when demand spikes",
            "Manual handoffs increase errors and customer churn",
        ]
    if re.search(r"school|student|learn|tutor|education", tokens):
        return [
            "Learners need guidance that adapts to their pace and gaps",
            f"Teachers and parents cannot personalize support for every {target_market.lower()} learner",
            "Administrative overhead reduces the time available for meaningful instruction",
        ]
    return [
        f"The target customer still depends on slow manual work in {industry.lower()}",
        f"Current tools do not fit the real workflows of {target_market}",
        "Execution costs rise faster than the team can absorb them",
    ]


def _build_market_trends(idea: str, industry: str, country: str) -> List[str]:
    sector = _sector_profile(idea, industry)
    return [
        f"Demand for {sector['name'].lower()} tools is increasing in {country}",
        f"Buyers are prioritizing lean deployment and visible ROI in {industry}",
        f"Teams are consolidating fragmented workflows under one {sector['launch_prefix']} operating layer",
    ]


def _build_competitors(idea: str, industry: str, target_market: str) -> List[Dict[str, Any]]:
    safe_industry = industry.strip().title() if industry else "Market"
    safe_idea = idea.split()[0].title() if idea else "Startup"
    return [
        {"name": f"Legacy {safe_industry} Providers", "gap": f"They remain too manual for {target_market} and lack modern onboarding", "threat_level": "Medium"},
        {"name": f"Incumbent {safe_idea} Platforms", "gap": "They focus on broad features instead of fast workflow execution", "threat_level": "High"},
    ]


def _build_expenses(currency: str, budget_val: int) -> List[Dict[str, Any]]:
    if budget_val < 30000:
        return [
            {"item": "Cloud hosting and lightweight tooling", "cost_type": "Fixed", "estimated_cost": f"{currency}80/mo"},
            {"item": "Customer onboarding and support", "cost_type": "Variable", "estimated_cost": f"{currency}120/mo"},
        ]
    return [
        {"item": "Core product engineering", "cost_type": "Fixed", "estimated_cost": f"{currency}1,200/mo"},
        {"item": "Customer success and operations", "cost_type": "Variable", "estimated_cost": f"{currency}800/mo"},
        {"item": "Growth and distribution", "cost_type": "Variable", "estimated_cost": f"{currency}600/mo"},
    ]


def _build_roadmap(stage: str, country: str, target_market: str) -> Dict[str, List[str]]:
    stage_prefix = f"for {stage}" if stage else "for the early stage"
    return {
        "30_day_plan": [
            f"Validate the hypothesis with {target_market} interviews",
            f"Set up the first operating workflow in {country}",
            "Document the core MVP scope and success metrics",
        ],
        "60_day_plan": [
            f"Build a focused prototype that serves {target_market}",
            "Collect feedback and tighten the onboarding path",
            f"Launch a small pilot {stage_prefix}",
        ],
        "90_day_plan": [
            "Refine pricing, support, and reporting based on feedback",
            f"Expand the pilot to more {target_market} accounts",
            "Prepare a disciplined growth plan and funding narrative",
        ],
    }


def get_dynamic_mock_data(agent_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    """Generate context-aware fallback content directly from the incoming startup snapshot."""
    idea = str(variables.get("idea") or "a tech startup").strip()
    industry = str(variables.get("industry") or "Technology").strip()
    country = str(variables.get("country") or "United States").strip()
    state = str(variables.get("state") or "").strip()
    district = str(variables.get("district") or "").strip()
    location_context = str(variables.get("location_context") or _location_phrase(country, state, district, country)).strip()
    stage = str(variables.get("stage") or "Idea").strip()
    budget_str = str(variables.get("budget") or "$10,000").strip()
    founder = str(variables.get("founder_name") or "Founder").strip()
    target_market = str(variables.get("target_market") or "General Public").strip()
    team_size_str = str(variables.get("team_size") or "1").strip()

    budget_val = _clean_number(budget_str)
    team_size = _clean_number(team_size_str) or 1
    currency = _currency_for_country(country)
    sector = _sector_profile(idea, industry)
    context_sentence = _build_context_sentence(idea, industry, country, state, district, target_market, founder, budget_str, stage, team_size_str)
    pain_points = _build_pain_points(idea, industry, target_market)
    market_trends = _build_market_trends(idea, industry, country)
    competitors = _build_competitors(idea, industry, target_market)
    roadmap = _build_roadmap(stage, country, target_market)

    validation_score = min(98, max(45, 73 + (len(idea) % 12) + (5 if "ai" in idea.lower() else 0) - (10 if budget_val < 15000 else 0)))
    feasibility_score = min(95, max(40, 82 - min(15, budget_val // 20000) - max(0, team_size - 2)))
    innovation_score = min(99, max(50, 64 + (len(idea) % 20) + (8 if "ai" in idea.lower() else 0)))
    risk_score = min(95, max(15, 26 + (budget_val // 15000) + (5 if "compliance" in idea.lower() else 0)))

    tam_value = max(5000000, budget_val * 500)
    sam_value = int(tam_value * 0.25)
    som_value = int(sam_value * 0.10)

    if agent_name == "discovery_agent":
        return {
            "problem": f"The core problem is that {target_market} still faces slow, error-prone work in {industry.lower()}.",
            "solution": f"{founder}'s {idea} uses software and automation to make the workflow faster, more reliable, and easier to adopt.",
            "customer": f"The primary customer is {target_market} operating in {location_context}.",
            "pain_points": pain_points,
            "industry": industry,
            "business_model": sector["business_model"],
            "confidence": validation_score,
        }

    if agent_name == "validation_agent":
        return {
            "validation_score": validation_score,
            "feasibility": feasibility_score,
            "innovation": innovation_score,
            "risk": risk_score,
            "reasoning": f"The concept is credible because {context_sentence} It remains practical for a {budget_str} launch plan and is supported by clear customer pain points in {location_context}.",
        }

    if agent_name == "market_agent":
        return {
            "industry_specific_market": f"The market opportunity for {idea} is strongest in {location_context}, where {sector['market_label']} demand is growing and buyers want faster execution.",
            "TAM": f"{currency}{tam_value/1000000:.1f}M globally for {industry.lower()} efficiency and automation",
            "SAM": f"{currency}{sam_value/1000000:.1f}M reachable in {country} for {target_market.lower()}",
            "SOM": f"{currency}{som_value/1000000:.1f}M obtainable in the first 12-24 months by focusing on {target_market.lower()}",
            "market_trends": market_trends,
            "sources": [
                f"Primary customer interviews in {location_context}",
                f"Observed demand patterns across {industry} operators",
            ],
        }

    if agent_name == "competitor_agent":
        return {
            "real_competitors": competitors,
            "pricing": f"A simple value-led pricing model should start around {currency}29 to {currency}99 per month for early adopters and scale with usage.",
            "strengths": ["Fast setup and clear workflow benefits", "Focused adoption for a specific customer group"],
            "weaknesses": ["Limited brand awareness early on", "Execution depends on strong onboarding and support"],
            "gap_analysis": f"The white space is a focused {sector['launch_prefix']} experience that better matches the workflows of {target_market} in {location_context}.",
        }

    if agent_name == "business_model_agent":
        return {
            "customer_segments": [target_market, f"Teams operating in {industry}"],
            "channels": [f"Direct outreach to {target_market}", f"Industry communities in {country}", "Content-led founder-led distribution"],
            "key_partners": [f"Early {target_market} adopters", f"Service providers in {country}", "Implementation partners"],
            "key_resources": ["Product and engineering focus", "Customer support and onboarding", "Domain expertise in the workflow"],
            "activities": ["Product iteration", "Customer discovery", "Pilot onboarding and support"],
            "value_proposition": [f"Reduce friction for {target_market}", f"Speed up delivery of {industry.lower()} outcomes", "Make the workflow easier to run and measure"],
            "revenue_model": sector["business_model"],
            "pricing_strategy": f"Start lean with a simple subscription for small teams, then move to usage-based expansion as the product proves value.",
        }

    if agent_name == "financial_planning_agent":
        monthly_burn = max(1200, budget_val // 12)
        return {
            "monthly_burn": f"{currency}{monthly_burn:,}/mo",
            "runway": f"{max(3, min(18, int(budget_val / max(1200, monthly_burn))))} months",
            "cash_flow": f"The plan keeps cash burn tight while the team proves demand for {idea.lower()} in {location_context}.",
            "expenses": _build_expenses(currency, budget_val),
            "revenue_projection": [
                {"year": "Year 1", "amount": f"{currency}{budget_val * 2:,}"},
                {"year": "Year 2", "amount": f"{currency}{budget_val * 5:,}"},
                {"year": "Year 3", "amount": f"{currency}{budget_val * 12:,}"},
                {"year": "Year 4", "amount": f"{currency}{budget_val * 24:,}"},
                {"year": "Year 5", "amount": f"{currency}{budget_val * 45:,}"},
            ],
            "break_even": "9-12 months" if budget_val < 30000 else "12-18 months",
        }

    if agent_name == "legal_agent":
        entity_type = "Private Limited Company" if "india" in country.lower() else "Limited Liability Company"
        compliance = ["Maintain clear data handling policies", "Keep founder and contractor agreements current"]
        if "health" in idea.lower() or "medical" in idea.lower():
            compliance.append("Prepare for healthcare data handling and audit requirements")
        if "finance" in idea.lower() or "payment" in idea.lower():
            compliance.append("Prepare for payment and financial-services compliance controls")
        return {
            "country_specific_requirements": f"Set up the operating entity in {location_context} and align contracts, accounting, and local registrations before launch.",
            "licenses": [f"Business registration in {country}", "Tax registration and basic compliance filings"],
            "taxes": ["Corporate tax registration", "Value-added or indirect tax registration if applicable"],
            "entity_type": entity_type,
            "compliance": compliance,
        }

    if agent_name == "funding_agent":
        if budget_val < 30000:
            funding = f"Bootstrap with a focused MVP and validate demand before seeking outside capital"
            investors = ["Local angel networks", "Founder-led customer prepayments"]
        elif budget_val < 100000:
            funding = f"Use a pre-seed round to fund product delivery and initial customer acquisition"
            investors = ["Micro-VCs", "Sector-focused angel syndicates"]
        else:
            funding = f"Prepare for a seed round to fund rapid product build-out and growth"
            investors = ["Institutional seed funds", "Strategic operators"]
        return {
            "recommended_funding": funding,
            "recommended_investors": investors,
            "bootstrap_strategy": f"Keep the launch lean, spend only on the highest-conviction steps, and use customer feedback to guide the next milestone in {location_context}.",
        }

    if agent_name == "roadmap_agent":
        return {
            "30_day_plan": roadmap["30_day_plan"],
            "60_day_plan": roadmap["60_day_plan"],
            "90_day_plan": roadmap["90_day_plan"],
        }

    if agent_name == "risk_agent":
        return {
            "technical_risk": f"Execution complexity could slow delivery if the product scope expands faster than the team can support.",
            "market_risk": f"Customers may delay adoption if the value case is not clear for {target_market}.",
            "financial_risk": f"Budget discipline matters because {budget_str} is enough for a lean start but not for broad experimentation.",
            "legal_risk": f"Local compliance and contracting gaps could create avoidable delays in {location_context}.",
            "mitigation": ["Keep the first release tightly scoped", "Use rapid customer feedback loops", "Track spend against milestone-based goals"],
        }

    return {}
