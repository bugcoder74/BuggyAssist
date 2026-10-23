from typing import List, Dict, Any
from app.schemas.subject import SubjectCreate

def map_cybervidya_to_subjects(raw_courses: List[Dict[str, Any]]) -> List[SubjectCreate]:
    """
    CyberVidya ke registered courses data ko flat SubjectCreate list mein convert karta hai.
    """
    mapped_subjects = []
    
    for course in raw_courses:
        course_name = course.get("courseName", "Unknown Course")
        course_code = course.get("courseCode", "UNKNOWN")
        
        # Har course ke components (Theory/Practical/Blended) ko iterate karein
        for comp in course.get("studentCourseCompDetails", []):
            comp_name = comp.get("courseCompName", "GENERAL")
            
            # Clear naming convention: "Database Systems (THEORY)"
            final_subject_name = f"{course_name} ({comp_name})"
            
            subject = SubjectCreate(
                name=final_subject_name,
                code=f"{course_code}-{comp_name}", # Unique identifier
                total_classes=int(comp.get("totalLecture", 0)),
                attended_classes=int(comp.get("presentLecture", 0))
            )
            mapped_subjects.append(subject)
            
    return mapped_subjects