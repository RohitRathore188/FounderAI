from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Discovery Schemas ---
class DiscoveryData(BaseModel):
    problem: str = Field(description="The primary pain points of the target audience")
    solution: str = Field(description="How the startup resolves the problem")
    customer: str = Field(description="Description of the target customer segment")
    pain_points: List[str] = Field(default=[], description="List of specific user frustrations")
    industry: str = Field(description="Relevant industry or vertical")
    business_model: str = Field(description="The operational business model type (e.g. SaaS, E-commerce)")
    confidence: int = Field(description="Confidence score of the concept (0-100)")

class DiscoveryResponse(BaseModel):
    status: str = "success"
    agent: str = "discovery_agent"
    summary: str
    data: DiscoveryData
    timestamp: str

# --- Validation Schemas ---
class ValidationData(BaseModel):
    validation_score: int = Field(description="Overall validation quotient (0-100)")
    feasibility: int = Field(description="Technical and operational feasibility (0-100)")
    innovation: int = Field(description="Degree of innovation and uniqueness (0-100)")
    risk: int = Field(description="Risk assessment score (0-100)")
    reasoning: str = Field(description="Detailed analysis backing these scores")

class ValidationResponse(BaseModel):
    status: str = "success"
    agent: str = "validation_agent"
    summary: str
    data: ValidationData
    timestamp: str

# --- Market Research Schemas ---
class MarketResearchData(BaseModel):
    industry_specific_market: str = Field(description="Qualitative summary of the niche market")
    TAM: str = Field(description="Total Addressable Market size and calculation basis")
    SAM: str = Field(description="Serviceable Addressable Market size and calculation basis")
    SOM: str = Field(description="Serviceable Obtainable Market size and calculation basis")
    market_trends: List[str] = Field(default=[], description="Key trends driving this sector")
    sources: List[str] = Field(default=[], description="Credible industry reports or research sources")

class MarketResearchResponse(BaseModel):
    status: str = "success"
    agent: str = "market_agent"
    summary: str
    data: MarketResearchData
    timestamp: str

# --- Competitor Schemas ---
class CompetitorItem(BaseModel):
    name: str
    gap: str = Field(description="What this competitor lacks compared to the startup")
    threat_level: str = Field(description="Low, Medium, or High")

class CompetitorData(BaseModel):
    real_competitors: List[CompetitorItem] = Field(default=[], description="Direct and indirect market competitors")
    pricing: str = Field(description="Competitor pricing standard overview")
    strengths: List[str] = Field(default=[], description="Typical competitor strengths")
    weaknesses: List[str] = Field(default=[], description="Typical competitor weaknesses")
    gap_analysis: str = Field(description="Key market gap opportunity for the startup")

class CompetitorResponse(BaseModel):
    status: str = "success"
    agent: str = "competitor_agent"
    summary: str
    data: CompetitorData
    timestamp: str

# --- Business Model Canvas ---
class BusinessModelData(BaseModel):
    customer_segments: List[str] = Field(default=[], description="Target user profiles")
    channels: List[str] = Field(default=[], description="Marketing and distribution channels")
    key_partners: List[str] = Field(default=[], description="Core vendor or strategic partnerships")
    key_resources: List[str] = Field(default=[], description="Essential technical or human resources")
    activities: List[str] = Field(default=[], description="Key operational activities")
    value_proposition: List[str] = Field(default=[], description="Primary value statements")
    revenue_model: str = Field(description="How the company captures value (SaaS, transactional, etc.)")
    pricing_strategy: str = Field(description="Detailed pricing plans and structures")

class BusinessModelResponse(BaseModel):
    status: str = "success"
    agent: str = "business_model_agent"
    summary: str
    data: BusinessModelData
    timestamp: str

# --- Financial Planning Schemas ---
class FinancialExpenseItem(BaseModel):
    item: str
    cost_type: str = Field(description="Fixed or Variable")
    estimated_cost: str

class FinancialForecastItem(BaseModel):
    year: str
    amount: str

class FinancialData(BaseModel):
    monthly_burn: str = Field(description="Estimated monthly operating expenses")
    runway: str = Field(description="Months of runway based on starting budget")
    cash_flow: str = Field(description="Qualitative state of cash flows")
    expenses: List[FinancialExpenseItem] = Field(default=[], description="Breakdown of fixed and variable operating costs")
    revenue_projection: List[FinancialForecastItem] = Field(default=[], description="5-year projected revenues")
    break_even: str = Field(description="Estimated timeline to reach break-even")

class FinancialResponse(BaseModel):
    status: str = "success"
    agent: str = "financial_planning_agent"
    summary: str
    data: FinancialData
    timestamp: str

# --- Legal & Compliance ---
class LegalData(BaseModel):
    country_specific_requirements: str = Field(description="Regional incorporation and legal frameworks")
    licenses: List[str] = Field(default=[], description="Required state and federal business licenses")
    taxes: List[str] = Field(default=[], description="Key tax categories and registration requirements")
    entity_type: str = Field(description="Recommended legal entity type (LLC, Pvt Ltd, etc.)")
    compliance: List[str] = Field(default=[], description="Compliance guidelines (HIPAA, GDPR, SOC2, GST, etc.)")

class LegalResponse(BaseModel):
    status: str = "success"
    agent: str = "legal_agent"
    summary: str
    data: LegalData
    timestamp: str

# --- Funding Schemas ---
class FundingData(BaseModel):
    recommended_funding: str = Field(description="Recommended funding round amount and type")
    recommended_investors: List[str] = Field(default=[], description="Target VCs, angel networks, or grants")
    bootstrap_strategy: str = Field(description="Lean deployment plan for starting budget")

class FundingResponse(BaseModel):
    status: str = "success"
    agent: str = "funding_agent"
    summary: str
    data: FundingData
    timestamp: str

# --- Execution Roadmap Schemas ---
class RoadmapData(BaseModel):
    thirty_day_plan: List[str] = Field(default=[], alias="30_day_plan", description="Immediate foundation and validation goals")
    sixty_day_plan: List[str] = Field(default=[], alias="60_day_plan", description="MVP build and beta customer launch")
    ninety_day_plan: List[str] = Field(default=[], alias="90_day_plan", description="Public scaling and distribution launch")

    class Config:
        populate_by_name = True

class RoadmapResponse(BaseModel):
    status: str = "success"
    agent: str = "roadmap_agent"
    summary: str
    data: RoadmapData
    timestamp: str

# --- Risk Assessment Schemas ---
class RiskData(BaseModel):
    technical_risk: str = Field(description="Technical or development failures and constraints")
    market_risk: str = Field(description="Customer adoption and competition challenges")
    financial_risk: str = Field(description="Cash burn, runway, or inflation sensitivities")
    legal_risk: str = Field(description="Regulatory, tax, and liability threats")
    mitigation: List[str] = Field(default=[], description="Actionable countermeasures for each risk area")

class RiskResponse(BaseModel):
    status: str = "success"
    agent: str = "risk_agent"
    summary: str
    data: RiskData
    timestamp: str
