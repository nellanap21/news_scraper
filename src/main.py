# Retrieving & Wrangling Data
from datetime import date  # Built-in Python library
import s3fs
import scrape_links
import scrape_articles
import matcher
import summarizer
import cleaner
import voice_generator

# Code refactor
import logging  # Built-in Python library


def main(s3_folder_path):
    """
    This function combines the scraping and saving functions.
    It logs the progress and prints out info messages.
    """
    # Start logging
    logger = logging.getLogger(__name__)

    # s3 = s3fs.S3FileSystem(profile='admin')
    # with s3.open('panoramic-news/example.txt', 'rb') as f:
    #     print(f.read())

    # Scrape Fox links
    # scrape_links.scrape_fox_links(s3_folder_path)
    # logger.info('Fox Links retrieved')

    # Scrape Fox articles
    # scrape_articles.scrape_fox_articles(s3_folder_path)
    # logger.info('Fox Articles retrieved')

    # Scrape CNN links
    # scrape_links.scrape_cnn_links(s3_folder_path)
    # logger.info('CNN Links retrieved')

    # Scrape CNN articles
    # scrape_articles.scrape_cnn_articles(s3_folder_path)
    # logger.info('CNN Articles retrieved')

    #Find matching articles
    # matches = matcher.find_matches(s3_folder_path)
    # if matches is None:
    #     logger.info('No matching articles found')
    # else:
    #     logger.info('Matching articles found')

    # Generate summaries
    # summaries = summarizer.summarize_articles(s3_folder_path)
    # if summaries is None:
    #     logger.info('No summaries generated')
    # else:
    #     logger.info('Summaries generated')

    # Generate scripts
    # cleaner.clean_scripts(s3_folder_path)
    # logger.info('Scripts generated')

    # Generate audio
    voice_generator.generate_audio(s3_folder_path)
    logger.info('Audio generated')



if __name__ == '__main__':
    # Define the required arguments
    s3_data_folder = "s3://panoramic-news/data/"

    # Configure the logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Run the main function
    main(s3_folder_path=s3_data_folder)