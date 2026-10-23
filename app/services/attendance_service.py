import logging
from sqlmodel import Session, select
from app.providers.cybervidya.client import CyberVidyaProvider
from app.providers.cybervidya.mapper import map_cybervidya_lectures_to_records
from app.repositories.attendance_repo import upsert_attendance_records, get_attendance_by_subject
from app.models.provider_mapping import ProviderSubjectMapping

logger = logging.getLogger(__name__)

async def sync_attendance_sheet(
    session: Session,
    username: str,
    password: str,
    subject_code: str,
    provider_name: str = "cybervidya"
) -> dict:
    provider = CyberVidyaProvider()
    sync_successful = False
    
    try:
        # 1. Get the provider-specific mapping for this subject
        stmt = select(ProviderSubjectMapping).where(
            ProviderSubjectMapping.subject_code == subject_code,
            ProviderSubjectMapping.provider_name == provider_name
        )
        mapping = session.exec(stmt).first()
        
        if not mapping:
            return {
                "sync_successful": False,
                "message": "Provider mapping not found. Please sync subjects first.",
                "records": []
            }
            
        # 2. Authenticate (we need the token)
        session_data = await provider.authenticate(username, password)
        
        # 3. Fetch attendance using the EXTERNAL IDs from the mapping
        raw_lectures = await provider.fetch_attendance(
            session_data=session_data,
            course_id=mapping.external_course_id,
            course_comp_id=mapping.external_course_comp_id,
            student_id=mapping.external_student_id
        )
        
        # 4. Map and Upsert to local DB
        mapped_records = map_cybervidya_lectures_to_records(subject_code, raw_lectures)
        upsert_attendance_records(session, mapped_records)
        sync_successful = True
        logger.info(f"Successfully synced {len(mapped_records)} attendance records for {subject_code}")
        
    except Exception as e:
        logger.warning(f"Attendance sync failed for {subject_code}. Reason: {str(e)}. Falling back to local data.")
    finally:
        await provider.close()
        
    local_records = get_attendance_by_subject(session, subject_code)
    
    return {
        "sync_successful": sync_successful,
        "message": "Attendance synced successfully" if sync_successful else "Using locally cached attendance data",
        "records": local_records
    }