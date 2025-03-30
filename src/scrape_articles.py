import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from pathlib import Path
import re


def request_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
               "Upgrade-Insecure-Requests": "1",
               "Referer": "https://www.google.com/"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        soup = "error"
    else:
        soup = BeautifulSoup(response.content, 'html.parser')

    return soup


def parse_fox_page(soup):
    # parse article headline
    headline = ""
    h1 = soup.find("h1")
    if h1:
        headline = h1.get_text(strip=True)
    else:
        print("No h1 tag")

    # parse article subtitle and add to headline
    h2 = soup.find("h2")
    if h2:
        headline = headline + " " + h2.get_text(strip=True)
    else:
        print("No h2 tag")

    # parse article text
    article_body = soup.find("div", class_="article-body").find_all("p", recursive=False)

    content = ""
    for paragraph in article_body:

        # Break if article starts talking about other news at end of article.
        if paragraph.get_text(strip=True) == "In other news:":
            break

        content = content + " " + paragraph.get_text(strip=True)

    # replace non-breaking space with actual space
    content = content.replace('\xa0', ' ')

    return headline, content


def remove_all_caps(string):
    return re.sub(r'\b[A-Z]{2}\w*+\b', '', string)


def scrape_fox_articles():
    # create lists of equal length to hold data
    companies = []
    headlines = []
    articles = []

    # create df of links
    today = date.today()
    links_filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/fox-links.csv')
    links = pd.read_csv(filepath_or_buffer=links_filepath)

    # create a new column called domain from the link
    links["domain"] = ""

    for i in range(0, len(links)):
        start = (links.iloc[i].url.find("www.")) + 4
        end = links.iloc[i].url.find(".com")
        links.at[i, "domain"] = links.iloc[i].url[start:end]

    # iterate through each link
    for i in range(0, len(links)):

        # get the url of the row
        url = links.at[i, "url"]

        # make HTTP request and get HTML
        soup = request_html(url)

        # if there was an error in request_html, continue to next
        if soup == "error":
            print("Error with HTTP request", url)
            continue

        # get the domain of the row
        domain = links.at[i, "domain"]

        # print to show progress of the work
        # print(url)

        # depending on the domain, parse the HTML to obtain the headline and content
        if domain == "foxnews":
            headline, content = parse_fox_page(soup)
            company = "Fox"
        elif domain == "cnn":
            headline, content = parse_cnn_page(soup)
            company = "CNN"
        else:
            print("URL is not from Fox or CNN", url)
            continue

        companies.append(company)
        headlines.append(headline)
        articles.append(content)

    # create dictionary of equal length lists
    raw_data = {"company": companies, "headline": headlines, "article": articles}

    # create dataframe
    data = pd.DataFrame(raw_data)

    # remove all caps from article
    data.loc[:, "articleCleaned"] = data["article"].apply(remove_all_caps)
    data.loc[:, "article"] = data["articleCleaned"]
    data.drop("articleCleaned", axis=1, inplace=True)

    # create filepath
    data_filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/fox-data.csv')
    data_filepath.parent.mkdir(parents=True, exist_ok=True)

    # save to CSV
    data.to_csv(path_or_buf=data_filepath, index=False)


def parse_cnn_page(soup):
    # parse article headline
    h1 = soup.find("h1")
    if h1:
        headline = h1.get_text(strip=True)
    else:
        print("No h1 tag")

    # parse article text
    article_content = soup.find("div", class_="article__content").find_all("p")

    content = ""
    for paragraph in article_content:
        content = content + " " + paragraph.get_text(strip=True)

    # replace non-breaking space with actual space
    content = content.replace('\xa0', ' ')

    return headline, content


def scrape_cnn_articles():
    # create lists of equal length to hold data
    companies = []
    headlines = []
    articles = []

    # create df of links
    today = date.today()
    links_filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/cnn-links.csv')
    links = pd.read_csv(filepath_or_buffer=links_filepath)

    # create a new column called company from the link
    links["domain"] = ""

    # add the domain to the dataframe
    for i in range(0, len(links)):
        start = (links.iloc[i].url.find("www.")) + 4
        end = links.iloc[i].url.find(".com")
        links.at[i, "domain"] = links.iloc[i].url[start:end]

    # iterate through links dataframe
    for i in range(0, len(links)):

        # get the url of the row
        url = links.at[i, "url"]

        # make HTTP request and get HTML
        soup = request_html(url)

        # if there was an error in requestHtml, continue to next
        if soup == "error":
            print("Error with HTTP request", url)
            continue

        # get the domain of the row
        domain = links.at[i, "domain"]

        # depending on the domain, parse the HTML to obtain the headline and content
        if domain == "foxnews":
            headline, content = parse_fox_page(soup)
            company = "Fox"
        elif domain == "cnn":
            headline, content = parse_cnn_page(soup)
            company = "CNN"
        else:
            print("URL is not from Fox or CNN", url)
            continue

        companies.append(company)
        headlines.append(headline)
        articles.append(content)

    # create dictionary of equal length lists
    raw_data = {"company": companies, "headline": headlines, "article": articles}

    # create dataframe
    data = pd.DataFrame(raw_data)

    # create file path and store CSV
    data_filepath = Path('./data/' + today.strftime("%Y-%m-%d") + '/cnn-data.csv')
    data_filepath.parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(path_or_buf=data_filepath, index=False)