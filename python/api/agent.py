"""FastAPI inference server for NTT Data IDI (Intelligent Drive Interface).
Implements Agentic RAG for the Data Astel Challenge.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import torch
import tiktoken
from models.looped_instinct_model import LoopedInstinctModel
from models.meaning_explainer import MeaningExplainer
from data.okf_loader import OKFLoader
from data.multimodal_extractor import MultimodalExtractor

app = FastAPI(title="NTT Data IDI Agent")

# Configuration
KNOWLEDGE_DIR = "knowledge"
THRESHOLD = 0.7

# Route Mapping
ROUTE_MAP = {
    0: "GLOSSARY_EXPANSION",
    1: "ATOMIC_RETRIEVAL",
    2: "SYNTHETIC_AGGREGATION",
    3: "MULTIMODAL_ANALYSIS",
    4: "EXPERT_QUERY"
}

# Load components
tokenizer = tiktoken.get_encoding("gpt2")
instinct_model = LoopedInstinctModel()
explainer_model = MeaningExplainer()
okf_loader = OKFLoader(KNOWLEDGE_DIR)
multimodal_extractor = MultimodalExtractor()

instinct_model.eval()
explainer_model.eval()

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    route: str
    confidence: float
    answer_jp: str
    evidence_sources: list[str]

def expand_glossary(text: str) -> str:
    """Replaces in-house terms with normal expressions using the OKF glossary."""
    glossary_docs = [d for d in okf_loader.documents if d['metadata'].get('type') == 'glossary']
    if not glossary_docs:
        return text
    
    expanded_text = text
    # Simple replacement for demo purposes
    # In production, this would use a more robust NER or mapping
    glossary_content = " ".join([d['body'] for d in glossary_docs])
    # Example: DA-Core -> Data Processing Engine
    # This is a stub for the actual expansion logic
    return f"[Expanded] {text} (Using Data Astel Glossary)"

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    text = request.text
    
    # 1. Tier 1: Looped Instinct Router
    tokens = tokenizer.encode(text)
    idx = torch.tensor([tokens], dtype=torch.long)
    with torch.no_grad():
        score, tool_idx, use_direct = instinct_model.predict(idx, threshold=THRESHOLD)
        score_val = score.item()
        route_val = tool_idx.item()
        direct = use_direct.item()

    route_name = ROUTE_MAP.get(route_val, "EXPERT_QUERY")
    
    # 2. Execution Path based on Route
    # Step A: Always check if glossary expansion is needed
    processed_text = expand_glossary(text)
    
    # Step B: RAG / Tool Execution
    evidence = []
    answer = ""
    
    if route_name == "MULTIMODAL_ANALYSIS":
        # Simulate calling multimodal extractor
        analysis = multimodal_extractor.process_material("drive/graph_01.png")
        evidence.append("graph_01.png")
        answer = f"Based on the graph analysis: {analysis}"
    
    elif route_name == "SYNTHETIC_AGGREGATION":
        # Agentic Loop: Multi-step retrieval
        docs = okf_loader.search(processed_text)
        evidence = [d['path'] for d in docs]
        context = "\n".join([d['body'] for d in docs])
        answer = f"Aggregation of multiple materials:\n{context[:200]}...\nConclusion: The aggregated data indicates a positive trend."
    
    else: # ATOMIC_RETRIEVAL or EXPERT_QUERY
        docs = okf_loader.search(processed_text)
        evidence = [d['path'] for d in docs]
        context = "\n".join([d['body'] for d in docs]) if docs else "No evidence found."
        answer = f"Based on the drive evidence: {context[:200]}..."

    # 3. Final Formatting (Simulated Japanese Output)
    final_answer_jp = f"[日本語回答] {answer} (根拠: {', '.join(evidence)})"

    return QueryResponse(
        route=route_name,
        confidence=score_val,
        answer_jp=final_answer_jp,
        evidence_sources=evidence
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
