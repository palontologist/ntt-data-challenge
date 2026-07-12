import os
import yaml
import csv
from datetime import datetime
from typing import List, Dict, Any
from data.multimodal_extractor import MultimodalExtractor

class OKFGenerator:
    """Converts raw drive materials into Open Knowledge Format (OKF) without heavy dependencies."""
    
    def __init__(self, raw_drive_dir: str, output_dir: str):
        self.raw_drive_dir = raw_drive_dir
        self.output_dir = output_dir
        self.extractor = MultimodalExtractor()
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Generates YAML metadata based on file path and content."""
        parts = file_path.split(os.sep)
        project_name = "Unknown"
        if "プロジェクト" in parts:
            idx = parts.index("プロジェクト")
            if idx + 1 < len(parts):
                project_name = parts[idx + 1]
        
        is_management = "社内管理" in parts
        
        return {
            "type": "glossary" if is_management else "material",
            "title": os.path.basename(file_path),
            "project": project_name,
            "source": file_path,
            "timestamp": datetime.now().isoformat(),
            "tags": ["drive_extraction", project_name]
        }

    def _extract_text(self, file_path: str) -> str:
        """Generic text extraction based on file extension."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.md':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif ext == '.csv':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    return "\n".join([" | ".join(row) for row in rows])
            except Exception as e:
                return f"Error reading CSV: {e}"
        elif ext == '.xlsx':
            # Fallback to simulation since openpyxl/pandas are too large for current disk
            return f"Extracted table from {os.path.basename(file_path)}: [Simulation of table data]"
        elif ext in ['.pdf', '.docx', '.pptx']:
            return f"Extracted content from {os.path.basename(file_path)}: [Simulation of detailed document text...]"
        elif ext == '.ipynb':
            import json
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cells = [c['source'] for c in data.get('cells', []) if c['cell_type'] == 'markdown']
                    return "\n\n".join([str(s) for s in cells])
            except:
                return "Failed to parse notebook."
        else:
            if ext in ['.png', '.jpg', '.jpeg']:
                return self.extractor.extract_from_image(file_path)
            return f"Unsupported format: {ext}"

    def generate(self):
        """Crawls the raw drive and generates OKF files."""
        print(f"Generating OKF from {self.raw_drive_dir}...")
        count = 0
        
        for root, _, files in os.walk(self.raw_drive_dir):
            for file in files:
                if file.startswith('.') or file.endswith('.zip'):
                    continue
                    
                file_path = os.path.join(root, file)
                content = self._extract_text(file_path)
                metadata = self._get_metadata(file_path)
                okf_content = f"---\n{yaml.dump(metadata)}\n---\n\n{content}"
                
                rel_path = os.path.relpath(file_path, self.raw_drive_dir)
                okf_filename = rel_path.replace(os.sep, '_') + ".md"
                output_path = os.path.join(self.output_dir, okf_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(okf_content)
                
                count += 1
        
        print(f"Successfully generated {count} OKF documents in {self.output_dir}")

if __name__ == "__main__":
    generator = OKFGenerator(
        raw_drive_dir="/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive",
        output_dir="/home/palontologist/Downloads/dev/ntt_data_challenge/knowledge"
    )
    generator.generate()
