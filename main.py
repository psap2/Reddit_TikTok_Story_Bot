import reddit_bot
from reddit_bot import get_top_stories, save_to_excel

def main():
    subreddits = ['stories', 'shortscarystories', 'StoryTimeWithReddit']  # Desired subreddits here
    all_posts = []
    for a_subreddit in subreddits:
        posts = get_top_stories(a_subreddit)
        all_posts.extend(posts)  # Collect all posts in one list
        save_to_excel(all_posts)  # Save all posts to an Excel file

    

if __name__ == "__main__":
    main()