from pydantic import BaseModel, Field

class GeminiModelConfig(BaseModel):
    """Configuration options for the Gemini 2.5 Flash model."""
    model_name: str = Field(default="gemini-2.5-flash", description="Gemini model identifier")
    temperature: float = Field(default=0.2, description="Controls randomness of output")
    max_output_tokens: int = Field(default=8192, description="Max response length limit")
    top_p: float = Field(default=0.95, description="Nucleus sampling parameter")

class SystemModelRegistry(BaseModel):
    """Registry representing models used by various agents."""
    discovery_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)
    market_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)
    competitor_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)
    business_model_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)
    registration_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)
    funding_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)
    report_agent: GeminiModelConfig = Field(default_factory=GeminiModelConfig)

registry = SystemModelRegistry()
