import logging
from sqlmodel import Session, select
from app.providers.cybervidya.client import CyberVidyaProvider
from app.providers.cybervidya.mapper import map_cybervidya_to_subjects
from app.repositories.subject_repo import upsert_subjects, get_all_subjects
from app.models.provider_mapping import ProviderSubjectMapping

logger = logging.getLogger(__name__)

async def sync_attendance_data(
    session: Session, 
    username: str, 
    password: str,
    provider_name: str = "cybervidya"
) -> dict:
    provider = CyberVidyaProvider()
    sync_successful = False
    
    try:
        session_data = await provider.authenticate(username, password)
        raw_courses = await provider.fetch_subjects(session_data)
        
        # 1. Map to generic subjects and upsert
        mapped_subjects = map_cybervidya_to_subjects(raw_courses)
        upsert_subjects(session, mapped_subjects)
        
        # 2. Upsert the Provider-Specific Mapping
        for course in raw_courses:
            course_code = course.get("courseCode")
            course_id = course.get("courseId") # Now this will NOT be None
            
            for comp in course.get("studentCourseCompDetails", []):
                comp_name = comp.get("courseCompName", "GENERAL")
                comp_id = comp.get("courseCompId") # Now this will NOT be None
                
                generic_code = f"{course_code}-{comp_name}"
                
                # Check if mapping exists
                stmt = select(ProviderSubjectMapping).where(
                    ProviderSubjectMapping.subject_code == generic_code,
                    ProviderSubjectMapping.provider_name == provider_name
                )
                existing_mapping = session.exec(stmt).first()
                
                if existing_mapping:
                    existing_mapping.external_course_id = course_id
                    existing_mapping.external_course_comp_id = comp_id
                    session.add(existing_mapping)
                else:
                    new_mapping = ProviderSubjectMapping(
                        subject_code=generic_code,
                        provider_name=provider_name,
                        external_course_id=course_id,
                        external_course_comp_id=comp_id,
                        external_student_id=session_data.get("user_id")
                    )
                    session.add(new_mapping)
                    
        session.commit()
        sync_successful = True
        logger.info(f"Successfully synced subjects and mappings for {username}")
        
    except Exception as e:
        # GRACEFUL DEGRADATION
        logger.warning(f"Sync failed for {username}. Reason: {str(e)}. Falling back to local data.")
        session.rollback() # <--- CRITICAL FIX: Reset the session state after an error
    finally:
        await provider.close()
    
    # Now this will work safely, even if the sync failed
    local_subjects = get_all_subjects(session)
    
    return {
        "sync_successful": sync_successful,
        "message": "Data synced successfully" if sync_successful else "Using locally cached data",
        "subjects": local_subjects
    }