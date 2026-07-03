# NTT Data AI Engineering Challenge: Intelligent Drive Interface (IDI)

## 🎯 The Vision
Transform a "cumbersome internal drive" from a graveyard of files into a living knowledge organism. Instead of traditional keyword search or expensive full-text indexing, we implement an **Edge-Native Reasoning Layer** using BabyLLM principles.

## 🏗️ Architecture: The Three-Tiered Drive Agent

### Tier 1: The Looped Instinct Router (~100k params)
- **Function**: Rapidly classifies user intent (e.g., "Retrieval", "Synthesis", "Action", "Query").
- **Innovation**: Uses a **Looped Transformer** architecture. By looping activations, we achieve the depth of a 1M parameter model with 10% of the footprint, ensuring near-zero latency on internal hardware.
- **Output**: Routes the query to the appropriate OKF namespace or tool.

### Tier 2: OKF-Powered RAG Engine
- **Knowledge Representation**: The "cumbersome drive" is mapped into the **Open Knowledge Format (OKF)**. Files are not just indexed; they are converted into markdown documents with YAML frontmatter (tags, owners, timestamps, relationships).
- **Retrieval**: A hybrid search (Keyword + Semantic) retrieves relevant OKF fragments.
- **Synthesis**: A distilled MoE (Mixture-of-Experts) model synthesizes the answer from retrieved fragments.

### Tier 3: Drive Action Tools (MCP)
- **Tools**: 
    - `DriveSearch`: Low-level file system crawl.
    - `DocSummarizer`: Local distillation of large PDFs/Docs.
    - `RelationalMapper`: Maps dependencies between files (e.g., "This spec refers to that codebase").
    - `AutoArchiver`: Proactively suggests OKF restructuring for messy folders.

## 🚀 Competitive Edge
1. **Extreme Efficiency**: Looped architectures allow the agent to run locally on workstations without needing a massive GPU cluster.
2. **Interoperability**: By using OKF, the knowledge is vendor-neutral and human-readable.
3. **Cognitive Distillation**: We don't just RAG; we distill the "institutional DNA" of the drive into the Instinct model's weights.
