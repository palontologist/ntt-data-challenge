from api.agent import process_query, LoopedInstinctModel, MeaningExplainer, OKFLoader, THRESHOLD, KNOWLEDGE_DIR
from api.synthesizer import ResponseSynthesizer
from data.multimodal_extractor import MultimodalExtractor
import pandas as pd
import torch
import tiktoken

def generate_predictions():
    # 1. Setup components
    tokenizer = tiktoken.get_encoding("gpt2")
    instinct_model = LoopedInstinctModel()
    explainer_model = MeaningExplainer()
    okf_loader = OKFLoader(KNOWLEDGE_DIR)
    multimodal_extractor = MultimodalExtractor()
    synthesizer = ResponseSynthesizer()
    
    instinct_model.eval()
    explainer_model.eval()
    
    # 2. Load questions
    questions_path = "/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive/share/質問回答/questions_valid.csv"
    df_questions = pd.read_csv(questions_path)
    
    predictions = []
    
    print(f"Processing {len(df_questions)} questions...")
    
    for idx, row in df_questions.iterrows():
        text = row['question']
        
        # Use the unified processing logic
        _, _, final_answer, _ = process_query(
            text, instinct_model, okf_loader, multimodal_extractor, synthesizer, tokenizer
        )
        
        predictions.append({
            "index": row['index'],
            "answer": final_answer
        })
        
        if idx % 10 == 0:
            print(f"Processed {idx}/{len(df_questions)}...")
    
    # 3. Save to predictions.csv
    df_predictions = pd.DataFrame(predictions)
    output_path = "/home/palontologist/Downloads/dev/ntt_data_challenge/predictions.csv"
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("index,answer\n")
        for _, row in df_predictions.iterrows():
            # Escape quotes in answer for CSV
            answer = f'"{row["answer"]}"'
            f.write(f"{row['index']},{answer}\n")
    print(f"Predictions saved to {output_path}")

if __name__ == "__main__":
    generate_predictions()

