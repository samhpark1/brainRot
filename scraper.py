import praw
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_SECRET")


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="apple:reddit.scraper:v1.0 (by /u/samhpark)"
)

subreddits = ['AmItheAsshole', 'BestofRedditorUpdates', 'TrueOffMyChest', 'relationship_advice']

for name in subreddits:
    print(f"_________{name}__________")
    subreddit = reddit.subreddit(name)
    for post in subreddit.hot(limit=25):
        #ifnore if pinned
        if post.stickied:
            continue
        #ignore if moderator post
        if post.author and post.author.name.lower() in ["automoderator"]:
            continue
        #ignore if content is not text
        if not post.selftext:
            continue

        # print(f"• {post.title} ({post.score}) by - ({post.author})")
        print(f"* {post.title}")
        print(f"{post.selftext}")
        print("_________")
