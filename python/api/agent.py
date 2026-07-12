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
TOKEN_LIMIT = 1000 # Strict limit per rules

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
from api.synthesizer import ResponseSynthesizer
synthesizer = ResponseSynthesizer()

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
    
    # Build a glossary map from all glossary documents
    glossary_map = {}
    for doc in glossary_docs:
        lines = doc['body'].split('\n')
        for line in lines:
            # Look for common glossary patterns: "Term: Meaning", "Term - Meaning", "Term \t Meaning"
            for separator in [':', ' - ', '\t']:
                if separator in line:
                    parts = line.split(separator, 1)
                    term = parts[0].strip()
                    meaning = parts[1].strip()
                    if term and meaning:
                        glossary_map[term] = meaning
                        break
    
    if not glossary_map:
        return text

    expanded_text = text
    for term, meaning in glossary_map.items():
        expanded_text = expanded_text.replace(term, f"{term}({meaning})")
    
    return expanded_text

def enforce_token_limit(text: str, limit: int) -> str:
    """Ensures the output does not exceed the token limit."""
    tokens = tokenizer.encode(text)
    if len(tokens) > limit:
        return tokenizer.decode(tokens[:limit]) + "... [Truncated]"
    return text

def process_query(text: str, instinct_model, okf_loader, multimodal_extractor, synthesizer, tokenizer):
    """Unified query processing logic used by both API and CSV generator."""
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
    processed_text = expand_glossary(text)
    
    evidence = []
    context = ""
    
    if route_name == "MULTIMODAL_ANALYSIS":
        # Search for image-like documents related to the query
        relevant_docs = okf_loader.search(text, top_k=5)
        context_parts = []
        for doc in relevant_docs:
            if any(ext in doc['path'] for ext in ['.png', '.jpg', '.jpeg', '.md']):
                analysis = multimodal_extractor.process_material(doc['path'])
                evidence.append(doc['path'])
                context_parts.append(analysis)
        
        context = "\n".join(context_parts) if context_parts else "画像解析の結果、該当する情報は見つかりませんでした。"
    
    elif route_name == "SYNTHETIC_AGGREGATION":
        docs = okf_loader.search(processed_text, top_k=5)
        evidence = [d['path'] for d in docs]
        context = "\n".join([f"Source: {d['path']}\nContent: {d['body']}" for d in docs])
    
    else: # ATOMIC_RETRIEVAL or EXPERT_QUERY
        docs = okf_loader.search(processed_text, top_k=3)
        evidence = [d['path'] for d in docs]
        context = "\n".join([f"Source: {d['path']}\nContent: {d['body']}" for d in docs]) if docs else "該当する情報が見つかりませんでした。"

    # 3. Final Synthesis
    final_answer_jp = synthesizer.synthesize(text, context, evidence)
    final_answer_jp = enforce_token_limit(final_answer_jp, TOKEN_LIMIT)
    
    return route_name, score_val, final_answer_jp, evidence

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    text = request.text
    route_name, score_val, final_answer_jp, evidence = process_query(
        text, instinct_model, okf_loader, multimodal_extractor, synthesizer, tokenizer
    )
    return QueryResponse(
        route=route_name,
        confidence=score_val,
        answer_jp=final_answer_jp,
        evidence_sources=evidence
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
