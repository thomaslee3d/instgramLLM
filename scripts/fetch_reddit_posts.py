# scripts/fetch_reddit_posts.py

import praw
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

def setup_logging():
    logging.basicConfig(
        filename='fetch_reddit_posts.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
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
        
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        
        for submission in subreddit.hot(limit=limit):
            if not submission.stickied:
                post = {
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'url': submission.url
                }
                posts.append(post)
                logging.info(f"Fetched post: {submission.title}")
        
        return posts
    except Exception as e:
        logging.error(f"Error fetching posts from subreddit '{subreddit_name}': {e}")
        return []

if __name__ == "__main__":
    setup_logging()
    SUBREDDIT = 'TrendingReddits'  # Replace with your target subreddit
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
