import praw
import pandas as pd
from datetime import datetime
import creds

reddit = praw.Reddit(
    client_id= creds.api_key,
    client_secret='SMD3xyq0fEEderPiTVWIHQyyz2Luqg',
    user_agent='Top10StoriesBot/0.1/u/Prasun-',
    username='Prasun-',
    password='Prasamsha1')

def get_top_stories(subreddit, period='all', limit=10):
    subreddit = reddit.subreddit(subreddit)
    top_stories = subreddit.top(time_filter=period, limit=limit)
    stories_data = [{
        'Title': post.title,
        'URL': post.url,
        'Upvotes': post.score,
        'Posted Date': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'Comments Count': post.num_comments
    } for post in top_stories]
    return stories_data

def save_to_excel(data, filename='Reddit_Top_Stories.xlsx'):
    df = pd.DataFrame(data)

    # Try to open an existing workbook
    try:
        with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, sheet_name='Top Stories')
    except FileNotFoundError:
        with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Top Stories')