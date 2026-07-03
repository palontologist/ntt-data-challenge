"""FastAPI inference server for NTT Data IDI (Intelligent Drive Interface)."""

from fastapi import FastAPI
from pydantic import BaseModel
import torch
import tiktoken
from models.looped_instinct_model import LoopedInstinctModel
from models.meaning_explainer import MeaningExplainer
from data.okf_loader import OKFLoader

app = FastAPI(title="NTT Data IDI Agent")

# Configuration for Internal Drive Context
KNOWLEDGE_DIR = "knowledge"
THRESHOLD = 0.7
# Map: 0: File Search, 1: Summarize, 2: Relationship Map, 3: Archive, 4: Expert Query
DRIVE_TOOLS = {0: "drive_search", 1: "doc_summarizer", 2: "relational_mapper", 3: "auto_archiver", 4: "expert_query"}

# Load components
tokenizer = tiktoken.get_encoding("gpt2")
instinct_model = LoopedInstinctModel()
explainer_model = MeaningExplainer()
okf_loader = OKFLoader(KNOWLEDGE_DIR)

instinct_model.eval()
explainer_model.eval()

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    intent: str
    confidence: float
    response: str
    source_okf: bool

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    text = request.text
    tokens = tokenizer.encode(text)
    idx = torch.tensor([tokens], dtype=torch.long)
    
    with torch.no_grad():
        score, tool_idx, use_direct = instinct_model.predict(idx, threshold=THRESHOLD)
        score_val = score.item()
        tool_val = tool_idx.item()
        direct = use_direct.item()

    # If the model is unsure or specifically requests an expert query/RAG
    if not direct or tool_val == 4:
        docs = okf_loader.search(text)
        context = "\n".join([f"{d['metadata'].get('title')}: {d['body']}" for d in docs]) if docs else "No specific drive context found."
        
        # Tier 2 synthesis (Simulated for this prototype)
        output = f"[IDI Reasoning Layer]\nUsing context from drive: {context[:150]}...\nAnswer: The requested information was located in the OKF-mapped drive structure."
        
        return QueryResponse(
            intent="expert_query",
            confidence=score_val,
            response=output,
            source_okf=True if docs else False
        )
    
    # Tier 3: Direct Drive Tool Use
    tool_name = DRIVE_TOOLS.get(tool_val, "unknown_tool")
    return QueryResponse(
        intent=tool_name,
        confidence=score_val,
        response=f"Executing drive tool {tool_name} for query: {text}",
        source_okf=False
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
