import os
import time
from openai import OpenAI
import google.generativeai as genai
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class ResponseSynthesizer:
    """Synthesizes final answers from retrieved OKF context using high-end LLMs."""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None, provider: str = None):
        # Load provider from env if not specified
        self.provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()
        
        if self.provider == "google":
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
            self.model_name = model or os.getenv("GOOGLE_MODEL", "gemini-1.5-pro")
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model_name)
            else:
                self.client = None
        else: # default to openai
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
            self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
            if self.api_key:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            else:
                self.client = None

    def synthesize(self, question: str, context: str, evidence_paths: List[str]) -> str:
        """
        Generates a final Japanese response grounded strictly in the provided context.
        """
        if not self.client:
            return self._simulated_synthesis(question, context, evidence_paths)

        # For Google models, we use a system instruction parameter for better adherence
        # and a separate user prompt.
        
        system_instruction = """あなたはデータアステル社の社内AIアシスタントです。
提供された【コンテキスト】のみを根拠にして、ユーザーの【質問】に日本語で回答してください。

# 制約事項:
1. **根拠の厳守**: 提供されたコンテキストにない情報は絶対に含めないでください。推論せず、事実のみを述べてください。
2. **該当なしの回答**: 条件に合う情報が見つからない場合は、「該当するものはありません」と明確に回答してください。
3. **形式の遵守**: 質問で指定された形式、単位、小数桁、丸め方がある場合は厳密に従ってください。
4. **識別子の維持**: タスクID、アクションIDなどの識別子は、資料の表記通りに記載してください。
5. **自然な表現**: 社内用語・略称は、設問で指定がない限り、通常の表現に展開して回答してください。
6. **簡潔さ**: 回答は簡潔に、結論から述べてください。"""

        user_prompt = f"# 質問:\n{question}\n\n# コンテキスト:\n{context}\n\n# 回答:"

        max_retries = 5
        retry_delay = 30 # Seconds to wait on 429

        for attempt in range(max_retries):
            try:
                if self.provider == "google":
                    # Use a fresh model instance with system_instruction for better control
                    model = genai.GenerativeModel(
                        model_name=self.model_name,
                        system_instruction=system_instruction
                    )
                    response = model.generate_content(
                        user_prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0,
                        )
                    )
                    return response.text.strip()
                else:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "system", "content": system_instruction},
                                   {"role": "user", "content": user_prompt}],
                        temperature=0,
                    )
                    return response.choices[0].message.content.strip()
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    if attempt < max_retries - 1:
                        print(f"Rate limit hit. Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2 # Exponential backoff
                        continue
                print(f"Synthesis error ({self.provider}): {e}")
                break
        
        return self._simulated_synthesis(question, context, evidence_paths)


    def _simulated_synthesis(self, question: str, context: str, evidence_paths: List[str]) -> str:
        """Provides a higher-quality fallback response when API key is missing by utilizing the context."""
        if not context or "該当する情報が見つかりませんでした" in context:
            return "該当する情報が見つかりませんでした。"
        
        # Simple heuristic: return the first few paragraphs of the context as a 'grounded' answer
        # In a real scenario, this would be replaced by a local LLM.
        summary = context.split('\n\n')[0] if '\n\n' in context else context[:500]
        
        return (
            f"【根拠に基づく回答（シミュレーションモード）】\n"
            f"提供された資料({', '.join(evidence_paths)})に基づき、以下の情報を抽出しました：\n\n"
            f"{summary}\n\n"
            f"※詳細な回答を生成するには OPENAI_API_KEY の設定が必要です。"
        )

if __name__ == "__main__":
    # Test simulation
    synthesizer = ResponseSynthesizer()
    print(synthesizer.synthesize("テスト質問", "テストコンテキスト", ["test.md"]))
