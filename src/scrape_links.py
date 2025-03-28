import requests  # Version 2.27.1
from bs4 import BeautifulSoup  # Version 4.11.1
import pandas as pd  # Version 1.4.2
from datetime import date  # Built-in Python library
from pathlib import Path
import numpy as np
import re

def request_html(url):
    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.google.com/"}
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        soup = "error"
    else:
        soup = BeautifulSoup(response.content, 'html.parser')

    return soup


def scrape_fox_links():
    """
    This function takes in the URL from the Fox News page.
    It scrapes this page and returns a dataframe with information on the day's news teasers.
    """

    url = "https://www.foxnews.com/politics"

    # Request the page's html script
    soup = request_html(url)

    # add links to list
    new_links = []

    # find all a tags and loop through them
    for link in soup.find_all('a'):

        # get the href attribute of a tag
        href = link.get('href')

        # check href is a string, sometimes a tag has no href
        if href is None:
            continue

        # only add links to politics articles
        if href.startswith('/politics/'):
            new_links.append('https://www.foxnews.com' + href)
        else:
            continue

    # remove duplicate links
    unique_links = list(dict.fromkeys(new_links))

    # remove newsletter links
    article_links = []
    for link in unique_links:
        if link.find('newsletter') == -1:
            article_links.append(link)

    # create filepath for CSV
    today = date.today()
    filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/fox-links.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # save to CSV
    df = pd.DataFrame(article_links, columns=['url'])
    df.to_csv(path_or_buf=filepath, index=False)


def scrape_cnn_links():
    url = "https://www.cnn.com/politics"

    # make the HTTP request
    soup = request_html(url)

    today = date.today()
    formatted_date = today.strftime("%Y/%m/%d")

    new_links = []

    # find all a tags and loop through them
    for link in soup.find_all('a'):

        # get the href attribute of a tag
        href = link.get('href')

        # check href is a string, sometimes a tag has no href
        if isinstance(href, str):
            # only add today's articles
            if href.startswith('/' + formatted_date):
                new_links.append('https://www.cnn.com' + href)
        else:
            continue

    # remove duplicate links
    unique_links = list(dict.fromkeys(new_links))

    # remove video links
    article_links = []
    for link in unique_links:
        if link.find('video') == -1:
            article_links.append(link)

    # create filepath for CSV
    today = date.today()
    filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/cnn-links.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # save to CSV
    df = pd.DataFrame(article_links, columns=['url'])
    df.to_csv(path_or_buf=filepath, index=False)