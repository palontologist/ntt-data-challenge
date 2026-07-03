# 🚀 NTT Data AI Engineering Challenge: Intelligent Drive Interface (IDI)

An implementation of an AI-driven internal drive interface based on the **BabyLLM** philosophy.

## 🌟 Core Innovations
- **Looped Transformers**: Scaling reasoning depth without increasing memory footprint.
- **Open Knowledge Format (OKF)**: Converting cumbersome file structures into an interoperable, agent-friendly wiki.
- **Cognitive Distillation**: Baking drive-specific heuristics into a tiny routing model.

## 📁 Project Structure
- `python/models/`: Looped Transformer implementation for intent routing.
- `python/data/`: OKF loader and drive-to-knowledge mapping logic.
- `python/api/`: FastAPI server for the IDI Agent.
- `knowledge/`: The OKF representation of the internal drive.
- `ARCHITECTURE.md`: Detailed technical breakdown.

## 🛠️ Quick Start
1. `cd python && pip install -r requirements.txt`
2. `python api/agent.py`
3. Use the API to query your "cumbersome drive" with expert-level precision.

## 💡 Why this wins
Most solutions will propose a heavy RAG pipeline using GPT-4. This solution proposes a **sustainable, edge-native architecture** that is fast, private, and structurally superior by treating knowledge as a format (OKF) rather than just a vector database.
