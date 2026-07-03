import os
import yaml
from typing import List, Dict, Any

class OKFLoader:
    """Loader for Open Knowledge Format (OKF) documents."""
    
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = knowledge_dir
        self.documents = []
        self.load_all()

    def load_all(self):
        """Loads all .md files from the knowledge directory."""
        if not os.path.exists(self.knowledge_dir):
            print(f"Warning: Knowledge directory {self.knowledge_dir} not found.")
            return

        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(self.knowledge_dir, filename)
                self.load_file(filepath)

    def load_file(self, filepath: str):
        """Parses a single OKF file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                    self.documents.append({
                        "metadata": metadata,
                        "body": body,
                        "path": filepath
                    })
            except Exception as e:
                print(f"Error parsing OKF file {filepath}: {e}")
        else:
            # Fallback for files without frontmatter
            self.documents.append({
                "metadata": {},
                "body": content,
                "path": filepath
            })

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Simple keyword-based search for RAG."""
        query_words = query.lower().split()
        results = []

        for doc in self.documents:
            score = 0
            text_to_search = (
                (doc['metadata'].get('title', '') + " " + 
                 doc['metadata'].get('description', '') + " " + 
                 " ".join(doc['metadata'].get('tags', [])) + " " + 
                 doc['body']).lower()
            )
            
            for word in query_words:
                if word in text_to_search:
                    score += 1
            
            if score > 0:
                results.append((score, doc))

        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results[:top_k]]

if __name__ == "__main__":
    # Quick test
    loader = OKFLoader("knowledge")
    print(f"Loaded {len(loader.documents)} documents.")
    results = loader.search("looped transformer")
    for res in results:
        print(f"Found: {res['metadata'].get('title')}")
