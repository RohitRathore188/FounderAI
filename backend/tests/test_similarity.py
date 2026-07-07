import pytest
import re
from typing import Dict, Any, Set
from app.graph.builder import graph

# 5 completely different startups
STARTUPS = [
    {
        "name": "Healthcare SaaS",
        "idea": "A HIPAA-compliant SaaS platform automating patient chart compliance for small clinics",
        "industry": "Healthcare Tech / SaaS",
        "country": "United States",
        "budget": "$25,000",
        "stage": "MVP",
        "founder_name": "Dr. Sarah",
        "target_market": "Private Clinics"
    },
    {
        "name": "Food Delivery",
        "idea": "An on-demand localized drone delivery platform for warm home-cooked meals",
        "industry": "Food Logistics",
        "country": "India",
        "budget": "INR 400,000",
        "stage": "Idea",
        "founder_name": "Amit",
        "target_market": "Suburban Families"
    },
    {
        "name": "AI EdTech",
        "idea": "An AI agent-based personalized tutor for teaching Python and data structures to high schoolers",
        "industry": "EdTech",
        "country": "United Kingdom",
        "budget": "$8,000",
        "stage": "Beta",
        "founder_name": "Emily",
        "target_market": "Parents and Students"
    },
    {
        "name": "FinTech",
        "idea": "A secure API-first micro-lending ledger for underbanked gig workers in Southeast Asia",
        "industry": "FinTech",
        "country": "Singapore",
        "budget": "$120,000",
        "stage": "Seed",
        "founder_name": "Marcus",
        "target_market": "Gig Platforms"
    },
    {
        "name": "D2C E-commerce",
        "idea": "Direct-to-consumer organic sustainable bamboo activewear and athletic products",
        "industry": "D2C Retail",
        "country": "Canada",
        "budget": "$45,000",
        "stage": "Launch",
        "founder_name": "Chloe",
        "target_market": "Eco-conscious Athletes"
    }
]

def extract_text_content(state: Dict[str, Any]) -> str:
    """
    Recursively extracts all text values from the final state dictionary
    to compile a comprehensive representation of the report content.
    """
    texts = []
    
    def walk(obj: Any):
        if isinstance(obj, str):
            # Only count words longer than 3 characters, filtering out common formatting markup
            texts.append(obj)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                # Skip common JSON keys/meta headers to avoid false similarity triggers
                if k in ["status", "agent", "run_id", "timestamp"]:
                    continue
                walk(v)

    # We inspect agent data modules specifically
    for key in ["discovery", "validation", "market", "competitors", "business_model", "financial", "legal", "funding", "roadmap", "risk"]:
        if key in state and state[key] and "data" in state[key]:
            walk(state[key]["data"])
            
    return " ".join(texts)

def get_word_tokens(text: str) -> Set[str]:
    """
    Tokenizes text into a set of lowercased alphanumeric words,
    filtering out short words and common stopwords.
    """
    words = re.findall(r"\b\w{4,}\b", text.lower())
    stopwords = {
        "with", "that", "this", "from", "your", "have", "will", "model",
        "stage", "focus", "team", "based", "first", "target", "market",
        "startup", "business", "value", "customer", "product", "platform",
        "service", "industry", "setup", "required", "system", "compliance",
        "analysis", "recommended", "strategy", "revenue", "operating",
        "estimated", "projected", "forecast", "amount", "budget", "month"
    }
    return {w for w in words if w not in stopwords}

def test_startup_reports_similarity():
    """
    Generates reports for all 5 startups and asserts that pairwise similarity is < 30%.
    """
    reports = {}
    
    # 1. Run orchestration for each startup
    for s_info in STARTUPS:
        name = s_info["name"]
        print(f"Generating report for: {name}...")
        
        initial_state = {
            "startup": s_info,
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
                "run_id": f"sim_test_{name.replace(' ', '_').lower()}",
                "status": "processing"
            }
        }
        
        final_state = graph.invoke(initial_state)
        reports[name] = extract_text_content(final_state)

    # 2. Compute Jaccard similarity matrix
    similarity_failures = []
    matrix = {}
    
    print("\n========== PAIRWISE SIMILARITY MATRIX ==========")
    names = [s["name"] for s in STARTUPS]
    for i in range(len(names)):
        matrix[names[i]] = {}
        for j in range(len(names)):
            if i == j:
                matrix[names[i]][names[j]] = 1.0
                continue
                
            tokens_a = get_word_tokens(reports[names[i]])
            tokens_b = get_word_tokens(reports[names[j]])
            
            intersection = tokens_a.intersection(tokens_b)
            union = tokens_a.union(tokens_b)
            
            similarity = len(intersection) / len(union) if union else 0.0
            matrix[names[i]][names[j]] = similarity
            
            if i < j:
                print(f"Similarity({names[i]} <-> {names[j]}): {similarity:.2%}")
                if similarity >= 0.30:
                    similarity_failures.append((names[i], names[j], similarity))
    print("================================================\n")

    # 3. Assert strict uniqueness criteria (< 30%)
    for name_a, name_b, sim in similarity_failures:
        print(f"CRITICAL: Contradiction found! {name_a} and {name_b} share {sim:.2%} similarity.")
        
    assert len(similarity_failures) == 0, f"Reports are too similar! Failures: {similarity_failures}"
