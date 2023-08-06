import os
import time
from datetime import datetime

import requests

from src.configs.api_credentials import RAPIDAPI_KEY


# Function to pull at minimum X amount of tweets from the api, use a constant variable from the constants.py
def pull_tweets(company, limit=10):
    time.sleep(1)
    # Setup Local Variables & request setup
    url = "https://twitter154.p.rapidapi.com/search/search"

    # Setup the date to search by
    date = datetime.now()
    date = date.strftime("%Y-%m-%d")

    # Querystring setup to request data
    querystring = {"query": f"#{company}", "section": "top", "min_retweets": "1", "min_likes": "1", "limit": {limit},
                   "start_date": date, "language": "en"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }

    # Request the data from the api
    response = requests.get(url, headers=headers, params=querystring)

    # Return the data
    return response.json()["results"]


# Function to pull all the replies & other info from a single tweet using the tweet id
def pull_tweet_replies(id):
    time.sleep(1)

    # Setup Local Variables & request setup
    url = "https://twitter154.p.rapidapi.com/tweet/replies"

    querystring = {"tweet_id": id}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }

    try:
        # Request the data from the api
        response = requests.get(url, headers=headers, params=querystring)

        # Setup for loop to capture all replies if possible
        messages = response.json()["replies"]
        cursor = None
        try:
            cursor = response.json()["continuation_token"]
        except Exception as e:
            print("Error in Tweets comments scrape: ", e)

        # Loop over and capture the first 500 replies if possible, otherwise return what was available
        for i in range(1):
            if cursor is None or cursor == "":
                break

            url = "https://twitter154.p.rapidapi.com/tweet/replies/continuation"

            querystring = {"tweet_id": "1349129669258448897",
                           "continuation_token": cursor}

            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            for message in response.json()["replies"]:
                messages.append(message)

            try:
                cursor = response.json()["continuation_token"]
            except KeyError:
                pass
    except:
        return []
    return messages


# Move function from nyse to the helpers to remove illegal items

def sanitize_json_for_csv(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                new_value = sanitize_json_for_csv(value)
            else:
                # Replace characters that might break CSV parsing
                new_value = str(value).replace(',', '|comma|').replace('\n', '↵').replace('"', '“')
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


# Function to save all cleaned data to csv file in output dir
def save_tweets(tweets, stock):
    # Setup Local Variables
    filename = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/{filename}"
    file_path = f"{output_dir}/tweets_{stock}.csv"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Export the data to the output file
    with open(file_path, "a+", encoding="utf-8") as f:
        if os.stat(file_path).st_size == 0:
            f.write("tweet_id,username,created_at,retweets,likes,replies,text,expanded_url\n")

        for tweet in tweets:
            try:
                # Extract and join the 'text' values from the replies list
                replies = [reply['text'] for reply in tweet.get("replies", [])]
                replies_str = ' | '.join(replies)

                # Write the data to the CSV file, properly escaping values
                writable = f"{tweet['tweet_id']},{tweet['user']['username']},{tweet['creation_date']},{tweet['retweet_count']},{tweet['favorite_count']},{replies_str},{tweet['text']},{tweet['expanded_url']}\n"
                f.write(writable)
            except Exception as e:
                print('error: ', e)
                pass


if __name__ == '__main__':
    # Fistly collect the tweets
    stock = "GME"
    tweets = pull_tweets(stock, 10)
    # Pull all the replies from the tweets
    for tweet in tweets:
        try:
            tweet["replies"] = pull_tweet_replies(tweet["tweet_id"])
        except KeyError:
            pass

    # Clean the tweets
    cleaned_tweets = sanitize_json_for_csv(tweets)
    # Save the tweets
    save_tweets(cleaned_tweets, stock)
