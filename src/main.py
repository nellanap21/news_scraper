# Retrieving & Wrangling Data
import scrape_links
import scrape_articles
import matcher
import summarizer
import cleaner
import voice_generator
import summarizer_cnn
import summarizer_fox

# Code refactor
import logging  # Built-in Python library


def main(s3_folder_path):
    """
    This function combines the scraping and saving functions.
    It logs the progress and prints out info messages.
    """
    # Start logging
    logger = logging.getLogger(__name__)

    # scrape CNN and Fox articles
    scrape(s3_folder_path)

    # create comparison script mp3
    # create_comparison(s3_folder_path)

    # create short summary cnn mp3
    create_short_summary_cnn(s3_folder_path)

    # create short summary fox mp3
    create_short_summary_fox(s3_folder_path)

def scrape(s3_folder_path):
    # Start logging
    logger = logging.getLogger(__name__)

    # Scrape Fox links
    scrape_links.scrape_fox_links(s3_folder_path)
    logger.info('Fox Links retrieved')

    # Scrape Fox articles
    scrape_articles.scrape_fox_articles(s3_folder_path)
    logger.info('Fox Articles retrieved')

    # Scrape CNN links
    scrape_links.scrape_cnn_links(s3_folder_path)
    logger.info('CNN Links retrieved')

    # Scrape CNN articles
    scrape_articles.scrape_cnn_articles(s3_folder_path)
    logger.info('CNN Articles retrieved')


def create_comparison(s3_folder_path):

    # Start logging
    logger = logging.getLogger(__name__)

    # NOTE: usually need to manually identify matches here.
    # TODO: need to improve algorithm to find matches
    #Find matching articles
    matches = matcher.find_matches(s3_folder_path)
    if matches is None:
        logger.info('No matching articles found')
        return None

    # Generate summaries
    summaries = summarizer.summarize_articles(s3_folder_path)
    if summaries is None:
        logger.info('No summaries generated')
        return None

    # Generate scripts
    cleaner.clean_scripts(s3_folder_path)
    logger.info('Scripts cleaned')

    # Generate audio
    voice_generator.generate_audio(s3_folder_path)
    logger.info('Audio generated')

    return 1


def create_short_summary_cnn(s3_folder_path):

    # Start logging
    logger = logging.getLogger(__name__)

    # Generate summaries
    summaries = summarizer_cnn.summarize_articles(s3_folder_path)
    if summaries is None:
        logger.info('No summaries generated')
        return None

    # convert summaries into script
    script = cleaner.clean_cnn_summaries(s3_folder_path)
    if script is None:
        logger.info('No CNN script generated')
        return None
    logger.info('CNN script created')

    # generate mp3
    voice_generator.generate_audio_cnn(s3_folder_path)
    logger.info('CNN audio generated')

    return 1

def create_short_summary_fox(s3_folder_path):

    # Start logging
    logger = logging.getLogger(__name__)

    # Generate summaries
    summaries = summarizer_fox.summarize_articles(s3_folder_path)
    if summaries is None:
        logger.info('No summaries generated')
        return None

    # convert summaries into script
    script = cleaner.clean_fox_summaries(s3_folder_path)
    if script is None:
        logger.info('No Fox script generated')
        return None
    logger.info('Fox script created')

    # generate mp3
    voice_generator.generate_audio_fox(s3_folder_path)
    logger.info('Fox audio generated')

    return 1

if __name__ == '__main__':
    # Define the required arguments
    s3_data_folder = "s3://panoramic-news/data/"

    # Configure the logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Run the main function
    main(s3_folder_path=s3_data_folder)