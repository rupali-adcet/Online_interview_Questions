"""
test_nlp_engine.py
Unit tests for the Online Interview Question Generator NLP system.
"""

import unittest
from core.nlp_engine import nlp_engine
from core.question_generator import question_generator
from core.resume_analyzer import resume_analyzer
from core.answer_evaluator import answer_evaluator
from core.export_utils import export_to_json, export_to_csv, export_to_interview_kit_markdown


class TestNLPEngine(unittest.TestCase):

    def setUp(self):
        self.sample_text = """
        Looking for a Senior Python Developer with deep experience in FastAPI, Docker, and PostgreSQL.
        Must have strong understanding of microservices architecture and distributed caching using Redis.
        """

    def test_clean_text(self):
        raw = "Check out https://test.com  and email test@example.com   now! "
        cleaned = nlp_engine.clean_text(raw)
        self.assertNotIn("https://", cleaned)
        self.assertNotIn("@example.com", cleaned)

    def test_skill_extraction(self):
        skills = nlp_engine.get_all_matched_skills(self.sample_text)
        self.assertIn("python", skills)
        self.assertIn("fastapi", skills)
        self.assertIn("docker", skills)
        self.assertIn("postgresql", skills)
        self.assertIn("redis", skills)

    def test_tfidf_keywords(self):
        keywords = nlp_engine.extract_tfidf_keywords(self.sample_text, top_n=10)
        self.assertTrue(len(keywords) > 0)
        kw_names = [kw for kw, _ in keywords]
        self.assertTrue(any(term in " ".join(kw_names) for term in ["architecture", "caching", "developer", "microservices"]))

    def test_textrank_keywords(self):
        keywords = nlp_engine.extract_textrank_keywords(self.sample_text, top_n=5)
        self.assertTrue(len(keywords) > 0)

    def test_question_generation_from_skills(self):
        skills = ["Python", "Docker", "PostgreSQL"]
        questions = question_generator.generate_from_skills(skills, num_questions=4)
        self.assertEqual(len(questions), 4)
        for q in questions:
            self.assertIn("question", q)
            self.assertIn("taxonomy", q)
            self.assertIn("difficulty", q)

    def test_resume_analysis(self):
        resume = "Software Engineer experienced in Python, FastAPI, and PostgreSQL."
        jd = "We need an engineer skilled in Python, FastAPI, Docker, and Kubernetes."
        res = resume_analyzer.analyze(resume, jd)

        self.assertIn("Python", res["matched_skills"])
        self.assertIn("Docker", res["missing_skills"])
        self.assertTrue(res["skill_match_pct"] > 0)
        self.assertTrue(len(res["gap_probing_questions"]) > 0)

    def test_answer_evaluation(self):
        cand_ans = """
        The Python GIL prevents multiple threads from executing bytecodes concurrently.
        For CPU-bound tasks, we use multiprocessing to achieve true parallelism.
        For I/O-bound tasks, threading works well because the GIL is released during I/O operations.
        """
        model_ans = "The GIL is a mutex preventing simultaneous thread execution. Use multiprocessing for CPU-bound tasks."
        keywords = ["gil", "multiprocessing", "cpu-bound", "i/o-bound"]

        eval_res = answer_evaluator.evaluate(cand_ans, model_ans, keywords)
        self.assertGreaterEqual(eval_res["overall_score"], 60)
        self.assertIn("gil", eval_res["found_keywords"])

    def test_export_utilities(self):
        sample_q = [{
            "id": "gen-001",
            "skill": "Python",
            "taxonomy": "Understanding",
            "difficulty": "Mid",
            "question": "What is Python GIL?",
            "model_answer": "Global Interpreter Lock.",
            "keywords": ["gil"],
            "source": "NLP Engine"
        }]
        json_out = export_to_json(sample_q)
        csv_out = export_to_csv(sample_q)
        md_out = export_to_interview_kit_markdown(sample_q)

        self.assertIn("gen-001", json_out)
        self.assertIn("gen-001", csv_out)
        self.assertIn("What is Python GIL?", md_out)


if __name__ == "__main__":
    unittest.main()
