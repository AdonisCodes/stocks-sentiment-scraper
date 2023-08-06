import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# A function that can scrape all the new articles about a given stock ticker
def scrape_yahoo_search_results(ticker):
    time.sleep(5)
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        params = {
            'q': 'gme',
            'lang': 'en-US',
            'region': 'US',
            'newsCount': '1',
            'listsCount': '2',
            'enableFuzzyQuery': 'false',
            'quotesQueryId': 'tss_match_phrase_query',
            'multiQuoteQueryId': 'multi_quote_single_token_query',
            'newsQueryId': 'news_cie_vespa',
            'enableCb': 'true',
            'enableNavLinks': 'true',
            'enableEnhancedTrivialQuery': 'true',
            'enableResearchReports': 'true',
            'enableCulturalAssets': 'true',
            'enableLogoUrl': 'true',
            'researchReportsCount': '2',
            'quotesCount': '1',
        }

        response = requests.get('https://query1.finance.yahoo.com/v1/finance/search', params=params,
                                headers=headers)
    except:
        return []

    return response.json()['news']


# A function that can scrape all the news articles by url
def scrape_yahoo_finance_article(article_object_list):
    time.sleep(5)
    articles = []
    for article in article_object_list:
        try:
            url = article['link']
            title = article['title']
            publisher = article['publisher']
            date = article['providerPublishTime']

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }

            response = requests.get(
                'https://finance.yahoo.com/m/ce15fd58-5475-3d7b-a260-9eb4c2e8b0f5/meme-stock-tupperware-is.html',
                headers=headers,
            )
            soup = BeautifulSoup(response.text, 'html.parser')  # 'html.parser' is the built-in parser
            body_tag = soup.find('body')
            body_text = body_tag.get_text()

            articles.append({"url": url, "title": title, "publisher": publisher, "date": date,
                             "text": body_text.replace('\n', '').replace('\r', '').replace('\t', '').replace(',',
                                                                                                             '').replace(
                                 '\\', '').replace('"', "'")})
        except:
            pass

    return articles


def save_posts(posts, stock):
    # Setup Local Variables
    filename = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/{filename}"
    file_path = f"{output_dir}/yahoo_{stock}.csv"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Export the data to the output file
    with open(file_path, "a+", encoding="utf-8") as f:
        # Write the header if the file is empty
        if os.stat(file_path).st_size == 0:
            f.write("url, title, publisher, date, text\n")

        for post in posts:
            try:
                # Extract and join the 'text' values from the replies list
                # Write the data to the CSV file, properly escaping values
                writable = f"{post['url']}, {post['title']}, {post['publisher']}, {post['date']}, {post['text']}\n"
                f.write(writable)
            except Exception as e:
                print('error: ', e)
                pass


if __name__ == '__main__':
    articles = scrape_yahoo_search_results("gme")
    articles = scrape_yahoo_finance_article(articles)
    save_posts(articles, stock='gme')
