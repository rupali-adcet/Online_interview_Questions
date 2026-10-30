"""
answer_evaluator.py
Evaluates candidate interview answers using NLP keyword coverage,
semantic similarity, VADER sentiment, tone/confidence, and readability metrics.
"""

import re
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from core.nlp_engine import nlp_engine

# Confidence indicators and hesitation markers
CONFIDENT_INDICATORS = {
    "implemented", "architected", "designed", "optimized", "benchmarked",
    "analyzed", "reduced", "scaled", "resolved", "debugged", "monitored",
    "ensured", "mitigated", "delivered", "demonstrated"
}

HESITATION_INDICATORS = {
    "maybe", "i guess", "probably", "perhaps", "sort of", "kind of",
    "not sure", "i think maybe", "might be", "honestly don't know"
}


class AnswerEvaluator:
    """
    NLP Answer Evaluator providing multi-factor grading and qualitative feedback.
    """

    def __init__(self):
        self.nlp = nlp_engine
        try:
            self.vader = SentimentIntensityAnalyzer()
        except Exception:
            try:
                import nltk
                nltk.download('vader_lexicon', quiet=True)
                self.vader = SentimentIntensityAnalyzer()
            except Exception:
                self.vader = None

    def evaluate(
        self,
        candidate_answer: str,
        model_answer: str,
        expected_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Grades candidate's response against expected model answer and keywords.
        """
        clean_cand = self.nlp.clean_text(candidate_answer)
        clean_model = self.nlp.clean_text(model_answer)

        if not clean_cand or len(clean_cand.split()) < 3:
            return {
                "overall_score": 0.0,
                "grade": "Incomplete",
                "semantic_similarity_pct": 0.0,
                "keyword_coverage_pct": 0.0,
                "found_keywords": [],
                "missing_keywords": expected_keywords or [],
                "confidence_score": 0.0,
                "readability_ease": 0.0,
                "feedback": ["Answer is too brief to evaluate. Please provide a substantive technical response."]
            }

        # 1. Keyword Coverage
        if not expected_keywords:
            # Extract keywords from model answer using TF-IDF
            extracted = self.nlp.extract_tfidf_keywords(clean_model, top_n=6)
            expected_keywords = [kw for kw, _ in extracted]

        found_keywords = []
        missing_keywords = []
        cand_lower = clean_cand.lower()

        for kw in expected_keywords:
            pattern = r'(?:\b|(?<=\W))' + re.escape(kw.lower()) + r'(?:\b|(?=\W))'
            if re.search(pattern, cand_lower):
                found_keywords.append(kw)
            else:
                missing_keywords.append(kw)

        keyword_coverage_pct = round(
            (len(found_keywords) / max(len(expected_keywords), 1)) * 100, 1
        )

        # 2. Semantic Similarity via TF-IDF Cosine Similarity
        semantic_sim_pct = 0.0
        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
            tfidf_mat = vectorizer.fit_transform([clean_cand, clean_model])
            sim = cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:2])[0][0]
            semantic_sim_pct = round(float(sim) * 100, 1)
        except Exception:
            semantic_sim_pct = keyword_coverage_pct

        # 3. Tone & Confidence Analysis
        cand_words = set(self.nlp.word_tokenize_clean(clean_cand))
        confident_count = len(cand_words.intersection(CONFIDENT_INDICATORS))

        hesitation_count = 0
        for phrase in HESITATION_INDICATORS:
            if phrase in cand_lower:
                hesitation_count += 1

        # VADER Sentiment
        sentiment_compound = 0.0
        if self.vader:
            vader_res = self.vader.polarity_scores(clean_cand)
            sentiment_compound = vader_res.get('compound', 0.0)

        confidence_score = max(0, min(100, round(
            50 + (confident_count * 15) - (hesitation_count * 20) + (sentiment_compound * 20), 1
        )))

        # 4. Length Adequacy & Readability
        cand_word_count = len(clean_cand.split())
        length_score = 100 if cand_word_count >= 50 else (cand_word_count / 50.0) * 100
        length_score = min(100.0, length_score)

        readability_metrics = self.nlp.compute_readability_metrics(clean_cand)
        reading_ease = readability_metrics["flesch_reading_ease"]

        # 5. Composite Weighted Score (0 to 100)
        # Weights: 40% Keyword Coverage + 35% Semantic Similarity + 15% Confidence + 10% Length
        overall_score = round(
            (0.40 * keyword_coverage_pct) +
            (0.35 * semantic_sim_pct) +
            (0.15 * confidence_score) +
            (0.10 * length_score),
            1
        )
        overall_score = max(0.0, min(100.0, overall_score))

        # Determine Letter Grade
        if overall_score >= 85:
            grade = "A (Exceptional)"
        elif overall_score >= 70:
            grade = "B (Proficient)"
        elif overall_score >= 55:
            grade = "C (Adequate)"
        elif overall_score >= 40:
            grade = "D (Needs Improvement)"
        else:
            grade = "F (Unsatisfactory)"

        # 6. Qualitative Actionable Feedback
        feedback = []
        if keyword_coverage_pct >= 75:
            feedback.append("Excellent technical terminology coverage. You effectively used core domain keywords.")
        elif keyword_coverage_pct < 40:
            feedback.append(f"Consider explicitly referencing key technical concepts such as: {', '.join(missing_keywords[:4])}.")

        if semantic_sim_pct >= 60:
            feedback.append("Strong semantic alignment with expected theoretical and practical principles.")
        else:
            feedback.append("Your response could align more closely with industry best practices and core architectural patterns.")

        if hesitation_count > 0:
            feedback.append(f"Detected {hesitation_count} hesitation marker(s). Express your technical solutions with greater assertiveness.")

        if confident_count >= 2:
            feedback.append("Great usage of active engineering action verbs, demonstrating hands-on execution.")

        if cand_word_count < 30:
            feedback.append("Your answer is somewhat brief. Elaborate on edge cases, scaling considerations, or real-world examples.")

        return {
            "overall_score": overall_score,
            "grade": grade,
            "keyword_coverage_pct": keyword_coverage_pct,
            "semantic_similarity_pct": semantic_sim_pct,
            "confidence_score": confidence_score,
            "word_count": cand_word_count,
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords,
            "readability_ease": reading_ease,
            "feedback": feedback
        }


# Singleton instance
answer_evaluator = AnswerEvaluator()
