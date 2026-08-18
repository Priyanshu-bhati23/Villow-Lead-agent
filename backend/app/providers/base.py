from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.models.schemas import ICPParseResult

class BaseLeadProvider(ABC):
    """Abstract base class for search and lead enrichment providers."""

    @abstractmethod
    def search_companies(self, icp: ICPParseResult, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Discover raw potential companies matching the parsed ICP criteria.
        Returns a list of raw company objects containing name, website, snippet, sources, etc.
        """
        pass

    @abstractmethod
    def enrich_company(self, raw_company: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich raw company object with detailed attributes, verified signals, and sources.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns provider name string."""
        pass

    @abstractmethod
    def is_mock(self) -> bool:
        """Returns True if provider is a mock fallback."""
        pass
