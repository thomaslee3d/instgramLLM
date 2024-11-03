# scripts/test_env.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Define the base directory
base_dir = Path(__file__).resolve().parent.parent

# Load the .env file with override to ensure .env variables take precedence
load_dotenv(dotenv_path=base_dir / '.env', override=True)

# Fetch environment variables
active_model = os.getenv('ACTIVE_MODEL')
reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

print(f"ACTIVE_MODEL: {active_model}")
print(f"REDDIT_USER_AGENT: {reddit_user_agent}")
