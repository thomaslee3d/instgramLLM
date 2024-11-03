# scripts/fetch_reddit_trends.py

import praw
import json
import logging
import os

def setup_logging():
    logging.basicConfig(
        filename='fetch_reddit_trends.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def fetch_top_subreddits(limit=10):
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        subreddits = reddit.subreddits.popular(limit=limit)
        subreddit_list = [sub.display_name for sub in subreddits]
        logging.info(f"Fetched top {len(subreddit_list)} subreddits.")
        return subreddit_list
    except Exception as e:
        logging.error(f"Failed to fetch top subreddits: {e}")
        return []

def fetch_hot_posts(subreddit_name, limit=5):
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        subreddit = reddit.subreddit(subreddit_name)
        hot_posts = []
        for submission in subreddit.hot(limit=limit):
            if not submission.stickied:
                post = {
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'url': submission.url
                }
                hot_posts.append(post)
        logging.info(f"Fetched {len(hot_posts)} hot posts from r/{subreddit_name}.")
        return hot_posts
    except Exception as e:
        logging.error(f"Failed to fetch hot posts from r/{subreddit_name}: {e}")
        return []

def fetch_reddit_trends(top_n_subreddits=10, posts_per_subreddit=5):
    trending_data = {}
    top_subs = fetch_top_subreddits(limit=top_n_subreddits)
    for sub in top_subs:
        hot_posts = fetch_hot_posts(sub, limit=posts_per_subreddit)
        trending_data[sub] = hot_posts
    return trending_data

if __name__ == "__main__":
    setup_logging()
    trending_data = fetch_reddit_trends(top_n_subreddits=10, posts_per_subreddit=5)
    if trending_data:
        with open('reddit_trends.json', 'w', encoding='utf-8') as f:
            json.dump(trending_data, f, ensure_ascii=False, indent=4)
        logging.info("Saved Reddit Trends data to 'reddit_trends.json'")
    else:
        logging.info("No Reddit trends data fetched.")
