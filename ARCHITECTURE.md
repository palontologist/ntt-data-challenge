# NTT Data AI Engineering Challenge: Agentic RAG for Data Astel

## 🎯 The Challenge
Build a general-purpose, autonomous RAG pipeline for "Data Astel" that extracts information from a messy shared drive containing text, tables, images, and graphs, handling in-house terminology and complex multi-document aggregation.

## 🏗️ Agentic RAG Architecture: The "Cognitive Drive"

### Tier 1: The Looped Instinct Router (~100k params)
- **Purpose**: Fast intent classification and routing.
- **Function**: Analyzes the query to determine the required "Cognitive Path":
    - `GLOSSARY_EXPANSION`: Query contains in-house terms $\to$ Route to Glossary.
    - `ATOMIC_RETRIEVAL`: Single fact search $\to$ Route to OKF-RAG.
    - `SYNTHETIC_AGGREGATION`: Multi-material collation $\to$ Route to Agentic Loop.
    - `MULTIMODAL_ANALYSIS`: Graph/Image query $\to$ Route to Vision-Tool.
- **Innovation**: Looped architecture ensures this routing happens in $<100$ms on edge hardware.

### Tier 2: The OKF Knowledge Core (Open Knowledge Format)
- **Normalization & Linearization**: Converts all drive materials (PDF, Excel, PPT, Images) into **OKF documents**. 
- **olmOCR Integration**: Instead of basic OCR, we use a **VLM-based Linearization pipeline (inspired by olmOCR)**. This ensures that complex layouts, multi-column PDFs, and graphs are converted into clean, readable Markdown while preserving the natural reading order and structural integrity.
- **Structural Mapping**: 
    - **Text**: Chunked and tagged.
    - **Tables**: Linearized into Markdown tables with column metadata.
    - **Images/Graphs**: Processed via Vision-LLMs into descriptive text summaries stored as OKF.
- **Glossary Layer**: A specialized OKF namespace that maps internal abbreviations $\to$ normal expressions.

### Tier 3: The Agentic Orchestrator (Reasoning Loop)
Instead of one-shot RAG, the system uses an iterative loop:
1. **Plan**: Decompose the complex question into sub-queries.
2. **Execute**: Call OKF-RAG or Vision-Tools for each sub-query.
3. **Collate**: Aggregate evidence, resolve contradictions, and perform calculations (rounding/units).
4. **Verify**: Check the final answer against the "evidence basis" extracted from the drive.

## 🛠️ Technical Pipeline
```
User Query (Japanese) 
    ↓
Looped Router (Intent)
    ↓
Glossary Expansion (Internal Terms → Normal)
    ↓
Agentic Planner (Sub-queries) 
    ↓
OKF-RAG / Multimodal Extractor (Evidence Retrieval)
    ↓
Evidence Synthesizer (Aggregation & Formatting)
    ↓
Final Answer (Japanese, <1000 tokens)
```

## 🚀 Competition Winning Strategy
1. **Generalizability**: No hard-coding. The system treats the drive as a dynamic OKF store.
2. **Evidence-Based**: Every answer is backed by a specific OKF file reference.
3. **Multimodal Grounding**: Graphs and images are not ignored; they are "textualized" into OKF for the LLM to reason over.
4. **Strict Constraints**: A final formatting layer ensures units, decimal places, and rounding match the prompt's requirements.
