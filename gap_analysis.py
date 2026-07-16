"""
Analyzes gaps between resume skills and job requirements
"""
def analyze_gaps(resume_skills: list[str], jd_skills: list[str]) -> dict:
    """Compare skills and identify strengths and gaps"""
    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)
    
    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    
    return {
        "strengths": matched,
        "gaps": missing,
        "match_percentage": round(len(matched) / len(jd_set) * 100, 1) if jd_set else 0.0,
    }