import React, { useState, useEffect, useRef } from 'react';
import { Country, State, City } from 'country-state-city';
import type { ICountry, IState, ICity } from 'country-state-city';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';
import {
  Sparkles,
  TrendingUp,
  Target,
  Layers,
  DollarSign,
  CheckCircle2,
  ChevronRight,
  Download,
  Brain,
  ShieldCheck,
  ArrowRight,
  Bell,
  User,
  Play,
  RotateCcw,
  FileCode,
  Menu,
  X,
  Cpu,
  Rocket
} from 'lucide-react';
import { INITIAL_MOCK_STATE, getDynamicFrontendMockData } from './services/mockData';
import type { AgentInfo, FounderState } from './services/api';
import NeuralBrain from './components/NeuralBrain';
import SplineScene from './components/SplineScene';
import OrchestrationTimeline from './components/OrchestrationTimeline';
import ProductDashboardMockup from './components/ProductDashboardMockup';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const navLinks = [
  { id: 'landing', label: 'Home' },
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'onboarding', label: 'Discovery' },
  { id: 'command', label: 'Command Center' },
  { id: 'reports', label: 'Reports' },
  { id: 'roadmap', label: 'Roadmap' },
  { id: 'agents', label: 'Agents' },
  { id: 'settings', label: 'Settings' }
] as const;

const normalizeState = (state: any): FounderState => {
  if (!state) return state;
  const normalized: any = { ...state };
  const keys = ['discovery', 'validation', 'market', 'competitors', 'business_model', 'registration', 'legal', 'funding', 'roadmap', 'report'];
  keys.forEach(key => {
    if (state[key] && typeof state[key] === 'object' && 'data' in state[key]) {
      const parentProps = { ...state[key] };
      delete parentProps.data;
      normalized[key] = { ...state[key].data, ...parentProps };
    }
  });

  // Align backend fields with what the UI displays at runtime
  if (normalized.legal) {
    const backendLegal = normalized.legal;
    if ('entity_type' in backendLegal || 'country_specific_requirements' in backendLegal) {
      normalized.registration = {
        company_type_recommendation: backendLegal.entity_type || '',
        country_specific: backendLegal.country_specific_requirements || '',
        gst_required: (backendLegal.taxes || []).some((t: string) => /gst/i.test(t)),
        trademark_recommendation: 'Reserve and register trademark for the business name.',
        required_licenses: backendLegal.licenses || [],
        required_documents: ['Articles of Incorporation', 'Operating Agreement / Bylaws', 'Tax Registration Certificates']
      };

      normalized.legal = {
        co_founder_agreement_reqs: [
          'Vesting schedule (e.g., 4-year vesting with 1-year cliff)',
          'Role definition and intellectual property assignment clauses',
          'Equity distribution and buy-back provisions'
        ],
        ip_assignment_reqs: [
          'Proprietary Information and Inventions Agreement (PIIA) for founders',
          'IP Assignment Agreement for all contractors and third-party devs',
          'Clear developer agreement templates'
        ],
        nda_reqs: [
          'Mutual NDA template for strategic partnerships',
          'Unilateral NDA template for early customer discovery feedback sessions',
          'Non-disclosure clauses in employee contracts'
        ],
        legal_compliance_checklist: backendLegal.compliance || []
      };
    }
  }

  if (normalized.funding) {
    const backendFunding = normalized.funding;
    if ('recommended_investors' in backendFunding && !backendFunding.government_grants) {
      normalized.funding = {
        investment_readiness_score: 85,
        bootstrap_strategy: backendFunding.bootstrap_strategy || '',
        vc_firms: [],
        angel_investors: [],
        government_grants: (backendFunding.recommended_investors || []).map((inv: string, idx: number) => {
          const amountMatch = inv.match(/\$[0-9,KM]+/i);
          const amount = amountMatch ? amountMatch[0] : 'Varies';
          const name = inv.replace(/\s*\([^)]+\)\s*/g, '').trim();
          return {
            name: name || `Investor Recommendation ${idx + 1}`,
            description: `Target funding match: ${inv}`,
            amount: amount
          };
        })
      };
    }
  }

  if (normalized.roadmap) {
    const raw = normalized.roadmap;
    const thirty = raw.thirty_day_plan || raw['30_day_plan'] || [];
    const sixty = raw.sixty_day_plan || raw['60_day_plan'] || [];
    const ninety = raw.ninety_day_plan || raw['90_day_plan'] || [];

    if (thirty.length > 0 || sixty.length > 0 || ninety.length > 0) {
      normalized.roadmap = {
        go_to_market_channels: raw.go_to_market_channels || [
          'Direct Outreach & Cold Demos',
          'Industry LinkedIn/Community Engagement',
          'Content Marketing & Founder-led SEO'
        ],
        roadmap_phases: [
          { phase: 'Phase 1: Foundation', duration: 'Days 1-30', milestones: thirty },
          { phase: 'Phase 2: MVP Launch', duration: 'Days 31-60', milestones: sixty },
          { phase: 'Phase 3: Scale & Growth', duration: 'Days 61-90', milestones: ninety }
        ]
      };
    }
  }

  return normalized;
};

const slidingAgents = [
  { name: 'Discovery Agent', role: 'Business Formulator', icon: '🧠' },
  { name: 'Validation Agent', role: 'Feasibility Evaluator', icon: '⚖️' },
  { name: 'Market Agent', role: 'TAM/SAM/SOM Sizer', icon: '📈' },
  { name: 'Competitor Agent', role: 'SWOT Intelligence', icon: '🎯' },
  { name: 'Business Model Agent', role: 'Canvas Architect', icon: '📊' },
  { name: 'Financial Agent', role: 'Runway Planner', icon: '💸' },
  { name: 'Legal Agent', role: 'Entity Formulator', icon: '🛡️' },
  { name: 'Funding Agent', role: 'Capital Matcher', icon: '💰' },
  { name: 'Roadmap Agent', role: 'GTM Scheduler', icon: '🚀' },
  { name: 'Risk Agent', role: 'Vulnerability Guard', icon: '🔍' }
];

export default function App() {
  const [activePage, setActivePage] = useState<'landing' | 'onboarding' | 'command' | 'dashboard' | 'reports' | 'roadmap' | 'agents' | 'settings'>('landing');
  const [activeReportTab, setActiveReportTab] = useState<'overview' | 'market' | 'competitors' | 'canvas' | 'registration' | 'funding' | 'roadmap' | 'legal'>('overview');
  
  const [loading, setLoading] = useState(false);
  const [wizardStep, setWizardStep] = useState(1);
  const [orchestratorProgress, setOrchestratorProgress] = useState(0);
  const [consoleLogs, setConsoleLogs] = useState<string[]>([]);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [pdfGenerating, setPdfGenerating] = useState(false);
  const [pdfError, setPdfError] = useState<string | null>(null);

  // Startup inputs state
  const [form, setForm] = useState({
    idea: '',
    industry: '',
    country: '',
    state: '',
    district: '',
    budget: '',
    stage: 'Idea',
    founder_name: '',
    target_market: '',
    team_size: '',
    customer_segment: ''
  });
  const [industryOther, setIndustryOther] = useState(false);

  // Current analysis state. Uses mock data by default for premium viewing.
  const [result, setResult] = useState<FounderState>(INITIAL_MOCK_STATE);
  
  const capabilityModules = [
    { title: 'AI Agent Core', description: 'Orchestrate agent synergy and model deployment.', icon: Cpu, visual: 'neural', accent: 'from-fuchsia-500/70 via-indigo-500/60 to-cyan-400/60' },
    { title: 'Market Forecaster', description: 'Real-time trends and competitive analysis.', icon: TrendingUp, visual: 'planet', accent: 'from-cyan-500/70 via-indigo-500/60 to-slate-200/30' },
    { title: 'Product Vision', description: 'Develop features and roadmap strategy.', icon: Layers, visual: 'chip', accent: 'from-violet-500/70 via-slate-500/50 to-cyan-400/60' },
    { title: 'Growth Catalyst', description: 'Scalability planning and go-to-market execution.', icon: Rocket, visual: 'rocket', accent: 'from-emerald-500/70 via-cyan-500/60 to-indigo-500/50' },
    { title: 'Data Sentinel', description: 'Secure your IP and data pipelines.', icon: ShieldCheck, visual: 'shield', accent: 'from-amber-500/70 via-rose-500/60 to-violet-500/60' },
    { title: 'Hub Connect', description: 'Facilitate seamless team and system integration.', icon: User, visual: 'hub', accent: 'from-sky-500/70 via-indigo-500/60 to-fuchsia-500/60' }
  ];
  
  // Terminal logs ref
  const terminalEndRef = useRef<HTMLDivElement>(null);

  // 10 Core Agents config
  const [agents, setAgents] = useState<AgentInfo[]>([
    { id: 'discovery', name: '1. Discovery Agent', role: 'Feature Extractor', status: 'completed', progress: 100, accuracy: 98, lastExecution: 'Just now', capabilities: ['Problem Parsing', 'Solution Mapping', 'USP Synthesis'] },
    { id: 'validation', name: '2. Idea Validation Agent', role: 'Viability Assessor', status: 'completed', progress: 100, accuracy: 95, lastExecution: 'Just now', capabilities: ['Feasibility Modeling', 'Risk Weighting', 'Startup Scoring'] },
    { id: 'market', name: '3. Market Research Agent', role: 'TAM/SAM/SOM Calculator', status: 'completed', progress: 100, accuracy: 96, lastExecution: 'Just now', capabilities: ['Niche Segmentation', 'Volume Estimation', 'Persona Development'] },
    { id: 'competitor', name: '4. Competitor Agent', role: 'SWOT Map Builder', status: 'completed', progress: 100, accuracy: 94, lastExecution: 'Just now', capabilities: ['Pricing Analysis', 'Competitor Scapes', 'Advantage Profiling'] },
    { id: 'business_model', name: '5. Business Model Agent', role: 'Canvas Orchestrator', status: 'completed', progress: 100, accuracy: 97, lastExecution: 'Just now', capabilities: ['9-Box Structuring', 'Cost Allocation', 'Revenue Stream Mapping'] },
    { id: 'registration', name: '6. Registration & Compliance Agent', role: 'Corporate Formulator', status: 'completed', progress: 100, accuracy: 99, lastExecution: 'Just now', capabilities: ['Entity Filings', 'Trademark Scopes', 'GST Verification'] },
    { id: 'legal', name: '7. Legal Agent', role: 'Governance Protocol Planner', status: 'completed', progress: 100, accuracy: 95, lastExecution: 'Just now', capabilities: ['NDA Layouts', 'Co-Founder Vesting', 'IP Assignments'] },
    { id: 'funding', name: '8. Funding Agent', role: 'Capital Sizer', status: 'completed', progress: 100, accuracy: 93, lastExecution: 'Just now', capabilities: ['Grants Scopes', 'VC Targeting', 'Angel Matching'] },
    { id: 'roadmap', name: '9. GTM & Roadmap Agent', role: 'Milestones Architect', status: 'completed', progress: 100, accuracy: 96, lastExecution: 'Just now', capabilities: ['Timeline Scheduling', 'Channels Formulation', 'Launch Tracking'] },
    { id: 'report', name: '10. Report Generator', role: 'Synthesis Engine', status: 'completed', progress: 100, accuracy: 99, lastExecution: 'Just now', capabilities: ['PDF Packaging', 'SLA Document Compile', 'Executive Summarization'] }
  ]);

  // Orbit angles for visual NeuralBrain nodes
  const [brainNodes, setBrainNodes] = useState([
    { id: 'discovery', name: 'Discovery Agent', angle: 0, status: 'completed' as any },
    { id: 'validation', name: 'Idea Validation Agent', angle: 36, status: 'completed' as any },
    { id: 'market', name: 'Market Research Agent', angle: 72, status: 'completed' as any },
    { id: 'competitor', name: 'Competitor Agent', angle: 108, status: 'completed' as any },
    { id: 'business_model', name: 'Business Model Agent', angle: 144, status: 'completed' as any },
    { id: 'registration', name: 'Registration & Compliance Agent', angle: 180, status: 'completed' as any },
    { id: 'legal', name: 'Legal Agent', angle: 216, status: 'completed' as any },
    { id: 'funding', name: 'Funding Agent', angle: 252, status: 'completed' as any },
    { id: 'roadmap', name: 'GTM & Roadmap Agent', angle: 288, status: 'completed' as any },
    { id: 'report', name: 'Report Generator', angle: 324, status: 'completed' as any }
  ]);

  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [consoleLogs]);

  const updateAgentStatus = (id: string, status: 'idle' | 'active' | 'completed' | 'error', progress = 0) => {
    setAgents(prev => prev.map(a => a.id === id ? { ...a, status, progress } : a));
    setBrainNodes(prev => prev.map(n => n.id === id ? { ...n, status } : n));
  };

  const addLog = (msg: string) => {
    setConsoleLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

  // Helper: Resolve ISO codes to readable location names
  const getCountryName = (isoCode: string): string => {
    if (!isoCode) return '';
    const country = Country.getCountryByCode(isoCode);
    return country ? country.name : isoCode;
  };
  const getStateName = (countryCode: string, stateCode: string): string => {
    if (!countryCode || !stateCode) return '';
    const state = State.getStateByCodeAndCountry(stateCode, countryCode);
    return state ? state.name : stateCode;
  };

  // Currency mapping by country ISO code
  const getCurrencySymbol = (countryCode: string): string => {
    const currencyMap: Record<string, string> = {
      'US': '$', 'IN': '₹', 'GB': '£', 'DE': '€', 'FR': '€', 'JP': '¥',
      'CN': '¥', 'KR': '₩', 'BR': 'R$', 'RU': '₽', 'ZA': 'R',
      'AU': 'A$', 'CA': 'C$', 'MX': 'MX$', 'SG': 'S$', 'AE': 'AED ',
      'SA': 'SAR ', 'NG': '₦', 'EG': 'E£', 'KE': 'KSh ', 'PK': '₨',
      'BD': '৳', 'LK': 'Rs ', 'NP': 'Rs ', 'MY': 'RM ', 'TH': '฿',
      'VN': '₫', 'PH': '₱', 'ID': 'Rp ', 'TR': '₺', 'PL': 'zł',
      'SE': 'kr ', 'NO': 'kr ', 'DK': 'kr ', 'CH': 'CHF ',
      'NZ': 'NZ$', 'IL': '₪', 'CL': 'CLP ', 'CO': 'COP ', 'AR': 'ARS ',
      'PE': 'S/', 'TW': 'NT$', 'HK': 'HK$',
    };
    return currencyMap[countryCode] || '$';
  };

  const formatBudget = (value: string, countryCode: string): string => {
    // Strip everything except digits
    const digits = value.replace(/[^0-9]/g, '');
    if (!digits) return '';
    // Format with commas
    const formatted = Number(digits).toLocaleString('en');
    const symbol = getCurrencySymbol(countryCode);
    return `${symbol}${formatted}`;
  };

  // Run Onboarding analysis flow
  const handleLaunchAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setActivePage('command');
    setOrchestratorProgress(5);
    setConsoleLogs([`[Orchestrator] Initializing FounderAI Multi-Agent Core for "${form.idea.substring(0, 35)}..."`]);

    // Reset status flags
    agents.forEach(a => updateAgentStatus(a.id, 'idle', 0));

    try {
      // 1. Discovery Agent
      updateAgentStatus('discovery', 'active', 40);
      addLog('Discovery Agent triggered.');
      addLog('Discovery Agent: Analyzing core business statement, target market, and stage...');
      await delay(900);
      updateAgentStatus('discovery', 'completed', 100);
      setOrchestratorProgress(12);
      addLog('Discovery Agent: Found USP: "API-first automated HIPAA compliance interception."');

      // 2. Validation Agent
      updateAgentStatus('validation', 'active', 50);
      addLog('Idea Validation Agent triggered.');
      addLog('Idea Validation Agent: Evaluating feasibility, budget parameters, and scaling risks...');
      await delay(900);
      updateAgentStatus('validation', 'completed', 100);
      setOrchestratorProgress(24);
      addLog('Idea Validation Agent: Feasibility index calculated. Score: 87/100.');

      // 3. Market Agent
      updateAgentStatus('market', 'active', 30);
      addLog('Market Research Agent triggered.');
      addLog('Market Research Agent: Compiling TAM/SAM/SOM ratios and structuring customer personas...');
      await delay(900);
      updateAgentStatus('market', 'completed', 100);
      setOrchestratorProgress(36);
      addLog('Market Research Agent: TAM estimated at $45B. Customer persona structured.');

      // 4. Competitor Agent
      updateAgentStatus('competitor', 'active', 60);
      addLog('Competitor Agent triggered.');
      addLog('Competitor Agent: Mapping competitor landscape and SWOT metrics...');
      await delay(900);
      updateAgentStatus('competitor', 'completed', 100);
      setOrchestratorProgress(48);
      addLog('Competitor Agent: Direct threats identified. SWOT matrix generated.');

      // 5. Business Model Agent
      updateAgentStatus('business_model', 'active', 45);
      addLog('Business Model Agent triggered.');
      addLog('Business Model Agent: Structuring 9-box Canvas with recurring pricing and cost estimates...');
      await delay(900);
      updateAgentStatus('business_model', 'completed', 100);
      setOrchestratorProgress(60);
      addLog('Business Model Agent: Canvas created successfully.');

      // 6. Registration & Compliance Agent
      updateAgentStatus('registration', 'active', 55);
      addLog('Registration & Compliance Agent triggered.');
      addLog(`Registration & Compliance Agent: Scoping entity filing standards for: ${form.country}...`);
      await delay(900);
      updateAgentStatus('registration', 'completed', 100);
      setOrchestratorProgress(72);
      addLog('Registration & Compliance Agent: Mapped Delaware C-Corp as top recommendation.');

      // 7. Legal Agent
      updateAgentStatus('legal', 'active', 40);
      addLog('Legal Agent triggered.');
      addLog('Legal Agent: Drafting vesting cliff ratios, IP assignments, and NDA rules...');
      await delay(900);
      updateAgentStatus('legal', 'completed', 100);
      setOrchestratorProgress(80);
      addLog('Legal Agent: Checklists and contract parameters prepared.');

      // 8. Funding Agent
      updateAgentStatus('funding', 'active', 70);
      addLog('Funding Agent triggered.');
      addLog('Funding Agent: Scanning VC matching matrices and seed grants databases...');
      await delay(900);
      updateAgentStatus('funding', 'completed', 100);
      setOrchestratorProgress(88);
      addLog('Funding Agent: Ready index logged. Pre-seed grant match: $150k.');

      // 9. GTM & Roadmap Agent
      updateAgentStatus('roadmap', 'active', 50);
      addLog('GTM & Roadmap Agent triggered.');
      addLog('GTM & Roadmap Agent: Structuring GTM acquisition funnels and milestone deadlines...');
      await delay(900);
      updateAgentStatus('roadmap', 'completed', 100);
      setOrchestratorProgress(95);
      addLog('GTM & Roadmap Agent: 30/60/90-Day launching stages scheduled.');

      // 10. Report Generator Agent (REST API Call)
      updateAgentStatus('report', 'active', 30);
      addLog('Report Generator triggered.');
      addLog('Report Agent: Assembling core modules, rendering layout flows, and drafting PDF...');
      
      const payload = { ...form, country: getCountryName(form.country), state: getStateName(form.country, form.state) };
      
      // Call endpoint
      const response = await fetch(`${API_BASE_URL}/api/startup/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('API server returned error during orchestration.');
      }

      const data = await response.json();
      setResult(normalizeState(data));

      updateAgentStatus('report', 'completed', 100);
      setOrchestratorProgress(100);
      addLog('Report Agent: Final PDF Compiled. All agents verified.');
      addLog('Orchestrator: Analysis finished. Loading Dashboard command metrics...');
      await delay(800);
      setLoading(false);
      setActivePage('dashboard');
    } catch (err) {
      console.warn("REST API connection failed, using high-fidelity local models as fallback.");
      // Fallback
      setResult(normalizeState(getDynamicFrontendMockData(form)));
      updateAgentStatus('report', 'completed', 100);
      setOrchestratorProgress(100);
      addLog('[Fallback] Loaded high-fidelity mock data model successfully.');
      await delay(800);
      setLoading(false);
      setActivePage('dashboard');
    }
  };

  const handleDownloadPDF = async () => {
    if (result && result.report?.pdf_url && result.report.pdf_url !== '#' && result.report.pdf_url !== '') {
      window.open(`${API_BASE_URL}${result.report.pdf_url}`, '_blank');
      return;
    }

    setPdfGenerating(true);
    setPdfError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/startup/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, country: getCountryName(form.country), state: getStateName(form.country, form.state) })
      });

      if (!response.ok) {
        throw new Error('API server returned error during orchestration.');
      }

      const data = await response.json();
      const normalized = normalizeState(data);
      setResult(normalized);

      if (normalized.report?.pdf_url && normalized.report.pdf_url !== '#' && normalized.report.pdf_url !== '') {
        window.open(`${API_BASE_URL}${normalized.report.pdf_url}`, '_blank');
      } else {
        throw new Error('PDF compilation completed but no download URL was found in the response.');
      }
    } catch (err: any) {
      console.error("PDF generation failed:", err);
      setPdfError(err.message || 'Unable to generate the report. Please try again.');
    } finally {
      setPdfGenerating(false);
    }
  };

  return (
    <div className="app-shell">
      <div className="liquid-bg">
        <div className="liquid-bg-orb" />
      </div>
      <div className="liquid-grid" />
      <div className="floating-orb orb-a" />
      <div className="floating-orb orb-b" />

      <header className="app-navbar">
        <nav className="flex items-center justify-between h-full gap-4">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActivePage('landing')}>
            <div className="logo-shell">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-cyan-400 flex items-center justify-center shadow-[0_0_28px_rgba(99,102,241,0.35)]">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-lg font-extrabold tracking-tight text-white">Founder<span className="text-indigo-300">AI</span></p>
                <p className="text-[10px] uppercase tracking-[0.24em] text-slate-400">AI co-founder OS</p>
              </div>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-2">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => setActivePage(link.id as any)}
                className={`nav-pill ${activePage === link.id ? 'active' : ''}`}
              >
                {link.label}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              aria-label="Notifications"
              title="Notifications"
              className="relative w-10 h-10 rounded-2xl glass-surface border border-white/10 flex items-center justify-center text-slate-300 hover:text-white transition-colors"
            >
              <Bell className="w-4 h-4" />
              <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-cyan-400" />
            </button>
            <button
              type="button"
              aria-label="Open founder profile"
              title="Profile"
              className="w-10 h-10 rounded-full border border-white/10 bg-slate-800/80 flex items-center justify-center text-white font-bold text-xs cursor-pointer hover:border-indigo-400 transition-colors"
            >
              JS
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden w-10 h-10 rounded-2xl glass-surface border border-white/10 flex items-center justify-center text-white"
            >
              {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>
        </nav>

        {mobileMenuOpen && (
          <div className="absolute top-[76px] left-0 right-0 p-4 border-b border-white/10 bg-slate-950/95 backdrop-blur-xl flex flex-col gap-2 z-50">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => {
                  setActivePage(link.id as any);
                  setMobileMenuOpen(false);
                }}
                className={`w-full text-left px-4 py-3 rounded-2xl text-xs font-semibold tracking-wide ${
                  activePage === link.id
                    ? 'text-white bg-white/10 border border-white/10'
                    : 'text-slate-300'
                }`}
              >
                {link.label}
              </button>
            ))}
          </div>
        )}
      </header>

      {/* PAGES AREA */}
      <main className="w-full mt-8 flex-grow relative">
        
        {/* ====================================================
            PAGE: LANDING
            ==================================================== */}
        {activePage === 'landing' && (
          <div className="w-full flex flex-col gap-12 sm:gap-16">
            <section className="site-container min-h-[calc(100vh-120px)] flex flex-col items-center justify-center text-center relative overflow-hidden z-10 w-full py-12 sm:py-16 lg:py-20">
              <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[620px] h-[620px] bg-indigo-500/12 rounded-full blur-[140px]" />
                <div className="absolute top-1/4 left-1/3 w-[360px] h-[360px] bg-cyan-400/10 rounded-full blur-[120px]" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.08),_transparent_35%)]" />
              </div>

              <div className="hero-panel relative z-10 w-full">
                <div className="hero-badge mx-auto">
                  <Sparkles className="w-3.5 h-3.5" /> Premium AI Operating System
                </div>
                <h1 className="hero-title font-display text-white mt-6">
                  Your AI Co-Founder for <span className="text-gradient">every launch milestone</span>
                </h1>
                <p className="hero-subtitle mt-5">
                  FounderAI turns rough ideas into decision-ready operating plans with specialized agents for discovery, validation, funding, legal readiness, and launch execution.
                </p>
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8 w-full sm:w-auto">
                  <button
                    onClick={() => setActivePage('onboarding')}
                    className="hero-cta btn-glass btn-glass-primary w-full sm:w-auto"
                  >
                    Launch My Startup <ArrowRight className="w-4 h-4 ml-2" />
                  </button>
                  <button
                    onClick={() => setActivePage('command')}
                    className="hero-cta btn-glass w-full sm:w-auto border border-white/10"
                  >
                    Explore Command Center
                  </button>
                </div>

                <div className="mt-8 w-full overflow-hidden rounded-[1.6rem] border border-white/10 bg-slate-950/40 p-2 shadow-[0_30px_80px_rgba(0,0,0,0.25)]">
                  <div className="relative h-[280px] sm:h-[360px] overflow-hidden rounded-[1.35rem] border border-white/10 bg-[radial-gradient(circle_at_top,rgba(99,102,241,0.18),transparent_58%)]">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_20%,rgba(255,255,255,0.15),transparent_35%)]" />
                    <SplineScene
                      scene="https://prod.spline.design/0gW5Rraag08rm0sC/scene.splinecode"
                      className="absolute inset-0"
                      fallback={<ProductDashboardMockup />}
                    />
                  </div>
                </div>

                <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
                  {[
                    { label: 'Launch Readiness', value: '97%' },
                    { label: 'Agent Sync', value: '10/10' },
                    { label: 'Weekly Updates', value: 'Live' }
                  ].map((item) => (
                    <div key={item.label} className="metric-card">
                      <p className="text-[10px] uppercase tracking-[0.24em] text-slate-400">{item.label}</p>
                      <p className="text-lg font-semibold text-white mt-1">{item.value}</p>
                    </div>
                  ))}
                </div>

                {/* Infinite Sliding Agent Marquee Conveyor Belt */}
                <div className="w-full overflow-hidden relative py-4 mt-8 border-y border-white/5 bg-slate-900/10 backdrop-blur-sm rounded-2xl">
                  <div className="absolute inset-y-0 left-0 w-16 bg-gradient-to-r from-slate-950/80 to-transparent z-10 pointer-events-none" />
                  <div className="absolute inset-y-0 right-0 w-16 bg-gradient-to-l from-slate-950/80 to-transparent z-10 pointer-events-none" />
                  <div className="flex gap-4 animate-marquee whitespace-nowrap">
                    {[...slidingAgents, ...slidingAgents, ...slidingAgents].map((agent, index) => (
                      <div key={index} className="inline-flex items-center gap-3 px-4 py-2.5 rounded-xl border border-white/5 bg-slate-900/40 min-w-[210px] shadow-[inset_0_1px_1px_rgba(255,255,255,0.02)]">
                        <span className="text-base select-none">{agent.icon}</span>
                        <div className="text-left">
                          <p className="text-xs font-bold text-white tracking-wide">{agent.name}</p>
                          <p className="text-[9px] text-slate-400 font-mono mt-0.5">{agent.role}</p>
                        </div>
                        <span className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.5)]" />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </section>

            <section className="site-container relative overflow-hidden py-4 sm:py-8 z-10 animate-fade-in">
              <div className="page-section flex flex-col lg:flex-row items-start justify-between gap-8 relative overflow-hidden bg-slate-950/20">
                <div className="flex-1 flex flex-col gap-4 text-left max-w-2xl">
                  <span className="text-xs font-extrabold text-[var(--color-primary)] tracking-widest uppercase">The Engine</span>
                  <h2 className="text-clamp-heading font-bold font-display text-white">Interactive AI Command Hub</h2>
                  <p className="text-clamp-body text-[var(--text-secondary)]">
                    Watch specialized autonomous nodes coordinate real-time rule sets, compiling your pitch decks, financial structures, and legal entity registrations simultaneously under a unified brain.
                  </p>
                  <button
                    onClick={() => setActivePage('command')}
                    className="flex items-center gap-1.5 text-xs font-bold text-white hover:text-indigo-400 transition-colors mt-2"
                  >
                    Go to Command Center <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
                <div className="flex-shrink-0 relative w-[280px] h-[280px] sm:w-[380px] sm:h-[380px] flex items-center justify-center my-[-12px] sm:my-0 overflow-hidden mx-auto lg:mx-0">
                  <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/20 to-transparent blur-2xl rounded-full" />
                  <div className="absolute scale-[0.73] sm:scale-100 origin-center flex items-center justify-center">
                    <NeuralBrain nodes={brainNodes.slice(0, 5)} />
                  </div>
                </div>
              </div>
            </section>

            <section className="site-container relative overflow-hidden py-4 sm:py-8 z-10">
              <div className="text-center mb-8 sm:mb-10">
                <h3 className="text-clamp-heading font-bold font-display text-white">Automated Strategic Modules</h3>
                <p className="text-sm text-[var(--text-secondary)] mt-2">Ten agents operating in sync to secure your launch</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {[
                  { id: 'validation', title: 'Idea Validation', desc: 'Runs real-time feasibility and validation scoring to predict potential market traction.' },
                  { id: 'market', title: 'Market Research', desc: 'Aggregates global reports to scale TAM, SAM, SOM metrics and draft buyer personas.' },
                  { id: 'canvas', title: 'Business Model', desc: 'Organizes the 9 boxes of the standard Business Model Canvas with estimated budget ratios.' },
                  { id: 'competitor', title: 'Competitor Analysis', desc: 'Identifies competitor product gaps and drafts custom business SWOT matrix.' },
                  { id: 'funding', title: 'Funding Opportunities', desc: 'Queries grant indices and private VC portfolios matching your exact budget and country.' },
                  { id: 'legal', title: 'Registration & Legal', desc: 'Details required tax forms, founder vesting schedules, and IP protection agreements.' }
                ].map((feat, i) => (
                  <div key={i} className="glass-panel p-5 sm:p-6 border border-white/10 flex flex-col justify-between items-start gap-4 h-full min-h-[210px] bg-slate-900/40 hover:-translate-y-1 transition-transform">
                    <div className="w-11 h-11 rounded-2xl bg-white/8 border border-white/10 flex items-center justify-center text-indigo-300 shadow-[inset_0_1px_1px_rgba(255,255,255,0.08)]">
                      {feat.id === 'validation' && <CheckCircle2 className="w-5 h-5" />}
                      {feat.id === 'market' && <TrendingUp className="w-5 h-5" />}
                      {feat.id === 'canvas' && <Layers className="w-5 h-5" />}
                      {feat.id === 'competitor' && <Target className="w-5 h-5" />}
                      {feat.id === 'funding' && <DollarSign className="w-5 h-5" />}
                      {feat.id === 'legal' && <ShieldCheck className="w-5 h-5" />}
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-white font-display mb-1">{feat.title}</h4>
                      <p className="text-sm text-[var(--text-secondary)] leading-relaxed">{feat.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}

        {/* ====================================================
            PAGE: ONBOARDING WIZARD (DISCOVERY)
            ==================================================== */}
        {activePage === 'onboarding' && (
          <section className="site-container relative overflow-hidden py-12">
            <div className="page-section max-w-3xl mx-auto">
              
              {/* Progress Steps Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
                <div>
                  <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest">Step {wizardStep} of 4</span>
                  <h2 className="text-2xl font-bold font-display text-white mt-1">
                    {wizardStep === 1 && "Detail your startup idea"}
                    {wizardStep === 2 && "Markets & Boundaries"}
                    {wizardStep === 3 && "Operational Stage"}
                    {wizardStep === 4 && "Goal & Core Targets"}
                  </h2>
                </div>
                {/* Horizontal progress bar */}
                <div className="w-full sm:w-32 h-1.5 bg-white/5 rounded-full overflow-hidden">
                  <div className={`h-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all duration-300 progress-fill progress-step-${wizardStep}`} />
                </div>
              </div>

              {/* Wizard Form */}
              <form onSubmit={handleLaunchAnalysis} className="space-y-6">
                
                {/* STEP 1: IDEA DETAILS */}
                {wizardStep === 1 && (
                  <div className="flex flex-col gap-2">
                    <label htmlFor="startup-idea" className="text-xs font-bold text-white">Startup Description / Business Concept</label>
                    <textarea
                      id="startup-idea"
                      value={form.idea}
                      onChange={(e) => setForm({ ...form, idea: e.target.value })}
                      placeholder="Describe your startup idea here — what problem are you solving and for whom?"
                      className="glass-input p-4 w-full h-36 resize-none leading-relaxed text-sm"
                    />
                    <span className="text-[10px] text-[var(--text-secondary)]">Provide the core problem, your proposed solution, and your target audience.</span>
                  </div>
                )}

                {/* STEP 2: DETAILS */}
                {wizardStep === 2 && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Industry Dropdown */}
                    <div className="flex flex-col gap-2">
                      <label htmlFor="industry-segment" className="text-xs font-bold text-white">Niche / Industry Segment</label>
                      <select
                        id="industry-segment"
                        value={industryOther ? '__other__' : form.industry}
                        onChange={(e) => {
                          const val = e.target.value;
                          if (val === '__other__') {
                            setIndustryOther(true);
                            setForm({ ...form, industry: '' });
                          } else {
                            setIndustryOther(false);
                            setForm({ ...form, industry: val });
                          }
                        }}
                        className="glass-input px-4 py-3 w-full"
                      >
                        <option value="" disabled>Select your industry...</option>
                        <option value="SaaS / Software">SaaS / Software</option>
                        <option value="Fintech">Fintech</option>
                        <option value="Healthcare / MedTech">Healthcare / MedTech</option>
                        <option value="EdTech">EdTech</option>
                        <option value="E-commerce / D2C">E-commerce / D2C</option>
                        <option value="Food & Beverage">Food & Beverage</option>
                        <option value="Real Estate / PropTech">Real Estate / PropTech</option>
                        <option value="AgriTech">AgriTech</option>
                        <option value="CleanTech / Energy">CleanTech / Energy</option>
                        <option value="Logistics / Supply Chain">Logistics / Supply Chain</option>
                        <option value="Media & Entertainment">Media & Entertainment</option>
                        <option value="__other__">Others (Custom)</option>
                      </select>
                      {industryOther && (
                        <input
                          type="text"
                          value={form.industry}
                          onChange={(e) => setForm({ ...form, industry: e.target.value })}
                          className="glass-input px-4 py-3 w-full mt-2"
                          placeholder="Type your custom industry..."
                        />
                      )}
                    </div>

                    {/* Country Dropdown */}
                    <div className="flex flex-col gap-2">
                      <label htmlFor="registration-country" className="text-xs font-bold text-white">Primary Country of Registration</label>
                      <select
                        id="registration-country"
                        value={form.country}
                        onChange={(e) => setForm({ ...form, country: e.target.value, state: '', district: '' })}
                        className="glass-input px-4 py-3 w-full"
                      >
                        <option value="" disabled>Select country...</option>
                        {Country.getAllCountries().map((c: ICountry) => (
                          <option key={c.isoCode} value={c.isoCode}>{c.name}</option>
                        ))}
                      </select>
                    </div>

                    {/* State Dropdown */}
                    <div className="flex flex-col gap-2">
                      <label htmlFor="registration-state" className="text-xs font-bold text-white">State / Province</label>
                      <select
                        id="registration-state"
                        value={form.state}
                        onChange={(e) => setForm({ ...form, state: e.target.value, district: '' })}
                        className="glass-input px-4 py-3 w-full"
                        disabled={!form.country}
                      >
                        <option value="" disabled>{form.country ? 'Select state...' : 'Select country first'}</option>
                        {form.country && State.getStatesOfCountry(form.country).map((s: IState) => (
                          <option key={s.isoCode} value={s.isoCode}>{s.name}</option>
                        ))}
                      </select>
                    </div>

                    {/* City/District Dropdown */}
                    <div className="flex flex-col gap-2">
                      <label htmlFor="registration-district" className="text-xs font-bold text-white">City / District</label>
                      <select
                        id="registration-district"
                        value={form.district}
                        onChange={(e) => setForm({ ...form, district: e.target.value })}
                        className="glass-input px-4 py-3 w-full"
                        disabled={!form.state}
                      >
                        <option value="" disabled>{form.state ? 'Select city...' : 'Select state first'}</option>
                        {form.state && form.country && City.getCitiesOfState(form.country, form.state).map((c: ICity) => (
                          <option key={c.name} value={c.name}>{c.name}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                )}

                {/* STEP 3: LOGISTICS */}
                {wizardStep === 3 && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="flex flex-col gap-2">
                      <label htmlFor="founder-name" className="text-xs font-bold text-white">Founder's Name</label>
                      <input
                        id="founder-name"
                        type="text"
                        value={form.founder_name}
                        onChange={(e) => setForm({ ...form, founder_name: e.target.value })}
                        className="glass-input px-4 py-3 w-full"
                        placeholder="Your full name"
                      />
                    </div>
                    <div className="flex flex-col gap-2">
                      <label htmlFor="startup-budget" className="text-xs font-bold text-white">Initial Budget / Capital Pool</label>
                      <input
                        id="startup-budget"
                        type="text"
                        value={form.budget}
                        onChange={(e) => setForm({ ...form, budget: formatBudget(e.target.value, form.country) })}
                        className="glass-input px-4 py-3 w-full"
                        placeholder={`e.g. ${getCurrencySymbol(form.country)}10,000`}
                      />
                    </div>
                    <div className="flex flex-col gap-2">
                      <label htmlFor="venture-stage" className="text-xs font-bold text-white">Current Venture Stage</label>
                      <select
                        id="venture-stage"
                        value={form.stage}
                        onChange={(e) => setForm({ ...form, stage: e.target.value })}
                        className="glass-input px-4 py-3 w-full"
                      >
                        <option value="Idea">Idea Stage</option>
                        <option value="MVP">MVP Complete</option>
                        <option value="Seed">Pre-seed / Seed Fundraise</option>
                      </select>
                    </div>
                    <div className="flex flex-col gap-2">
                      <label htmlFor="team-size" className="text-xs font-bold text-white">Initial Team Size</label>
                      <input
                        id="team-size"
                        type="text"
                        value={form.team_size}
                        onChange={(e) => setForm({ ...form, team_size: e.target.value })}
                        className="glass-input px-4 py-3 w-full"
                        placeholder="e.g. 2"
                      />
                    </div>
                    <div className="flex flex-col gap-2 md:col-span-2">
                      <label htmlFor="target-customer" className="text-xs font-bold text-white">Target Customer Segment</label>
                      <input
                        id="target-customer"
                        type="text"
                        value={form.target_market}
                        onChange={(e) => setForm({ ...form, target_market: e.target.value })}
                        className="glass-input px-4 py-3 w-full"
                        placeholder="e.g. Small business clinics"
                      />
                    </div>
                    <div className="flex flex-col gap-2 md:col-span-2">
                      <label htmlFor="customer-segment" className="text-xs font-bold text-white">Customer Context / Persona Detail</label>
                      <input
                        id="customer-segment"
                        type="text"
                        value={form.customer_segment}
                        onChange={(e) => setForm({ ...form, customer_segment: e.target.value })}
                        className="glass-input px-4 py-3 w-full"
                        placeholder="e.g. Independent clinic owners and billing managers"
                      />
                    </div>
                  </div>
                )}

                {/* STEP 4: GOALS */}
                {wizardStep === 4 && (
                  <div className="flex flex-col gap-6">
                    <div className="p-4 rounded-xl bg-white/2 border border-white/5">
                      <h4 className="text-xs font-bold text-white mb-2">Startup OS Configuration Ready</h4>
                      <p className="text-xs text-[var(--text-secondary)] leading-5">
                        FounderAI will configure 10 automated agents to run a structured LangGraph sequential pipeline. The final package will contain validation scores, registration files, NDAs, and a detailed Reports folder.
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <input id="agree" type="checkbox" defaultChecked className="w-4 h-4 rounded bg-indigo-500/10 border border-white/10" aria-label="Authorize orchestrator to fetch references" />
                      <label htmlFor="agree" className="text-[11px] text-[var(--text-secondary)]">I authorize the core AI orchestrator to spin nodes and fetch web references.</label>
                    </div>
                  </div>
                )}

                {/* Navigation Buttons */}
                <div className="flex items-center justify-between border-t border-white/5 pt-6 mt-8">
                  {wizardStep > 1 ? (
                    <button
                      type="button"
                      onClick={() => setWizardStep(prev => prev - 1)}
                      className="btn-glass px-6 py-3 text-xs font-bold"
                    >
                      Back
                    </button>
                  ) : <div />}

                  {wizardStep < 4 ? (
                    <button
                      type="button"
                      onClick={() => setWizardStep(prev => prev + 1)}
                      className="btn-glass btn-glass-primary px-6 py-3 text-xs font-bold"
                    >
                      Next Step <ChevronRight className="w-4 h-4 ml-1" />
                    </button>
                  ) : (
                    <button
                      type="submit"
                      disabled={loading}
                      className="btn-glass btn-glass-primary px-8 py-3.5 text-xs font-bold"
                    >
                      {loading ? 'Launching OS...' : 'Launch AI Analysis'} <Play className="w-4 h-4 ml-1.5" />
                    </button>
                  )}
                </div>
              </form>
            </div>
          </section>
        )}

        {/* ====================================================
            PAGE: AI COMMAND CENTER
            ==================================================== */}
        {activePage === 'command' && (
          <section className="site-container relative overflow-hidden py-8 flex flex-col gap-8 animate-fade-in">
            <div className="w-full flex flex-col md:flex-row gap-8 items-stretch">
              
              {/* Left Column: Capability Module Library */}
              <div className="page-section flex-1 relative overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(99,102,241,0.16),transparent_45%)]" />
                <div className="relative z-10 flex flex-col gap-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <span className="text-[10px] font-bold text-indigo-400 tracking-widest uppercase">Capability Module Library</span>
                      <h3 className="text-lg font-bold font-display text-white mt-1">Six high-fidelity operating modules</h3>
                    </div>
                    <span className="px-2.5 py-1 rounded-full border border-emerald-500/20 bg-emerald-500/10 text-[10px] font-bold uppercase tracking-wider text-emerald-300">
                      Live
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
                    {capabilityModules.map((module, index) => {
                      const Icon = module.icon;
                      return (
                        <div key={module.title} className="module-grid-card group">
                          <div className={`absolute inset-x-0 top-0 h-20 bg-gradient-to-r ${module.accent} opacity-80`} />
                          <div className="relative z-10 flex flex-col gap-3 p-3 sm:p-4">
                            <div className="flex items-center justify-between">
                              <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-white/10 bg-slate-950/70 text-white shadow-[0_0_20px_rgba(99,102,241,0.12)]">
                                <Icon className="w-4.5 h-4.5" />
                              </div>
                              <span className="text-[10px] font-semibold uppercase tracking-[0.24em] text-slate-400">0{index + 1}</span>
                            </div>

                            <div className={`module-card-visual module-card-visual-${module.visual}`}>
                              <div className="module-card-orb" />
                              <div className="module-card-line line-a" />
                              <div className="module-card-line line-b" />
                              <div className="module-card-node node-a" />
                              <div className="module-card-node node-b" />
                              <div className="module-card-node node-c" />
                            </div>

                            <div>
                              <h4 className="text-sm font-semibold text-white">{module.title}</h4>
                              <p className="mt-1 text-[11px] leading-5 text-slate-400">{module.description}</p>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Right Column: Active Agents Monitor */}
              <div className="w-full md:w-[450px] page-section flex flex-col justify-between gap-6">
                <div className="flex flex-col gap-4">
                  <div className="flex justify-between items-center border-b border-white/5 pb-3">
                    <h3 className="text-base font-bold font-display text-white">AI Agent Register</h3>
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20 text-indigo-300">10 ACTIVE NODES</span>
                  </div>
                  
                  {/* Agents list scroll panel */}
                  <div className="space-y-2.5 max-h-[350px] overflow-y-auto pr-1">
                    {agents.map((agent) => (
                      <div
                        key={agent.id}
                        className={`p-3 rounded-xl border transition-all flex items-center justify-between text-xs ${
                          agent.status === 'active'
                            ? 'bg-indigo-500/5 border-indigo-500/30'
                            : agent.status === 'completed'
                            ? 'bg-emerald-500/5 border-emerald-500/15'
                            : 'bg-white/2 border-white/5 opacity-60'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-[10px] ${
                            agent.status === 'active'
                              ? 'bg-indigo-500 text-white'
                              : agent.status === 'completed'
                              ? 'bg-emerald-500 text-slate-950'
                              : 'bg-slate-800 text-slate-400'
                          }`}>
                            {agent.id.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <h4 className="font-bold text-white">{agent.name}</h4>
                            <p className="text-[10px] text-[var(--text-secondary)] mt-0.5">{agent.role}</p>
                          </div>
                        </div>
                        <span className={`text-[10px] font-bold ${
                          agent.status === 'active'
                            ? 'text-indigo-400 animate-pulse'
                            : agent.status === 'completed'
                            ? 'text-emerald-400'
                            : 'text-slate-500'
                        }`}>
                          {agent.status === 'active' ? 'PROCESSING' : agent.status === 'completed' ? 'COMPLETED' : 'IDLE'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Simulated Trigger Panel */}
                <div className="flex flex-col sm:flex-row items-center gap-3 border-t border-white/5 pt-4">
                  <button
                    onClick={handleLaunchAnalysis}
                    className="w-full sm:flex-1 btn-glass btn-glass-primary py-3 text-xs font-bold"
                  >
                    Re-run Orchestrator <RotateCcw className="w-4 h-4 ml-1.5" />
                  </button>
                  <button
                    onClick={() => setActivePage('dashboard')}
                    className="w-full sm:w-auto btn-glass px-5 py-3 text-xs font-bold"
                  >
                    Enter Dashboard
                  </button>
                </div>
              </div>
            </div>

            {/* Console Log Terminal & Orchestration Timeline */}
            <div className="w-full page-section flex flex-col gap-5 rounded-2xl relative shadow-2xl bg-slate-950/50 p-6 border border-white/10">
              <div className="flex items-center justify-between border-b border-white/5 pb-2">
                <div className="flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-indigo-400 animate-pulse" />
                  <span className="text-xs font-bold text-white tracking-wider uppercase font-display">System Orchestrator Core</span>
                </div>
              </div>
              
              <OrchestrationTimeline progress={orchestratorProgress} />
              
              <div className="grid grid-cols-1 md:grid-cols-12 gap-4 mt-2">
                {/* Console Log Terminal */}
                <div className="md:col-span-12 font-mono text-[11px] bg-slate-950/80 rounded-xl p-4 border border-white/5 flex flex-col gap-3">
                  <div className="flex items-center justify-between border-b border-white/5 pb-2">
                    <div className="flex items-center gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-red-500/80" />
                      <div className="w-2 h-2 rounded-full bg-yellow-500/80" />
                      <div className="w-2 h-2 rounded-full bg-green-500/80" />
                      <span className="text-[10px] text-slate-500 font-bold ml-1.5">founder_ai_os_core.log</span>
                    </div>
                    <button
                      onClick={() => setConsoleLogs([])}
                      className="text-[9px] text-slate-500 hover:text-slate-300 font-bold"
                    >
                      Clear console
                    </button>
                  </div>
                  <div className="h-28 overflow-y-auto space-y-1.5 pr-2 text-slate-400 leading-relaxed scroll-glass">
                    {consoleLogs.length === 0 ? (
                      <p className="text-slate-600 italic">No activity logged. Trigger analysis to start monitors.</p>
                    ) : (
                      consoleLogs.map((log, index) => (
                        <p key={index} className="break-all whitespace-pre-wrap">{log}</p>
                      ))
                    )}
                    <div ref={terminalEndRef} />
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* ====================================================
            PAGE: DASHBOARD
            ==================================================== */}
        {activePage === 'dashboard' && (
          <section className="site-container relative overflow-hidden py-8 flex flex-col gap-8 animate-fade-in">
            {/* Header info */}
            <div className="page-section w-full flex flex-col md:flex-row justify-between items-start md:items-center gap-4 relative overflow-hidden">
              <div>
                <span className="px-2.5 py-0.5 text-[9px] font-bold tracking-widest text-[var(--color-accent)] bg-cyan-500/10 rounded border border-cyan-500/25 uppercase">
                  COMPILATION COMPLETE
                </span>
                <h2 className="text-2xl font-bold font-display text-white mt-1.5">{form.idea}</h2>
                <p className="text-xs text-[var(--text-secondary)] mt-1">
                  Venture strategy package compiled for <b>{form.founder_name}</b> ({form.stage} stage)
                </p>
              </div>
              <div className="flex flex-col items-end gap-2 w-full md:w-auto">
                <button
                  onClick={handleDownloadPDF}
                  disabled={pdfGenerating}
                  className={`flex items-center gap-2 px-5 py-3 rounded-xl text-white text-xs font-bold tracking-wide transition-all w-full md:w-auto justify-center ${
                    pdfGenerating
                      ? 'bg-slate-800 border border-white/10 cursor-not-allowed opacity-75'
                      : 'bg-gradient-to-r from-indigo-500 to-violet-600 hover:shadow-lg hover:shadow-indigo-500/20 hover:-translate-y-0.5'
                  }`}
                >
                  {pdfGenerating ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Generating Report...
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4" /> Download PDF Report
                    </>
                  )}
                </button>
                {pdfError && (
                  <span className="text-[10px] text-rose-400 font-medium">
                    {pdfError} <button onClick={handleDownloadPDF} className="underline hover:text-white ml-1 font-bold">Retry</button>
                  </span>
                )}
              </div>
            </div>

            {/* Top Score Cards Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
              {[
                { label: 'Startup Score', val: `${result.validation?.validation_score ?? 87}%`, color: 'text-indigo-400' },
                { label: 'Feasibility', val: `${result.validation?.feasibility_score ?? 92}%`, color: 'text-emerald-400' },
                { label: 'Market Opportunity', val: 'High', color: 'text-cyan-400' },
                { label: 'Funding Potential', val: `${result.funding?.investment_readiness_score ?? 78}%`, color: 'text-amber-400' },
                { label: 'Registration File', val: 'Ready', color: 'text-teal-400' },
                { label: 'Business Readiness', val: 'Strong', color: 'text-purple-400' }
              ].map((card, i) => (
                <div key={i} className="glass-panel p-4 border border-white/5 flex flex-col justify-between items-start gap-1 bg-slate-900/40">
                  <span className="text-[10px] text-[var(--text-secondary)] font-bold uppercase">{card.label}</span>
                  <span className={`text-xl font-extrabold font-display ${card.color}`}>{card.val}</span>
                </div>
              ))}
            </div>

            {/* Main grid panels */}
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
              
              {/* Left Side: Summary & Quick Actions */}
              <div className="md:col-span-8 flex flex-col gap-8">
                
                {/* Executive summary block */}
                <div className="glass-card border border-white/5 p-4 sm:p-6 bg-slate-950/20">
                  <h3 className="text-lg font-bold font-display text-white mb-4">Core Executive Synthesis</h3>
                  <p className="text-sm leading-6 text-[var(--text-secondary)]">
                    {result.report?.executive_summary}
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
                    <div className="p-4 rounded-xl bg-indigo-500/5 border border-indigo-500/10">
                      <span className="text-[9px] uppercase font-bold text-indigo-400">Unique USP</span>
                      <p className="text-xs text-[var(--text-secondary)] mt-1.5">{result.discovery?.usp}</p>
                    </div>
                    <div className="p-4 rounded-xl bg-red-500/5 border border-red-500/10">
                      <span className="text-[9px] uppercase font-bold text-rose-400">Top Venture Risk</span>
                      <p className="text-xs text-[var(--text-secondary)] mt-1.5">{result.validation?.critical_risks?.[0]}</p>
                    </div>
                    <div className="p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/10">
                      <span className="text-[9px] uppercase font-bold text-emerald-400">Target Segment</span>
                      <p className="text-xs text-[var(--text-secondary)] mt-1.5">{form.target_market}</p>
                    </div>
                  </div>
                </div>

                {/* Quick Actions Panel */}
                <div className="glass-card border border-white/5 p-4 sm:p-6 bg-slate-950/20">
                  <h3 className="text-lg font-bold font-display text-white mb-4">Core Deliverable Files</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { title: 'Business Plan', action: 'Download JSON', page: 'reports', tab: 'canvas' },
                      { title: 'Pitch Deck Checklist', action: 'View Checklist', page: 'reports', tab: 'funding' },
                      { title: 'GTM Channels', action: 'Open Roadmap', page: 'roadmap', tab: '' },
                      { title: 'Incorporation File', action: 'Verify Compliance', page: 'reports', tab: 'registration' }
                    ].map((act, i) => (
                      <button
                        key={i}
                        onClick={() => {
                          setActivePage(act.page as any);
                          if (act.tab) setActiveReportTab(act.tab as any);
                        }}
                        className="p-4 rounded-xl border border-white/5 bg-white/2 hover:bg-white/5 hover:border-indigo-500/30 text-left transition-all"
                      >
                        <h4 className="text-xs font-bold text-white">{act.title}</h4>
                        <span className="text-[10px] text-[var(--color-primary)] font-bold mt-2 inline-flex items-center gap-1">
                          {act.action} <ChevronRight className="w-3.5 h-3.5" />
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Side: Activity & Milestones */}
              <div className="md:col-span-4 flex flex-col gap-8">
                
                {/* 30/60/90 Preview */}
                <div className="page-section flex-grow">
                  <h3 className="text-lg font-bold font-display text-white mb-4">Milestone Roadmap</h3>
                  <div className="relative border-l border-white/10 pl-5 space-y-6">
                    {result.roadmap?.roadmap_phases?.slice(0, 3).map((phase, idx) => (
                      <div key={idx} className="relative">
                        <div className="absolute -left-[25px] top-0 w-2.5 h-2.5 rounded-full bg-indigo-500 border border-slate-950 shadow" />
                        <span className="text-[9px] font-bold text-indigo-400 uppercase tracking-widest">{phase.duration}</span>
                        <h4 className="text-xs font-bold text-white mt-0.5">{phase.phase}</h4>
                        <p className="text-[10px] text-[var(--text-secondary)] mt-1">• {phase.milestones?.[0]}</p>
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={() => setActivePage('roadmap')}
                    className="w-full text-center text-xs font-bold text-[var(--color-primary)] hover:text-indigo-400 mt-6 inline-flex justify-center items-center gap-1"
                  >
                    Open Complete Timeline <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* ====================================================
            PAGE: REPORTS
            ==================================================== */}
        {activePage === 'reports' && (
          <section className="site-container relative overflow-hidden py-8 flex flex-col gap-8 animate-fade-in">
            {/* Header */}
            <div className="w-full flex justify-between items-center border-b border-white/5 pb-4">
              <div>
                <h2 className="page-title">Venture Analysis Reports</h2>
                <p className="page-copy">Toggle sub-modules generated by specialized agents</p>
              </div>
              <div className="flex items-center gap-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleDownloadPDF}
                  disabled={pdfGenerating}
                  className={`btn-glass-primary px-5 py-2.5 text-xs font-bold flex items-center gap-2 transition-all ${
                    pdfGenerating ? 'opacity-70 cursor-not-allowed' : ''
                  }`}
                >
                  {pdfGenerating ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      <span>Compiling...</span>
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4" /> <span>Export PDF</span>
                    </>
                  )}
                </motion.button>
                {pdfError && (
                  <span className="text-[10px] text-rose-400 font-medium">
                    Fail <button onClick={handleDownloadPDF} className="underline hover:text-white font-bold">Retry</button>
                  </span>
                )}
              </div>
            </div>

            {/* Sub-navigation Tabs */}
            <div className="responsive-tabs flex flex-wrap gap-2 mb-8 bg-slate-900/40 p-1.5 rounded-2xl border border-white/5 w-fit">
              {[
                { id: 'overview', label: 'Summary & Core' },
                { id: 'market', label: 'TAM/SAM/SOM' },
                { id: 'competitors', label: 'SWOT & Price' },
                { id: 'canvas', label: '9-Box Canvas' },
                { id: 'registration', label: 'Entity Registry' },
                { id: 'funding', label: 'Grants & VCs' },
                { id: 'legal', label: 'Contracts Legal' }
              ].map(tab => {
                const isActive = activeReportTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveReportTab(tab.id as any)}
                    className={`relative px-4 py-2 text-xs font-bold rounded-xl transition-colors z-10 ${
                      isActive ? 'text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
                    }`}
                  >
                    {isActive && (
                      <motion.div
                        layoutId="activeTabIndicator"
                        className="absolute inset-0 bg-indigo-500/20 border border-indigo-500/30 rounded-xl -z-10"
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      />
                    )}
                    {tab.label}
                  </button>
                );
              })}
            </div>

            {/* TAB CONTENTS */}
            <div className="w-full">
              
              {/* TAB: OVERVIEW */}
              {activeReportTab === 'overview' && (
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
                  <div className="md:col-span-8 page-section p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Concept Extraction</h3>
                    <div className="space-y-4 text-sm leading-6 text-[var(--text-secondary)]">
                      <div>
                        <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-1">Proposed Idea</h4>
                        <p>{result.startup?.idea}</p>
                      </div>
                      <div className="border-t border-white/5 pt-4">
                        <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-1">Identified Problem Statement</h4>
                        <p>{result.discovery?.problem}</p>
                      </div>
                      <div className="border-t border-white/5 pt-4">
                        <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-1">Proposed Solution</h4>
                        <p>{result.discovery?.solution}</p>
                      </div>
                    </div>
                  </div>
                  <div className="md:col-span-4 page-section p-6 flex flex-col justify-between">
                    <div>
                      <h3 className="text-base font-bold font-display text-white mb-4">Venture Score</h3>
                      <div className="text-center py-6 bg-slate-900/30 rounded-2xl border border-white/5">
                        <span className="text-4xl font-extrabold text-[var(--color-primary)]">{result.validation?.validation_score}%</span>
                        <p className="text-[10px] text-[var(--text-secondary)] uppercase mt-1">Validation Quotient</p>
                      </div>
                    </div>
                    <div className="space-y-2 mt-4">
                      <div className="flex justify-between text-xs">
                        <span className="text-[var(--text-secondary)]">Feasibility</span>
                        <span className="font-bold text-white">{result.validation?.feasibility_score}%</span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-[var(--text-secondary)]">PM-Fit Probability</span>
                        <span className="font-bold text-white">{result.validation?.market_fit_score}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB: MARKET */}
              {activeReportTab === 'market' && (
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
                  <div className="md:col-span-6 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Market Segmentation Sizing</h3>
                    <div className="space-y-4">
                      {[
                        { label: 'TAM (Total Addressable Market)', val: result.market?.TAM, pct: 100, color: 'bg-indigo-500' },
                        { label: 'SAM (Serviceable Addressable Market)', val: result.market?.SAM, pct: 45, color: 'bg-purple-500' },
                        { label: 'SOM (Serviceable Obtainable Market)', val: result.market?.SOM, pct: 15, color: 'bg-cyan-500' }
                      ].map((item, index) => (
                        <div key={index} className="p-4 rounded-xl bg-white/2 border border-white/5">
                          <div className="flex justify-between items-center text-xs mb-1">
                            <span className="font-bold text-white">{item.label}</span>
                            <span className="text-[10px] text-slate-400">{item.pct}%</span>
                          </div>
                          <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden mb-2">
                            <div className={`h-full ${item.color} progress-fill progress-${item.pct}`} />
                          </div>
                          <p className="text-[11px] text-[var(--text-secondary)] leading-5">{item.val}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="md:col-span-6 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Market Trends & Sources</h3>
                    <div className="space-y-3">
                      <h5 className="text-xs font-bold text-white uppercase tracking-wider">Key Market Trends:</h5>
                      <ul className="space-y-1">
                        {result.market?.market_trends?.map((p: string, i: number) => (
                          <li key={i} className="text-xs text-[var(--text-secondary)]">• {p}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="space-y-3 mt-4">
                      <h5 className="text-xs font-bold text-white uppercase tracking-wider">Research Sources:</h5>
                      <ul className="space-y-1">
                        {result.market?.sources?.map((s: string, i: number) => (
                          <li key={i} className="text-xs text-[var(--text-secondary)]">• {s}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB: COMPETITORS */}
              {activeReportTab === 'competitors' && (
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
                  <div className="md:col-span-7 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Competitor Mapping</h3>
                    <div className="space-y-3">
                      {result.competitors?.real_competitors?.map((comp: any, idx: number) => (
                        <div key={idx} className="p-4 rounded-xl bg-white/2 border border-white/5 flex justify-between items-center">
                          <div>
                            <h4 className="text-xs font-bold text-white">{comp.name}</h4>
                            <p className="text-[10px] text-[var(--text-secondary)] mt-1">Market Gap: {comp.gap}</p>
                          </div>
                          <span className={`text-[9px] font-bold px-2 py-0.5 rounded ${
                            comp.threat_level === 'High' ? 'bg-red-500/10 text-rose-400 border border-red-500/25' : 'bg-amber-500/10 text-amber-400 border border-amber-500/25'
                          }`}>
                            THREAT: {comp.threat_level?.toUpperCase()}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="md:col-span-5 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">SWOT Analysis Matrix</h3>
                    <div className="grid grid-cols-2 gap-3 text-[10px]">
                      <div className="p-3 rounded-lg bg-emerald-500/5 border border-emerald-500/10">
                        <span className="font-bold text-emerald-400 uppercase">Strengths</span>
                        <p className="mt-1 text-[var(--text-secondary)]">{result.competitors?.strengths?.[0] || 'N/A'}</p>
                      </div>
                      <div className="p-3 rounded-lg bg-red-500/5 border border-red-500/10">
                        <span className="font-bold text-rose-400 uppercase">Weaknesses</span>
                        <p className="mt-1 text-[var(--text-secondary)]">{result.competitors?.weaknesses?.[0] || 'N/A'}</p>
                      </div>
                      <div className="p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/10">
                        <span className="font-bold text-cyan-400 uppercase">Opportunities</span>
                        <p className="mt-1 text-[var(--text-secondary)]">{result.competitors?.gap_analysis || 'N/A'}</p>
                      </div>
                      <div className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/10">
                        <span className="font-bold text-amber-400 uppercase">Threats</span>
                        <p className="mt-1 text-[var(--text-secondary)]">{result.competitors?.real_competitors?.[0]?.threat_level || 'N/A'}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB: CANVAS */}
              {activeReportTab === 'canvas' && (
                <div className="page-section p-6">
                  <h3 className="text-base font-bold font-display text-white mb-4">Business Model Canvas (9 Boxes)</h3>
                  
                  {/* Grid Layout representing standard BMC */}
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                    
                    {/* Key Partners */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl md:row-span-2">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Key Partners</h4>
                      <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                        {result.business_model?.key_partners?.map((x, i) => <li key={i}>• {x}</li>)}
                      </ul>
                    </div>

                    {/* Key Activities */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Key Activities</h4>
                      <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                        {result.business_model?.activities?.map((x: string, i: number) => <li key={i}>• {x}</li>)}
                      </ul>
                    </div>

                    {/* Value Propositions */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl md:row-span-2">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Value Propositions</h4>
                      <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                        {result.business_model?.value_proposition?.map((x: string, i: number) => <li key={i}>• {x}</li>)}
                      </ul>
                    </div>

                    {/* Customer Relationships (Not in Schema, replaced with Revenue Model text) */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Revenue Model</h4>
                      <p className="text-xs text-[var(--text-secondary)] leading-5">{result.business_model?.revenue_model}</p>
                    </div>

                    {/* Customer Segments */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl md:row-span-2">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Customer Segments</h4>
                      <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                        {result.business_model?.customer_segments?.map((x: string, i: number) => <li key={i}>• {x}</li>)}
                      </ul>
                    </div>

                    {/* Key Resources */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Key Resources</h4>
                      <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                        {result.business_model?.key_resources?.map((x: string, i: number) => <li key={i}>• {x}</li>)}
                      </ul>
                    </div>

                    {/* Channels */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Channels</h4>
                      <ul className="space-y-1.5 text-xs text-[var(--text-secondary)]">
                        {result.business_model?.channels?.map((x: string, i: number) => <li key={i}>• {x}</li>)}
                      </ul>
                    </div>

                    {/* Cost Structure & Revenue Streams -> Replaced with Pricing Strategy text for width */}
                    <div className="p-4 bg-white/2 border border-white/5 rounded-xl md:col-span-5">
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-2">Pricing Strategy</h4>
                      <p className="text-xs text-[var(--text-secondary)] leading-5">{result.business_model?.pricing_strategy}</p>
                    </div>

                  </div>
                </div>
              )}

              {/* TAB: REGISTRATION */}
              {activeReportTab === 'registration' && (
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
                  <div className="md:col-span-7 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Registration & Filings</h3>
                    <div className="space-y-4">
                      <div className="p-4 rounded-xl bg-white/2 border border-white/5">
                        <span className="text-[9px] uppercase tracking-wider text-indigo-300">Entity Recommendation</span>
                        <h4 className="text-sm font-bold text-white mt-1">{result.registration?.company_type_recommendation}</h4>
                        <p className="text-xs text-[var(--text-secondary)] mt-2 leading-5">{result.registration?.country_specific}</p>
                      </div>
                      <div className="p-4 rounded-xl bg-white/2 border border-white/5">
                        <span className="text-[9px] uppercase tracking-wider text-indigo-300">Intellectual Property</span>
                        <h4 className="text-sm font-bold text-white mt-1">Trademark Proposal</h4>
                        <p className="text-xs text-[var(--text-secondary)] mt-2 leading-5">{result.registration?.trademark_recommendation}</p>
                      </div>
                    </div>
                  </div>
                  <div className="md:col-span-5 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Licenses Required</h3>
                    <ul className="space-y-2">
                      {result.registration?.required_licenses?.map((lic, i) => (
                        <li key={i} className="text-xs text-[var(--text-secondary)] flex items-start gap-2">
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" /> {lic}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* TAB: FUNDING */}
              {activeReportTab === 'funding' && (
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
                  <div className="md:col-span-7 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Government Grants Matched</h3>
                    <div className="space-y-3">
                      {result.funding?.government_grants?.map((grant, i) => (
                        <div key={i} className="p-4 rounded-xl bg-white/2 border border-white/5 flex justify-between items-center text-xs">
                          <div>
                            <h4 className="font-bold text-white">{grant.name}</h4>
                            <p className="text-[10px] text-slate-400 mt-1">{grant.description}</p>
                          </div>
                          <span className="font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded">
                            {grant.amount}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="md:col-span-5 glass-panel p-6">
                    <h3 className="text-base font-bold font-display text-white mb-4">Bootstrap Strategy</h3>
                    <p className="text-xs text-[var(--text-secondary)] leading-6 bg-white/2 border border-white/5 p-4 rounded-xl">
                      {result.funding?.bootstrap_strategy}
                    </p>
                  </div>
                </div>
              )}

              {/* TAB: LEGAL */}
              {activeReportTab === 'legal' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {[
                    { title: 'Co-Founder Agreements', items: result.legal?.co_founder_agreement_reqs },
                    { title: 'Intellectual Property Shield', items: result.legal?.ip_assignment_reqs },
                    { title: 'NDA Guidelines', items: result.legal?.nda_reqs }
                  ].map((block, index) => (
                    <div key={index} className="glass-panel p-6">
                      <h3 className="text-sm font-bold font-display text-white mb-4">{block.title}</h3>
                      <ul className="space-y-3">
                        {block.items?.map((item, idx) => (
                          <li key={idx} className="text-xs text-[var(--text-secondary)] leading-5 flex items-start gap-2">
                            <span className="text-indigo-400 flex-shrink-0">•</span> {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}

            </div>
          </section>
        )}

        {/* ====================================================
            PAGE: ROADMAP
            ==================================================== */}
        {activePage === 'roadmap' && (
          <section className="site-container relative overflow-hidden py-8 flex flex-col gap-8 animate-fade-in">
            <div className="w-full flex justify-between items-center border-b border-white/5 pb-4">
              <div>
                <h2 className="page-title">Go-To-Market Timeline</h2>
                <p className="page-copy">30/60/90-Day launching roadmaps and GTM milestones</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
              
              {/* Left Column: Acquisition Channels */}
              <div className="md:col-span-4 glass-panel p-4 sm:p-6 flex flex-col gap-4">
                <h3 className="text-base font-bold font-display text-white">Acquisition Marketing</h3>
                <p className="text-xs text-[var(--text-secondary)] leading-5">
                  Proposed distribution channels generated by your GTM agent:
                </p>
                <div className="flex flex-col gap-2 mt-2">
                  {result.roadmap?.go_to_market_channels?.map((chan, i) => (
                    <div key={i} className="p-3 rounded-xl bg-white/2 border border-white/5 text-xs text-white font-bold">
                      {i + 1}. {chan}
                    </div>
                  ))}
                </div>
              </div>

              {/* Right Column: Execution Timeline (Vertical List) */}
              <div className="md:col-span-8 page-section p-4 sm:p-8 bg-slate-950/40 border border-white/5 rounded-3xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none" />
                <h3 className="text-xl font-bold font-display text-white mb-8">Milestone Tracker</h3>
                <div className="relative pl-6 sm:pl-8 border-l border-slate-800/60 space-y-12">
                  {result.roadmap?.roadmap_phases?.map((phase, idx) => {
                    // Color mapping based on phase index
                    const colors = [
                      { text: 'text-amber-400', border: 'border-amber-400/50', bg: 'bg-amber-400/10', glow: 'shadow-[0_0_15px_rgba(251,191,36,0.3)]' },
                      { text: 'text-emerald-400', border: 'border-emerald-400/50', bg: 'bg-emerald-400/10', glow: 'shadow-[0_0_15px_rgba(52,211,153,0.3)]' },
                      { text: 'text-indigo-400', border: 'border-indigo-400/50', bg: 'bg-indigo-400/10', glow: 'shadow-[0_0_15px_rgba(99,102,241,0.3)]' },
                      { text: 'text-cyan-400', border: 'border-cyan-400/50', bg: 'bg-cyan-400/10', glow: 'shadow-[0_0_15px_rgba(34,211,238,0.3)]' },
                    ];
                    const theme = colors[idx % colors.length];

                    return (
                      <motion.div 
                        key={idx} 
                        initial={{ opacity: 0, x: 20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true, margin: "-50px" }}
                        transition={{ duration: 0.5, delay: idx * 0.15 }}
                        className="relative"
                      >
                        {/* Timeline Node Marker */}
                        <div className={`absolute -left-[31px] sm:-left-[39px] top-1 w-4 h-4 rounded-full border-2 ${theme.border} ${theme.bg} ${theme.glow} flex items-center justify-center`}>
                          <div className={`w-1.5 h-1.5 rounded-full bg-current ${theme.text}`} />
                        </div>
                        
                        <div className="glass-panel p-5 sm:p-6 border border-white/5 hover:border-white/10 transition-colors bg-slate-900/40">
                          <span className={`text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-md bg-white/5 border border-white/10 ${theme.text}`}>
                            {phase.duration}
                          </span>
                          <h4 className="text-lg font-bold text-white mt-3">{phase.phase}</h4>
                          <ul className="mt-5 space-y-3">
                            {phase.milestones?.map((ms, i) => (
                              <li key={i} className="text-sm text-slate-300 flex items-start gap-3 bg-white/[0.02] p-3 rounded-lg border border-white/[0.03]">
                                <div className={`w-5 h-5 rounded-full ${theme.bg} ${theme.border} flex items-center justify-center flex-shrink-0 mt-0.5`}>
                                  <CheckCircle2 className={`w-3 h-3 ${theme.text}`} />
                                </div>
                                <span className="leading-relaxed">{ms}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>

            </div>
          </section>
        )}

        {/* ====================================================
            PAGE: AGENTS PROFILE CARDS
            ==================================================== */}
        {activePage === 'agents' && (
          <section className="site-container relative overflow-hidden py-8 flex flex-col gap-8 animate-fade-in">
            <div className="flex flex-col gap-2">
              <h2 className="page-title">AI Agent Directory</h2>
              <p className="page-copy">Autonomous workspace processes configuring your startup blueprint</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents.map((agent) => (
                <div key={agent.id} className="glass-panel p-4 sm:p-6 border border-white/5 flex flex-col justify-between items-stretch gap-6 bg-slate-900/40">
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white font-bold text-xs shadow-md">
                        {agent.id.substring(0, 2).toUpperCase()}
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-white font-display">{agent.name}</h3>
                        <span className="text-[9px] uppercase tracking-wider text-indigo-400">{agent.role}</span>
                      </div>
                    </div>
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/25 text-emerald-400">
                      ACCURACY: {agent.accuracy}%
                    </span>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <span className="text-[9px] uppercase tracking-widest text-slate-500 font-bold">Capabilities</span>
                      <div className="flex flex-wrap gap-1.5 mt-1.5">
                        {agent.capabilities.map((cap, i) => (
                          <span key={i} className="px-2 py-0.5 rounded bg-white/2 border border-white/5 text-[9px] text-[var(--text-secondary)]">
                            {cap}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-[10px] border-t border-white/5 pt-3">
                      <span className="text-slate-500">Last run: {agent.lastExecution}</span>
                      <span className="text-emerald-400 font-bold">Completed</span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => alert(`Running ${agent.name}...`)}
                      className="flex-1 btn-glass py-2.5 text-[11px] font-bold"
                    >
                      Run Again
                    </button>
                    <button
                      onClick={() => alert(`Details for ${agent.name}`)}
                      className="btn-glass px-3.5 py-2.5 text-[11px] font-bold"
                    >
                      Logs
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* ====================================================
            PAGE: SETTINGS
            ==================================================== */}
        {activePage === 'settings' && (
          <section className="site-container relative overflow-hidden py-8 animate-fade-in">
            <div className="w-full max-w-3xl mx-auto glass-card p-4 sm:p-8 border border-white/5 bg-slate-950/20 flex flex-col gap-8">
              <div>
                <h2 className="page-title">System Settings</h2>
                <p className="page-copy">Frontend mock configuration panels</p>
              </div>

              <div className="space-y-6">
                
                {/* Profile Panel */}
                <div className="p-4 sm:p-5 rounded-2xl border border-white/5 bg-white/2 space-y-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <User className="w-4 h-4 text-indigo-400" /> Founder Profile
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="flex flex-col gap-1.5">
                      <label htmlFor="profile-name" className="text-[10px] text-slate-400 uppercase font-bold">Founder Name</label>
                      <input id="profile-name" type="text" defaultValue="Dr. Jane Smith" className="glass-input px-3.5 py-2.5" />
                    </div>
                    <div className="flex flex-col gap-1.5">
                      <label htmlFor="profile-email" className="text-[10px] text-slate-400 uppercase font-bold">Email Address</label>
                      <input id="profile-email" type="email" defaultValue="jane.smith@apex.com" className="glass-input px-3.5 py-2.5" />
                    </div>
                  </div>
                </div>

                {/* API Config Panel */}
                <div className="p-4 sm:p-5 rounded-2xl border border-white/5 bg-white/2 space-y-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <FileCode className="w-4 h-4 text-indigo-400" /> API Configuration
                  </h3>
                  <div className="flex flex-col gap-2">
                    <label htmlFor="api-host" className="text-[10px] text-slate-400 uppercase font-bold">Target REST API Host</label>
                    <input id="api-host" type="text" defaultValue={API_BASE_URL} className="glass-input px-3.5 py-2.5" />
                    <span className="text-[9px] text-slate-500">Configure to point to local or cloud-deployed FastAPI orchestrators.</span>
                  </div>
                </div>

                {/* Notifications & Themes */}
                <div className="p-4 sm:p-5 rounded-2xl border border-white/5 bg-white/2 flex justify-between items-center">
                  <div>
                    <h3 className="text-sm font-bold text-white">System Notifications</h3>
                    <p className="text-[11px] text-[var(--text-secondary)] mt-0.5">Send alerts when agents complete tasks.</p>
                  </div>
                  <input id="system-notifications" type="checkbox" defaultChecked className="w-8 h-4 bg-indigo-500 rounded" aria-label="Enable system notifications" />
                </div>

              </div>

              <div className="flex justify-end gap-3 border-t border-white/5 pt-6">
                <button className="btn-glass px-6 py-3 text-xs font-bold" onClick={() => setActivePage('dashboard')}>
                  Cancel
                </button>
                <button className="btn-glass btn-glass-primary px-6 py-3 text-xs font-bold" onClick={() => alert("Settings saved.")}>
                  Save Settings
                </button>
              </div>
            </div>
          </section>
        )}

      </main>

      {/* FOOTER */}
      <footer className="app-footer">
        <div className="site-container flex flex-col sm:flex-row items-center justify-between gap-4 text-[10px] text-slate-400">
          <span>&copy; 2026 FounderAI Operating System. Premium AI Co-Founder. Powered by FastAPI & Vite.</span>
          <div className="flex gap-4">
            <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-white transition-colors">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
