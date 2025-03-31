# Retrieving & Wrangling Data
from datetime import date  # Built-in Python library

import scrape_links
import scrape_articles
import matcher
# import summarizer
# import cleaner

# Code refactor
import logging  # Built-in Python library


def main(s3_folder_path):
    """
    This function combines the scraping and saving functions.
    It logs the progress and prints out info messages.
    """
    # Start logging
    logger = logging.getLogger(__name__)

    # Scrape Fox links
    scrape_links.scrape_fox_links(s3_folder_path)
    logger.info('Fox Links retrieved')

    # Scrape Fox articles
    # scrape_articles.scrape_fox_articles()
    # logger.info('Fox Articles retrieved')

    # Scrape CNN links
    # scrape_links.scrape_cnn_links()
    # logger.info('CNN Links retrieved')

    # Scrape CNN articles
    # scrape_articles.scrape_cnn_articles()
    # logger.info('CNN Articles retrieved')

    # Find matching articles
    # matches = matcher.find_matches()
    # if matches is None:
    #     logger.info('No matching articles found')
    # else:
    #     logger.info('Matching articles found')

    # Generate scripts
    # scripts = summarizer.generate_summary()
    # if scripts is None:
    #     logger.info('No scripts generated')


    # Clean scripts


if __name__ == '__main__':
    # Define the required arguments
    s3_data_folder = "s3://news/data/"

    # Configure the logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Run the main function
    main(s3_folder_path=s3_data_folder)