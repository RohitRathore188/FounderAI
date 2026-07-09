from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger


class TavilySearchService:
    """Service to search for local competitors using Tavily API."""

    def __init__(self):
        self.client = None
        if settings.TAVILY_API_KEY:
            try:
                from tavily import TavilyClient
                self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
                logger.info("[TavilySearch] Client initialized successfully.")
            except Exception as e:
                logger.error(f"[TavilySearch] Failed to initialize: {e}")

    def search_local_competitors(
        self,
        industry: str,
        country: str,
        state: str = "",
        district: str = "",
        idea: str = "",
        max_results: int = 8
    ) -> str:
        """Search for local competitors and return formatted results string."""
        if not self.client:
            logger.warning("[TavilySearch] No client available. Skipping search.")
            return ""

        # Build a location-specific query
        location_parts = [p for p in [district, state, country] if p]
        location_str = ", ".join(location_parts)

        query = f"top {industry} companies and startups in {location_str}"
        if idea:
            # Add context from the idea to narrow results
            idea_snippet = idea[:100]
            query = f"{industry} competitors and businesses similar to '{idea_snippet}' in {location_str}"

        try:
            logger.info(f"[TavilySearch] Searching: {query}")
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=True
            )

            results = []
            if response.get("answer"):
                results.append(f"Search Summary: {response['answer']}")

            for i, item in enumerate(response.get("results", []), 1):
                title = item.get("title", "Unknown")
                content = item.get("content", "")[:200]
                url = item.get("url", "")
                results.append(f"{i}. {title} — {content} (Source: {url})")

            formatted = "\n".join(results)
            logger.info(f"[TavilySearch] Found {len(response.get('results', []))} results.")
            return formatted

        except Exception as e:
            logger.error(f"[TavilySearch] Search failed: {e}")
            return ""
