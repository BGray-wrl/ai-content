import praw
import datetime
import json

# Reddit API credentials
REDDIT_CLIENT_ID = 'LnhEpRMEe5HqEKkGUSFCWQ'
REDDIT_SECRET = 'p0K8tA8CLihEyKHf9s-WAwdJ4zPpUA'
REDDIT_USER_AGENT = 'storydownloader'

# Jove2082

# Initialize PRAW Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Function to fetch stories
def fetch_stories(subreddit_name, min_upvotes=1000, max_length=200, min_length=30, days_ago=730):
    subreddit = reddit.subreddit(subreddit_name)
    
    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_ago)
    
    # Fetch submissions
    stories = []
    for submission in subreddit.top(time_filter='all', limit=100):
        # Filter by upvotes, length, and date
        if submission.score >= min_upvotes and cutoff_date.timestamp() > submission.created_utc and "reddit" not in submission.title.lower():
            story_length = len(submission.selftext.split())
            if min_length <= story_length <= max_length:
                stories.append({
                    'id': submission.id,  
                    'title': submission.title,
                    'text': submission.selftext,
                    'upvotes': submission.score,
                    'created_utc': submission.created_utc,
                    'url': submission.url,
                    'used': False
                })
    
    return stories

# Fetch stories from r/NoSleep
if __name__ == "__main__":
    subreddit_name = "ShortScaryStories"
    stories = fetch_stories(subreddit_name)

    # Save to a JSON file
    output_file = f"{subreddit_name}.json"
    with open(output_file, "w") as f:
        json.dump(stories, f, indent=4)


