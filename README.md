Reddit-to-Instagram AI Automation Project


Welcome to the Reddit-to-Instagram AI Automation Project! This project automates the process of generating engaging Instagram scripts based on Reddit stories using AI models. Below, you'll find a detailed description of the setup process, configuration, and troubleshooting steps that were undertaken to ensure the project runs smoothly with GPU acceleration.


Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.8 or higher
Git
NVIDIA GPU with CUDA support
CUDA Toolkit (compatible with your PyTorch version)
Git LFS (Large File Storage) [optional, if using large models]

Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/reddit-to-instagram-ai.git
cd reddit-to-instagram-ai
Set Up a Virtual Environment:

It's recommended to use a virtual environment to manage project dependencies.

bash
Copy code
python -m venv env
Activate the Virtual Environment:

Windows:

bash
Copy code
env\Scripts\activate
macOS/Linux:

bash
Copy code
source env/bin/activate
Upgrade pip:

bash
Copy code
pip install --upgrade pip
Install Required Python Packages:

bash
Copy code
pip install -r requirements.txt
Ensure your requirements.txt includes necessary packages such as torch, transformers, dotenv, etc.



Configuration
Create and Configure the .env File:

The .env file holds your environment variables, including API credentials and model configuration.

env
Copy code
# .env

REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
ACTIVE_MODEL=gpt-j-6B
# Or distilgpt2


Important Notes:

No Inline Comments: Comments should be on separate lines starting with #.
No Code Snippets: The .env file should contain only KEY=VALUE pairs.
Ensure .env Overrides Global Environment Variables:

To prevent global environment variables from interfering, ensure that the .env file takes precedence.

In config.py, the load_dotenv function is set with override=True to prioritize .env settings:

load_dotenv(dotenv_path=base_dir / '.env', override=True)


Model Setup
Verify Model Directory:

Ensure that the model directory exists at D:\AI\instagramAI\models\gpt-j-6B. If it doesn't, follow the steps below to download and set it up.

Download the gpt-j-6B Model:

A Python script is provided to download and save the model locally.

Create download_model.py:

# scripts/download_model.py

import os
from transformers import AutoModelForCausalLM, AutoTokenizer

def download_model(model_name, save_directory):
    print(f"Downloading model '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, low_cpu_mem_usage=True)
    print(f"Saving model to '{save_directory}'...")
    tokenizer.save_pretrained(save_directory)
    model.save_pretrained(save_directory)
    print("Model downloaded and saved successfully.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download and save a Hugging Face model locally.")
    parser.add_argument('model_name', type=str, help="Name of the model to download (e.g., 'EleutherAI/gpt-j-6B').")
    parser.add_argument('save_directory', type=str, help="Local directory to save the model.")
    args = parser.parse_args()

    download_model(args.model_name, args.save_directory)


    Run the Download Script:

(env) D:\AI\instagramAI> python scripts/download_model.py EleutherAI/gpt-j-6B models/gpt-j-6B

Notes:

Downloading gpt-j-6B requires significant disk space (over 6 GB).
Ensure a stable internet connection during the download process.



Verify the Download:

After the download completes, confirm that the gpt-j-6B directory contains essential files like config.json, pytorch_model.bin, tokenizer_config.json, vocab.json, and merges.txt.

Check config.json:

Open D:\AI\instagramAI\models\gpt-j-6B\config.json and ensure it includes the model_type


{
  "model_type": "gptj",
  "vocab_size": 50257,
  ...
}



Running the Script
With the environment configured and the model set up, you can now run the generate_script.py to generate Instagram scripts based on Reddit stories.



Ensure the Virtual Environment is Activated:

bash
Copy code
(env) D:\AI\instagramAI> env\Scripts\activate
Run the Script:

bash
Copy code
(env) D:\AI\instagramAI> python scripts/generate_script.py
Expected Output:

vbnet
Copy code
DEBUG: ACTIVE_MODEL is set to: gpt-j-6B
Loading tokenizer and model from: D:\AI\instagramAI\models\gpt-j-6B
Model moved to GPU.
Model 'gpt-j-6B' loaded successfully.
Generating script for title: 'An Unexpected Adventure'
Generating output from the model...
Script generated successfully.
Script printed to console.
Generated Script:
"Hey everyone! 🌟 Today, I stumbled upon an incredible story from Reddit about an unexpected adventure during a simple hike. Swipe to read more and let me know your thoughts! #RedditStories #Adventure #Inspiration"
Optional Arguments:

Specify a Different Model:

bash
Copy code
python scripts/generate_script.py --model distilgpt2
Provide Custom Title and Selftext:

bash
Copy code
python scripts/generate_script.py --title "Your Reddit Title" --selftext "Your Reddit content..."
Adjust Maximum Length:

bash
Copy code
python scripts/generate_script.py --max_length 250




Troubleshooting
If you encounter issues during setup or execution, follow these steps to diagnose and resolve them.

Incorrect ACTIVE_MODEL Value:

Error Message:

go
Copy code
An error occurred: Model directory 'D:\AI\instagramAI\models\gpt-j-6B  # Or 'distilgpt2'' does not exist.
Solution:

Ensure Correct .env Configuration:

Open the .env file and verify that ACTIVE_MODEL is set without any trailing comments or extra characters.

env
Copy code
ACTIVE_MODEL=gpt-j-6B
# Or distilgpt2
Remove Conflicting Global Environment Variables:

Windows:

Go to System Properties > Advanced > Environment Variables.
Delete any ACTIVE_MODEL entries under System variables or User variables.
macOS/Linux:

Check shell configuration files (.bashrc, .zshrc, etc.) for ACTIVE_MODEL and remove or correct them.
Restart Command Prompt/Terminal:

After making changes to environment variables, close and reopen your command prompt or terminal to apply the changes.

Model Directory Exists but Not Recognized:

Possible Causes:

Missing or incorrect config.json file.
Incomplete model download.
Solutions:

Verify config.json:

Ensure that config.json in models/gpt-j-6B contains the model_type key.

Re-download the Model:

If config.json is missing or incorrect, delete the gpt-j-6B folder and re-run the download_model.py script.

CUDA Issues:

Symptoms:

Model fails to load on GPU.
PyTorch does not recognize CUDA.
Solutions:

Verify CUDA Installation:

Ensure that the CUDA Toolkit is installed and matches the version required by your PyTorch installation.

Check NVIDIA Drivers:

Update your NVIDIA drivers to the latest version compatible with your CUDA Toolkit.

Test CUDA with PyTorch:

Run a simple CUDA test script to verify GPU availability.

python
Copy code
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
Logging Issues:

Solution:

Check generate_script.log:

Review the log file for detailed error messages and timestamps to identify where the script is failing.

Ensure Console Logging is Enabled:

The updated generate_script.py includes a console handler for real-time logs.

Project Structure
Here's an overview of the project's directory structure:

arduino
Copy code
reddit-to-instagram-ai/
├── models/
│   └── gpt-j-6B/
│       ├── config.json
│       ├── pytorch_model.bin
│       ├── tokenizer_config.json
│       ├── vocab.json
│       └── merges.txt
├── scripts/
│   ├── download_model.py
│   ├── generate_script.py
│   └── simple_cuda_test.py
├── .env
├── config.py
├── requirements.txt
└── README.md
Final Notes
Maintain a Clean .env File:

Always adhere to the KEY=VALUE format without embedding code or placing comments on the same line as variable assignments.

Regularly Update Dependencies:

Keep your Python packages updated to benefit from the latest features and fixes. Use pip list --outdated to identify outdated packages.

Monitor Logs:

Regularly check generate_script.log for any warnings or errors. Logs provide valuable insights into the script's execution flow.

Backup Important Files:

Regularly backup your model directories and important scripts to prevent data loss.

Explore Further Enhancements:

Consider automating Reddit data retrieval and Instagram posting for full automation of the workflow.


Automate Reddit Data Retrieval
Integrate with Instagram API
Schedule Automated Posts 
Enhance Script Generation
Implement Logging and Monitoring
Deploy the Automation Pipeline
(Optional) Create a User Interface


Reddit Data Scraping

pip install praw

make a new git branch 

git branch praw




Create a file  called fetch_reddit_posts.py in the scripts folder

# scripts/fetch_reddit_posts.py

import praw
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

def setup_logging():
    logging.basicConfig(
        filename='fetch_reddit_posts.log',
        level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def fetch_posts(subreddit_name, limit=10):
    try:
        # Initialize Reddit instance
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        # Debugging: Print user_agent
        user_agent = os.getenv('REDDIT_USER_AGENT')
        print(f"DEBUG: Using user_agent: {user_agent}")
        logging.debug(f"Using user_agent: {user_agent}")
        
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        
        logging.debug(f"Fetching top {limit} hot posts from subreddit '{subreddit_name}'")
        
        for submission in subreddit.hot(limit=limit):
            if not submission.stickied:
                post = {
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'url': submission.url
                }
                posts.append(post)
                logging.info(f"Fetched post: {submission.title}")
        
        logging.debug(f"Total posts fetched: {len(posts)}")
        return posts
    except praw.exceptions.PRAWException as e:
        logging.error(f"PRAW Exception: {e}")
    except Exception as e:
        logging.error(f"Error fetching posts from subreddit '{subreddit_name}': {e}")
    return []

if __name__ == "__main__":
    setup_logging()
    SUBREDDIT = 'TrendingReddits'  # Replace with your target subreddit without 'r/' or trailing '/'    < -------------------------->
    LIMIT = 10  # Number of posts to fetch
    
    posts = fetch_posts(SUBREDDIT, LIMIT)
    
    if posts:
        # Save posts to a JSON or CSV file for further processing
        import json
        with open('reddit_posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)
        logging.info(f"Saved {len(posts)} posts to 'reddit_posts.json'")
    else:
        logging.info("No posts fetched.")


    update .env with reddit credentials

    # .env

REDDIT_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxx
REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxx
REDDIT_USER_AGENT=OPERATING_SYSTEM:APP_NAME/VERSION(by /u/USERNAME)
ACTIVE_MODEL=gpt-j-6B
# Or distilgpt2














