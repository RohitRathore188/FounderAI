import os
import time
from typing import Type, Dict, Any, Optional
from pydantic import BaseModel, ValidationError
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.logging import logger
from app.utils.helpers import get_dynamic_mock_data  # We will implement this to handle fallbacks

class BaseAgent:
    def __init__(self, agent_name: str, response_schema: Type[BaseModel], prompt_file: str):
        self.agent_name = agent_name
        self.response_schema = response_schema
        self.prompt_file = prompt_file
        self.client = None
        
        # Initialize Google GenAI client if API key is provided
        if settings.GEMINI_API_KEY:
            try:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info(f"[{self.agent_name}] Official Google GenAI client initialized successfully.")
            except Exception as e:
                logger.error(f"[{self.agent_name}] Error initializing GenAI client: {e}. Fallback will be used.")

    def _get_prompt_path(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            self.prompt_file
        )

    def load_prompt_template(self) -> str:
        path = self._get_prompt_path()
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"[{self.agent_name}] Prompt file not found at: {path}")
            raise RuntimeError(f"Prompt template {self.prompt_file} not found.")
        except Exception as e:
            logger.error(f"[{self.agent_name}] Error reading prompt file: {e}")
            raise

    def build_prompt(self, variables: Dict[str, Any]) -> str:
        template = self.load_prompt_template()
        context_block = self._build_context_block(variables)
        return f"{template}\n\n[CRITICAL INSTRUCTION]\nYou must treat every supplied field as mandatory context. Every field in the startup snapshot below must materially influence the analysis and the final output. Do not reuse generic template language; regenerate the response from scratch for this specific context.\n{context_block}"

    def _build_context_block(self, variables: Dict[str, Any]) -> str:
        ordered_fields = [
            ("idea", variables.get("idea", "")),
            ("industry", variables.get("industry", "")),
            ("country", variables.get("country", "")),
            ("state", variables.get("state", "")),
            ("district", variables.get("district", "")),
            ("location_context", variables.get("location_context", variables.get("country", ""))),
            ("budget", variables.get("budget", "")),
            ("stage", variables.get("stage", "")),
            ("founder_name", variables.get("founder_name", "")),
            ("target_market", variables.get("target_market", "")),
            ("team_size", variables.get("team_size", "")),
        ]
        lines = ["Startup Snapshot:"]
        for key, value in ordered_fields:
            if value not in (None, ""):
                lines.append(f"- {key}: {value}")
        lines.append("- discovery_summary: " + str(variables.get("discovery_summary", "")))
        lines.append("- market_summary: " + str(variables.get("market_summary", "")))
        lines.append("- business_model_summary: " + str(variables.get("business_model_summary", "")))
        lines.append("- financial_summary: " + str(variables.get("financial_summary", "")))
        lines.append("- legal_summary: " + str(variables.get("legal_summary", "")))
        return "\n".join(lines)

    def invoke_llm(self, variables: Dict[str, Any]) -> BaseModel:
        prompt = self.build_prompt(variables)
        
        if self.client:
            try:
                logger.info(f"[{self.agent_name}] Invoking Gemini 2.5 Flash...")
                # DIAGNOSTIC: Print the exact prompt being sent to Gemini
                print(f"\n{'='*60}")
                print(f"[DIAGNOSTIC] Agent: {self.agent_name}")
                print(f"[DIAGNOSTIC] Variables received: {list(variables.keys())}")
                print(f"[DIAGNOSTIC] country={variables.get('country', 'MISSING')}")
                print(f"[DIAGNOSTIC] industry={variables.get('industry', 'MISSING')}")
                print(f"[DIAGNOSTIC] idea={variables.get('idea', 'MISSING')[:80]}")
                print(f"[DIAGNOSTIC] FULL PROMPT:\n{prompt}")
                print(f"{'='*60}\n")
                
                # Delay for 4 seconds to avoid hitting the 15 RPM Gemini Free Tier limit
                logger.info(f"[{self.agent_name}] Applying 4-second delay for rate limiting...")
                time.sleep(4)
                
                # Call Gemini 2.5 Flash
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=self.response_schema,
                        temperature=0.2,
                    ),
                )
                
                # DIAGNOSTIC: Print the raw Gemini response
                print(f"\n{'='*60}")
                print(f"[DIAGNOSTIC] Agent: {self.agent_name} RAW GEMINI RESPONSE:")
                print(response.text if response and response.text else "EMPTY RESPONSE")
                print(f"{'='*60}\n")
                
                if response and response.text:
                    # Validate output JSON
                    validated_data = self.validate(response.text)
                    if validated_data:
                        return validated_data
                    else:
                        raise ValueError("Gemini output validation failed.")
                else:
                    raise ValueError("Gemini returned empty response.")
            except Exception as e:
                logger.warning(f"[{self.agent_name}] LLM invocation failed: {e}. Relying on fallback generator.")
        
        # Fallback to high-fidelity mock data generator
        logger.info(f"[{self.agent_name}] Using high-fidelity fallback generator for {variables.get('idea', 'startup')}.")
        mock_json = get_dynamic_mock_data(self.agent_name, variables)
        return self.response_schema.model_validate(mock_json)

    def validate(self, json_str: str) -> Optional[BaseModel]:
        try:
            logger.info(f"[{self.agent_name}] Validating structured output...")
            # We parse the Pydantic schema
            return self.response_schema.model_validate_json(json_str)
        except ValidationError as e:
            logger.error(f"[{self.agent_name}] Validation error: {e}")
            return None
        except Exception as e:
            logger.error(f"[{self.agent_name}] Error during validation: {e}")
            return None

    def create_response_payload(self, summary: str, data: BaseModel) -> Dict[str, Any]:
        return {
            "status": "success",
            "agent": self.agent_name,
            "summary": summary,
            "data": data.model_dump(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
