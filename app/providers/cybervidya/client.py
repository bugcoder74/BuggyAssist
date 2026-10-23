import httpx
import logging
from typing import Dict, Any, List
from app.providers.base import BaseAttendanceProvider
from app.providers.cybervidya.schemas import (
    CyberVidyaLoginRequest, 
    CyberVidyaLoginResponse,
    RegisteredCoursesResponse
)

logger = logging.getLogger(__name__)

class CyberVidyaProvider(BaseAttendanceProvider):
    def __init__(self, base_url: str = "https://proxy.cybervidya.workers.dev"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=15.0)

    async def authenticate(self, username: str, password: str, **kwargs) -> Dict[str, Any]:
        login_url = f"{self.base_url}/api/auth/login"
        payload = {
            "userName": username.strip(),
            "password": password.strip()
        }
        
        response = await self.client.post(login_url, json=payload)
        if response.status_code != 200:
            logger.error(f"❌ CyberVidya Login Failed: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        login_response = CyberVidyaLoginResponse(**response.json())
        
        return {
            "token": login_response.data.token,
            # Yahan hdr_auth ki jagah auth_pref use karna hai!
            "auth_pref": login_response.data.auth_pref.strip(), 
            "user_id": login_response.data.id
        }

    async def fetch_subjects(self, session_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/api/student/dashboard/registered-courses"
        
        # Sahi format: "GlobalEducation <token>"
        auth_header_value = f"{session_data['auth_pref']} {session_data['token']}"
        headers = {
            "Authorization": auth_header_value,
            "Accept": "application/json"
        }
        
        response = await self.client.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"❌ CyberVidya Fetch Subjects Failed: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        courses_response = RegisteredCoursesResponse(**response.json())
        return [course.model_dump() for course in courses_response.data]

    async def fetch_attendance(self, session_data: Dict[str, Any], subject_code: str) -> Dict[str, Any]:
        return {
            "message": "Detailed date-wise attendance not yet implemented",
            "subject_code": subject_code
        }

    async def close(self):
        await self.client.aclose()