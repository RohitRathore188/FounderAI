from typing import TypedDict, Dict, Any, Optional

class FounderState(TypedDict):
    startup: Dict[str, Any]
    discovery: Optional[Dict[str, Any]]
    validation: Optional[Dict[str, Any]]
    market: Optional[Dict[str, Any]]
    competitors: Optional[Dict[str, Any]]
    business_model: Optional[Dict[str, Any]]
    financial: Optional[Dict[str, Any]]
    legal: Optional[Dict[str, Any]]
    funding: Optional[Dict[str, Any]]
    roadmap: Optional[Dict[str, Any]]
    risk: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]
