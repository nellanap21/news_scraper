import requests
from bs4 import BeautifulSoup
import pandas as pd
import s3fs
from dotenv import load_dotenv
import os
import arrow

def request_html(url):

    load_dotenv()
    oxylabs_user = os.getenv("OXYLABS_USER")
    oxylabs_pass = os.getenv("OXYLABS_PASSWORD")

    username = oxylabs_user
    password = oxylabs_pass
    proxy = "pr.oxylabs.io:7777"

    proxies = {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'http://{username}:{password}@{proxy}'
    }

    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.google.com/"}

    response = requests.get(url, headers=headers, proxies=proxies)
    print(response)
    if response.status_code != 200:
        soup = "error"
        print("Error with HTTP request")
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def scrape_fox_links(s3_folder_path):
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
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    filepath = s3_folder_path + formatted_date + '/fox-links.csv'

    # create data frame
    df = pd.DataFrame(article_links, columns=['url'])

    # save to S3
    s3 = s3fs.S3FileSystem(profile='admin')
    df.to_csv(path_or_buf=filepath, index=False)

def scrape_cnn_links(s3_folder_path):
    url = "https://www.cnn.com/politics"

    # make the HTTP request
    soup = request_html(url)

    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY/MM/DD')

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
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    formatted_date = local.format('YYYY-MM-DD')
    filepath = s3_folder_path + formatted_date + '/cnn-links.csv'

    # create data frame
    df = pd.DataFrame(article_links, columns=['url'])

    # save to S3
    df.to_csv(path_or_buf=filepath, index=False)