import time

from src.cron_jobs.fools.fools_scrape import scrape_fool_article
from src.cron_jobs.nyse_stocks.nyse_scrape import fetch_stocks, parse
from src.cron_jobs.reddit.reddit_scrape import pull_subreddit_posts, save_posts, pull_reddit_comments
from src.cron_jobs.seeking_alpha.seeking_alpha import pull_seeking_alpha_posts, save_alpha_article
from src.cron_jobs.tweets.tweets_scrape import pull_tweets, pull_tweet_replies, sanitize_json_for_csv, save_tweets
from src.cron_jobs.yahoofinance.yahoo_scraper import scrape_yahoo_search_results, scrape_yahoo_finance_article, \
    save_posts as save_yahoo
from src.helpers.fs import export_csv


def main():
    # pull all the stocks from the stock analysis api
    stocks = fetch_stocks()
    parsed_stocks = parse(stocks, price=100)
    if export_csv(parsed_stocks, "stocks"):
        print("successfully scraped all stocks under 10usd")
    else:
        return 1

    for index, stock in enumerate(parsed_stocks):
        stock = stock["s"]
        print(f"Scraping {index} / {len(parsed_stocks)}")
        print('.', end='')
        # # PULL ALL THE TWEETS & SAVE THEM
        tweets = pull_tweets(stock, 10)
        # # Pull all the replies from the tweets
        for tweet in tweets:
            try:
                tweet["replies"] = pull_tweet_replies(tweet["tweet_id"])
            except Exception as e:
                print("Error in tweet replies scrape: ", e)

        # # Clean the tweets
        cleaned_tweets = sanitize_json_for_csv(tweets)
        # # Save the tweets
        save_tweets(cleaned_tweets, "")

        print('.', end='')
        # # PULL ALL THE COMMENTS FROM REDDIT & SAVE THEM
        posts = pull_subreddit_posts(stock)
        # # Get 100 / all the comments from the posts
        posts = pull_reddit_comments(posts)
        # # Save the posts to a csv file
        save_posts(posts, "")

        print('.', end='')
        # PULL ALL THE ARTICLES FROM YAHOO FINANCE AND SAVE THEM
        articles = scrape_yahoo_search_results(stock)
        articles = scrape_yahoo_finance_article(articles)
        save_yahoo(articles, stock="")

        print('.', end='')
        # PULL ALL THE ARTICLES FROM MOTELEY FOOL AND SAVE THEM
        article = scrape_fool_article(stock)
        # save_fool(article, "")

        print('.', end='')
        # PULL ALL THE ARTICLES FROM SEEKING ALPHA
        article = pull_seeking_alpha_posts(stock)
        save_alpha_article(article, '')

        print(f"\nScraped {index} / {len(parsed_stocks)}")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60 * 60 * 24)
