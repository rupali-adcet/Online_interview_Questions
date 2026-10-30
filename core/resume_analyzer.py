"""
resume_analyzer.py
Performs Resume vs Job Description semantic comparison, skill matching,
gap analysis, and targeted gap-probing question generation.
"""

from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.nlp_engine import nlp_engine


class ResumeAnalyzer:
    """
    Analyzes resumes against job descriptions, calculating match scores
    and generating gap-probing interview questions.
    """

    def __init__(self):
        self.nlp = nlp_engine

    def analyze(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Runs comprehensive comparative analysis between a resume and a job description.
        """
        clean_resume = self.nlp.clean_text(resume_text)
        clean_jd = self.nlp.clean_text(jd_text)

        # 1. Skill Extraction
        resume_skills_dict = self.nlp.extract_skills_from_text(clean_resume)
        jd_skills_dict = self.nlp.extract_skills_from_text(clean_jd)

        resume_skills_set = set(self.nlp.get_all_matched_skills(clean_resume))
        jd_skills_set = set(self.nlp.get_all_matched_skills(clean_jd))

        # 2. Skill Gap & Overlap Analysis
        matched_skills = sorted(list(resume_skills_set.intersection(jd_skills_set)))
        missing_skills = sorted(list(jd_skills_set.difference(resume_skills_set)))
        bonus_skills = sorted(list(resume_skills_set.difference(jd_skills_set)))

        # Skill match percentage (Recall on JD requirements)
        if len(jd_skills_set) > 0:
            skill_match_pct = round((len(matched_skills) / len(jd_skills_set)) * 100, 1)
        else:
            skill_match_pct = 0.0

        # 3. Overall TF-IDF Semantic Cosine Similarity
        cosine_sim_pct = 0.0
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            cosine_sim_pct = round(float(sim) * 100, 1)
        except Exception:
            cosine_sim_pct = skill_match_pct

        # Combined Composite Fit Score
        composite_score = round((0.6 * skill_match_pct) + (0.4 * cosine_sim_pct), 1)

        # 4. Generate Targeted Gap & Verification Questions
        gap_probing_questions = self._generate_gap_probing_questions(missing_skills)
        deep_dive_questions = self._generate_verification_questions(matched_skills)

        return {
            "composite_score": composite_score,
            "skill_match_pct": skill_match_pct,
            "cosine_similarity_pct": cosine_sim_pct,
            "jd_skills_count": len(jd_skills_set),
            "resume_skills_count": len(resume_skills_set),
            "matched_skills": [s.title() for s in matched_skills],
            "missing_skills": [s.title() for s in missing_skills],
            "bonus_skills": [s.title() for s in bonus_skills],
            "jd_skills_by_category": jd_skills_dict,
            "resume_skills_by_category": resume_skills_dict,
            "gap_probing_questions": gap_probing_questions,
            "verification_questions": deep_dive_questions
        }

    def _generate_gap_probing_questions(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generates questions aimed at assessing aptitude for missing requirements."""
        questions = []
        for i, skill in enumerate(missing_skills[:5]):
            title_skill = skill.title()
            questions.append({
                "id": f"gap-{i+1:02d}",
                "skill": title_skill,
                "type": "Skill Gap Probe",
                "question": f"The job description highlights {title_skill}, which is not explicitly mentioned in your resume. Have you had exposure to {title_skill} in personal projects or coursework, or how would your existing skills help you get up to speed quickly?",
                "rationale": f"Probes candidate's adaptability and foundational readiness for {title_skill}."
            })
        return questions

    def _generate_verification_questions(self, matched_skills: List[str]) -> List[Dict[str, Any]]:
        """Generates deep-dive verification questions for skills claimed on the resume."""
        questions = []
        for i, skill in enumerate(matched_skills[:5]):
            title_skill = skill.title()
            questions.append({
                "id": f"verify-{i+1:02d}",
                "skill": title_skill,
                "type": "Resume Verification",
                "question": f"You listed {title_skill} as a key skill in your resume. Can you walk us through the most technically challenging implementation or production bug you resolved involving {title_skill}?",
                "rationale": f"Verifies authenticity and senior-level depth in {title_skill}."
            })
        return questions


# Singleton instance
resume_analyzer = ResumeAnalyzer()
