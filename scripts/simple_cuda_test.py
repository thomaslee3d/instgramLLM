# scripts/simple_cuda_test.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path
import config

def main():
    model_name = config.ACTIVE_MODEL.strip()
    print(f"Model Name: {model_name}")
    model_path = Path(__file__).resolve().parent.parent / 'models' / model_name
    print(f"Model Path: {model_path}")

    if not model_path.exists():
        print(f"Error: Model directory '{model_path}' does not exist.")
        return

    try:
        tokenizer = AutoTokenizer.from_pretrained(str(model_path), use_fast=True)
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        model.eval()
        if torch.cuda.is_available():
            model.to('cuda')
            print("Model loaded on GPU.")
        else:
            model.to('cpu')
            print("Model loaded on CPU.")
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")

if __name__ == "__main__":
    main()
