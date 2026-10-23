from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAttendanceProvider(ABC):
    """
    Every new provider will have to implement these methods
    """

    @abstractmethod
    async def authenticate(self, username: str, password: str, **kwargs) -> Dict[str, Any]:
        """Login krke session token/cookies wgra return kara denge"""
        pass

    @abstractmethod
    async def fetch_subjects(self, session_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Provider ke raw subject data ko fetch karega."""
        pass

    @abstractmethod
    async def fetch_attendance(self, session_data: Dict[str, Any], subject_code: str) -> Dict[str, Any]:
        """Kisi specific subject ki attendance details fetch karega."""
        pass