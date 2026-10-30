"""
app.py
Production-ready Streamlit Dashboard for Online Interview Questions Generator using NLP.
Features multi-tab navigation, JD & Resume analysis, domain question studio,
live candidate answer evaluation, and NLP pipeline visualization.
"""

import os
import streamlit as st
import pandas as pd
import altair as alt

# Import core modules
from core.nlp_engine import nlp_engine
from core.question_generator import question_generator
from core.resume_analyzer import resume_analyzer
from core.answer_evaluator import answer_evaluator
from core.dataset_loader import (
    SKILL_TAXONOMY,
    CURATED_QUESTIONS,
    SAMPLE_JOB_DESCRIPTIONS,
    SAMPLE_RESUMES,
    get_all_skills
)
from core.export_utils import (
    export_to_json,
    export_to_csv,
    export_to_interview_kit_markdown
)

# Page configuration
st.set_page_config(
    page_title="CogniHire | NLP Interview Question Generator & Evaluator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    .badge-junior {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-mid {
        background-color: #E1EFFE;
        color: #1E429F;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-senior {
        background-color: #FDF2E9;
        color: #9C4221;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-bloom {
        background-color: #F3E8FF;
        color: #6B21A8;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .skill-tag {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        border-radius: 16px;
        padding: 2px 10px;
        font-size: 0.82rem;
        margin: 2px 4px 2px 0;
        font-weight: 500;
    }
    .skill-missing {
        display: inline-block;
        background-color: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECACA;
        border-radius: 16px;
        padding: 2px 10px;
        font-size: 0.82rem;
        margin: 2px 4px 2px 0;
        font-weight: 500;
    }
    .question-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #3B82F6;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = []
if "mock_question" not in st.session_state:
    st.session_state.mock_question = CURATED_QUESTIONS[0]["question"]
if "mock_model_answer" not in st.session_state:
    st.session_state.mock_model_answer = CURATED_QUESTIONS[0]["model_answer"]
if "mock_keywords" not in st.session_state:
    st.session_state.mock_keywords = CURATED_QUESTIONS[0]["keywords"]

# Sidebar Navigation & Settings
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
st.sidebar.title("CogniHire NLP")
st.sidebar.caption("Automated Interview Question Generator & Answer Grader")

selected_tab = st.sidebar.radio(
    "Navigation Menu",
    [
        "📊 Overview & Analytics",
        "🎯 JD & Resume Matcher",
        "🧠 Domain & Topic Studio",
        "✍️ Mock Interview & Grader",
        "🔬 NLP Pipeline Visualizer",
        "📑 Export & Interview Kits"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Generation Parameters")
global_difficulty = st.sidebar.selectbox("Target Difficulty", ["All", "Junior", "Mid", "Senior"])
global_taxonomy = st.sidebar.selectbox(
    "Bloom's Taxonomy Level",
    ["All", "Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating"]
)
num_questions_slider = st.sidebar.slider("Number of Questions", min_value=3, max_value=15, value=6)

# Optional Gemini API Key
st.sidebar.markdown("---")
with st.sidebar.expander("🤖 Optional AI Enhancement"):
    gemini_key = st.text_input("Gemini API Key (Optional)", type="password", help="Leave blank to use the offline local NLP engine.")
    if gemini_key:
        st.success("Gemini API configured!")
    else:
        st.info("Using 100% offline local NLP engine (NLTK + Scikit-Learn + TextRank).")


# ==============================================================================
# TAB 1: OVERVIEW & ANALYTICS
# ==============================================================================
if selected_tab == "📊 Overview & Analytics":
    st.markdown('<div class="main-header">🎯 Online Interview Questions Generator using NLP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">An intelligent Natural Language Processing dashboard that transforms Job Descriptions, syllabi, and resumes into multi-tiered, rubric-backed interview questions.</div>', unsafe_allow_html=True)

    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">250+</div>
            <div class="metric-label">Curated Questions & Rubrics</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">7</div>
            <div class="metric-label">Tech Skill Taxonomies</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">6 Levels</div>
            <div class="metric-label">Bloom's Cognitive Taxonomy</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">100%</div>
            <div class="metric-label">Offline Local NLP Engine</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.subheader("🏗️ System Architecture & NLP Workflow")
        st.markdown("""
        The system implements a multi-paradigm NLP pipeline to synthesize high-relevance technical interview questions:

        1. **Text Normalization & Preprocessing**: Cleans input artifacts, handles irregular casing, preserves technical terms (`C++`, `.NET`, `Node.js`), and removes low-signal stopwords.
        2. **Syntactic Chunking & POS Tagging**: Identifies noun phrases and technical verb-object compounds (`<JJ.*>*<NN.*>+`) via NLTK Regexp chunking.
        3. **TF-IDF & TextRank Graph Centrality**: Scores core engineering competencies and extracts central keywords using NetworkX PageRank over word co-occurrence graphs.
        4. **Skill Taxonomy Extraction**: Maps extracted entities against structured taxonomies across Languages, Cloud, AI/ML, Databases, and Architecture.
        5. **Bloom's Cognitive Synthesis**: Maps target concepts across 6 cognitive tiers (from recall to architectural evaluation and synthesis).
        6. **Semantic Answer Evaluation**: Evaluates candidate responses against model answers using TF-IDF cosine similarity, keyword coverage, and VADER sentiment.
        """)

    with col_right:
        st.subheader("📊 Domain Knowledge Coverage")
        taxonomy_data = []
        for cat, skills in SKILL_TAXONOMY.items():
            taxonomy_data.append({"Category": cat, "Total Skills": len(skills)})
        df_tax = pd.DataFrame(taxonomy_data)

        chart = alt.Chart(df_tax).mark_bar(cornerRadius=6, color="#3B82F6").encode(
            x=alt.X("Total Skills:Q", title="Recognized Keywords"),
            y=alt.Y("Category:N", sort="-x", title=None),
            tooltip=["Category", "Total Skills"]
        ).properties(height=260)
        st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Key Features & Capabilities")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("#### 🎯 JD & Resume Analysis")
        st.write("Calculates candidate-job fit, identifies critical skill gaps, and synthesizes tailored probing questions to assess readiness.")
    with f2:
        st.markdown("#### 🧠 Bloom's Taxonomy Scaling")
        st.write("Generates questions scaled from Junior understanding up to Senior architectural evaluation and failure-mode analysis.")
    with f3:
        st.markdown("#### ✍️ Automated Answer Grader")
        st.write("NLP evaluator measuring semantic relevance, technical keyword coverage, tone assertiveness, and communication clarity.")


# ==============================================================================
# TAB 2: JD & RESUME MATCHER
# ==============================================================================
elif selected_tab == "🎯 JD & Resume Matcher":
    st.markdown('<div class="main-header">🎯 Job Description & Resume Gap Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload or paste a Job Description and candidate resume to discover skill matches, critical gaps, and auto-generate targeted interview questions.</div>', unsafe_allow_html=True)

    col_jd, col_res = st.columns(2)

    with col_jd:
        st.markdown("### 📄 Job Description (JD)")
        jd_preset = st.selectbox("Select Preset JD or Enter Custom", list(SAMPLE_JOB_DESCRIPTIONS.keys()) + ["Custom Input"])
        if jd_preset != "Custom Input":
            default_jd = SAMPLE_JOB_DESCRIPTIONS[jd_preset]
        else:
            default_jd = ""
        jd_input = st.text_area("Job Description Content", value=default_jd, height=280)

    with col_res:
        st.markdown("### 👤 Candidate Resume")
        res_preset = st.selectbox("Select Preset Resume or Enter Custom", list(SAMPLE_RESUMES.keys()) + ["Custom Input"])
        if res_preset != "Custom Input":
            default_res = SAMPLE_RESUMES[res_preset]
        else:
            default_res = ""
        res_input = st.text_area("Candidate Resume Content", value=default_res, height=280)

    if st.button("🚀 Analyze Fit & Generate Targeted Interview Questions", type="primary", use_container_width=True):
        if not jd_input.strip() or not res_input.strip():
            st.warning("Please provide both a Job Description and a Candidate Resume.")
        else:
            with st.spinner("Extracting NLP features, computing semantic similarity, and generating questions..."):
                analysis = resume_analyzer.analyze(res_input, jd_input)

                # Store analysis in session state
                st.session_state.last_analysis = analysis

    if "last_analysis" in st.session_state:
        analysis = st.session_state.last_analysis
        st.markdown("---")
        st.subheader("📊 Match Results & Fit Analytics")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Composite Fit Score", f"{analysis['composite_score']}%")
        with m2:
            st.metric("Skill Match Recall", f"{analysis['skill_match_pct']}%")
        with m3:
            st.metric("Semantic Cosine Sim", f"{analysis['cosine_similarity_pct']}%")
        with m4:
            st.metric("Missing Skills", f"{len(analysis['missing_skills'])}")

        st.markdown("---")
        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("#### ✅ Matching Technical Skills")
            if analysis["matched_skills"]:
                tags_html = " ".join([f'<span class="skill-tag">✓ {s}</span>' for s in analysis["matched_skills"]])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.info("No direct skill overlaps detected.")

            st.markdown("#### 🌟 Candidate Bonus Skills")
            if analysis["bonus_skills"]:
                tags_html = " ".join([f'<span class="skill-tag">+ {s}</span>' for s in analysis["bonus_skills"]])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.write("None")

        with c_right:
            st.markdown("#### ⚠️ Missing / Skill Gaps (Required by JD)")
            if analysis["missing_skills"]:
                tags_html = " ".join([f'<span class="skill-missing">✗ {s}</span>' for s in analysis["missing_skills"]])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.success("Candidate covers 100% of detected JD technical skills!")

        st.markdown("---")
        st.subheader("🎯 Auto-Generated Targeted Interview Questions")

        tab_gaps, tab_verify = st.tabs(["⚠️ Skill Gap Probing Questions", "🔍 Resume Verification Questions"])

        with tab_gaps:
            st.caption("These questions evaluate whether the candidate has foundational aptitude to pick up missing requirements.")
            for i, q in enumerate(analysis["gap_probing_questions"], 1):
                st.markdown(f"""
                <div class="question-box">
                    <strong>Q{i} [{q['skill']}]:</strong> {q['question']}<br>
                    <small style="color: #64748B;"><em>💡 Interviewer Rationale: {q['rationale']}</em></small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Test Q{i} in Mock Interview Grader", key=f"btn_gap_{i}"):
                    st.session_state.mock_question = q["question"]
                    st.session_state.mock_model_answer = f"Candidate should demonstrate clear transferable fundamentals, willingness to learn, and relate past experience to {q['skill']}."
                    st.session_state.mock_keywords = [q["skill"].lower(), "fundamentals", "learning", "architecture"]
                    st.success(f"Loaded Question {i} into Mock Interview tab!")

        with tab_verify:
            st.caption("Deep-dive technical questions to verify the depth and authenticity of claimed skills.")
            for i, q in enumerate(analysis["verification_questions"], 1):
                st.markdown(f"""
                <div class="question-box">
                    <strong>Q{i} [{q['skill']}]:</strong> {q['question']}<br>
                    <small style="color: #64748B;"><em>💡 Interviewer Rationale: {q['rationale']}</em></small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Test Q{i} in Mock Interview Grader", key=f"btn_verify_{i}"):
                    st.session_state.mock_question = q["question"]
                    st.session_state.mock_model_answer = f"Candidate should explain architectural trade-offs, debugging methodologies, and concrete metrics achieved with {q['skill']}."
                    st.session_state.mock_keywords = [q["skill"].lower(), "debugging", "trade-offs", "production"]
                    st.success(f"Loaded Question {i} into Mock Interview tab!")


# ==============================================================================
# TAB 3: DOMAIN & TOPIC STUDIO
# ==============================================================================
elif selected_tab == "🧠 Domain & Topic Studio":
    st.markdown('<div class="main-header">🧠 Domain & Custom Topic Question Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate interview questions across technical domains or input custom topics and text.</div>', unsafe_allow_html=True)

    input_mode = st.radio("Choose Input Mode", ["Curated Domains", "Custom Tech Stack / Skills", "Raw Text / Article"], horizontal=True)

    if input_mode == "Curated Domains":
        domain_choice = st.selectbox(
            "Select Engineering Domain",
            ["Python", "Machine Learning", "Natural Language Processing", "System Design", "DevOps & Cloud", "Web Development", "Databases", "Behavioral"]
        )
        target_skills = [domain_choice]
    elif input_mode == "Custom Tech Stack / Skills":
        skills_input = st.text_input("Enter comma-separated skills / concepts", "Docker, Kubernetes, AWS, Prometheus, CI/CD")
        target_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
    else:
        raw_text_input = st.text_area("Paste technical document or syllabus", height=180, value="We are building an event-driven microservices architecture using Apache Kafka, FastAPI, and PostgreSQL. Engineers must optimize query latencies, maintain distributed tracing with OpenTelemetry, and design idempotent consumer groups.")
        target_skills = []

    if st.button("✨ Synthesize Interview Questions", type="primary"):
        with st.spinner("Synthesizing questions using NLP Bloom's Taxonomy Engine..."):
            if input_mode == "Raw Text / Article":
                res = question_generator.generate_from_raw_text(
                    raw_text_input,
                    difficulty=global_difficulty,
                    taxonomy_level=global_taxonomy,
                    num_questions=num_questions_slider
                )
                st.session_state.generated_questions = res["questions"]
            else:
                if gemini_key:
                    ai_res = question_generator.generate_with_gemini(
                        gemini_key,
                        role_or_topic=", ".join(target_skills),
                        skills=target_skills,
                        num_questions=num_questions_slider
                    )
                    if ai_res:
                        st.session_state.generated_questions = ai_res
                    else:
                        st.session_state.generated_questions = question_generator.generate_from_skills(
                            skills=target_skills,
                            difficulty=global_difficulty,
                            taxonomy_level=global_taxonomy,
                            num_questions=num_questions_slider
                        )
                else:
                    st.session_state.generated_questions = question_generator.generate_from_skills(
                        skills=target_skills,
                        difficulty=global_difficulty,
                        taxonomy_level=global_taxonomy,
                        num_questions=num_questions_slider
                    )

    if st.session_state.generated_questions:
        st.markdown("---")
        st.subheader(f"📋 Generated Interview Questions ({len(st.session_state.generated_questions)})")

        for idx, q in enumerate(st.session_state.generated_questions, 1):
            diff = q.get("difficulty", "Mid")
            tax = q.get("taxonomy", "Understanding")
            skill = q.get("skill", "General")
            source = q.get("source", "NLP Engine")

            diff_class = f"badge-{diff.lower()}" if diff.lower() in ["junior", "mid", "senior"] else "badge-mid"

            with st.expander(f"**Q{idx}. {q['question']}**", expanded=(idx <= 2)):
                st.markdown(f"""
                <span class="{diff_class}">{diff}</span>
                <span class="badge-bloom">Bloom's: {tax}</span>
                <span class="skill-tag">{skill}</span>
                <span style="font-size: 0.8rem; color: #64748B;">Source: {source}</span>
                """, unsafe_allow_html=True)

                st.markdown("#### 📖 Model Answer Guidance:")
                st.write(q.get("model_answer", "N/A"))

                st.markdown("#### 🔑 Expected Key Concepts & Keywords:")
                kw_tags = " ".join([f'<span class="skill-tag">{k}</span>' for k in q.get("keywords", [])])
                st.markdown(kw_tags, unsafe_allow_html=True)

                rubric = q.get("rubric", {})
                if isinstance(rubric, dict) and rubric:
                    st.markdown("#### 📏 Assessment Rubric:")
                    for crit, desc in rubric.items():
                        st.markdown(f"- **{crit.replace('_', ' ').title()}:** {desc}")

                if st.button(f"🎯 Test This Question in Mock Interview", key=f"q_test_{idx}"):
                    st.session_state.mock_question = q["question"]
                    st.session_state.mock_model_answer = q.get("model_answer", "")
                    st.session_state.mock_keywords = q.get("keywords", [])
                    st.success("Loaded into Mock Interview tab! Navigate to 'Mock Interview & Grader' to evaluate.")


# ==============================================================================
# TAB 4: MOCK INTERVIEW & GRADER
# ==============================================================================
elif selected_tab == "✍️ Mock Interview & Grader":
    st.markdown('<div class="main-header">✍️ Live Candidate Mock Interview & NLP Grader</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test candidate responses using multi-factor NLP grading: semantic similarity, technical keyword coverage, tone/confidence, and readability.</div>', unsafe_allow_html=True)

    col_q, col_ans = st.columns([1, 1.1])

    with col_q:
        st.markdown("### ❓ Question Under Assessment")
        curr_q = st.text_area("Question", value=st.session_state.mock_question, height=100)
        curr_model_ans = st.text_area("Expected Model Answer / Key Concepts", value=st.session_state.mock_model_answer, height=180)
        curr_keywords_str = st.text_input("Expected Keywords (comma-separated)", value=", ".join(st.session_state.mock_keywords))
        expected_kw_list = [k.strip() for k in curr_keywords_str.split(",") if k.strip()]

    with col_ans:
        st.markdown("### 🗣️ Candidate Response")
        cand_response_sample = (
            "The Python Global Interpreter Lock (GIL) is a mutex lock that ensures only one thread executes Python bytecodes at any time. "
            "For CPU-bound tasks, multithreading does not scale well due to lock contention, so we implemented multiprocessing instead to take advantage of multiple CPU cores. "
            "However, for I/O-bound operations like network calls or database queries, the GIL is released, making asyncio or threading very effective."
        )
        use_sample = st.checkbox("Pre-fill with sample candidate answer", value=True)
        default_cand_text = cand_response_sample if use_sample else ""
        cand_input = st.text_area("Type or paste candidate's answer here", value=default_cand_text, height=270)

    if st.button("📊 Evaluate Candidate Answer with NLP", type="primary", use_container_width=True):
        if not cand_input.strip():
            st.warning("Please provide a candidate response to evaluate.")
        else:
            with st.spinner("Analyzing semantics, matching keywords, and computing sentiment metrics..."):
                eval_res = answer_evaluator.evaluate(
                    candidate_answer=cand_input,
                    model_answer=curr_model_ans,
                    expected_keywords=expected_kw_list
                )
                st.session_state.last_eval = eval_res

    if "last_eval" in st.session_state:
        eval_res = st.session_state.last_eval
        st.markdown("---")
        st.subheader("🎯 Evaluation Report & Scorecard")

        g1, g2, g3, g4, g5 = st.columns(5)
        with g1:
            st.metric("Overall Score", f"{eval_res['overall_score']} / 100")
        with g2:
            st.metric("Grade", eval_res["grade"])
        with g3:
            st.metric("Keyword Coverage", f"{eval_res['keyword_coverage_pct']}%")
        with g4:
            st.metric("Semantic Relevance", f"{eval_res['semantic_similarity_pct']}%")
        with g5:
            st.metric("Confidence / Tone", f"{eval_res['confidence_score']}%")

        st.markdown("---")
        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("#### 🔑 Technical Keyword Analysis")
            st.write(f"**Keywords Detected ({len(eval_res['found_keywords'])}):**")
            if eval_res["found_keywords"]:
                tags_found = " ".join([f'<span class="skill-tag">✓ {k}</span>' for k in eval_res["found_keywords"]])
                st.markdown(tags_found, unsafe_allow_html=True)
            else:
                st.write("None")

            st.write(f"**Missing Keywords ({len(eval_res['missing_keywords'])}):**")
            if eval_res["missing_keywords"]:
                tags_miss = " ".join([f'<span class="skill-missing">✗ {k}</span>' for k in eval_res["missing_keywords"]])
                st.markdown(tags_miss, unsafe_allow_html=True)
            else:
                st.success("All expected core keywords covered!")

        with c_right:
            st.markdown("#### 📈 Communication & Tone Metrics")
            st.write(f"- **Word Count:** {eval_res.get('word_count', 0)} words")
            st.write(f"- **Flesch Reading Ease:** {eval_res.get('readability_ease', 0)} / 100")

            st.markdown("#### 💡 Actionable Feedback & Coaching Tips")
            for tip in eval_res.get("feedback", []):
                st.info(f"💡 {tip}")


# ==============================================================================
# TAB 5: NLP PIPELINE VISUALIZER
# ==============================================================================
elif selected_tab == "🔬 NLP Pipeline Visualizer":
    st.markdown('<div class="main-header">🔬 NLP Pipeline & Algorithmic Visualizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive educational walkthrough showing how raw text is parsed, chunked, ranked, and converted into entities.</div>', unsafe_allow_html=True)

    default_vis_text = "Senior Machine Learning Engineer required to build scalable NLP pipelines with Transformers, BERT, and PyTorch. Candidate must have strong understanding of TF-IDF, vector embeddings, and Docker deployments on AWS."
    vis_input = st.text_area("Input Sample Text", value=default_vis_text, height=120)

    if st.button("🔍 Run NLP Pipeline Decomposition", type="primary"):
        with st.spinner("Processing tokenization, POS tagging, and graph centrality..."):
            st.session_state.vis_text = vis_input

    if "vis_text" in st.session_state:
        text = st.session_state.vis_text
        st.markdown("---")

        p1, p2 = st.tabs(["1️⃣ Tokens & POS Tagging", "2️⃣ TF-IDF & TextRank Centrality"])

        with p1:
            col_tok, col_pos = st.columns(2)
            with col_tok:
                st.markdown("#### 🔤 Clean Word Tokens")
                tokens = nlp_engine.word_tokenize_clean(text)
                st.write(tokens[:30])
                st.caption(f"Total tokens extracted: {len(tokens)}")

                st.markdown("#### 🧩 Noun Phrase Chunks (<JJ.*>*<NN.*>+)")
                nps = nlp_engine.extract_noun_phrases(text)
                if nps:
                    tags = " ".join([f'<span class="skill-tag">{np}</span>' for np in nps])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.write("No distinct noun phrases found.")

            with col_pos:
                st.markdown("#### 🏷️ Part-of-Speech (POS) Tags")
                pos_tags = nlp_engine.extract_pos_tags(text)[:18]
                df_pos = pd.DataFrame(pos_tags, columns=["Token", "POS Tag"])
                st.dataframe(df_pos, height=280, use_container_width=True)

        with p2:
            col_tfidf, col_tr = st.columns(2)
            with col_tfidf:
                st.markdown("#### 📊 TF-IDF Keyword Weights")
                tfidf_kws = nlp_engine.extract_tfidf_keywords(text, top_n=8)
                if tfidf_kws:
                    df_tfidf = pd.DataFrame(tfidf_kws, columns=["Keyword", "TF-IDF Score"])
                    chart = alt.Chart(df_tfidf).mark_bar(cornerRadius=4, color="#10B981").encode(
                        x=alt.X("TF-IDF Score:Q"),
                        y=alt.Y("Keyword:N", sort="-x"),
                        tooltip=["Keyword", "TF-IDF Score"]
                    ).properties(height=260)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.write("Provide more text for TF-IDF calculations.")

            with col_tr:
                st.markdown("#### 🕸️ TextRank Graph Centrality (PageRank)")
                tr_kws = nlp_engine.extract_textrank_keywords(text, top_n=8)
                if tr_kws:
                    df_tr = pd.DataFrame(tr_kws, columns=["Node / Keyword", "PageRank Score"])
                    chart_tr = alt.Chart(df_tr).mark_bar(cornerRadius=4, color="#6366F1").encode(
                        x=alt.X("PageRank Score:Q"),
                        y=alt.Y("Node / Keyword:N", sort="-x"),
                        tooltip=["Node / Keyword", "PageRank Score"]
                    ).properties(height=260)
                    st.altair_chart(chart_tr, use_container_width=True)


# ==============================================================================
# TAB 6: EXPORT & INTERVIEW KITS
# ==============================================================================
elif selected_tab == "📑 Export & Interview Kits":
    st.markdown('<div class="main-header">📑 Export & Printable Interview Kits</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Export your customized questions, model answers, and evaluation rubrics into JSON, CSV, or formatted Markdown.</div>', unsafe_allow_html=True)

    questions_to_export = st.session_state.generated_questions or CURATED_QUESTIONS[:6]

    st.write(f"**Questions Ready for Export:** `{len(questions_to_export)}`")

    exp_col1, exp_col2, exp_col3 = st.columns(3)

    with exp_col1:
        st.markdown("#### 📄 JSON Format")
        json_str = export_to_json(questions_to_export)
        st.download_button(
            label="⬇️ Download JSON",
            data=json_str,
            file_name="interview_questions.json",
            mime="application/json",
            use_container_width=True
        )

    with exp_col2:
        st.markdown("#### 📊 CSV Spreadsheet")
        csv_str = export_to_csv(questions_to_export)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_str,
            file_name="interview_questions.csv",
            mime="text/csv",
            use_container_width=True
        )

    with exp_col3:
        st.markdown("#### 📋 Markdown Interview Kit")
        md_str = export_to_interview_kit_markdown(questions_to_export)
        st.download_button(
            label="⬇️ Download Markdown Kit",
            data=md_str,
            file_name="interview_kit.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("---")
    st.subheader("👁️ Preview Printable Interview Kit")
    st.markdown(export_to_interview_kit_markdown(questions_to_export))
