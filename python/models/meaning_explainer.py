"""Tier 2: Meaning Explainer - TinyLlama partner for explanations."""

import torch
import torch.nn as nn


class MeaningExplainer(nn.Module):
    """Lightweight explanation model.
    
    Used as the local explanation partner in Tier 3 tools.
    Can be replaced with TinyLlama for better quality.
    """

    def __init__(
        self,
        vocab_size: int = 8192,
        embed_dim: int = 384,
        num_heads: int = 6,
        num_layers: int = 6,
        max_seq_len: int = 256,
    ):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Embedding(max_seq_len, embed_dim)

        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=num_heads,
                dim_feedforward=embed_dim * 4,
                dropout=0.1,
                batch_first=True,
            )
            for _ in range(num_layers)
        ])

        self.ln = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok = self.token_embed(idx)
        pos = self.pos_embed(torch.arange(T, device=idx.device))
        x = tok + pos

        for layer in self.layers:
            x = layer(x)

        x = self.ln(x)
        logits = self.head(x)

        loss = None
        if targets is not None:
            loss = nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.view(-1),
                ignore_index=-100,
            )
        return logits, loss


if __name__ == "__main__":
    model = MeaningExplainer()
    total_params = sum(p.numel() for p in model.parameters())
    print(f"MeaningExplainer parameters: {total_params:,}")
