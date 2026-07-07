import re
from typing import Dict, Any, List

class ConsistencyEngine:
    @staticmethod
    def validate_and_correct(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates logical consistency across all generated agent data
        against user inputs (budget, country, industry, stage).
        Modifies and corrects contradictions inline in the state dictionary.
        """
        startup = state.get("startup") or {}
        idea = startup.get("idea", "")
        industry = startup.get("industry", "")
        country = startup.get("country", "")
        budget = startup.get("budget", "")
        stage = startup.get("stage", "")

        # Extract numeric budget value
        clean_budget = re.sub(r"[^\d]", "", str(budget))
        budget_val = int(clean_budget) if clean_budget else 10000

        # Classification
        is_india = bool(re.search(r"india", country, re.IGNORECASE))
        is_us = bool(re.search(r"usa|united states|us|america", country, re.IGNORECASE))

        is_health = bool(re.search(r"health|med|doctor|clinic|fit|bio|pharm", idea + " " + industry, re.IGNORECASE))
        is_fintech = bool(re.search(r"finance|pay|bank|wealth|money|fintech|crypto", idea + " " + industry, re.IGNORECASE))
        is_food = bool(re.search(r"food|delivery|restaurant|eat|cook|meal", idea + " " + industry, re.IGNORECASE))
        is_ecommerce = bool(re.search(r"shop|e-commerce|store|sell|retail|marketplace", idea + " " + industry, re.IGNORECASE))

        # 1. Correct Financials
        if "financial" in state and state["financial"] and "data" in state["financial"]:
            findata = state["financial"]["data"]
            # Ensure monthly burn is within reason for low budgets
            if budget_val < 30000:
                findata["monthly_burn"] = "$1,000 - $2,000"
                findata["runway"] = f"{max(6, int(budget_val / 1500))} months"
                # Strip out any expensive engineering team payroll references
                filtered_expenses = []
                for exp in findata.get("expenses", []):
                    item_name = exp.get("item", "")
                    if re.search(r"hire|engineer|payroll|salaries|office lease", item_name, re.IGNORECASE):
                        continue
                    filtered_expenses.append(exp)
                # Ensure simple SaaS/hosting costs are listed
                if not filtered_expenses:
                    filtered_expenses = [
                        {"item": "HIPAA/Secure Cloud Hosting", "cost_type": "Fixed", "estimated_cost": "$120/mo"} if is_health else
                        {"item": "Cloud database and storage", "cost_type": "Fixed", "estimated_cost": "$80/mo"},
                        {"item": "AI API Token consumption", "cost_type": "Variable", "estimated_cost": "$150/mo"}
                    ]
                findata["expenses"] = filtered_expenses
            else:
                # High budgets require engineering teams
                has_payroll = False
                for exp in findata.get("expenses", []):
                    if re.search(r"hire|engineer|payroll|salaries", exp.get("item", ""), re.IGNORECASE):
                        has_payroll = True
                if not has_payroll:
                    findata["expenses"].append({
                        "item": "Core Engineering Team Salaries",
                        "cost_type": "Fixed",
                        "estimated_cost": "$8,500/mo"
                    })

        # 2. Correct Legal entity and compliance
        if "legal" in state and state["legal"] and "data" in state["legal"]:
            legdata = state["legal"]["data"]
            # Entity and country mismatch checks
            if is_india:
                legdata["entity_type"] = "Private Limited Company (Pvt Ltd)"
                legdata["country_specific_requirements"] = "MCA filing guidelines, PAN/TAN registration, and board resolution setup."
                if not any(re.search(r"GST", t, re.IGNORECASE) for t in legdata.get("taxes", [])):
                    legdata["taxes"].append("GST (Goods & Services Tax) registration required (20L threshold)")
                # Remove US-specific suggestions
                legdata["compliance"] = [c for c in legdata.get("compliance", []) if not re.search(r"delaware|ein|california", c, re.IGNORECASE)]
                # Add Indian compliance certificates
                if is_food and not any(re.search(r"FSSAI", c, re.IGNORECASE) for c in legdata.get("compliance", [])):
                    legdata["compliance"].append("FSSAI (Food Safety and Standards Authority of India) license")
            elif is_us:
                legdata["entity_type"] = "Delaware C-Corporation" if budget_val >= 50000 else "Limited Liability Company (LLC)"
                legdata["country_specific_requirements"] = "Delaware state filings, Registered Agent setup, and EIN filing."
                legdata["compliance"] = [c for c in legdata.get("compliance", []) if not re.search(r"GST|FSSAI|MCA", c, re.IGNORECASE)]
            
            # Industry compliance mandates
            if is_health and not any(re.search(r"HIPAA", c, re.IGNORECASE) for c in legdata.get("compliance", [])):
                legdata["compliance"].append("HIPAA Business Associate Agreement (BAA) & Data protection guidelines")
            if is_fintech and not any(re.search(r"PCI|DSS", c, re.IGNORECASE) for c in legdata.get("compliance", [])):
                legdata["compliance"].append("PCI-DSS payment encryption standards compliance")

        # 3. Correct Funding Strategy
        if "funding" in state and state["funding"] and "data" in state["funding"]:
            fundata = state["funding"]["data"]
            if budget_val < 30000:
                # Do not recommend Series A VCs for small budgets
                fundata["bootstrap_strategy"] = f"Deploy the starting ${budget_val:,} strictly on a micro-MVP, validating workflows manually prior to seeking external institutional capital."
                fundata["recommended_funding"] = "Bootstrapping / Pre-Seed Angel networks"
                fundata["recommended_investors"] = [i for i in fundata.get("recommended_investors", []) if not re.search(r"sequoia|andreessen|accel|redpoint", i, re.IGNORECASE)]
                if not fundata["recommended_investors"]:
                    fundata["recommended_investors"] = ["Regional Angel Networks", "Startup India Seed Fund" if is_india else "SBIR Innovation Grant"]

        return state

class VerificationEngine:
    @staticmethod
    def audit_and_verify(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits all generated texts to flag placeholder values, template repetitions,
        or contradictions. Regenerates or corrects placeholders dynamically.
        """
        startup = state.get("startup") or {}
        founder = startup.get("founder_name", "Founder")
        idea = startup.get("idea", "")
        industry = startup.get("industry", "")
        country = startup.get("country", "")

        # 1. Enforce strict personal references. Clean placeholder templates.
        for key in ["discovery", "validation", "market", "competitors", "business_model", "financial", "legal", "funding", "roadmap", "risk"]:
            if key not in state or not state[key] or "data" not in state[key]:
                continue
            
            # Recursively walk dictionary data to scrub templates
            data_dict = state[key]["data"]
            state[key]["data"] = VerificationEngine._scrub_placeholders(data_dict, founder, idea, industry, country)

        # 2. Re-run Consistency checks
        state = ConsistencyEngine.validate_and_correct(state)
        return state

    @staticmethod
    def _scrub_placeholders(obj: Any, founder: str, idea: str, industry: str, country: str) -> Any:
        if isinstance(obj, str):
            # Strip standard static template placeholders
            text = obj
            text = re.sub(r"\bDr\.\s+Jane\s+Smith\b|\bDr\.\s+Smith\b|\bJane\s+Smith\b", founder, text, flags=re.IGNORECASE)
            text = re.sub(r"\bSarah\s+Jenkins\b", f"Lead Customer for {founder}", text, flags=re.IGNORECASE)
            text = re.sub(r"\bApex\s+Medical\s+Group\b|\bApex\s+Compliance\b", f"{founder} Ventures", text, flags=re.IGNORECASE)
            text = re.sub(r"\bDr\.\s+Aaron\s+Patel\b", f"Advisor for {founder}", text, flags=re.IGNORECASE)
            text = re.sub(r"\bRock\s+Health\s+Ventures\b", f"Target VC in {country}", text, flags=re.IGNORECASE)
            text = re.sub(r"\bClaimVerify\s+Co\b", f"Competitor Inc.", text, flags=re.IGNORECASE)
            text = re.sub(r"\bLegacyCorp\b", f"Incumbent {industry} Corp", text, flags=re.IGNORECASE)
            # Make sure the text mentions the startup country/industry context
            if "Delaware C-Corporation" in text and not re.search(r"USA|United States", country, re.IGNORECASE):
                text = text.replace("Delaware C-Corporation", "local business registry entity")
            return text
        elif isinstance(obj, list):
            return [VerificationEngine._scrub_placeholders(item, founder, idea, industry, country) for item in obj]
        elif isinstance(obj, dict):
            return {k: VerificationEngine._scrub_placeholders(v, founder, idea, industry, country) for k, v in obj.items()}
        return obj
