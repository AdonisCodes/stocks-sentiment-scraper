import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# Function to scrape the article from both exchanges available
def scrape_fool_article(ticker):
    exchanges = ['nyse', 'nasdaq']

    # Loop over the exchanges used to do the lookup on fool
    for exchange in exchanges:
        time.sleep(5)
        try:
            # Create the base url to query towards
            url = f"https://www.fool.com/quote/{exchange}/{ticker}"

            # Gather the information
            response = requests.get(url)

            # Check if stock is listed on the exchange
            print(response.status_code)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')  # 'html.parser' is the built-in parser
                body_tag = soup.find('body')
                body_text = body_tag.get_text()
                return body_text
            else:
                print('404')
        except:
            pass

    return ''
    # GO to next if failed


# Function to save data from article to csv file
def save_posts(article, stock):
    # Setup Local Variables
    filename = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"/output{filename}"
    file_path = f"{output_dir}/fools_{stock}.csv"

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
    article = scrape_fool_article(stock)
    save_posts(article, stock)
