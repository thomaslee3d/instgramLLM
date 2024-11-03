# scripts/fetch_google_trends.py

from pytrends.request import TrendReq
from tenacity import retry, wait_exponential, stop_after_attempt
import json
import logging
import os

def setup_logging():
    logging.basicConfig(
        filename='fetch_google_trends.log',
        level=logging.DEBUG,  # Detailed logs
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def fetch_trending_searches(geo='united_states'):  # Updated region code
    try:
        logging.info(f"Initializing PyTrends with geo='{geo}'")
        pytrends = TrendReq(hl='en-US', tz=360)
        logging.info("Fetching trending searches...")
        trending_searches_df = pytrends.trending_searches(pn=geo)
        
        if trending_searches_df.empty:
            logging.warning("No trending searches found. The DataFrame is empty.")
            return []
        
        trending_searches = trending_searches_df[0].tolist()
        logging.info(f"Fetched {len(trending_searches)} trending searches.")
        return trending_searches
    except Exception as e:
        logging.error(f"Failed to fetch trending searches: {e}")
        raise e  # Let tenacity handle the retry

if __name__ == "__main__":
    setup_logging()
    geo_region = 'united_states'  # Updated region code
    trending_searches = fetch_trending_searches(geo=geo_region)
    
    if trending_searches:
        try:
            with open('google_trends.json', 'w', encoding='utf-8') as f:
                json.dump(trending_searches, f, ensure_ascii=False, indent=4)
            logging.info("Saved Google Trends data to 'google_trends.json'")
        except Exception as e:
            logging.error(f"Failed to save trends to JSON: {e}")
    else:
        logging.info("No trending searches to save.")
