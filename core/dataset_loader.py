"""
dataset_loader.py
Provides predefined tech skill taxonomies, sample Job Descriptions, sample Resumes,
and a rich curated technical and behavioral question bank for offline/instant evaluation.
"""

from typing import Dict, List, Any

# Technical skills taxonomy organized by category
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "sql"
    ],
    "Web & App Frameworks": [
        "react", "angular", "vue", "next.js", "node.js", "express", "django",
        "fastapi", "flask", "spring boot", "asp.net", "laravel", "ruby on rails",
        "tailwind css", "bootstrap", "graphql", "rest api"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker",
        "kubernetes", "k8s", "terraform", "ansible", "jenkins", "ci/cd", "git",
        "github actions", "linux", "bash", "prometheus", "grafana", "helm"
    ],
    "Databases & Messaging": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "sqlite", "kafka", "rabbitmq", "rabbitmq",
        "oracle", "neo4j", "snowflake", "bigquery"
    ],
    "AI, ML & NLP": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "llm", "large language models", "transformers", "bert",
        "pytorch", "tensorflow", "keras", "scikit-learn", "pandas", "numpy",
        "spacy", "nltk", "langchain", "embeddings", "vector database"
    ],
    "Architecture & Methodologies": [
        "system design", "microservices", "monolith", "event-driven architecture",
        "concurrency", "multithreading", "oop", "object oriented programming",
        "solid principles", "design patterns", "clean code", "agile", "scrum",
        "tdd", "test driven development", "ci/cd", "scalability", "caching"
    ],
    "Behavioral & Soft Skills": [
        "leadership", "teamwork", "conflict resolution", "communication",
        "problem solving", "time management", "stakeholder management", "mentorship",
        "adaptability", "critical thinking"
    ]
}

# Pre-curated question repository categorized by domain, difficulty, and Bloom's Taxonomy
CURATED_QUESTIONS: List[Dict[str, Any]] = [
    # Python & Backend
    {
        "id": "py-001",
        "domain": "Python",
        "topic": "Memory & Execution",
        "difficulty": "Mid",
        "taxonomy": "Understanding",
        "question": "Explain how the Python Global Interpreter Lock (GIL) impacts multi-threaded CPU-bound versus I/O-bound applications.",
        "model_answer": "The Python GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously. For CPU-bound tasks, multithreading does not provide true parallelism and can even degrade performance due to lock contention; multiprocessing or native extensions should be used instead. However, for I/O-bound tasks (network, disk), threads release the GIL while waiting for I/O operations, making threading effective.",
        "keywords": ["gil", "global interpreter lock", "multiprocessing", "cpu-bound", "i/o-bound", "concurrency", "thread"],
        "rubric": {
            "understanding": "Explains what GIL is and why it exists.",
            "application": "Distinguishes behavior between CPU-bound and I/O-bound workloads.",
            "solution": "Mentions multiprocessing, asyncio, or C extensions as alternatives."
        }
    },
    {
        "id": "py-002",
        "domain": "Python",
        "topic": "Generators & Memory",
        "difficulty": "Junior",
        "taxonomy": "Applying",
        "question": "What is the difference between a generator and a regular function returning a list in Python, and when would you use yield?",
        "model_answer": "A regular function computes all items upfront and stores the entire list in memory before returning. A generator yields items one at a time on demand using the 'yield' keyword, maintaining state between iterations. Generators provide lazy evaluation and drastic memory savings when dealing with massive datasets or infinite sequences.",
        "keywords": ["generator", "yield", "lazy evaluation", "memory efficiency", "iterator", "stream"],
        "rubric": {
            "understanding": "Clarifies yield vs return.",
            "benefit": "Identifies memory efficiency and lazy evaluation.",
            "use_case": "Provides examples such as processing large log files."
        }
    },
    {
        "id": "py-003",
        "domain": "Python",
        "topic": "Decorators & Metaprogramming",
        "difficulty": "Senior",
        "taxonomy": "Creating",
        "question": "How would you design and implement a custom parameterized decorator in Python that caches function results with a time-to-live (TTL)?",
        "model_answer": "A parameterized decorator requires three nested functions: an outer factory taking arguments (e.g. ttl_seconds), a middle wrapper taking the target function, and an inner wrapper accepting *args and **kwargs. It uses a dictionary storing (timestamp, result) tuples, checks if current_time - cached_time < ttl before returning the cached value, and wraps using functools.wraps to preserve docstrings and metadata.",
        "keywords": ["decorator", "functools.wraps", "closure", "ttl", "cache", "args", "kwargs"],
        "rubric": {
            "syntax": "Describes triple-nested function pattern for arguments.",
            "caching_logic": "Explains timestamp checking and cache invalidation.",
            "clean_code": "Mentions functools.wraps to preserve function metadata."
        }
    },

    # Machine Learning & NLP
    {
        "id": "ml-001",
        "domain": "Machine Learning",
        "topic": "Model Evaluation",
        "difficulty": "Junior",
        "taxonomy": "Evaluating",
        "question": "In a dataset with high class imbalance (e.g., fraud detection with 99.5% legitimate transactions), why is accuracy a misleading metric, and what metrics should be used instead?",
        "model_answer": "Accuracy is misleading because a naive classifier predicting all transactions as legitimate would achieve 99.5% accuracy while completely failing to detect fraud. Instead, one should evaluate Precision, Recall, F1-Score, PR-AUC (Precision-Recall Area Under Curve), and ROC-AUC. In fraud detection, Recall (Sensitivity) is usually critical to minimize False Negatives.",
        "keywords": ["class imbalance", "accuracy paradox", "precision", "recall", "f1-score", "pr-auc", "confusion matrix"],
        "rubric": {
            "accuracy_flaw": "Articulates why majority class skews accuracy.",
            "alternatives": "Lists Precision, Recall, F1-Score, and PR-AUC.",
            "domain_context": "Relates metric priority to cost of false negatives in fraud."
        }
    },
    {
        "id": "nlp-001",
        "domain": "Natural Language Processing",
        "topic": "Embeddings & Attention",
        "difficulty": "Senior",
        "taxonomy": "Analyzing",
        "question": "Compare traditional Word2Vec / TF-IDF representations with modern Transformer Self-Attention mechanisms in handling polysemy (words with multiple meanings).",
        "model_answer": "TF-IDF assigns static lexical weights ignoring syntax and polysemy. Word2Vec produces static vector representations where each word (e.g., 'bank') has a single embedding regardless of whether it refers to a river bank or a financial institution. In contrast, Transformer Self-Attention dynamically weights all surrounding tokens in a sentence, generating distinct contextualized representations for every occurrence based on context.",
        "keywords": ["word2vec", "tf-idf", "transformer", "self-attention", "contextualized embeddings", "polysemy", "bert"],
        "rubric": {
            "static_vs_dynamic": "Contrasts static vector space with context-dependent representations.",
            "attention_mechanism": "Explains how self-attention keys, queries, and values resolve ambiguity.",
            "depth": "Mentions BERT or GPT token representations."
        }
    },
    {
        "id": "nlp-002",
        "domain": "Natural Language Processing",
        "topic": "Text Preprocessing & Feature Extraction",
        "difficulty": "Mid",
        "taxonomy": "Applying",
        "question": "Describe the NLP pipeline steps needed to extract domain-specific technical keywords from unstructured engineering job descriptions.",
        "model_answer": "The pipeline involves: 1) Text normalization (cleaning HTML, lowercasing, unicode normalization); 2) Sentence segmentation and word tokenization; 3) Part-of-Speech (POS) tagging to filter noun phrases and adjective-noun compounds; 4) Stopword removal with custom technical exclusion lists; 5) Lemmatization; 6) N-gram generation and TF-IDF or TextRank graph ranking; 7) Entity linking against a tech taxonomy.",
        "keywords": ["tokenization", "pos tagging", "lemmatization", "tf-idf", "textrank", "noun phrase", "stopword removal"],
        "rubric": {
            "pipeline_stages": "Names preprocessing, tokenization, POS tagging, and ranking.",
            "keyword_logic": "Explains n-grams, noun chunks, or graph-based ranking.",
            "domain_fit": "Considers technical terminology specificity."
        }
    },

    # System Design & Cloud
    {
        "id": "sd-001",
        "domain": "System Design",
        "topic": "Scalability & Caching",
        "difficulty": "Senior",
        "taxonomy": "Creating",
        "question": "Design a high-throughput URL shortening service (like Bitly) handling 100M new URLs daily. How do you handle ID generation, storage, and caching?",
        "model_answer": "Use Base62 encoding on unique 64-bit integer IDs (generated via distributed ID generators like Twitter Snowflake or database sequence offsets). For storage, use a distributed NoSQL or Key-Value store (like Cassandra, DynamoDB, or Redis cluster) sharded on the short hash key. Implement a multi-tier LRU cache (Redis) for hot URLs obeying the 80/20 rule, with HTTP 302 redirects for analytics or 301 for browser caching.",
        "keywords": ["base62", "snowflake", "distributed id", "redis", "caching", "sharding", "lru", "nosql", "301 vs 302"],
        "rubric": {
            "id_generation": "Explains Base62 conversion and collision avoidance.",
            "storage_strategy": "Proposes sharded database or key-value store.",
            "caching": "Specifies Redis LRU cache and redirect status codes."
        }
    },
    {
        "id": "devops-001",
        "domain": "DevOps & Cloud",
        "topic": "Containers & Orchestration",
        "difficulty": "Mid",
        "taxonomy": "Analyzing",
        "question": "What is the difference between a Kubernetes Pod, Deployment, and Service? How does traffic reach a container inside a private cluster node?",
        "model_answer": "A Pod is the smallest deployable unit containing one or more tightly-coupled containers sharing network namespace and storage. A Deployment manages declarative updates, rolling releases, self-healing, and scaling of replica sets of Pods. A Service provides a stable internal/external IP and load-balanced DNS endpoint across dynamic pod IPs. Traffic arrives via an Ingress Controller or LoadBalancer Service, routing via kube-proxy and iptables to the target Pod endpoint.",
        "keywords": ["kubernetes", "pod", "deployment", "service", "ingress", "kube-proxy", "replica set"],
        "rubric": {
            "distinction": "Defines Pod, Deployment, and Service roles accurately.",
            "networking": "Explains service abstraction and virtual IP.",
            "traffic_flow": "Traces ingress/load balancer through kube-proxy to pod."
        }
    },

    # Web & Full Stack
    {
        "id": "web-001",
        "domain": "Web Development",
        "topic": "React State & Performance",
        "difficulty": "Mid",
        "taxonomy": "Understanding",
        "question": "How does React's Virtual DOM reconciliation algorithm work, and why are unique 'key' props essential when rendering dynamic lists?",
        "model_answer": "React maintains a lightweight in-memory representation of the DOM. When state changes, a new Virtual DOM tree is created and diffed against the previous one using a heuristic O(n) algorithm. Keys give elements a persistent identity across renders, allowing React to match children across trees efficiently to insert, move, or delete only what changed instead of recreating the whole list.",
        "keywords": ["virtual dom", "reconciliation", "diffing", "key prop", "render performance", "fiber"],
        "rubric": {
            "virtual_dom": "Explains diffing of in-memory virtual tree vs real DOM.",
            "keys_purpose": "Identifies stable element identity to avoid unnecessary re-renders.",
            "performance": "Explains performance consequences of array index keys."
        }
    },
    {
        "id": "db-001",
        "domain": "Databases",
        "topic": "Indexing & Query Optimization",
        "difficulty": "Senior",
        "taxonomy": "Evaluating",
        "question": "How does a B-Tree database index improve read query performance, and what are the trade-offs regarding write performance and index selectivity?",
        "model_answer": "A B-Tree index maintains sorted key-pointer nodes in balanced tree levels, reducing search complexity from O(N) full table scans to O(log N) page lookups. However, every INSERT, UPDATE, and DELETE requires updating index trees, rebalancing nodes, and page splits, creating write amplification. High selectivity (columns with many unique values) makes indexes beneficial, whereas low selectivity can cause query planners to bypass the index.",
        "keywords": ["b-tree", "index", "o(log n)", "selectivity", "write amplification", "page split", "query planner"],
        "rubric": {
            "data_structure": "Explains balanced tree traversal and page lookups.",
            "tradeoffs": "Highlights write latency, disk overhead, and maintenance.",
            "selectivity": "Explains how column cardinality impacts index usage."
        }
    },

    # Behavioral & Leadership
    {
        "id": "beh-001",
        "domain": "Behavioral",
        "topic": "Conflict & Stakeholder Management",
        "difficulty": "Senior",
        "taxonomy": "Evaluating",
        "question": "Describe a situation where you had a strong technical disagreement with a team member or architect regarding technology choices. How did you resolve it?",
        "model_answer": "Structured using the STAR framework (Situation, Task, Action, Result): Focus on de-escalating interpersonal tension, framing the discussion around business objectives, creating objective POCs (Proof-of-Concepts) or benchmark matrices with defined criteria (latency, developer ergonomics, maintainability), seeking third-party peer input, and committing fully to the chosen decision (disagree and commit).",
        "keywords": ["star method", "poc", "benchmarks", "disagree and commit", "collaboration", "trade-offs"],
        "rubric": {
            "star_structure": "Uses clear Situation, Task, Action, Result framing.",
            "objective_criteria": "Relies on data, benchmarks, and POCs rather than opinion.",
            "team_alignment": "Demonstrates mature consensus building and accountability."
        }
    }
]

# Sample Job Descriptions for instant testing
SAMPLE_JOB_DESCRIPTIONS: Dict[str, str] = {
    "Senior Python & Backend Engineer": """
Role: Senior Python / Backend Engineer
Company: CloudScale Analytics

Responsibilities:
- Architect and develop high-throughput microservices using Python 3, FastAPI, and Django.
- Design resilient distributed systems using Apache Kafka, Redis caching, and PostgreSQL databases.
- Containerize services with Docker and manage deployments across AWS ECS and Kubernetes (EKS).
- Optimize SQL queries, database indexing, and implement asynchronous event-driven pipelines.
- Write unit, integration, and performance tests using Pytest and Locust.
- Collaborate with cross-functional engineering teams in an Agile / Scrum framework.

Requirements:
- 5+ years of software development experience with Python.
- Strong knowledge of concurrency, asyncio, multithreading, and RESTful API architecture.
- Hands-on experience with PostgreSQL, Redis, and event streaming via Kafka or RabbitMQ.
- Solid understanding of Docker, Kubernetes, and AWS cloud infrastructure (S3, RDS, CloudWatch).
- Passion for clean code, SOLID principles, and CI/CD automation with GitHub Actions.
""",

    "Machine Learning & NLP Engineer": """
Role: Machine Learning / NLP Engineer
Company: Cortex Intelligence Labs

Responsibilities:
- Build and deploy state-of-the-art NLP pipelines for information extraction, entity linking, and summarization.
- Fine-tune Transformer models (BERT, RoBERTa, T5) and explore Large Language Model (LLM) orchestration using LangChain and HuggingFace.
- Implement vector search and retrieval-augmented generation (RAG) using FAISS and vector databases.
- Develop production inference APIs using FastAPI and TorchScript / ONNX Runtime.
- Perform feature engineering, sentiment analysis, TF-IDF, and topic modeling using Scikit-Learn and NLTK.
- Monitor model drift and inference latency in production on AWS / GCP.

Requirements:
- Strong programming background in Python, PyTorch, and Scikit-Learn.
- Deep theoretical and practical knowledge of NLP, tokenization, embeddings, and self-attention.
- Experience with text preprocessing, regular expressions, and syntactic parsing.
- Familiarity with MLOps, Docker, and cloud-based model serving.
""",

    "Full-Stack React & Node Developer": """
Role: Full-Stack React & Node.js Developer
Company: FinTech Velocity

Responsibilities:
- Design and build responsive, accessible web dashboards using React, TypeScript, and Tailwind CSS.
- Develop scalable backend REST and GraphQL APIs using Node.js, Express, and NestJS.
- Integrate relational and document databases including PostgreSQL and MongoDB.
- Manage client-side state with Redux Toolkit or React Query.
- Implement JWT authentication, OAuth2, and role-based access control (RBAC).
- Build automated testing suites with Jest, React Testing Library, and Cypress.

Requirements:
- 3+ years experience with modern JavaScript / TypeScript.
- Strong proficiency in React hooks, component lifecycle, and virtual DOM performance.
- Solid server-side experience with Node.js and async programming.
- Understanding of web security best practices (CORS, CSRF, XSS prevention).
"""
}

# Sample Resumes for instant testing
SAMPLE_RESUMES: Dict[str, str] = {
    "Candidate A (Experienced Python Backend Dev)": """
Alex Chen
Senior Software Engineer - Backend Systems
Email: alex.chen@example.com | Location: Seattle, WA

SUMMARY:
Results-driven software engineer with 6 years of experience building scalable backend services,
data pipelines, and REST APIs using Python, Django, and PostgreSQL. Proficient in database
optimization, Redis caching, and microservices architecture.

EXPERIENCE:
Software Engineer | DataFlow Systems (2021 - Present)
- Developed and maintained 12+ Python FastAPI and Django microservices serving 1.5M daily active users.
- Designed database schemas and optimized complex SQL queries in PostgreSQL, cutting query response time by 42%.
- Integrated Redis for distributed session caching and rate-limiting.
- Built asynchronous job queues using Celery and Redis.
- Wrote automated test suites using Pytest with 90%+ branch code coverage.

Junior Developer | WebSolutions Inc (2018 - 2021)
- Built internal tooling and administrative portals using Python, Flask, and SQLite.
- Created RESTful APIs for mobile application synchronization.
- Automated deployment scripts using Bash and Git.

SKILLS:
- Languages: Python, SQL, Bash
- Frameworks: FastAPI, Django, Flask, Pytest
- Databases & Caching: PostgreSQL, MySQL, Redis, SQLite
- Concepts: REST APIs, Concurrency, Asyncio, OOP, SOLID Principles
- Version Control: Git, GitHub
""",

    "Candidate B (NLP & Data Science Specialist)": """
Dr. Priya Nair
Machine Learning & NLP Specialist
Email: priya.nair@example.com | San Francisco, CA

SUMMARY:
Data Scientist with 4 years of expertise in Natural Language Processing, text mining,
and predictive modeling. Specialized in transformer models, sentiment analysis, and topic modeling.

EXPERIENCE:
Machine Learning Engineer | LinguaMetrics (2022 - Present)
- Fine-tuned BERT and RoBERTa models for customer support ticket classification with 94% F1-score.
- Built end-to-end NLP preprocessing pipelines using NLTK, Spacy, and Scikit-learn for keyword extraction.
- Developed semantic similarity search using sentence embeddings and FAISS vector indices.
- Deployed real-time inference models using FastAPI and Docker containers on AWS.

Data Scientist | Alpha Analytics (2020 - 2022)
- Analyzed unstructured text reviews using TF-IDF, Word2Vec, and LDA topic modeling.
- Trained classification models using PyTorch, LightGBM, and Pandas.
- Implemented automated report generation dashboards with Streamlit and Matplotlib.

SKILLS:
- Machine Learning: PyTorch, Scikit-learn, Transformers, HuggingFace, XGBoost
- NLP: NLTK, Spacy, TF-IDF, BERT, Word2Vec, Embeddings, Tokenization
- Programming: Python, SQL, R
- Tools: Docker, Git, Streamlit, Pandas, NumPy
"""
}


def get_skill_categories() -> List[str]:
    """Returns the list of skill category names."""
    return list(SKILL_TAXONOMY.keys())


def get_all_skills() -> List[str]:
    """Returns a flat sorted list of all unique skills in the taxonomy."""
    all_skills = set()
    for skills in SKILL_TAXONOMY.values():
        all_skills.update(skills)
    return sorted(list(all_skills))


def get_questions_by_domain(domain: str) -> List[Dict[str, Any]]:
    """Filters curated questions by domain."""
    return [q for q in CURATED_QUESTIONS if domain.lower() in q["domain"].lower()]
