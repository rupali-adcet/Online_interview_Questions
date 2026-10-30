"""
nlp_engine.py
Core Natural Language Processing engine implementing tokenization, POS tagging,
noun-phrase chunking, TF-IDF ranking, TextRank graph centrality, and skill extraction.
"""

import re
import math
from typing import List, Dict, Tuple, Set, Any
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, RegexpParser

from core.dataset_loader import SKILL_TAXONOMY, get_all_skills

# Ensure necessary NLTK data packages are available
def _bootstrap_nltk():
    packages = [
        ('corpora/stopwords', 'stopwords'),
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
        ('corpora/wordnet', 'wordnet'),
        ('sentiment/vader_lexicon', 'vader_lexicon'),
    ]
    for path, pkg in packages:
        try:
            nltk.data.find(path)
        except (LookupError, AttributeError):
            try:
                nltk.download(pkg, quiet=True)
            except Exception:
                pass

_bootstrap_nltk()

try:
    _STOP_WORDS = set(stopwords.words('english'))
except Exception:
    nltk.download('stopwords', quiet=True)
    _STOP_WORDS = set(stopwords.words('english'))

# Custom stop words that might be generic filler in job descriptions
EXTRA_STOPWORDS = {
    "experience", "years", "working", "work", "responsibilities", "requirements",
    "required", "preferred", "knowledge", "ability", "strong", "team", "hands-on",
    "understanding", "skills", "good", "etc", "using", "including", "familiarity",
    "responsible", "opportunity", "role", "company", "candidate", "position"
}
_STOP_WORDS.update(EXTRA_STOPWORDS)

try:
    _LEMMATIZER = WordNetLemmatizer()
except Exception:
    _LEMMATIZER = None


class NLPEngine:
    """
    Modular Natural Language Processing Engine for interview question generation.
    """

    def __init__(self):
        self.lemmatizer = _LEMMATIZER or WordNetLemmatizer()
        self.stop_words = _STOP_WORDS
        self.all_skills = get_all_skills()
        self.skill_taxonomy = SKILL_TAXONOMY

        # Noun Phrase Chunking Grammar
        self.chunk_grammar = r"""
            NP: {<DT|PP\$>?<JJ.*>*<NN.*>+}
                {<NNP>+}
        """
        self.chunk_parser = RegexpParser(self.chunk_grammar)

    def clean_text(self, text: str) -> str:
        """Removes excessive whitespace, URLs, and normalizes characters."""
        if not text:
            return ""
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        # Clean extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def sentence_tokenize(self, text: str) -> List[str]:
        """Splits text into sentences."""
        clean = self.clean_text(text)
        if not clean:
            return []
        try:
            return sent_tokenize(clean)
        except Exception:
            # Fallback regex split
            return [s.strip() for s in re.split(r'[.!?]+', clean) if s.strip()]

    def word_tokenize_clean(self, text: str) -> List[str]:
        """Extracts cleaned word tokens (alphanumeric and tech identifiers)."""
        clean = self.clean_text(text).lower()
        # Preserve terms like c++, c#, node.js, .net, scikit-learn
        tokens = re.findall(r'[a-zA-Z0-9+#.\-_]{2,}', clean)
        return [t.strip('.-_') for t in tokens if len(t.strip('.-_')) > 1]

    def extract_pos_tags(self, text: str) -> List[Tuple[str, str]]:
        """Computes Part-of-Speech (POS) tags for the given text."""
        try:
            words = word_tokenize(text)
            return pos_tag(words)
        except Exception:
            # Simple fallback
            tokens = self.word_tokenize_clean(text)
            return [(t, "NN") for t in tokens]

    def extract_noun_phrases(self, text: str) -> List[str]:
        """
        Extracts candidate noun phrases and technical multi-word compounds using
        shallow syntactic chunking.
        """
        sentences = self.sentence_tokenize(text)
        noun_phrases = []

        for sent in sentences:
            try:
                tagged = pos_tag(word_tokenize(sent))
                tree = self.chunk_parser.parse(tagged)
                for subtree in tree.subtrees():
                    if subtree.label() == "NP":
                        phrase_words = [word.lower() for word, tag in subtree.leaves()]
                        # Filter out stopwords at boundaries
                        phrase = " ".join([w for w in phrase_words if len(w) > 1])
                        if phrase and phrase not in self.stop_words and len(phrase) > 2:
                            noun_phrases.append(phrase)
            except Exception:
                continue

        return list(dict.fromkeys(noun_phrases))

    def extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        """
        Extracts recognized technical skills grouped by category from the text.
        """
        clean = " " + text.lower() + " "
        extracted: Dict[str, List[str]] = {}

        for category, skills in self.skill_taxonomy.items():
            found_category_skills = []
            for skill in skills:
                # Use regex with boundary checking to avoid false positives (e.g. 'c' or 'r')
                pattern = r'(?:\b|(?<=\W))' + re.escape(skill) + r'(?:\b|(?=\W))'
                if re.search(pattern, clean):
                    found_category_skills.append(skill)
            if found_category_skills:
                extracted[category] = sorted(list(set(found_category_skills)))

        return extracted

    def get_all_matched_skills(self, text: str) -> List[str]:
        """Returns a flat list of all matched skills."""
        cat_dict = self.extract_skills_from_text(text)
        all_found = []
        for skills in cat_dict.values():
            all_found.extend(skills)
        return sorted(list(set(all_found)))

    def extract_tfidf_keywords(self, text: str, top_n: int = 15) -> List[Tuple[str, float]]:
        """
        Extracts top keywords and keyphrases using TF-IDF over sentence n-grams.
        """
        sentences = self.sentence_tokenize(text)
        if not sentences or len(sentences) < 1:
            return []

        if len(sentences) == 1:
            # Split into chunks if only 1 long sentence
            sentences = [s.strip() for s in text.split(',') if len(s.strip()) > 3]
            if len(sentences) < 2:
                words = [w for w in self.word_tokenize_clean(text) if w not in self.stop_words]
                return [(w, 1.0) for w in words[:top_n]]

        try:
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                stop_words='english',
                max_features=200,
                token_pattern=r'(?u)\b[a-zA-Z0-9#+.]{2,}\b'
            )
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            keyword_scores = list(zip(feature_names, scores))

            # Filter out single-character, stopwords, and bigrams with stopwords
            filtered = []
            for kw, score in keyword_scores:
                parts = kw.split()
                if any(p in self.stop_words or len(p) <= 2 for p in parts):
                    continue
                filtered.append((kw, float(score)))

            filtered.sort(key=lambda x: x[1], reverse=True)
            return filtered[:top_n]
        except Exception:
            return []

    def extract_textrank_keywords(self, text: str, top_n: int = 10, window_size: int = 4) -> List[Tuple[str, float]]:
        """
        Extracts top keywords using the graph-based TextRank algorithm.
        Co-occurring words within a sliding window form an undirected graph,
        and PageRank scores quantify their prestige/centrality.
        """
        words = [w.lower() for w in self.word_tokenize_clean(text) if w.lower() not in self.stop_words and len(w) > 2]
        if len(words) < 3:
            return [(w, 1.0) for w in words[:top_n]]

        graph = nx.Graph()

        # Add nodes
        for w in set(words):
            graph.add_node(w)

        # Add edges for words in sliding window
        for i in range(len(words)):
            for j in range(i + 1, min(i + window_size, len(words))):
                w1, w2 = words[i], words[j]
                if w1 != w2:
                    if graph.has_edge(w1, w2):
                        graph[w1][w2]['weight'] += 1.0
                    else:
                        graph.add_edge(w1, w2, weight=1.0)

        if graph.number_of_edges() == 0:
            return [(w, 1.0) for w in list(set(words))[:top_n]]

        try:
            ranks = nx.pagerank(graph, weight='weight', max_iter=100)
            sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
            return sorted_ranks[:top_n]
        except Exception:
            return [(w, 1.0) for w in list(set(words))[:top_n]]

    def compute_readability_metrics(self, text: str) -> Dict[str, Any]:
        """
        Computes text statistics, lexical diversity, and reading ease metrics.
        """
        sentences = self.sentence_tokenize(text)
        words = self.word_tokenize_clean(text)
        num_sentences = max(len(sentences), 1)
        num_words = max(len(words), 1)
        unique_words = len(set(words))

        # Lexical Diversity (Type-Token Ratio)
        lexical_diversity = round((unique_words / num_words) * 100, 2)
        avg_sentence_len = round(num_words / num_sentences, 1)

        # Estimate syllables for Flesch Reading Ease
        def count_syllables(w):
            w = w.lower()
            count = len(re.findall(r'[aeiouy]+', w))
            return max(count, 1)

        total_syllables = sum(count_syllables(w) for w in words)
        avg_syllables_per_word = total_syllables / num_words

        # Flesch Reading Ease Formula: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        flesch_score = 206.835 - (1.015 * avg_sentence_len) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, round(flesch_score, 1)))

        return {
            "sentence_count": num_sentences,
            "word_count": num_words,
            "unique_words": unique_words,
            "avg_sentence_length": avg_sentence_len,
            "lexical_diversity_pct": lexical_diversity,
            "flesch_reading_ease": flesch_score
        }


# Singleton instance for convenient reuse
nlp_engine = NLPEngine()
