import pandas as pd
import torch
import tiktoken
import os
import json
from api.agent import process_query, LoopedInstinctModel, MeaningExplainer, OKFLoader, THRESHOLD, KNOWLEDGE_DIR
from api.synthesizer import ResponseSynthesizer
from data.multimodal_extractor import MultimodalExtractor

CHECKPOINT_PATH = "/home/palontologist/Downloads/dev/ntt_data_challenge/predictions_checkpoint.json"
OUTPUT_PATH = "/home/palontologist/Downloads/dev/ntt_data_challenge/predictions.csv"

def save_checkpoint(predictions, completed_indices):
    with open(CHECKPOINT_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            'predictions': predictions,
            'completed_indices': list(completed_indices)
        }, f, ensure_ascii=False, indent=2)

def load_checkpoint():
    if os.path.exists(CHECKPOINT_PATH):
        with open(CHECKPOINT_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('predictions', []), set(data.get('completed_indices', []))
    return [], set()

def write_final_csv(predictions):
    df_predictions = pd.DataFrame(predictions)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for _, row in df_predictions.iterrows():
            answer = f'"{row["answer"]}"'
            f.write(f"{row['index']},{answer}\n")
    print(f"Final predictions saved to {OUTPUT_PATH}")

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
    
    # 2. Load questions (TEST SET - 100 questions for submission)
    questions_path = "raw_drive/share/質問回答/questions_test.csv"
    if not os.path.exists(questions_path):
        questions_path = "share/質問回答/questions_test.csv"
    
    try:
        df_questions = pd.read_csv(questions_path)
    except FileNotFoundError:
        print(f"Error: Questions file not found at {questions_path}")
        return
    
    # Load checkpoint
    predictions, completed_indices = load_checkpoint()
    print(f"Resuming from checkpoint: {len(completed_indices)} questions already completed")
    
    print(f"Processing {len(df_questions)} questions...")
    
    for idx, row in df_questions.iterrows():
        q_idx = row['index']
        
        # Skip if already completed
        if q_idx in completed_indices:
            continue
            
        text = row['question']
        
        # Use the unified processing logic
        _, _, final_answer, _ = process_query(
            text, instinct_model, okf_loader, multimodal_extractor, synthesizer, tokenizer
        )
        
        predictions.append({
            "index": q_idx,
            "answer": final_answer
        })
        completed_indices.add(q_idx)
        
        # Save checkpoint every 5 questions
        if len(completed_indices) % 5 == 0:
            save_checkpoint(predictions, completed_indices)
            print(f"Checkpoint saved: {len(completed_indices)}/{len(df_questions)} completed")
        
        if len(completed_indices) % 10 == 0:
            print(f"Processed {len(completed_indices)}/{len(df_questions)}...")
    
    # 3. Save final predictions.csv
    write_final_csv(predictions)
    
    # Clean up checkpoint
    if os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)
    print("Done!")

if __name__ == "__main__":
    generate_predictions()

