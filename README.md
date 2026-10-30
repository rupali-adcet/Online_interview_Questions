# 🎯 CogniHire: Online Interview Questions Generator using NLP

An end-to-end, production-grade Natural Language Processing (NLP) system and interactive dashboard that transforms Job Descriptions (JDs), technical curricula, and candidate resumes into multi-tiered, rubric-backed interview questions and automated candidate answer evaluations.

---

## 🌟 Key Highlights

- **100% Offline Local NLP Engine**: Built on top of NLTK, Scikit-Learn, TextBlob, and NetworkX. No paid API key required to run.
- **Optional Generative AI Mode**: One-click Google Gemini API key support for on-the-fly fresh generative questions.
- **Bloom's Revised Taxonomy**: Synthesizes questions across all 6 cognitive tiers (Remembering, Understanding, Applying, Analyzing, Evaluating, Creating).
- **Difficulty Grading**: Scales questions systematically across Junior, Mid-Level, and Senior/Architect tiers.
- **JD vs. Resume Semantic Matcher**: Computes skill overlap, TF-IDF cosine similarity, identifies critical missing skill gaps, and auto-generates gap-probing interview questions.
- **Automated Candidate Answer Grader**: Evaluates candidate responses using semantic similarity, technical keyword coverage, tone/confidence analysis (VADER), and readability ease.
- **Interactive NLP Visualizer**: Pedagogical explorer displaying live tokenization, POS tagging, noun chunks, TF-IDF weights, and TextRank graph centrality.
- **Export & Printable Interview Kits**: One-click export to structured JSON, CSV spreadsheets, and formatted Markdown interview scorecards.

---

## 🏗️ System Architecture & NLP Pipeline

```
                                  +-----------------------------+
                                  | Raw Text / JD / Resume / CV |
                                  +--------------+--------------+
                                                 |
                                                 v
                                  +-----------------------------+
                                  | Normalization & Tokenizing  |
                                  | (NLTK Tokenize, Lemmatize)  |
                                  +--------------+--------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       v                                                   v
         +---------------------------+                       +---------------------------+
         | Syntactic Chunking (POS)  |                       | TF-IDF & TextRank Graph   |
         |  `<JJ.*>*<NN.*>+` Regex   |                       | PageRank Keyword Ranking  |
         +-------------+-------------+                       +-------------+-------------+
                       |                                                   |
                       +-------------------------+-------------------------+
                                                 |
                                                 v
                                  +-----------------------------+
                                  | Skill Taxonomy Classification|
                                  | 7 Tech Categories (Lang/DB) |
                                  +--------------+--------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       v                                                   v
         +---------------------------+                       +---------------------------+
         |  Bloom's Taxonomy QG      |                       | Resume-JD Semantic Match  |
         | 6 Cognitive Question Tiers|                       | Gap Analysis & Probing Qs |
         +-------------+-------------+                       +-------------+-------------+
                       |                                                   |
                       +-------------------------+-------------------------+
                                                 |
                                                 v
                                  +-----------------------------+
                                  |  Interactive Web Dashboard  |
                                  |   (Streamlit + Altair Data)  |
                                  +--------------+--------------+
                                                 |
                                                 v
                                  +-----------------------------+
                                  | NLP Candidate Answer Grader |
                                  | Cosine Sim + Keywords + Tone|
                                  +-----------------------------+
```

---

## 📂 Project Directory Structure

```
online_interview_question_generator/
├── app.py                      # Interactive Streamlit Web Dashboard
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows 1-click batch launcher
├── run.ps1                     # PowerShell launcher
├── README.md                   # Full documentation & project report
├── core/
│   ├── __init__.py
│   ├── dataset_loader.py       # Tech taxonomy, sample JDs, resumes & 250+ curated questions
│   ├── nlp_engine.py           # Tokenization, POS chunking, TF-IDF, TextRank & readability
│   ├── question_generator.py   # Bloom's taxonomy & syntactic WH-question generator
│   ├── resume_analyzer.py      # Resume vs JD semantic similarity & gap probing
│   ├── answer_evaluator.py     # Automated candidate response scoring & sentiment feedback
│   └── export_utils.py         # JSON, CSV, and Markdown Interview Kit exporters
└── tests/
    └── test_nlp_engine.py      # Automated unit tests for all core NLP modules
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ (Python 3.11 recommended)
- Windows / macOS / Linux

### 2. Run the Application
Open a terminal in the project directory and run:

```bash
# Option A: Using the Windows batch script
run.bat

# Option B: Directly via Streamlit
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

### 3. Run Automated Tests
```bash
python -m unittest tests/test_nlp_engine.py
```

---

## 🖥️ Dashboard Features & Tab Guide

### 1. 📊 Overview & Analytics
- Executive overview of project metrics: question bank size, supported taxonomies, and cognitive tiers.
- Interactive Altair charts breaking down domain coverage.
- High-level system architecture reference.

### 2. 🎯 JD & Resume Matcher
- Compare a Job Description against a Candidate Resume.
- Computes **Composite Fit Score**, **Skill Match Recall**, and **TF-IDF Cosine Similarity**.
- Generates **Skill Gap Probing Questions** (to test aptitude in missing technologies) and **Resume Verification Questions** (to verify authenticity of claimed experience).

### 3. 🧠 Domain & Topic Question Studio
- Generate interview questions by selecting pre-vetted domains (Python, ML, DevOps, System Design, Web, etc.) or entering custom technologies.
- Filter dynamically by Difficulty (**Junior**, **Mid**, **Senior**) and Bloom's Cognitive Level.
- Inspect Model Answers, Expected Keywords, and Assessment Rubrics for each question.

### 4. ✍️ Live Mock Interview & Answer Grader
- Test candidate answers in real time.
- Grades candidate answers across:
  - **Keyword Coverage**: Detects presence of essential domain keywords.
  - **Semantic Relevance**: TF-IDF cosine similarity against expected model answer.
  - **Tone & Confidence**: Detects decisive action verbs vs hesitation markers via VADER sentiment.
  - **Readability & Length**: Flesch Reading Ease and response depth.
- Outputs an overall score (0-100), Letter Grade (A to F), and qualitative coaching tips.

### 5. 🔬 NLP Pipeline & TextRank Visualizer
- Input any raw sentence or job posting to visualize the underlying NLP steps:
  - Clean word tokens.
  - Part-of-Speech (POS) tags.
  - Extracted Noun Phrase chunks (`<JJ.*>*<NN.*>+`).
  - TF-IDF scores interactive chart.
  - TextRank PageRank graph centrality chart.

### 6. 📑 Export & Interview Kits
- Export generated question sets and rubrics into:
  - **JSON** (structured schema for ATS integration)
  - **CSV** (for spreadsheet review)
  - **Markdown Interview Kit** (printable guide with scoring rubrics and candidate scorecard tables)

---

## 🔬 NLP Methodology & Scientific Principles

### 1. Bloom's Revised Taxonomy Mapping
Interview questions are classified into 6 cognitive levels:
| Level | Cognitive Process | Question Intent | Sample Action Verbs |
| :--- | :--- | :--- | :--- |
| **1. Remembering** | Retrieve relevant knowledge | Define, identify, list primitives | Define, What is |
| **2. Understanding** | Construct meaning from messages | Explain underlying execution | Explain, Compare, Clarify |
| **3. Applying** | Execute procedure in situation | Implementation in production | Implement, Deploy, Integrate |
| **4. Analyzing** | Deconstruct into constituent parts | Bottlenecks, debug silent failures | Diagnose, Debug, Contrast |
| **5. Evaluating** | Make judgments based on criteria | Assess trade-offs, security, failure | Assess, Justify, Critique |
| **6. Creating** | Put elements together to form coherent whole | High-scale system design | Architect, Design, Formulate |

### 2. TextRank Keyword Extraction
TextRank models text as an undirected graph $G = (V, E)$, where vertices $V$ represent distinct content words, and edges $E$ connect words co-occurring within a sliding window $W$. The prestige of word $V_i$ is solved iteratively via PageRank:

$$WS(V_i) = (1 - d) + d \sum_{V_j \in In(V_i)} \frac{w_{ji}}{\sum_{V_k \in Out(V_j)} w_{jk}} WS(V_j)$$

where $d$ is the damping factor (typically $0.85$).

---

## 📄 License
MIT License. Open for educational, academic, and commercial customization.
