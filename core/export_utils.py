"""
export_utils.py
Utilities to export generated interview questions and assessment rubrics
into JSON, CSV, and formatted Interview Kit Markdown documents.
"""

import json
import csv
import io
from typing import List, Dict, Any


def export_to_json(questions: List[Dict[str, Any]]) -> str:
    """Exports questions list to formatted JSON string."""
    return json.dumps(questions, indent=2)


def export_to_csv(questions: List[Dict[str, Any]]) -> str:
    """Exports questions list to CSV format."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "ID", "Skill / Domain", "Taxonomy Level", "Difficulty",
        "Question", "Model Answer", "Keywords", "Source"
    ])

    for q in questions:
        kw_str = ", ".join(q.get("keywords", []))
        writer.writerow([
            q.get("id", ""),
            q.get("skill", ""),
            q.get("taxonomy", ""),
            q.get("difficulty", ""),
            q.get("question", ""),
            q.get("model_answer", ""),
            kw_str,
            q.get("source", "")
        ])

    return output.getvalue()


def export_to_interview_kit_markdown(
    questions: List[Dict[str, Any]],
    role_or_topic: str = "Technical Interview",
    candidate_name: str = "Candidate"
) -> str:
    """
    Generates a professional, printable Interview Kit in Markdown.
    Includes interviewer guidelines, questions, Bloom's level, model answers, and rubric scorecards.
    """
    md = []
    md.append(f"# 📋 Technical Interview Kit: {role_or_topic}")
    md.append(f"**Candidate:** {candidate_name} | **Total Questions:** {len(questions)}")
    md.append("\n---\n")

    md.append("## 🎯 Interviewer Instructions & Best Practices")
    md.append("- Probe for real-world depth rather than memorized definitions.")
    md.append("- Rate each question on Technical Accuracy, Depth/Trade-offs, and Communication Clarity (1-5 scale).")
    md.append("- Use the provided model answers and keywords as baseline guideposts.\n")

    md.append("## 📝 Interview Questions & Evaluation Guide\n")

    for i, q in enumerate(questions, 1):
        diff = q.get('difficulty', 'Mid')
        tax = q.get('taxonomy', 'Understanding')
        skill = q.get('skill', 'General')
        q_text = q.get('question', '')
        model_ans = q.get('model_answer', 'N/A')
        keywords = ", ".join(q.get('keywords', []))

        md.append(f"### Q{i}. {q_text}")
        md.append(f"- **Domain/Skill:** `{skill}` | **Difficulty:** `{diff}` | **Bloom's Taxonomy:** `{tax}`")
        md.append(f"- **Key Concepts Expected:** *{keywords}*")
        md.append(f"\n> **Model Answer Guidance:**\n> {model_ans}\n")

        rubric = q.get("rubric", {})
        if isinstance(rubric, dict) and rubric:
            md.append("**Evaluation Rubric:**")
            for criterion, desc in rubric.items():
                md.append(f"  - **{criterion.replace('_', ' ').title()}:** {desc}")

        md.append("\n**Candidate Scorecard:**")
        md.append("| Criterion | Score (1-5) | Interviewer Notes |")
        md.append("| :--- | :---: | :--- |")
        md.append("| Technical Accuracy | [ ] | |")
        md.append("| System Depth & Trade-offs | [ ] | |")
        md.append("| Communication & Articulation | [ ] | |")
        md.append("\n---\n")

    return "\n".join(md)
