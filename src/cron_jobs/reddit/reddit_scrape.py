import os
import time
from datetime import datetime

import requests

from src.configs.api_credentials import RAPIDAPI_KEY


# Function to pull the top newest 100 posts from each subreddit, looking for stock name
def pull_subreddit_posts(company, limit=100):
    # Setup local variables
    subreddits = ["wallstreetbets", 'investing', 'stocks', 'stockmarket', 'pennystocks', 'robinhood']

    # Loop over each subreddit and pull the data
    posts = []
    for sub in subreddits:
        time.sleep(1)
        try:
            url = "https://reddit3.p.rapidapi.com/subreddit"

            querystring = {"url": f"https://www.reddit.com/r/{sub}", "filter": "new"}

            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "reddit3.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring).json()
            print(response.get('posts'))
            messages = [posts.append({"permalink": f"https://reddit.com{post['permalink']}", "text": post['selftext'],
                                      "author": post['name']}) for post in response.get("posts") if
                        post['selftext'] is not None and post['name'] is not None]
        except:
            pass

    return posts


# Function to parse the data from the api
def sanitize_json_for_csv(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                new_value = sanitize_json_for_csv(value)
            else:
                # Replace characters that might break CSV parsing
                new_value = str(value).replace(',', '‚').replace('\n', '↵').replace('"', '“')
            new_dict[key] = new_value
        return new_dict
    elif isinstance(data, list):
        new_list = []
        for item in data:
            if isinstance(item, (dict, list)):
                new_item = sanitize_json_for_csv(item)
            else:
                # Replace characters that might break CSV parsing
                new_item = str(item).replace(',', '‚').replace('\n', '↵').replace('"', '“')
            new_list.append(new_item)
        return new_list
    else:
        # For other types, simply return the value as is
        return data


# Function to pull all the coments from a post
def pull_reddit_comments(posts):
    for post in posts:
        time.sleep(1)
        try:
            url = "https://reddit3.p.rapidapi.com/post"

            querystring = {
                "url": post['permalink']}

            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "reddit3.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            for result in response.json()['post_comments']:
                if post.get('replies') is None:
                    post['replies'] = ''

                post['replies'] += f"{result['author']}: {result['content']}"
        except Exception as e:
            pass

    return posts


# Function to save the data to a csv file
def save_posts(posts, stock):
    # Setup Local Variables
    filename = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/{filename}"
    file_path = f"{output_dir}/reddit_{stock}.csv"
    print('saved to ', file_path)
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Export the data to the output file
    with open(file_path, "a+", encoding="utf-8") as f:
        f.write("permalink, text, author, stock, replies")

        for post in posts:
            try:
                replies = [reply[''] for reply in posts.get("replies", [])]
                replies_str = ' | '.join(replies)
                # Extract and join the 'text' values from the replies list
                # Write the data to the CSV file, properly escaping values
                writable = f"{post['permalink']},{post['text']},{post['author']},{stock}, {replies_str}\n"
                f.write(writable)
            except Exception as e:
                print('error', e)
                pass


if __name__ == "__main__":
    # Get the posts from all major finance subreddits
    posts = pull_subreddit_posts('GME')
    # Get 100 / all the comments from the posts
    posts = pull_reddit_comments(posts)
    # Save the posts to a csv file
    save_posts(posts, 'GME')
