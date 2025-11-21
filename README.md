# The Language of Autonomy: Narratives and Strategic Implications of Agentic AI

**Course:** Advanced Data for International Studies  
**Status:** Active | **Python Version:** 3.10+

---

## 📘 Project Overview

**Agentic AI**—systems capable of autonomous decision-making, task orchestration, and multi-step execution—is emerging as the defining technological shift of 2024–2025. However, despite the hype, the concept suffers from inconsistent definitions. Consulting firms, academic institutions, and tech giants frame the "agent" differently, oscillating between the narrative of a *productivity booster* (ROI focus) and an *autonomous governance risk*.

This project aims to deconstruct these narratives. By applying **Natural Language Processing (NLP)** techniques to a corpus of high-level strategic reports, we analyze how global stakeholders define, frame, and position AI agents.

### 🎯 Research Objectives
1.  **Deconstruct Definitions:** How do consulting firms vs. tech giants define "Agentic AI"?
2.  **Identify Dominant Narratives:** What are the prevailing themes (e.g., "AI as Copilot" vs. "AI as Autonomous Worker")?
3.  **Strategic Implications:** How do these divergent framings impact enterprise adoption strategies and governance frameworks?

---

## 📚 The Corpus

The analysis is based on a curated dataset of strategic reports from major global institutions (Consulting, Tech, and Academia) published between 2024 and 2025.

| Institution | Report Title | Type |
| :--- | :--- | :--- |
| **McKinsey & Company** | *The Agentic Organization: Contours of the Next Paradigm* | Strategy / Org |
| **McKinsey (QuantumBlack)** | *Seizing the Agentic AI Advantage: A CEO Playbook* | Strategy / CEO |
| **McKinsey (QuantumBlack)** | *One Year of Agentic AI: Six Lessons from the Field* | Implementation |
| **McKinsey** | *Empowering Advanced Industries with Agentic AI* | Sectorial (Industry) |
| **McKinsey** | *AI for IT Modernization: Faster, Cheaper, Better* | Technical / IT |
| **Deloitte** | *The Business Imperative for Agentic AI* | Strategy (India Focus) |
| **PwC** | *Agentic AI: The New Frontier in GenAI (Executive Playbook)* | Strategy / GCC |
| **Bain & Company** | *Technology Report 2025 (Agentic AI Chapter)* | Tech Trends |
| **Google Cloud** | *Shaping the Future: Agentic AI TAM Analysis* | Market Sizing / Tech |
| **MIT Tech Review / EY** | *Reimagining the Future of Banking with Agentic AI* | Sectorial (Finance) |
| ... | ... | ... |

---

## 🛠️ Methodology & Tech Stack

This project utilizes a standard Data Science pipeline, moving from unstructured PDF text to structured insights.

### 1. Data Engineering
* **Ingestion:** Text extraction from complex PDF layouts using `pypdf` and `pdfplumber`.
* **Preprocessing:** Tokenization, Stop-word removal (customized for corporate jargon), Lemmatization using `spaCy` / `NLTK`.

### 2. NLP Analysis
* **Lexical Analysis:** N-gram frequency distributions to identify collocations (e.g., "autonomous orchestration", "human-in-the-loop").
* **TF-IDF:** Identifying unique conceptual markers per institution (e.g., What terms are specific to Google vs. McKinsey?).
* **Topic Modeling:** Using **LDA (Latent Dirichlet Allocation)** or **BERTopic** to extract latent themes across the corpus.

### 3. Visualization
* Generating Word Clouds, t-SNE clusters, and frequency heatmaps to visualize the semantic distance between reports.

---

## 📂 Project Structure

The directory structure follows the **Cookiecutter Data Science** standard:

```text
language-of-autonomy/
├── data/
│   ├── raw/            # Original PDFs (ignored by git)
│   ├── processed/      # Cleaned text data (CSV/Parquet)
│   └── external/       # Lexicons and helper lists
├── notebooks/          # Jupyter notebooks for exploration
├── src/                # Source code for use in this project
├── reports/            # Generated analysis as HTML, PDF, LaTeX
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

-----

## 🚀 Getting Started

### Prerequisites

  * Python 3.10 or higher
  * Virtual Environment recommended

### Installation

(To be added soon.)

-----

## 👤 Authors

| **Name** | **Organization** | **E-mail** |
|:--------:|:----------------:|:----------:|
| Héloïse Robin | Hanyang University (Dept. of Computer Science) | [heloiserobin@hanyang.ac.kr](mailto:heloiserobin@hanyang.ac.kr) |
| Antoine Vansieleghem | Hanyang University (Dept. of Computer Science) | [antoinevansieleghem@hanyang.ac.kr](mailto:antoinevansieleghem@hanyang.ac.kr) |

-----

## 📄 License

This project is for academic purposes. The source reports remain the intellectual property of their respective authors (McKinsey, Bain, Deloitte, PwC, Google, MIT, etc.).
