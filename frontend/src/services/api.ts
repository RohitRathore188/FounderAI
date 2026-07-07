export interface StartupRequest {
  idea: string;
  industry: string;
  country: string;
  state?: string;
  district?: string;
  budget: string;
  stage: string;
  founder_name: string;
  target_market: string;
  team_size?: string;
  customer_segment?: string;
}

export interface AgentInfo {
  id: string;
  name: string;
  role: string;
  status: 'idle' | 'active' | 'completed' | 'error';
  progress: number;
  accuracy: number;
  lastExecution: string;
  capabilities: string[];
}

export interface DiscoveryData {
  problem: string;
  solution: string;
  usp: string;
}

export interface ValidationData {
  validation_score: number;
  feasibility_score: number;
  market_fit_score: number;
  growth_potential_score: number;
  feedback: string;
  critical_risks: string[];
}

export interface MarketData {
  TAM: string;
  SAM: string;
  SOM: string;
  tam?: string;
  sam?: string;
  som?: string;
  market_trends: string[];
  sources: string[];
  customer_persona?: {
    name: string;
    role: string;
    pain_points: string[];
    buying_power: string;
  };
}

export interface CompetitorData {
  real_competitors: Array<{ name: string; gap: string; threat_level: string }>;
  pricing: string;
  strengths: string[];
  weaknesses: string[];
  gap_analysis: string;
  competitors?: Array<{ name: string; gap: string; threat_level: string }>;
  swot?: {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  };
  competitive_advantage?: string;
}

export interface BusinessModelData {
  key_partners: string[];
  activities: string[];
  key_resources: string[];
  value_proposition: string[];
  channels: string[];
  customer_segments: string[];
  revenue_model: string;
  pricing_strategy: string;
  key_activities?: string[];
  value_propositions?: string[];
  customer_relationships?: string[];
  cost_structure?: Array<{ item: string; estimated_cost: string }>;
  revenue_streams?: Array<{ source: string; pricing: string }>;
}

export interface RegistrationData {
  company_type_recommendation: string;
  country_specific: string;
  gst_required: boolean;
  trademark_recommendation: string;
  required_licenses: string[];
  required_documents: string[];
}

export interface LegalData {
  co_founder_agreement_reqs: string[];
  ip_assignment_reqs: string[];
  nda_reqs: string[];
  legal_compliance_checklist: string[];
}

export interface FundingData {
  investment_readiness_score: number;
  bootstrap_strategy: string;
  vc_firms: Array<{ name: string; stage: string; focus: string }>;
  angel_investors: Array<{ name: string; stage: string; focus: string }>;
  government_grants: Array<{ name: string; description: string; amount: string }>;
}

export interface RoadmapData {
  go_to_market_channels: string[];
  roadmap_phases: Array<{
    phase: string;
    duration: string;
    milestones: string[];
  }>;
}

export interface ReportData {
  executive_summary: string;
  pdf_url?: string;
}

export interface FounderState {
  startup: StartupRequest;
  discovery?: DiscoveryData;
  validation?: ValidationData;
  market?: MarketData;
  competitors?: CompetitorData;
  business_model?: BusinessModelData;
  registration?: RegistrationData;
  legal?: LegalData;
  funding?: FundingData;
  roadmap?: RoadmapData;
  report?: ReportData;
}

/**
 * REST API Client Placeholders for FounderAI OS.
 * Ready to point to backend endpoints when backend is integrated.
 */
export class FounderAPIService {
  // POST /analyze
  static async analyzeStartup(request: StartupRequest): Promise<FounderState> {
    // Placeholder only. Returns typed response block.
    console.log("API Service: Calling POST /analyze with startup:", request);
    return new Promise((resolve) => setTimeout(resolve, 1500));
  }

  // POST /generate-report
  static async generateReport(runId: string): Promise<string> {
    console.log("API Service: Calling POST /generate-report for runId:", runId);
    return `/api/startup/report/download/${runId}`;
  }

  // GET /agents
  static async getAgents(): Promise<AgentInfo[]> {
    console.log("API Service: Calling GET /agents");
    return [];
  }

  // GET /roadmap
  static async getRoadmap(runId: string): Promise<RoadmapData> {
    console.log("API Service: Calling GET /roadmap for runId:", runId);
    return { go_to_market_channels: [], roadmap_phases: [] };
  }

  // GET /reports
  static async getReports(): Promise<Array<{ id: string; name: string; date: string }>> {
    console.log("API Service: Calling GET /reports");
    return [];
  }
}
