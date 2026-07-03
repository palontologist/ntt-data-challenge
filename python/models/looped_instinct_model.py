"""Tier 1: LoopedInstinctModel - Parameter-efficient expert heuristics.

Inspired by 'Looped Transformers are Better at Learning Learning Algorithms'.
Instead of N different layers, we use a single layer looped N times to emulate 
iterative refinement of the heuristic.

Reduction in parameter count: ~90% compared to standard deep transformers.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from models.instinct_model import TransformerBlock

class LoopedInstinctModel(nn.Module):
    """Looped transformer for parameter-efficient heuristic routing."""
    
    def __init__(
        self,
        vocab_size: int = 8192,
        embed_dim: int = 128,
        num_heads: int = 4,
        num_loops: int = 4, # The 'depth' is now a loop count, not layer count
        num_tools: int = 5,
        max_seq_len: int = 64,
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_tools = num_tools
        self.num_loops = num_loops

        # Embeddings
        self.token_embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Embedding(max_seq_len, embed_dim)

        # A SINGLE transformer block that is reused
        self.looped_layer = TransformerBlock(embed_dim, num_heads)

        self.ln_final = nn.LayerNorm(embed_dim)

        # Output heads
        self.understanding_head = nn.Sequential(
            nn.Linear(embed_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

        self.tool_head = nn.Linear(embed_dim, num_tools)

    def forward(self, idx: torch.Tensor):
        B, T = idx.shape

        # Embeddings
        token_emb = self.token_embed(idx)
        pos_ids = torch.arange(T, device=idx.device)
        pos_emb = self.pos_embed(pos_ids)
        x = token_emb + pos_emb

        # Looped Iteration: Pass through the SAME layer N times
        for _ in range(self.num_loops):
            x = self.looped_layer(x)

        x = self.ln_final(x)

        # Pool over sequence
        x_pooled = x.mean(dim=1)

        # Output heads
        understanding_score = self.understanding_head(x_pooled)
        tool_logits = self.tool_head(x_pooled)

        return understanding_score, tool_logits

    def predict(self, idx: torch.Tensor, threshold: float = 0.7):
        understanding_score, tool_logits = self.forward(idx)
        tool_idx = torch.argmax(tool_logits, dim=-1)
        use_direct = (understanding_score.squeeze(-1) > threshold)
        return understanding_score, tool_idx, use_direct

if __name__ == "__main__":
    # Test
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LoopedInstinctModel().to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"LoopedInstinctModel parameters: {total_params:,}")

    # Test forward pass
    batch_size = 4
    seq_len = 64
    idx = torch.randint(0, 8192, (batch_size, seq_len)).to(device)

    score, tool_logits = model(idx)
    print(f"Understanding score shape: {score.shape}")
    print(f"Tool logits shape: {tool_logits.shape}")
