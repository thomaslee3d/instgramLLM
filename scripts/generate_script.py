# scripts/generate_script.py

import sys
from pathlib import Path

# Add the project root to sys.path **before** importing config
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import config  # Import the config file after adjusting sys.path
import argparse

def setup_logging():
    logging.basicConfig(
        filename='generate_script.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def load_model():
    model_name = config.ACTIVE_MODEL.strip()
    logging.info(f"Loading model '{model_name}'")
    
    base_dir = Path(__file__).resolve().parent.parent
    model_path = base_dir / 'models' / model_name

    # Check if the model directory exists
    if not model_path.exists():
        logging.error(f"Model directory '{model_path}' does not exist.")
        raise FileNotFoundError(f"Model directory '{model_path}' does not exist.")

    print(f"Loading tokenizer and model from: {model_path}")

    try:
        # Load tokenizer and model from the local directory
        tokenizer = AutoTokenizer.from_pretrained(str(model_path), use_fast=True)
        
        # Assign eos_token as pad_token if not already set
        if not tokenizer.pad_token:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load the model with appropriate precision
        if model_name == 'gpt-j-6B':
            model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(str(model_path))
        
        # Update model config with pad_token_id
        model.config.pad_token_id = tokenizer.eos_token_id

        model.eval()
        if torch.cuda.is_available():
            model.to('cuda')
            logging.info("Model moved to GPU.")
        else:
            model.to('cpu')
            logging.info("Model moved to CPU.")

        logging.info(f"Model '{model_name}' loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load the model: {e}")
        raise e

    return tokenizer, model

def generate_script(title, selftext, tokenizer, model, max_length=200):
    logging.info(f"Generating script for title: '{title}'")
    prompt = (
        f"Create an engaging Instagram script based on the following Reddit story:\n\n"
        f"Title: {title}\n\n{selftext}\n\nScript:"
    )
    inputs = tokenizer.encode_plus(
        prompt,
        return_tensors='pt',
        padding=True,
        truncation=True,
        max_length=512  # Adjust as needed
    )
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    if torch.cuda.is_available():
        input_ids = input_ids.to('cuda')
        attention_mask = attention_mask.to('cuda')
    else:
        input_ids = input_ids.to('cpu')
        attention_mask = attention_mask.to('cpu')

    logging.info("Generating output from the model...")
    try:
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id  # Explicitly set pad_token_id
        )
        script = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract the script part
        if "Script:" in script:
            script = script.split("Script:")[-1].strip()
        else:
            script = script.strip()
        logging.info("Script generated successfully.")
    except Exception as e:
        logging.error(f"Failed to generate script: {e}")
        raise e

    return script

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Instagram script from Reddit story.")
    parser.add_argument('--model', type=str, default=config.ACTIVE_MODEL, help="Model to use for script generation.")
    parser.add_argument('--title', type=str, help="Title of the Reddit story.")
    parser.add_argument('--selftext', type=str, help="Selftext/content of the Reddit story.")
    parser.add_argument('--max_length', type=int, default=200, help="Maximum length of the generated script.")
    return parser.parse_args()

if __name__ == "__main__":
    setup_logging()
    args = parse_arguments()
    try:
        tokenizer, model = load_model()
        sample_title = args.title if args.title else "An Unexpected Adventure"
        sample_selftext = args.selftext if args.selftext else "I never thought a simple hike would lead me to discovering a hidden waterfall..."
        script = generate_script(sample_title, sample_selftext, tokenizer, model, args.max_length)
        print("Generated Script:\n", script)
        logging.info("Script printed to console.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
