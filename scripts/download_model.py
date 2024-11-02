# scripts/download_model.py

from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path
import torch

def download_model(model_name='EleutherAI/gpt-j-6B'):
    # Define the base directory relative to this script's location
    base_dir = Path(__file__).resolve().parent.parent  # Moves up to 'instagramAI'
    model_path = base_dir / 'models' / 'gpt-j-6B'

    # Create the model directory if it doesn't exist
    model_path.mkdir(parents=True, exist_ok=True)

    print(f"Model will be saved to: {model_path}")  # Debugging line

    # Determine if a GPU with sufficient memory is available
    if torch.cuda.is_available():
        print("CUDA is available. Attempting to use float16 precision.")
        torch_dtype = torch.float16
        revision = "float16"
    else:
        print("CUDA is not available. Using float32 precision.")
        torch_dtype = torch.float32
        revision = None  # Default revision

    try:
        # Load tokenizer and model from Hugging Face Hub
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            revision=revision,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True
        )

        # Assign eos_token as pad_token
        tokenizer.pad_token = tokenizer.eos_token

        # Save tokenizer and model locally
        tokenizer.save_pretrained(str(model_path))
        model.save_pretrained(str(model_path))

        print(f"Model '{model_name}' downloaded and saved to '{model_path}'")
    except Exception as e:
        print(f"An error occurred during model download: {e}")

if __name__ == "__main__":
    download_model()
