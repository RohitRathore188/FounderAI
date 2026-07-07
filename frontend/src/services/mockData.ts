import type { FounderState } from './api';

function toDisplayValue(value: unknown, fallback: string): string {
  if (typeof value === 'string' && value.trim()) return value.trim();
  return fallback;
}

function toBudgetValue(value: unknown): number {
  const digits = String(value ?? '').replace(/[^0-9]/g, '');
  return digits ? Number.parseInt(digits, 10) : 10000;
}

function toTeamSize(value: unknown): number {
  const digits = String(value ?? '').replace(/[^0-9]/g, '');
  return digits ? Number.parseInt(digits, 10) : 1;
}

function getLocationText(form: any): string {
  const parts = [form?.district, form?.state, form?.country].filter(Boolean);
  return parts.length ? parts.join(', ') : 'the chosen market';
}

export const INITIAL_MOCK_STATE: FounderState = {
  startup: {
    idea: 'A lean startup concept',
    industry: 'Technology',
    country: 'United States',
    budget: '$10,000',
    stage: 'Idea',
    founder_name: 'Founder',
    target_market: 'Early adopters'
  },
  report: {
    executive_summary: 'The report will reflect the startup inputs once the backend runs.',
    pdf_url: ''
  }
};

export function getDynamicFrontendMockData(form: any): FounderState {
  const idea = toDisplayValue(form?.idea, 'a tech startup');
  const industry = toDisplayValue(form?.industry, 'Technology');
  const country = toDisplayValue(form?.country, 'United States');
  const budget = toDisplayValue(form?.budget, '$10,000');
  const founder = toDisplayValue(form?.founder_name, 'Founder');
  const targetMarket = toDisplayValue(form?.target_market, 'General Public');
  const teamSize = toTeamSize(form?.team_size);
  const budgetVal = toBudgetValue(budget);
  const locationText = getLocationText(form);

  const isIndia = /india/i.test(country);
  const isUs = /usa|united states|us|america/i.test(country);
  const isAi = /ai|artificial|ml|intelligence|bot|gpt|neural|agent/i.test(`${idea} ${industry}`);

  let companyType = 'Private Limited Company (Ltd)';
  if (isIndia) companyType = 'Private Limited Company (Pvt Ltd)';
  else if (isUs) companyType = budgetVal >= 50000 ? 'Delaware C-Corporation' : 'Limited Liability Company (LLC)';

  const validationScore = Math.min(98, Math.max(45, 73 + (idea.length % 11) + (isAi ? 4 : 0) - (budgetVal < 15000 ? 8 : 0)));
  const feasibilityScore = Math.min(95, Math.max(40, 80 - Math.floor(budgetVal / 22000) - Math.max(0, teamSize - 2)));
  const innovationScore = Math.min(99, Math.max(50, 62 + (idea.length % 17) + (isAi ? 8 : 0)));

  const tamValue = budgetVal * 420;
  const samValue = Math.floor(tamValue * 0.24);
  const somValue = Math.floor(samValue * 0.1);

  return {
    startup: {
      ...form,
      idea,
      industry,
      country,
      budget,
      founder_name: founder,
      target_market: targetMarket,
      team_size: String(teamSize)
    },
    discovery: {
      problem: `The core challenge for ${targetMarket} is that the current workflow is still fragmented and hard to scale in ${locationText}.`,
      solution: `${founder} is building ${idea} as an automation-first product that reduces friction and improves execution quality.`,
      usp: `The product is designed around the real operating needs of ${targetMarket} in ${locationText}.`
    },
    validation: {
      validation_score: validationScore,
      feasibility_score: feasibilityScore,
      market_fit_score: Math.max(45, validationScore - 2),
      growth_potential_score: innovationScore,
      feedback: `The concept has a ${validationScore}% validation signal and a ${feasibilityScore}% feasibility score, which suggests a credible path for ${founder} to launch lean and iterate quickly.`,
      critical_risks: [
        `Adoption risk if the offer is not tailored to ${targetMarket}`,
        `Execution risk when the team grows faster than the operating process`,
        `Compliance and contracting questions in ${country}`
      ]
    },
    market: {
      TAM: `$${(tamValue / 1000000).toFixed(1)}M globally for ${industry.toLowerCase()} efficiency and automation.`,
      SAM: `$${(samValue / 1000000).toFixed(1)}M in ${country} for the most relevant ${targetMarket.toLowerCase()} segment.`,
      SOM: `$${(somValue / 1000000).toFixed(1)}M obtainable in the first 12-24 months by focusing on the most promising early customers.`,
      market_trends: [
        'Growing adoption of automated compliance tools',
        'Shift towards integrated niche vertical software',
        'Increased regulatory scrutiny on data handling'
      ],
      sources: [
        'Industry Market Analysis Report 2026',
        'SaaS Compliance Index Q1 2026'
      ],
      customer_persona: {
        name: `${founder}, Founder`,
        role: `Founder / operator in ${industry}`,
        pain_points: [
          `Needs a faster path to validate ${targetMarket}`,
          `Needs a clear path to reduce operational overhead`,
          `Needs a lean launch plan that fits a ${budget} budget`
        ],
        buying_power: budgetVal >= 50000 ? 'High' : 'Medium'
      }
    },
    competitors: {
      real_competitors: [
        { name: `Legacy ${industry} Providers`, gap: 'They are slower to adopt and harder to customize.', threat_level: 'Medium' },
        { name: `Incumbent Platforms`, gap: 'They focus on breadth rather than fit for this workflow.', threat_level: 'High' }
      ],
      pricing: `A value-led pricing structure should start around $29-$99 per month for early adopters and expand with usage.`,
      strengths: ['Clear use case', 'Lean delivery path', 'Strong founder insight'],
      weaknesses: ['Limited brand awareness early on', 'Operating discipline is still being proven'],
      gap_analysis: `The key advantage is a more tailored and faster path to value for ${targetMarket} than generic alternatives.`
    },
    business_model: {
      key_partners: [`Early ${targetMarket} adopters`, `Service providers in ${country}`, 'Implementation partners'],
      activities: ['Customer discovery', 'Product iteration', 'Onboarding and support'],
      key_resources: ['Product and engineering focus', 'Founder domain expertise', 'A repeatable operating workflow'],
      value_proposition: [`Reduce friction for ${targetMarket}`, `Speed up execution in ${industry}`, 'Make the workflow easier to run and measure'],
      channels: [`Direct outreach to ${targetMarket}`, `Industry communities in ${country}`, 'Founder-led content distribution'],
      customer_segments: [targetMarket, `Small teams in ${industry}`],
      revenue_model: `SaaS subscription model with tiered plans starting around $29-$99 per month.`,
      pricing_strategy: `A value-led pricing structure that starts low for early adopters and expands with usage/features.`
    },
    registration: {
      company_type_recommendation: companyType,
      country_specific: `Register the operating entity in ${country} and align the local paperwork before the first pilot launch.`,
      gst_required: isIndia,
      trademark_recommendation: 'Reserve the brand name and key product marks before launch.',
      required_licenses: [`Business registration in ${country}`, 'Basic tax registration'],
      required_documents: ['Founding documents', 'Founder agreements', 'Initial operating plan']
    },
    legal: {
      co_founder_agreement_reqs: ['Clear founder vesting and decision rights', 'IP assignment and confidentiality clauses'],
      ip_assignment_reqs: ['All product and code contributions assigned to the company', 'Clear contractor ownership terms'],
      nda_reqs: ['Mutual NDA for customer and partner conversations', 'Simple contractor confidentiality terms'],
      legal_compliance_checklist: [`Set up the entity in ${country}`, 'Document contracts and data handling policies', 'Track the first compliance milestones']
    },
    funding: {
      investment_readiness_score: budgetVal >= 50000 ? 68 : 82,
      bootstrap_strategy: budgetVal >= 50000 ? 'Use initial capital for a tighter prototype and a structured pre-seed conversation.' : 'Keep the launch lean and validate demand before spending more.',
      vc_firms: [{ name: 'Early-stage sector funds', stage: 'Pre-Seed', focus: `${industry} and workflow software` }],
      angel_investors: [{ name: 'Founder-friendly angel networks', stage: 'Pre-Seed', focus: 'Operational software and vertical tools' }],
      government_grants: [{ name: 'Innovation support grant', description: 'Useful for the first product build-out', amount: '$10,000-$50,000' }]
    },
    roadmap: {
      go_to_market_channels: [`Direct outreach to ${targetMarket}`, `Community channels in ${country}`, 'Founder-led content distribution'],
      roadmap_phases: [
        { phase: 'Phase 1', duration: 'Days 1-30', milestones: ['Validate the problem with a few named prospects', 'Define the MVP and success metric'] },
        { phase: 'Phase 2', duration: 'Days 31-60', milestones: ['Ship the first release for pilot users', 'Collect feedback and refine the onboarding flow'] },
        { phase: 'Phase 3', duration: 'Days 61-90', milestones: ['Expand to more early customers', 'Tighten pricing, support, and marketing messages'] }
      ]
    },
    report: {
      executive_summary: `${founder} is building ${idea} for ${targetMarket} in ${country}. The launch plan is shaped by the local market context, a lean budget, and a clear path to early validation.`,
      pdf_url: ''
    }
  };
}

