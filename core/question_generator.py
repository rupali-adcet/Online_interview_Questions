"""
question_generator.py
Synthesizes structured interview questions using NLP syntactic transforms,
Bloom's Cognitive Taxonomy templates, skill relational synthesis, and difficulty scaling.
"""

import os
import random
from typing import List, Dict, Any, Optional
from core.nlp_engine import nlp_engine
from core.dataset_loader import CURATED_QUESTIONS

# Bloom's Taxonomy Cognitive Levels & Question Templates
BLOOM_TEMPLATES = {
    "Remembering": [
        "What is {skill} and what core problem does it solve in modern software architecture?",
        "Define {skill}. What are its primary building blocks and standard terminology?",
        "What are the default configuration parameters or core primitives in {skill}?"
    ],
    "Understanding": [
        "Explain how {skill} works under the hood and contrast it with traditional alternatives.",
        "Can you explain the lifecycle and execution model of {skill} in a production environment?",
        "Why is {skill} preferred over older patterns, and what are its key conceptual advantages?"
    ],
    "Applying": [
        "How would you integrate {skill} into a production application to handle sudden traffic spikes?",
        "Walk us through how you would configure and deploy {skill} with automated error handling and logging.",
        "Describe a real-world scenario where you used {skill} to solve a critical engineering bottleneck."
    ],
    "Analyzing": [
        "Analyze the performance bottlenecks, latency overhead, and resource trade-offs when using {skill}.",
        "Compare and contrast {skill_a} versus {skill_b}. In what scenarios would you choose one over the other?",
        "How would you diagnose and debug a silent failure or memory leak involving {skill}?"
    ],
    "Evaluating": [
        "Under what specific business or technical constraints would you advise AGAINST adopting {skill}?",
        "How do you evaluate whether {skill} is performing optimally versus becoming technical debt?",
        "Assess the security risks and attack vectors associated with {skill} and how to mitigate them."
    ],
    "Creating": [
        "Design a resilient, scalable architecture that combines {skill_a} with {skill_b} for high availability.",
        "How would you architect an end-to-end continuous monitoring and automated failover strategy using {skill}?",
        "Draft a technical RFC proposing the migration of a legacy monolithic stack to {skill}."
    ]
}

# Domain-specific scenario prompts
SCENARIO_TEMPLATES = [
    "You notice that your production service utilizing {skill} is experiencing a 5x increase in p99 latency during peak hours. Outline your step-by-step troubleshooting playbook.",
    "A junior developer on your team submits a PR using {skill} that has potential race conditions or unhandled exceptions. What code review checklist items would you evaluate?",
    "Your team needs to scale {skill} to support 10 million daily active users with 99.99% uptime. What caching, sharding, and redundancy strategies would you employ?"
]


class QuestionGenerator:
    """
    Intelligent Question Generator using syntactic NLP templates, Bloom's Taxonomy,
    and optional LLM enhancement.
    """

    def __init__(self):
        self.nlp = nlp_engine
        self.curated_pool = CURATED_QUESTIONS

    def generate_from_skills(
        self,
        skills: List[str],
        difficulty: str = "All",
        taxonomy_level: str = "All",
        num_questions: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Generates interview questions targeting the supplied technical skills.
        """
        if not skills:
            skills = ["software engineering", "distributed systems", "database indexing"]

        questions: List[Dict[str, Any]] = []
        clean_skills = [s.strip().title() for s in skills if len(s.strip()) > 1]

        # 1. First, search curated questions for high-quality pre-vetted matches
        matched_curated = []
        for q in self.curated_pool:
            q_keywords = [k.lower() for k in q.get("keywords", [])]
            for s in clean_skills:
                s_low = s.lower()
                if any(s_low in kw for kw in q_keywords) or s_low in q["question"].lower():
                    matched_curated.append(q)
                    break

        for q in matched_curated:
            if difficulty != "All" and q.get("difficulty") != difficulty:
                continue
            if taxonomy_level != "All" and q.get("taxonomy") != taxonomy_level:
                continue
            questions.append({
                "id": f"gen-{len(questions)+1:03d}",
                "skill": q.get("domain", "General"),
                "question": q["question"],
                "taxonomy": q.get("taxonomy", "Understanding"),
                "difficulty": q.get("difficulty", "Mid"),
                "model_answer": q.get("model_answer", "Candidate should discuss core architectural tradeoffs."),
                "keywords": q.get("keywords", [s.lower() for s in clean_skills[:3]]),
                "rubric": q.get("rubric", {
                    "depth": "Covers underlying concepts and trade-offs.",
                    "accuracy": "Correctly articulates industry-standard best practices.",
                    "clarity": "Structures response with clear examples."
                }),
                "source": "Curated Knowledge Base"
            })

        # 2. Synthesize dynamic questions using Bloom's Taxonomy templates
        bloom_levels = list(BLOOM_TEMPLATES.keys())
        target_levels = [taxonomy_level] if taxonomy_level != "All" else bloom_levels

        for skill in clean_skills:
            if len(questions) >= num_questions:
                break

            for level in target_levels:
                if len(questions) >= num_questions:
                    break

                templates = BLOOM_TEMPLATES.get(level, BLOOM_TEMPLATES["Understanding"])
                tmpl = random.choice(templates)

                # Pair with another skill if available
                other_skills = [s for s in clean_skills if s != skill]
                skill_b = other_skills[0] if other_skills else "Microservices Architecture"

                q_text = tmpl.format(skill=skill, skill_a=skill, skill_b=skill_b)

                # Assign appropriate difficulty based on Bloom Level
                assigned_diff = "Junior" if level in ["Remembering"] else ("Mid" if level in ["Understanding", "Applying"] else "Senior")

                if difficulty != "All" and assigned_diff != difficulty:
                    continue

                questions.append({
                    "id": f"gen-{len(questions)+1:03d}",
                    "skill": skill,
                    "question": q_text,
                    "taxonomy": level,
                    "difficulty": assigned_diff,
                    "model_answer": f"A comprehensive response should explain the core mechanics of {skill}, compare it with industry standards, discuss operational trade-offs, and outline failure modes.",
                    "keywords": [skill.lower(), "performance", "scalability", "architecture"],
                    "rubric": {
                        "depth": f"Exhibits in-depth knowledge of {skill}.",
                        "accuracy": "Highlights correct architectural patterns and APIs.",
                        "tradeoffs": "Understands edge cases and production constraints."
                    },
                    "source": "NLP Bloom's Synthesizer"
                })

        # 3. Add Scenario Questions if needed to reach target count
        while len(questions) < num_questions and clean_skills:
            sk = random.choice(clean_skills)
            sc_tmpl = random.choice(SCENARIO_TEMPLATES)
            q_text = sc_tmpl.format(skill=sk)
            questions.append({
                "id": f"gen-{len(questions)+1:03d}",
                "skill": sk,
                "question": q_text,
                "taxonomy": "Evaluating",
                "difficulty": "Senior",
                "model_answer": f"The candidate should describe monitoring metrics, alert thresholds, reproducible isolation steps, root cause analysis, and long-term mitigation for {sk}.",
                "keywords": [sk.lower(), "monitoring", "latency", "troubleshooting", "root cause"],
                "rubric": {
                    "systematic_approach": "Methodical debugging without guesswork.",
                    "metrics_focus": "References latency percentiles (p99), CPU, I/O, or connection pools.",
                    "communication": "Explains team escalation and post-mortem procedures."
                },
                "source": "NLP Scenario Engine"
            })

        return questions[:num_questions]

    def generate_from_raw_text(
        self,
        text: str,
        difficulty: str = "All",
        taxonomy_level: str = "All",
        num_questions: int = 8
    ) -> Dict[str, Any]:
        """
        Parses raw text (Job Description, syllabus, or technical article),
        extracts entities and key concepts, and generates customized questions.
        """
        # 1. NLP Feature Extraction
        skills_dict = self.nlp.extract_skills_from_text(text)
        flat_skills = self.nlp.get_all_matched_skills(text)
        tfidf_kw = self.nlp.extract_tfidf_keywords(text, top_n=10)
        noun_phrases = self.nlp.extract_noun_phrases(text)[:8]
        readability = self.nlp.compute_readability_metrics(text)

        # 2. Combine detected skills and top TF-IDF keywords
        primary_entities = flat_skills.copy()
        for kw, score in tfidf_kw:
            if kw.title() not in primary_entities and len(kw) > 3:
                primary_entities.append(kw.title())

        # If nothing recognized, fallback to top noun phrases or generic tech
        if not primary_entities:
            primary_entities = [np.title() for np in noun_phrases[:5]] or ["Software Architecture", "Data Structures"]

        # 3. Synthesize Questions
        generated_questions = self.generate_from_skills(
            skills=primary_entities,
            difficulty=difficulty,
            taxonomy_level=taxonomy_level,
            num_questions=num_questions
        )

        return {
            "skills_by_category": skills_dict,
            "detected_skills": flat_skills,
            "top_tfidf_keywords": tfidf_kw,
            "noun_phrases": noun_phrases,
            "readability": readability,
            "questions": generated_questions
        }

    def generate_with_gemini(
        self,
        api_key: str,
        role_or_topic: str,
        skills: List[str],
        num_questions: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Optional Generative AI extension using Google Gemini API if the user has a key.
        Falls back to local NLP on failure.
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            skills_str = ", ".join(skills) if skills else "General Software Engineering"
            prompt = f"""
            You are an expert technical interviewer. Generate {num_questions} rigorous, realistic interview questions
            for the topic or role: '{role_or_topic}' focusing on these technical skills: {skills_str}.

            Format your response strictly as valid JSON containing a list of objects with these keys:
            [
              {{
                "skill": "skill name",
                "question": "the question text",
                "taxonomy": "Remembering | Understanding | Applying | Analyzing | Evaluating | Creating",
                "difficulty": "Junior | Mid | Senior",
                "model_answer": "concise bulleted model answer",
                "keywords": ["keyword1", "keyword2"]
              }}
            ]
            Return only the JSON array with no extra markdown backticks or commentary.
            """
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            # Clean possible markdown ticks
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("`").replace("json", "").strip()

            import json
            data = json.loads(raw_text)
            for i, q in enumerate(data):
                q["id"] = f"gemini-{i+1:03d}"
                q["source"] = "Gemini AI"
                if "rubric" not in q:
                    q["rubric"] = {
                        "accuracy": "Covers accurate technical concepts.",
                        "depth": "Demonstrates thorough understanding."
                    }
            return data
        except Exception:
            return None


# Singleton instance
question_generator = QuestionGenerator()
