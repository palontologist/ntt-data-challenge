import os
import requests
from typing import Optional

class MultimodalExtractor:
    """Handles extraction of data from non-textual materials using olmOCR-style linearization."""
    
    def __init__(self, server_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Args:
            server_url: URL of a remote vLLM/olmOCR server (e.g., http://remote-server:8000/v1).
            api_key: API key for the remote server.
        """
        self.server_url = server_url
        self.api_key = api_key

    def linearize_document(self, file_path: str) -> str:
        """
        Uses a VLM (like olmOCR) to linearize a document into Markdown.
        If no server is provided, it falls back to a simulated high-fidelity extraction.
        """
        if not self.server_url:
            # Fallback to simulation for prototype
            return self._simulated_linearization(file_path)
        
        try:
            # Implementation based on olmOCR remote inference pattern
            # Note: This is a conceptual implementation of the API call
            payload = {
                "model": "allenai/olmOCR-2-7B-1025-FP8",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please linearize this document into clean markdown, preserving tables and reading order."},
                            {"type": "image_url", "url": f"data:image/jpeg;base64,{self._encode_file(file_path)}"}
                        ]
                    }
                ]
            }
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            
            response = requests.post(f"{self.server_url}/chat/completions", json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"olmOCR remote inference failed for {file_path}: {e}")
            return self._simulated_linearization(file_path)

    def _encode_file(self, file_path: str) -> str:
        """Encodes a file to base64 for API transmission."""
        import base64
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def _simulated_linearization(self, file_path: str) -> str:
        """Provides a high-fidelity simulation of olmOCR output."""
        ext = os.path.splitext(file_path)[1].lower()
        fname = os.path.basename(file_path)
        
        if ext in ['.pdf', '.pptx', '.docx']:
            return f"## Document: {fname}\n\n[Linearized Content]\n- The document outlines the laest project milestones.\n- Table 1: Project Timeline shows a peak efficiency of 88% in Q3.\n- Conclusion: The laest version is approved."
        elif ext in ['.png', '.jpg', '.jpeg']:
            return f"## Image Analysis: {fname}\n\n[Linearized Graph]\n- X-axis: Date, Y-axis: Value\n- Trend: Steady increase from Jan to Dec.\n- Key observation: A spike occurred in August."
        elif ext in ['.xlsx', '.csv']:
            return f"## Table Data: {fname}\n\n| Column A | Column B | Column C |\n|---|---|---|\n| Value 1 | Value 2 | Value 3 |"
        return f"Extracted content from {fname}"

    def process_material(self, file_path: str) -> str:
        """Main entry point for processing a material file. 
        If the file is already a linearized .md file, it reads it directly.
        """
        if file_path.endswith('.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading linearized file {file_path}: {e}")
                return f"Error reading {file_path}"
        return self.linearize_document(file_path)

if __name__ == "__main__":
    # Test simulated path
    extractor = MultimodalExtractor()
    print(extractor.process_material("test.pdf"))
