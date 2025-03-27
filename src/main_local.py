# Retrieving & Wrangling Data
import requests  # Version 2.27.1
from bs4 import BeautifulSoup  # Version 4.11.1
import pandas as pd  # Version 1.4.2
from datetime import date  # Built-in Python library
import re

# Code refactor
import logging  # Built-in Python library

def requestHtml(url):
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
    This function takes in the URL from the Fox news page.
    It scrapes this page and returns a dataframe with information on the day's news teasers.

    Required arguments:
    - URL: string, the SRF website to be scraped
    """

    url = "https://www.foxnews.com/politics"

    # Request the page's html script
    soup = requestHtml(url)

    # add links to list
    newLinks = []

    # find all a tags and loop through them
    for link in soup.find_all('a'):

        # get the href attribute of a tag
        href = link.get('href')
        
        # check href is a string, sometimes a tag has no href
        if href is None:
            continue
            
        # only add links to politics articles
        if href.startswith('/politics/'):
            newLinks.append('https://www.foxnews.com' + href)
        else:
            continue

    # remove duplicate links
    uniqueLinks = list(dict.fromkeys(newLinks))

    # remove newsletter links
    articleLinks = []
    for link in uniqueLinks:
        if link.find('newsletter') == -1:
            articleLinks.append(link)
    
    # create name for CSV
    today = date.today()
    csvName = today.strftime("%Y-%m-%d") + '-fox-links.csv'

    # save to CSV
    df = pd.DataFrame(articleLinks, columns=['url'])
    df.to_csv(csvName, index=False)

def parseFoxPage(soup):
    # parse article headline
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
    articleBody = soup.find("div", class_="article-body").find_all("p", recursive=False)

    content = ""
    for paragraph in articleBody:
        
        # Break if article starts talking about other news at end of article. 
        if paragraph.get_text(strip=True) == "In other news:":
            break

        content = content + " " + paragraph.get_text(strip=True)

    # replace non-breaking space with actual space
    content = content.replace('\xa0', ' ')
    
    return headline, content

def removeAllCaps(string):
    return re.sub(r'\b[A-Z]{2}\w*+\b', '', string)

def scrape_fox_pages():
    # create lists of equal length to hold data
    companies = []
    headlines = []
    articles = []

    # create df of links
    today = date.today()
    csvName = today.strftime("%Y-%m-%d") + '-fox-links.csv'
    links = pd.read_csv(csvName)

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
        soup = requestHtml(url)

        # if there was an error in requestHtml, continue to next 
        if soup == "error":
            print("Error with HTTP request", url)
            continue

        # get the domain of the row
        domain = links.at[i, "domain"]

        #print to show progress of the work
        # print(url)
        
        # depending on the domain, parse the HTML to obtain the headline and content
        if domain == "foxnews":
            headline, content = parseFoxPage(soup)
            company = "Fox"
        elif domain == "cnn":
            headline, content = parseCnnPage(soup)
            company = "CNN"
        else:
            print("URL is not from Fox or CNN", url)
            continue

        companies.append(company)
        headlines.append(headline)
        articles.append(content)

    # create dictionary of equal length lists
    rawData = {"company": companies, "headline": headlines, "article": articles}

    # check to make sure dictionary of equal-length lists
    if len(rawData["company"]) == len(rawData["headline"]) & len(rawData["headline"]) == len(rawData["article"]):
        data = pd.DataFrame(rawData)

    data.loc[:,"articleCleaned"] = data["article"].apply(removeAllCaps)
    data.loc[:,"article"] = data["articleCleaned"]
    data.drop("articleCleaned", axis=1, inplace=True)
    
    csvDataName = today.strftime("%Y-%m-%d") + '-fox-data.csv'
    data.to_csv(csvDataName, index=False)

def main():
    """
    This function combines the scraping and saving functions.
    It logs the progress and prints out info messages.
    """
    # Start logging
    logger = logging.getLogger(__name__)

    # Scrape the links
    scrape_fox_links()
    logger.info('Links retrieved')

    # Scrape the pages
    scrape_fox_pages()
    logger.info('Data retrieved')





if __name__ == '__main__':
    # Define the required arguments

    # Configure the logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Run the main function
    main()