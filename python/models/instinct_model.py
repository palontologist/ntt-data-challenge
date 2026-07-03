"""Tier 1: InstinctModel - Fast understanding and tool selection.

~1M params, runs on CPU in <100ms.
Outputs: understanding_score (0-1), tool_idx (0-4)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class InstinctModel(nn.Module):
    """Fast understanding model for tool selection.
    
    Architecture:
    - Token embedding
    - Position embedding
    - Transformer blocks (lightweight)
    - Dual head: understanding score + tool classification
    """

    def __init__(
        self,
        vocab_size: int = 8192,
        embed_dim: int = 128,
        num_heads: int = 4,
        num_layers: int = 4,
        num_tools: int = 5,
        max_seq_len: int = 64,
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_tools = num_tools

        # Embeddings
        self.token_embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Embedding(max_seq_len, embed_dim)

        # Transformer blocks
        self.layers = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads)
            for _ in range(num_layers)
        ])

        self.ln_final = nn.LayerNorm(embed_dim)

        # Output heads
        self.understanding_head = nn.Sequential(
            nn.Linear(embed_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),  # Score 0-1
        )

        self.tool_head = nn.Linear(embed_dim, num_tools)

    def forward(self, idx: torch.Tensor):
        """Forward pass.
        
        Args:
            idx: (batch, seq_len) token indices
            
        Returns:
            understanding_score: (batch, 1) confidence 0-1
            tool_logits: (batch, num_tools) tool selection
        """
        B, T = idx.shape

        # Embeddings
        token_emb = self.token_embed(idx)
        pos_ids = torch.arange(T, device=idx.device)
        pos_emb = self.pos_embed(pos_ids)
        x = token_emb + pos_emb

        # Transformer layers
        for layer in self.layers:
            x = layer(x)

        x = self.ln_final(x)

        # Pool over sequence (mean pooling)
        x_pooled = x.mean(dim=1)  # (B, embed_dim)

        # Output heads
        understanding_score = self.understanding_head(x_pooled)  # (B, 1)
        tool_logits = self.tool_head(x_pooled)  # (B, num_tools)

        return understanding_score, tool_logits

    def predict(self, idx: torch.Tensor, threshold: float = 0.7):
        """Full prediction with routing decision.
        
        Args:
            idx: (batch, seq_len) token indices
            threshold: understanding score threshold for direct tool use
            
        Returns:
            understanding_score: (batch, 1)
            tool_idx: (batch,) selected tool index
            use_direct: (batch,) bool, True if score > threshold
        """
        understanding_score, tool_logits = self.forward(idx)
        tool_idx = torch.argmax(tool_logits, dim=-1)
        use_direct = (understanding_score.squeeze(-1) > threshold)

        return understanding_score, tool_idx, use_direct


class TransformerBlock(nn.Module):
    """Lightweight transformer block."""

    def __init__(self, embed_dim: int, num_heads: int):
        super().__init__()
        self.attn = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout=0.1,
            batch_first=True,
        )
        self.ln1 = nn.LayerNorm(embed_dim)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Linear(embed_dim * 4, embed_dim),
            nn.Dropout(0.1),
        )
        self.ln2 = nn.LayerNorm(embed_dim)

    def forward(self, x: torch.Tensor):
        # Self-attention
        attn_out, _ = self.attn(x, x, x)
        x = x + attn_out
        x = self.ln1(x)

        # FFN
        ffn_out = self.ffn(x)
        x = x + ffn_out
        x = self.ln2(x)

        return x


class InstinctTrainer:
    """Training loop for InstinctModel."""

    def __init__(self, model: InstinctModel, lr: float = 1e-3):
        self.model = model
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
        self.tool_loss_fn = nn.CrossEntropyLoss()

    def train_step(self, batch):
        """Single training step.
        
        Args:
            batch: dict with 'text' and 'action' tensors
            
        Returns:
            loss: total loss
            understanding_score: mean understanding score
        """
        text = batch["text"]
        action = batch["action"]

        understanding_score, tool_logits = self.model(text)

        # Tool selection loss
        tool_loss = self.tool_loss_fn(tool_logits, action)

        # Understanding score: train to be high for easy inputs
        # Use inverse of tool loss as signal
        target_score = torch.where(
            tool_logits.argmax(dim=-1) == action,
            torch.ones_like(understanding_score),
            torch.zeros_like(understanding_score),
        )
        understanding_loss = F.mse_loss(understanding_score, target_score)

        loss = tool_loss + 0.5 * understanding_loss

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()

        return loss.item(), understanding_score.mean().item()


if __name__ == "__main__":
    # Test
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = InstinctModel().to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"InstinctModel parameters: {total_params:,}")

    # Test forward pass
    batch_size = 4
    seq_len = 64
    idx = torch.randint(0, 8192, (batch_size, seq_len)).to(device)

    score, tool_logits = model(idx)
    print(f"Understanding score shape: {score.shape}")
    print(f"Tool logits shape: {tool_logits.shape}")
    print(f"Score range: [{score.min():.3f}, {score.max():.3f}]")
