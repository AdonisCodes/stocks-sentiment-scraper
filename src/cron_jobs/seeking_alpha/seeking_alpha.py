import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# Function to pull all the posts from seeking alpha html
def pull_seeking_alpha_posts(stock):
    try:
        response = requests.get('https://seekingalpha.com/symbol/aapl')
        soup = BeautifulSoup(response.text, 'html.parser')  # 'html.parser' is the built-in parser
        body_tag = soup.find('body')
        body_text = body_tag.get_text()
        return body_text
    except:
        return ''


# Function to save data from article to csv file
def save_alpha_article(article, stock):
    # Setup Local Variables
    filename = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"output/{filename}"
    file_path = f"{output_dir}/alpha_{stock}.csv"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Export the data to the output file
    with open(file_path, "a+", encoding="utf-8") as f:
        # Write the header if the file is empty
        if os.stat(file_path).st_size == 0:
            f.write("stock, article,\n")

        clean_article = article.replace(",", "").replace('"', "'").replace('\n', '').replace('\r', '').replace('\t',
                                                                                                               '').replace(
            "\\", "")

        f.write(f"{stock}, {clean_article},\n")


if __name__ == "__main__":
    # scrape the fools website
    stock = 'AAPL'
    article = pull_seeking_alpha_posts(stock)
    save_alpha_article(article, stock)
